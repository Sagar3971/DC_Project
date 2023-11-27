from django.shortcuts import render
from django.http import HttpResponse
# from .chatbot_logic import get_bot_response
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'index.html')

def vegetables(request):
    return render(request, 'vegetables.html')

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

def contact(request):
    return render(request, 'contact.html')

def get_bot_response(user_input):
    # Simple rule-based responses
    if "hello" in user_input.lower():
        return "Hi there!"
    elif "how are you" in user_input.lower():
        return "I'm just a computer program, but thanks for asking!"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day."
    else:
        return "I'm sorry, I didn't understand that."

def chatbot(request):
    return render(request, 'chatbot.html')

def get_bot_response_view(request):
    user_input = request.GET.get('user_input', '')
    bot_response = get_bot_response(user_input)
    return JsonResponse({'bot_response': bot_response})
