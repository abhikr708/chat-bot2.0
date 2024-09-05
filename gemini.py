import google.generativeai as genai
import sys
import argparse
import datetime
import speech_recognition as sr
import pyttsx3
import PIL.Image

# API KEY
api_key="AIzaSyB6bPpOTHgHD1tu5Jdg85Rh9vqMgBy6BJk"

# Initialize the recognizer for voice recognition
r = sr.Recognizer()

# Argument parsing
def parse_argument():
    parser = argparse.ArgumentParser(description="Give prompt to access the AI charbot", epilog="Either provide input through Text, Image, or Voice")
    parser.add_argument("--text", help="True or False, Text based input")
    parser.add_argument("--image", help="True or False, Enter Image source here") 
    parser.add_argument("--voice", help="True or False, Give input through Voice Recognition")
    parser.add_argument("--speak", help="True or False, Depends on whether you want the output to be spoken or not")

    return parser.parse_args()

# main logic
def chat_with_gemini(prompt):
    # configure the api_key
    genai.configure(api_key="AIzaSyB6bPpOTHgHD1tu5Jdg85Rh9vqMgBy6BJk")

    # post request
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # returning the request
    return response.text

# Function to take image input
def image_search(args):
    while True:
                path = input("Enter the path of the image: ")
                img = PIL.Image.open(path)
                prompt = input("Enter the prompt: ")
                if prompt.lower() in ["exit", "quit", "end"]:
                    break
                try:
                    time = datetime.datetime.now()
                    genai.configure(api_key="AIzaSyB6bPpOTHgHD1tu5Jdg85Rh9vqMgBy6BJk")
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([prompt, img])
                    print("Chatbot: ", response.text)
                    # Speak out the response
                    if(args.speak):
                        SpeakText(response)
                    write_log(time, prompt, "success", response)
                except:
                    print("Error occured when recognising the image!")
                    # sys.exit(1)

# Function to speak the response
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.say(command) # something do here
    engine.runAndWait()

# Function for Speech recognition
def voice_search():
    print("Speak to give the prompt....Listening...")
    while True:    
    # Exception handling to handle
    # exceptions at the runtime
        try:
        
            # use the microphone as source for input.
            with sr.Microphone() as source2:
            
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
            
                #listens for the user's input 
                audio2 = r.listen(source2)
            
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                return MyText
                # print("Did you say;",MyText)
                # SpeakText(MyText)
            
        except sr.RequestError as e:
            print("Could not request results; {0};".format(e))
        
        except sr.UnknownValueError:
            print("unknown error occurred;")
    return 

# Function to create chat history
def chat_history(history):
    data = []
    data.append(history)
    # print("Chat history: ")
    # print(data)

#Function to read the chats from the logs
def read_logs():
    curr_date = todays_date()
    with open(f"C:\Data\Python\Projects\Gemini chatbot\Chats\chat-{curr_date}.log", mode="r") as file:
        print(file.read())

# Function to get the today's date
def todays_date():
    date = str(datetime.datetime.now())
    x = date[:10]
    return x

# Function to generate logs
def write_log(time, prompt, status, response):
    curr_date = todays_date()
    with open(f"C:\Data\Python\Projects\Gemini chatbot\Chats\chat-{curr_date}.log", mode="a") as file:
        file.write(f"{time}, status : {status}\n   You: {prompt}\n   Chatbot: {response}\n\n\n")
    log = [prompt, response] # this will be used to store chat history
    chat_history(log)        
        
# main function
def main() -> None:
    # parsing the arguments
    args = parse_argument()

    # checking what type of argument is provided
    text_input = bool(args.text)
    image_input = bool(args.image)
    voice_input = bool(args.voice)
    speaker = bool(args.speak)

    while True:
        # If text input is provided 
        if text_input:
            user_input = input("You: ")

        # If text input i provided
        if image_input:
            image_search(args)
            break
        
        # If voice input is provided
        if voice_input:
            user_input = voice_search()
            print("You: ", user_input)
        
        # End the chat
        if user_input.lower() in ["quit", "bye", "exit"]:
            break
        # Show chat history
        if user_input.lower() in ["history", "logs", "show chats"]:
                read_logs()
        try:
            time = datetime.datetime.now()
            response = chat_with_gemini(user_input)

            print("Chatbot: ", response)

            # Speak out the response
            if(args.speak):
                SpeakText(response)

            write_log(time, user_input, "success", response)
        except:
            time = datetime.datetime.now()
            print("Error occured! Failed to generate response")
            write_log(time, user_input, "failed", "Error occured! Failed to generate response")
            sys.exit(1)

if __name__ == "__main__":
    main()