from decouple import config
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from google import genai
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from akada.models import AkadaConversations
from website.models import User


def _send_request_to_ai(prompt) -> str | None:
    """
    This function sends a request to the connected AI model and returns a string response from the model
    """
    try:
        gemini_api_key = config('GEMINI_API_KEY')
        client = genai.Client(api_key=gemini_api_key)
        gemini_model = 'gemini-2.0-flash-lite'
        # FETCH RESPONSE FROM GEMINI AI
        conversation_context += f'{prompt}'
        response = client.models.generate_content(
            model=gemini_model,
            contents=[conversation_context],
        )
        return response.text
    except:
        return 'Request to AI model Failed'


@csrf_exempt
def prompt_akada(request, username: str):
    # GET LIST OF ALL PROMPTS SENT TO AKADA
    prompts = AkadaConversations.objects.filter(
        user__username=username).order_by('-id')
    prompts_list = []
    for p in prompts:
        prompts_list.append({
            'role': 'model',
            'parts': p.system_response,
        })
        prompts_list.append({
            'role': 'user',
            'parts': p.prompt,
        })
    conversation_context = 'Here are past responses as context:\n\n"'
    for pr in prompts_list[:6]:
        conversation_context += f'{pr["parts"]}\n'
    else:
        conversation_context += f'"\n\nRespond in an informal tone, and as simply and short as possible\n\n'
    if request.method == 'POST':
        try:
            # INIT GEMINI PARAMS
            prompt = request.POST.get('prompt')
            generated_text = _send_request_to_ai(prompt=prompt)
            akada_response = {
                'role': 'model',
                'parts': generated_text or '',
            }

            # SAVE PROMPT AND RESPONSE TO DATABASE
            user = User.objects.get(username=username)
            instance = AkadaConversations()
            instance.user = user
            instance.prompt = prompt
            instance.system_response = generated_text
            instance.save()
            prompts_list = [akada_response]
        except:
            prompts_list = [{
                'role': 'model',
                'parts': "🚨 Oops! Connection Trouble\nWe can't reach the AI server or knowledge base.\nCheck your internet and give it another try soon! 🔄🌐",
            }]

    return JsonResponse({
        'success': True,
        'prompts': prompts_list,
    })


@require_POST
@csrf_exempt
def request_smartlink(request, username: str):
    try:
        # VERIFY USER
        if not User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Invalid user!',
            })
        # INIT GEMINI PARAMS
        prompt = request.POST.get('prompt')
        generated_text = _send_request_to_ai(prompt=prompt)
        akada_response = generated_text or ''
    except:
        akada_response = "🚨 Oops! Connection Trouble\nWe can't reach the AI server or knowledge base.\nCheck your internet and give it another try soon! 🔄🌐",
    return JsonResponse({
        'success': True,
        'smartlink_response': akada_response,
    })


# import os
# from tempfile import NamedTemporaryFile
# from django.shortcuts import get_object_or_404, render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import PyPDF2
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import string
# import spacy
# from transformers import BertTokenizer, BertModel, pipeline
# from summarizer import Summarizer
# from akada.models import AkadaKnowledgeBank
# from website.models import User


# # Load BERT tokenizer and model
# def loadDependencies():
#     # Load spaCy English language model
#     nltk.download('punkt')
#     nltk.download('stopwords')
#     nltk.download('wordnet')
#     tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#     model = BertModel.from_pretrained('bert-base-uncased')

# # loadDependencies()


# class AIModel:
#     def _init_(self):
#         self.nlp = spacy.load("en_core_web_sm")

#     def read_pdf(self, pdf_file):
#         text = ""
#         with pdf_file.open(mode='rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             for page in reader.pages:
#                 text += page.extract_text()
#         return text

#     def add_to_knowledge_base(self, content):
#         doc = self.nlp(content)

#         for sentence in doc.text.split('\n\n'):
#             AkadaKnowledgeBank.objects.create(content=sentence)

#     def summarize_text(self, text):
#         summarizer = Summarizer()
#         summary = summarizer(text)
#         return summary

#     def process_query(self, query):
#         global knowledge_base
#         global conversation_history

#         response = ""
#         best_score = 0
#         query_doc = self.nlp(query)
#         query_keywords = [
#             token.lemma_ for token in query_doc if not token.is_stop and not token.is_punct]

#         # Check if there's context in the conversation history
#         # if conversation_history:
#         #     last_query, last_response = conversation_history[-1]
#         #     last_query_doc = self.nlp(last_query)
#         #     similarity_score = query_doc.similarity(last_query_doc)

#         #     # If similarity is high, consider it as a follow-up question
#         #     if similarity_score > 0.7:
#         #         response = self.process_follow_up_query(query, last_response)
#         #         conversation_history.append((query, response))
#         #         return response

#         # If no context or not a follow-up question, search knowledge base
#         for item in AkadaKnowledgeBank.objects.all():
#             doc = self.nlp(item.content)
#             for sentence in doc.sents:
#                 if any(keyword.lower() in sentence.text.lower() for keyword in query_keywords):
#                     try:
#                         similarity_score = query_doc.similarity(
#                             self.nlp(sentence.text))
#                         if similarity_score > best_score:
#                             response = sentence.text
#                             best_score = similarity_score
#                         elif similarity_score == best_score:
#                             response = f"{response}\n\n{sentence.text}"
#                     except:
#                         response = "Sorry, I don't quite understand your question. Could you rephrase it?"

#         if not response:
#             response = "Sorry, I couldn't find any information matching your query. Please provide a more detailed question."

#         # conversation_history.append((query, response))
#         nlg_pipeline = pipeline("text2text-generation",
#                                 model="facebook/bart-large-cnn")
#         generated_response = nlg_pipeline(response)
#         generated_text = generated_response[0]['generated_text']
#         return generated_text

#     def process_follow_up_query(self, query, last_response):
#         # Sample implementation for handling follow-up questions

#         # Extract entities from the current query
#         query_doc = self.nlp(query)
#         entities = [ent.text.lower() for ent in query_doc.ents]

#         # Extract entities from the last response
#         last_response_doc = self.nlp(last_response)
#         last_response_entities = [ent.text.lower()
#                                   for ent in last_response_doc.ents]

#         # Check if any entity in the current query matches with entities in the last response
#         common_entities = set(entities).intersection(last_response_entities)

#         if common_entities:
#             # If there are common entities, generate a response based on that
#             response = f"I see you're interested in {', '.join(common_entities)}. Here is more information about it..."
#         else:
#             # If no common entities, provide a generic follow-up response
#             response = "Could you please clarify your question further?"

#         return response


# def akada_home(request):
#     if request.method == 'POST':
#         ai_model = AIModel()
#         m_file = request.FILES.get('m_file')

#         if m_file.name.lower().endswith('.pdf'):
#             text = ai_model.read_pdf(m_file) if m_file is not None else ''
#             ai_model.add_to_knowledge_base(text)

#             context = {'success': True,
#                        'message': 'Knowledge base has been updated'}
#             return render(request, 'akada/home.html', context)
#         else:
#             context = {
#                 'success': False, 'message': 'Unsupported file format. Please upload a PDF file.'}
#             return render(request, 'akada/home.html', context)

#     return render(request, 'akada/home.html')


# @csrf_exempt
# def chat_with_akada(request, username: str):
#     user = User.objects.filter(username=username)
#     if user.exists():
#         if request.method == 'POST':
#             user_query = request.POST['query']
#             ai_model = AIModel()
#             answer = ai_model.process_query(user_query)

#             return JsonResponse({'response': answer})
#     else:
#         return JsonResponse({
#             'success': False,
#             'message': 'You are not allowed access to this feature',
#             'response': '',
#         })
