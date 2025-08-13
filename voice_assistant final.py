import os
import random
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import pygame
import time  # For timer

pygame.mixer.init()
engine = pyttsx3.init()

current_song = None

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""

# Function to play music
def play_music():
    global current_song
    music_dir = r"C:\Users\efran\Music"  # Path to music directory
    if not os.path.exists(music_dir):
        speak("Music folder not found.")
        return
    
    songs = [song for song in os.listdir(music_dir) if song.endswith(".mp3")]
    if songs:
        random_song = random.choice(songs)
        current_song = os.path.join(music_dir, random_song)
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()
        speak(f"Playing {random_song}.")
    else:
        speak("No music files found.")

# Function to pause music
def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        speak("Music paused.")
    else:
        speak("No music is currently playing.")

# Function to resume music
def resume_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
        speak("Music resumed.")
    else:
        speak("No music is currently playing.")

# Function to play next song
def next_song():
    global current_song
    if not current_song:
        speak("No song is currently playing.")
        return
    
    music_dir = r"C:\Users\efran\Music"  # Path to music directory
    songs = [song for song in os.listdir(music_dir) if song.endswith(".mp3")]
    if songs:
        songs.remove(os.path.basename(current_song))
        random_song = random.choice(songs)
        current_song = os.path.join(music_dir, random_song)
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()
        speak(f"Playing the next song: {random_song}.")
    else:
        speak("No other songs to play.")

# Function to set a timer
def set_timer(seconds):
    try:
        seconds = int(seconds)
        speak(f"Setting a timer for {seconds} seconds.")
        time.sleep(seconds)
        speak("Time's up!")
    except ValueError:
        speak("Invalid time format.")

def execute_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")
    
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}.")

    elif "set timer" in command:
        speak("How many seconds?")
        seconds_input = recognize_speech()
        if seconds_input.isdigit():
            set_timer(seconds_input)
        else:
            speak("Please say a valid number of seconds.")
    
    elif "search google" in command:
        speak("What do you want to search on Google?")
        search_query = recognize_speech()
        if search_query:
            search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            speak(f"Searching Google for {search_query}.")
            webbrowser.open(search_url)
        else:
            speak("I couldn't catch that. Please say the search term again.")
    
    elif "open youtube" in command:
        speak("What do you want to search on YouTube?")
        search_query = recognize_speech()
        if search_query:
            youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            speak(f"Opening YouTube search results for {search_query}.")
            webbrowser.open(youtube_url)
        else:
            speak("I couldn't catch that. Please say the search term again.")
    
    elif "open roblox" in command:
        speak("Opening Roblox home page.")
        webbrowser.open("https://www.roblox.com/home")
    
    elif "wikipedia" in command:
        speak("What do you want to search in Wikipedia?")
        search_query = recognize_speech()
        if search_query:
            wikipedia_url = f"https://en.wikipedia.org/wiki/{search_query.replace(' ', '_')}"
            speak(f"Opening Wikipedia article for {search_query}.")
            webbrowser.open(wikipedia_url)
        else:
            speak("I couldn't catch that. Please say the search term again.")
    
    elif "play music" in command:
        play_music()
    
    elif "pause" in command:
        pause_music()
    
    elif "resume" in command:
        resume_music()
    
    elif "next song" in command:
        next_song()
    
    elif "bye" in command or "goodbye" in command:
        speak("Goodbye Efran, have a nice day!")
        exit()
    
    elif "L" in command:
        speak("sssshh, I'm listening...")
    
    elif "exit" in command or "quit" in command:
        speak("Goodbye Efran, have a nice day!")
        exit()
    
    else:
        speak("Sorry, I don't understand that command.")

# Main loop
if __name__ == "__main__":
    speak("Hello Efran! I am your advanced voice assistant. How can I assist you?")
    while True:
        user_command = recognize_speech()
        if user_command:
            execute_command(user_command)
