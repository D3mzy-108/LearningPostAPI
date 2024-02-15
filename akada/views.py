import os
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from epub_conversion.utils import open_book, convert_epub_to_lines
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
from ebooklib import epub
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import string
import spacy
from transformers import BertTokenizer, BertModel, pipeline
import json
from summarizer import Summarizer

from akada.models import AkadaKnowledgeBank

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10000000
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Modify the path as needed
knowledge_base_file_path = 'knowledge_base.json'


class AIModel:
    def __init__(self):
        pass

    def read_pdf(self, pdf_file):
        text = ""
        with pdf_file.open(mode='rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def add_to_knowledge_base(self, file_path, content):
        AkadaKnowledgeBank.objects.create(file_path=file_path, content=content)

    def load_knowledge_base(self, query_keywords=None):
        # Load data from Django model
        if query_keywords:
            knowledge_entries = AkadaKnowledgeBank.objects.filter(
                content__icontains=query_keywords)
        else:
            knowledge_entries = AkadaKnowledgeBank.objects.all()
        self.knowledge_base = {
            entry.file_path: entry.content for entry in knowledge_entries}

    def summarize_text(self, text):
        summarizer = Summarizer()
        summary = summarizer(text)
        return summary

    def process_query(self, query):
        best_score = 0
        best_response = ""
        responses = []
        query_doc = nlp(query)
        ents = [ent.text.lower() for ent in query_doc.ents]
        self.load_knowledge_base(query_keywords=None)

        for file_path, content in self.knowledge_base.items():
            doc = nlp(content)

            for sentence in doc.sents:
                if any(ent.lower() in sentence.text.lower() for ent in ents):
                    similarity_score = query_doc.similarity(nlp(sentence.text))

                    if similarity_score > best_score:
                        best_score = similarity_score
                        best_response = sentence.text
                        responses.insert(0, '')
            else:
                if best_response:
                    nlg_pipeline = pipeline(
                        "text2text-generation", model="facebook/bart-large-cnn")
                    generated_response = nlg_pipeline(best_response)
                    generated_text = generated_response[0]['generated_text']
                    return f"{generated_text}"

        return "Sorry, I couldn't find any information matching your query.\nPlease provide a more detailed question so I can understand better."


@csrf_exempt
def akada_home(request):
    if request.method == 'POST':
        ai_model = AIModel()
        m_file = request.FILES.get('m_file')

        if m_file.name.lower().endswith(('.pdf')):
            file_type = 'pdf'
            text = ai_model.read_pdf(m_file) if m_file is not None else ''
            ai_model.add_to_knowledge_base(m_file.name.lower(), text)

            context = {'success': True,
                       'message': 'Knowledge base has been updated'}
            return render(request, 'akada/home.html', context)
        else:
            context = {
                'success': False, 'message': 'Unsupported file format. Please upload a PDF or EPUB file.'}
            return render(request, 'akada/home.html', context)

    return render(request, 'akada/home.html')


@csrf_exempt
def chat_with_akada(request):
    if request.method == 'POST':
        user_query = request.POST['query']
        ai_model = AIModel()
        answer = ai_model.process_query(user_query)

        return JsonResponse({'response': answer})
