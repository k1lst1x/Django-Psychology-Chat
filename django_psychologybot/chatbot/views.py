from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

# from g4f.client import Client

# import asyncio
# if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

assistant_id = "asst_f0PmPM76Nc8dbyEEfeYVQlRy"

client = OpenAI(
    api_key="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"
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

thread = client.beta.threads.create()

def ask_openai_with_assistant(message):
    # Создаем новый поток
    
    # Отправляем сообщение пользователю
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # Обработчик событий
    event_handler = EventHandler()

    # Обрабатываем поток
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
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


# def ask_openai(message):
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

def chatbot(request):
	if request.method == 'POST':
		message = request.POST.get('message')
		response = ask_openai_with_assistant(message)
		return JsonResponse({'message': message, 'response': response})
	return render(request, 'chatbot.html')
