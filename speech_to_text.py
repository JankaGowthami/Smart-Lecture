import speech_recognition as sr
import threading

recording = True

def stop_recording():
    global recording
    input("Press ENTER to stop recording...\n")
    recording = False

def record_audio_and_convert_to_text():
    global recording
    recognizer = sr.Recognizer()

    print("Adjusting for ambient noise, please wait...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Recording... Speak as long as needed. Press ENTER to stop.")

        full_text = []
        while recording:
            try:
                print("Listening for the next segment...")
                audio = recognizer.listen(source, timeout=None)
                print("Converting segment to text...")
                segment_text = recognizer.recognize_google(audio)
                print("You said:", segment_text)
                full_text.append(segment_text)
            except sr.UnknownValueError:
                print("Could not understand part of the speech.")
            except sr.RequestError as e:
                print(f"Google Speech Recognition error: {e}")

    print("Recording stopped.")
    final_text = " ".join(full_text)
    return final_text

if _name_ == "_main_":
    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.start()

    print("Starting recording...")
    text_output = record_audio_and_convert_to_text()

    if text_output:
        print("\nFinal Transcription:\n", text_output)
        with open("transcription.txt", "w") as file:
            file.write(text_output)