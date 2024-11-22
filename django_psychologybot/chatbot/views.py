from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override


assistant_id = "asst_f0PmPM76Nc8dbyEEfeYVQlRy"

client = OpenAI(
    api_key="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"
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


thread = client.beta.threads.create()

QUESTIONNAIRE_PASSED = 'Анкетирование пройдено!'


def ask_openai_with_assistant(message):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    event_handler = EventHandler()

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    return event_handler.get_response()


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        number = request.POST.get('number', '').strip()
        # language = request.POST.get('language', '').strip()  # если потребуется
        
        if username and number:
            # Здесь можно передать данные через сессию или URL параметры
            request.session['message'] = f"Меня зовут {username}, мой номер {number}."
            return redirect('chatbot')  # Предполагается, что 'chatbot' принимает сессионные данные
        else:
            error_message = 'Пожалуйста, заполните все поля.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai_with_assistant(message)
        return JsonResponse({'message': message, 'response': response})
    message = request.session.get('message', 'Данные отсутствуют.')
    response = ask_openai_with_assistant(message)
    return render(request, 'chatbot.html', {'message': message, 'response': response})
