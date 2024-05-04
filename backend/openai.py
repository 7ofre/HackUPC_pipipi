import openai
from collections import deque
import spacy

# Load spaCy's English tokenizer
nlp = spacy.load("en_core_web_sm")

# Initialize ChatGPT with OpenAI's API
openai.api_key = 'sk-proj-HofrZijFbKwT2RER204sT3BlbkFJ4s15UmnlEAJzVALwbZH4'

def chat_with_gpt(prompt):
    # Start a conversation with GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def extract_keywords(text):
    # Use spaCy to extract keywords
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.pos_ in {'NOUN', 'PROPN'} and not token.is_stop]

# Start the conversation
conversation_history = deque(maxlen=5)  # Limit history to manage context size
user_input = "Tell me about your hobbies and interests."

while True:
    conversation_history.append({"role": "user", "content": user_input})
    system_response = chat_with_gpt(user_input)
    conversation_history.append({"role": "assistant", "content": system_response})

    print("GPT-3:", system_response)
    keywords = extract_keywords(system_response)
    print("Extracted Keywords:", keywords)

    user_input = input("You: ")  # Get the next user input
    if user_input.lower() == 'quit':
        break
