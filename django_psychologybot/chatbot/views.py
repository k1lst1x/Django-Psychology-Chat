from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from . import creds
from django_psychologybot import settings
from weasyprint import HTML
import os


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

QUESTIONNAIRE_LABEL_RU = 'Анектирование завершено!'
QUESTIONNAIRE_LABEL_KZ = 'Сауалдау аяқталды!'


def generate_pdf(content):
    """
    Генерирует PDF-файл из текста.
    """
    html_content = f"""
    <html>
    <head>
        <title>Отчёт ассистента</title>
    </head>
    <body>
        <h1>Отчёт ассистента</h1>
        <p>{content}</p>
    </body>
    </html>
    """
    pdf_file = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file


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
        pdf_file = generate_pdf(assistant_response)
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'report.pdf')

        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.getvalue())

        # Перенаправляем на URL для скачивания
        return JsonResponse({
            'message': 'Анкетирование завершено. Отчёт готов для скачивания.',
            'file_url': os.path.join(settings.MEDIA_URL, 'assistant_report.pdf')
        })



    return JsonResponse({'message': assistant_response})


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


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        thread_id = request.session.get('thread_id')

        if not thread_id:
            return redirect('login')

        response = ask_openai_with_assistant(message, thread_id)
        return JsonResponse({'message': message, 'response': response})

    message = request.session.get('message', 'Данные отсутствуют.')
    thread_id = request.session.get('thread_id')

    if not thread_id:
        return redirect('login')

    response = ask_openai_with_assistant(message, thread_id)
    return render(request, 'chatbot.html', {'message': message, 'response': response})
