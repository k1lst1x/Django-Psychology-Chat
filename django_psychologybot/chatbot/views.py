from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from . import creds
from django_psychologybot import settings
from docx import Document
import os
import io


assistant_id = creds.assistant_id

client = OpenAI(
    api_key=creds.api_key
)

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.response = ""
        
    @override
    def on_text_delta(self, delta, snapshot):
        self.response += delta.value


    def get_response(self):
        return self.response

# thread = client.beta.threads.create()

QUESTIONNAIRE_LABEL_RU = 'Анкетирование завершено!'
QUESTIONNAIRE_LABEL_KZ = 'Сауалдау аяқталды!'


def generate_word(content):
    """
    Генерирует Word-документ из текста.
    """
    # Создаём объект Word-документа
    document = Document()
    
    # Добавляем заголовок
    document.add_heading("Отчёт ассистента", level=1)
    
    # Добавляем основной текст (контент)
    document.add_paragraph(content)
    
    # Сохраняем документ в поток
    word_file = io.BytesIO()
    document.save(word_file)
    word_file.seek(0)


    return word_file


def ask_openai_with_assistant(message, thread_id):
    # Отправляем сообщение пользователю
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    event_handler = EventHandler()

    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    # return event_handler.get_response()
    assistant_response = event_handler.get_response()

    if QUESTIONNAIRE_LABEL_RU in assistant_response or QUESTIONNAIRE_LABEL_KZ in assistant_response:
        word_file = generate_word(assistant_response)
        word_file_path = os.path.join(settings.STATIC_ROOT, 'report.docx')
        word_file_url = 'http://127.0.0.1:8000/static/report.docx'

        with open(word_file_path, 'wb') as f:
            f.write(word_file.getvalue())

        # Перенаправляем на URL для скачивания
        # return JsonResponse({
        #     'message': 'Анкетирование завершено. Отчёт готов для скачивания.',
        #     'file_url': os.path.join(settings.MEDIA_URL, 'assistant_report.pdf')
        # })
        return assistant_response, word_file_url

    return assistant_response, None
    # return JsonResponse({'message': assistant_response})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        number = request.POST.get('number', '').strip()
        language = request.POST.get('language', '').strip()

        if username and number and language:
            thread = client.beta.threads.create()
            request.session['thread_id'] = thread.id
            request.session['message'] = f"Меня зовут {username}, мой номер {number} и я хочу разговаривать на {language}."
            return redirect('chatbot')
        else:
            error_message = 'Пожалуйста, заполните все поля.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def video_callback(request):
    return HttpResponse('Callback')



def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        thread_id = request.session.get('thread_id')

        if not thread_id:
            return redirect('login')

        response, file_url = ask_openai_with_assistant(message, thread_id)
        return JsonResponse({'message': message, 'response': response, 'fileURL': file_url})

    message = request.session.get('message', 'Данные отсутствуют.')
    thread_id = request.session.get('thread_id')

    if not thread_id:
        return redirect('login')

    response, _ = ask_openai_with_assistant(message, thread_id)
    return render(request, 'chatbot.html', {'message': message, 'response': response})
