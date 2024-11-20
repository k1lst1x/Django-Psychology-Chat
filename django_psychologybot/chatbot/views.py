from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
# from g4f.client import Client

# import asyncio
# if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = OpenAI(
    api_key="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"
)

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
		response = ask_openai(message)
		return JsonResponse({'message': message, 'response': response})
	return render(request, 'chatbot.html')