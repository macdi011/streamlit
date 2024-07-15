#!pip install streamlit
#!pip install speechrecognition
#!pip install nltk

import json
import nltk
from nltk.chat.util import Chat, reflections
import streamlit as st
import speech_recognition as sr

# Charger les données depuis le fichier JSON
with open('intents.json') as file:
    data = json.load(file)

# Convertir les données JSON en paires de questions-réponses pour NLTK
pairs = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        pairs.append([pattern, intent['responses']])

# Créer le chatbot avec NLTK
def chatbot_response(message):
    chatbot = Chat(pairs, reflections)
    return chatbot.respond(message)

# Fonction pour transcrire la parole en texte
def transcribe_speech():
    # Initialize recognizer class
    r = sr.Recognizer()

    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")
        # listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            # using Google Speech Recognition
            text = r.recognize_google(audio_text)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand what you said."
        except sr.RequestError:
            return "Sorry, my speech service is down."
        except sr.Error as e:
            return f"Error: {str(e)}"

# Fonction principale pour l'interface utilisateur
def main():
    st.title("Voice Command Chatbot")

    # Text input for chatbot
    user_input = st.text_input("You:", "")

    # Button for voice input
    if st.button("Voice Input"):
        voice_input = transcribe_speech()
        st.write("You:", voice_input)
        st.write("Bot:", chatbot_response(voice_input))

    # Button for text input
    if st.button("Send"):
        st.write("You:", user_input)
        st.write("Bot:", chatbot_response(user_input))

if __name__ == "__main__":
    main()
