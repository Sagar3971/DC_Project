import random


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



def main():
    print("Chatbot: Hello! Type 'bye' to exit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye!")
            break

        bot_response = get_bot_response(user_input)
        print("Chatbot:", bot_response)


if __name__ == "__main__":
    main()