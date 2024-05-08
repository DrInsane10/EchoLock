import azure.cognitiveservices.speech as speechsdk
import pyttsx3
import hashlib
import random
import os
import json


# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()




# Initialize the Speech SDK client
speech_key = "6e3c34396a944ae99c71c6c1bf666d18"
service_region = "centralindia"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)


# File where the credentials are stored
credentials_file = 'credentials.json'


# Function definitions go here...
# ...
def speak(text):
    """Use text-to-speech to speak out the text."""
    tts_engine.say(text)
    tts_engine.runAndWait()


def record_voice(prompt):
    """Records voice from the microphone and returns the recognized text using Microsoft Cognitive Services."""
    print(prompt)
    speak(prompt)


    # Set up the speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)


    print("Listening...")
   
    # Perform speech recognition
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return None
def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as file:
            return json.load(file)
    return None


def save_credentials(data):
    with open(credentials_file, 'w') as file:
        json.dump(data, file)


def setup_credentials():
    main_password = record_voice("Please say your main password:")
    main_password_hash = hash_password(main_password)
    password_hashes, questions = set_passwords()
    credentials = {
        'main_password': main_password_hash,
        'secondary_passwords': password_hashes,
        'questions': questions
    }
    save_credentials(credentials)
def hash_password(password):
    """Hashes a password using SHA-256 and returns the hexadecimal representation."""
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()


def set_passwords():
    """Ask the user to set multiple passwords by answering security questions and hash them."""
    password_hashes = {}
    questions = [
        "What is your favorite color?",
        "What is your birth city?",
        "What is your pet's name?"
    ]
    for question in questions:
        answer = record_voice(question)
        if answer:
            hashed_answer = hash_password(answer.lower())  # Hash and store answers
            password_hashes[question] = hashed_answer
        else:
            print(f"No input detected for the question: {question}")
            # Optionally, you could allow the user to try again or skip the question.
    return password_hashes, questions
def change_main_password(credentials):
    """Allows the user to change their main password with error handling for no input."""
    new_password = record_voice("Please say your new main password.")
    if not new_password:  # Check if new_password is None or an empty string
        speak("No password detected. Please try again.")
        return  # Return to the main menu or you could loop to ask again
   
    new_password_hash = hash_password(new_password)
    credentials['main_password'] = new_password_hash
    save_credentials(credentials)
    speak("Your main password has been successfully changed.")


def change_security_questions(credentials):
    """Allows the user to change the answers to their security questions."""
    password_hashes, questions = set_passwords()  # Reuse the set_passwords function to set new answers
    credentials['secondary_passwords'] = password_hashes
    credentials['questions'] = questions
    save_credentials(credentials)
    speak("Your security questions and answers have been successfully updated.")


def verify_security_question(password_hashes, questions):
    """Asks a random security question that has an answer and verifies the answer."""
    # Filter out questions that don't have a recorded answer
    valid_questions = [question for question in questions if question in password_hashes]
    if not valid_questions:
        print("No security questions have been answered. Verification cannot proceed.")
        return False
    question = random.choice(valid_questions)  # Ask a random question from the set of valid questions
    voice_answer = record_voice(question)
    if voice_answer:
        voice_answer_hash = hash_password(voice_answer.lower())
        if voice_answer_hash == password_hashes[question]:
            return True
    return False


# ... (rest of your existing code)


def interpret_choice(choice):
    """Interprets the spoken choice and returns a corresponding number as a string."""
    choice = choice.lower()
    numeric_choices = {
        "one": "1",
        "two": "2",
        "three": "3",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "first": "1",
        "second": "2",
        "third": "3",
        "fourth": "4",
        "fifth": "5",
        "won": "1",
        "verify main password": "1",
        "verify security question": "2",
        "exit": "3",
        "to": "2",  # Common misinterpretation of 'two'
        "tree": "3" , # Common misinterpretation of 'three'
        "four": "4",
        "for": "4",  # Common misinterpretation
        "five": "5",
        "change main password": "3",
        "change answers to security questions": "4",
        "change security questions": "4",
        "exit": "5"
    }


    # Handle capitalized variations
    numeric_choices.update({k.capitalize(): v for k, v in numeric_choices.items()})


    for spoken, number in numeric_choices.items():
        if spoken in choice:
            return number
    return None
def main_menu():
    credentials = load_credentials()
   
    if not credentials:
        speak("No credentials found. Let's set up your security questions.")
        setup_credentials()
        credentials = load_credentials()


    while True:
        speak("Welcome to the voice-operated menu.")
        print("\n1. Verify Main Password")
        print("2. Verify Security Question")
        print("3. Change Main Password")
        print("4. Change Answers to Security Questions")
        print("5. Exit")
        speak("Please say the number of the option you want to choose.")


        choice_spoken = record_voice("Beep. Please speak now.")
        choice = interpret_choice(choice_spoken) if choice_spoken else None


        if choice == '1':
            main_password = record_voice("Please say your main password.")
            if main_password and hash_password(main_password) == credentials['main_password']:
                speak("Main password verified successfully.")
                break
            else:
                speak("Main password incorrect.")
        elif choice == '2':
            if verify_security_question(credentials['secondary_passwords'], credentials['questions']):
                speak("Verification successful.")
                break
            else:
                speak("Verification failed.")
        elif choice == '3':
            change_main_password(credentials)
            # Refresh credentials after change
            credentials = load_credentials()
        elif choice == '4':
            change_security_questions(credentials)
            # Refresh credentials after change
            credentials = load_credentials()
        elif choice == '5':
            speak("Exiting program.")
            break
        else:
            speak("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()


