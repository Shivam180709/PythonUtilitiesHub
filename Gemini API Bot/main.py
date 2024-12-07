# Python 3.12.6

import google.generativeai as genai

# Replace this with your API key
apikey = "Replace it with your API key."

# Configure the API with the provided API key
genai.configure(api_key=apikey)

# Set up the configuration for text generation
generation_config = {
    "temperature": 1.2,  # Controls randomness in responses (higher = more random)
    "top_p": 0.95,       # Controls the diversity of the model's responses
    "top_k": 64,         # Limits the number of candidate tokens considered
    "max_output_tokens": 8192,  # Maximum number of tokens to generate in a response
    "response_mime_type": "text/plain",  # Specifies the response format
}

# Define safety settings for content moderation
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",  # No content is blocked for harassment
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",  # No content is blocked for hate speech
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",  # No content is blocked for explicit content
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",  # No content is blocked for dangerous content
    },
]

# Initialize the generative model with the configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Model name
    safety_settings=safety_settings,  # Apply the defined safety settings
    generation_config=generation_config,  # Apply the generation configuration
    system_instruction="Answer me briefly",  # Instruction to the model for concise responses
)

# Start a chat session with the model
chat_session = model.start_chat(history=[])

def AI_Response(user_input):
    """
    The function sends the input to the generative model, receives the response, 
    and prints it. It also appends the user input and model's response to the chat history.
    """
    response = chat_session.send_message(user_input)  # Send input to the model
    model_response = response.text  # Extract the model's response text
    print(f'Gemini: {model_response}')  # Print the model's response
    
    # Append the user input and model response to the chat session history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})

if __name__ == "__main__":
    user_input = input("User: ")  # Take input from the user
    AI_Response(user_input)  # Send input to the AI model and print the response
