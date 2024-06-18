import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio_data = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            print("You said: " + text)
            
            # Write the recognized text to a file
            with open("recognized_speech.txt", "a") as file:
                file.write(text + "\n")
            print("Recognized speech has been written to recognized_speech.txt")
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

speech_to_text()
