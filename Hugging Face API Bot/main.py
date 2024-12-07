# Python 3.12.6

from hugchat import hugchat
from hugchat.login import Login

# User credentials for Hugging Face account
hugging_face_username = ""
hugging_face_password = ""

# Login to Hugging Face using the provided username and password
sign = Login(hugging_face_username, hugging_face_password)

# Retrieve cookies after successful login
cookies = sign.login()

# Initialize the chatbot with the retrieved cookies to maintain the session
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

if __name__ == "__main__":
    while True:
        User_Input = input("User: ")  # Prompt the user for input
        # Send the user input to the chatbot and display the bot's response
        print("Bot: ", chatbot.chat(User_Input))
