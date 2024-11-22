from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from django.shortcuts import redirect
from . import creds


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

    return event_handler.get_response()


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

# старая функция chatbot
# def chatbot(request):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         response = ask_openai_with_assistant(message)
#         return JsonResponse({'message': message, 'response': response})
#     message = request.session.get('message', 'Данные отсутствуют.')
#     response = ask_openai_with_assistant(message)
#     return render(request, 'chatbot.html', {'message': message, 'response': response})

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
