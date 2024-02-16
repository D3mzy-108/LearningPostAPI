import os
from tempfile import NamedTemporaryFile
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import spacy
from transformers import BertTokenizer, BertModel, pipeline
from summarizer import Summarizer
from akada.models import AkadaKnowledgeBank
from website.models import User

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10000000
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Global variables
knowledge_base = {}
conversation_history = []


class AIModel:
    def _init_(self):
        pass

    def read_pdf(self, pdf_file):
        text = ""
        with pdf_file.open(mode='rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def add_to_knowledge_base(self, content):
        doc = nlp(content)

        for sentence in doc.text.split('\n\n'):
            AkadaKnowledgeBank.objects.create(content=sentence)

    def summarize_text(self, text):
        summarizer = Summarizer()
        summary = summarizer(text)
        return summary

    def process_query(self, query):
        global knowledge_base
        global conversation_history

        response = ""
        best_score = 0
        query_doc = nlp(query)
        query_keywords = [
            token.lemma_ for token in query_doc if not token.is_stop and not token.is_punct]

        # Check if there's context in the conversation history
        # if conversation_history:
        #     last_query, last_response = conversation_history[-1]
        #     last_query_doc = nlp(last_query)
        #     similarity_score = query_doc.similarity(last_query_doc)

        #     # If similarity is high, consider it as a follow-up question
        #     if similarity_score > 0.7:
        #         response = self.process_follow_up_query(query, last_response)
        #         conversation_history.append((query, response))
        #         return response

        # If no context or not a follow-up question, search knowledge base
        for item in AkadaKnowledgeBank.objects.all():
            doc = nlp(item.content)
            for sentence in doc.sents:
                if any(keyword.lower() in sentence.text.lower() for keyword in query_keywords):
                    try:
                        similarity_score = query_doc.similarity(
                            nlp(sentence.text))
                        if similarity_score > best_score:
                            response = sentence.text
                            best_score = similarity_score
                        elif similarity_score == best_score:
                            response = f"{response}\n\n{sentence.text}"
                    except:
                        response = "Sorry, I don't quite understand your question. Could you rephrase it?"

        if not response:
            response = "Sorry, I couldn't find any information matching your query. Please provide a more detailed question."

        # conversation_history.append((query, response))
        nlg_pipeline = pipeline("text2text-generation",
                                model="facebook/bart-large-cnn")
        generated_response = nlg_pipeline(response)
        generated_text = generated_response[0]['generated_text']
        return generated_text

    def process_follow_up_query(self, query, last_response):
        # Sample implementation for handling follow-up questions

        # Extract entities from the current query
        query_doc = nlp(query)
        entities = [ent.text.lower() for ent in query_doc.ents]

        # Extract entities from the last response
        last_response_doc = nlp(last_response)
        last_response_entities = [ent.text.lower()
                                  for ent in last_response_doc.ents]

        # Check if any entity in the current query matches with entities in the last response
        common_entities = set(entities).intersection(last_response_entities)

        if common_entities:
            # If there are common entities, generate a response based on that
            response = f"I see you're interested in {', '.join(common_entities)}. Here is more information about it..."
        else:
            # If no common entities, provide a generic follow-up response
            response = "Could you please clarify your question further?"

        return response


def akada_home(request):
    if request.method == 'POST':
        ai_model = AIModel()
        m_file = request.FILES.get('m_file')

        if m_file.name.lower().endswith('.pdf'):
            text = ai_model.read_pdf(m_file) if m_file is not None else ''
            ai_model.add_to_knowledge_base(text)

            context = {'success': True,
                       'message': 'Knowledge base has been updated'}
            return render(request, 'akada/home.html', context)
        else:
            context = {
                'success': False, 'message': 'Unsupported file format. Please upload a PDF file.'}
            return render(request, 'akada/home.html', context)

    return render(request, 'akada/home.html')


@csrf_exempt
def chat_with_akada(request, username: str):
    user = User.objects.filter(username=username)
    if user.exists():
        if request.method == 'POST':
            user_query = request.POST['query']
            ai_model = AIModel()
            answer = ai_model.process_query(user_query)

            return JsonResponse({'response': answer})
    else:
        return JsonResponse({
            'success': False,
            'message': 'You are not allowed access to this feature',
            'response': '',
        })
