from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from django.shortcuts import redirect
from . import creds

# from g4f.client import Client

# import asyncio
# if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

assistant_id = creds.assistant_id

client = OpenAI(
    api_key=creds.api_key
)

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.response = ""
        
    # @override
    # def on_text_created(self, text) -> None:
    #     self.response += f"{text}"
    
    @override
    def on_text_delta(self, delta, snapshot):
        self.response += delta.value

    # def on_tool_call_created(self, tool_call):
    #     self.response += f"{tool_call.type}\n"

    # def on_tool_call_delta(self, delta, snapshot):
    #     if delta.type == 'code_interpreter':
    #         if delta.code_interpreter.input:
    #             self.response += delta.code_interpreter.input
    #         if delta.code_interpreter.outputs:
    #             self.response += "\n\noutput >"
    #             for output in delta.code_interpreter.outputs:
    #                 if output.type == "logs":
    #                     self.response += f"\n{output.logs}"

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

    # Обработчик событий
    event_handler = EventHandler()

    # Обрабатываем поток
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler,
    ) as stream:
        stream.until_done()

    return event_handler.get_response()

def ask_openai(message):
	response = client.chat.completions.create(
		messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ],
		model="gpt-3.5-turbo",
	)

	response_dict = response.to_dict()
	return response_dict['choices'][0]['message']['content'].strip()


#фришный gpt
# def ask_openai_free(message):
# 	client = Client()
# 	model_list = ["gpt-4o-mini", "gpt-4-turbo", "gpt-4"]
# 	for model in model_list:
# 		try:
# 			response = client.chat.completions.create(
# 				model = model,
# 				messages=[
# 					{"role": "user", "content": message},
# 				],
# 			)
# 			return response.choices[0].message.content
# 		except Exception as error:
# 			print("ОШИБКА: ", error)
# 			continue

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
