from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI


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


def chatbot(request):
	if request.method == 'POST':
		message = request.POST.get('message')
		response = ask_openai(message)
		return JsonResponse({'message': message, 'response': response})
	return render(request, 'chatbot.html')