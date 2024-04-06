import json
import os
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from pydictionary import PyDictionary
from datetime import datetime, timedelta
import time
from threading import Timer
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from tkinter import ttk
import sympy as sp
from PIL import ImageTk, Image
import pyglet
import re

# Global variables
admin_credentials = {'username': 'admin', 'password': 'HermesAdmin'}
current_user = None

pyglet.font.add_file('montserrat.ttf')

# Basic database (dictionary) for storing user data
user_data = {}

# JSON file path for storing user accounts
USER_ACCOUNTS_FILE = "user_accounts.json"

def load_user_accounts():
    try:
        with open(USER_ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user accounts to JSON file
def save_user_accounts(user_accounts):
    with open(USER_ACCOUNTS_FILE, "w") as file:
        json.dump(user_accounts, file)

# Basic database (dictionary) for storing user data
user_accounts = load_user_accounts()

def save_user_data(username, chat_history_text):
    if chat_history_text:
        new_chat_history = chat_history_text.get("1.0", tk.END)
        filename = f"{username}_chat_history.txt"
        mode = 'a' if os.path.exists(filename) else 'w'

        existing_chat_history = ""
        if mode == 'a':
            with open(filename, 'r') as file:
                existing_chat_history = file.read()

        if existing_chat_history:
            new_messages = new_chat_history.split(existing_chat_history)[-1].strip()
        else:
            new_messages = new_chat_history.strip()
        
        if new_messages:
            with open(filename, mode) as file:
                file.write('\n' + new_messages + '\n')
            messagebox.showinfo("Chat History Saved", "New messages appended to chat history.")
        else:
            messagebox.showinfo("Chat History Saved", "No new messages to save.")
    else:
        messagebox.showwarning("No Data", "There is no chat history to save.")


# Function to load user data from a file
def load_user_data(username):
    filename = f"{username}_chat_history.txt"
    if os.path.exists(filename):
        print(f"Loading chat history from file: {filename}") 
        with open(filename, "r") as file:
            chat_history_text = file.read()
            print("Chat history loaded successfully")  
            return chat_history_text
    else:
        print(f"Chat history file '{filename}' not found")  
        return None
    
# Function to handle login
def login():
    global username, user_reminders
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        if username == "Admin" and password =="HermesAdmin":  
                open_admin_window()  
                login_window.destroy()
                
        elif username in user_accounts and user_accounts[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            login_window.destroy()
            user_reminders = load_reminders_from_file(username)
            create_chat_window(username)  
            login_button.pack_forget()
            signup_button.pack_forget() 
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

# Function to handle signup
def signup():
    global username
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    
    # Define validation and restriction criteria for username and password
    username_min_length = 5
    password_min_length = 8
    forbidden_usernames = ["admin"]
    password_complexity_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$')
    
    if username and password:
        # Check if username meets length requirement
        if len(username) < username_min_length:
            messagebox.showerror("Signup Failed", f"Username must be at least {username_min_length} characters long.")
        # Check if password meets length requirement
        elif len(password) < password_min_length:
            messagebox.showerror("Signup Failed", f"Password must be at least {password_min_length} characters long.")
        # Check if username is in the list of forbidden usernames
        elif username.lower() in forbidden_usernames:
            messagebox.showerror("Signup Failed", "You are not authorized to use this username.")
        # Check for valid characters in the username (alphanumeric only)
        elif not username.isalnum():
            messagebox.showerror("Signup Failed", "Username must contain only letters and numbers.")
        # Check for whitespace characters in the username
        elif ' ' in username:
            messagebox.showerror("Signup Failed", "Username cannot contain whitespace characters.")
        else:
            # Add the username and password to the user_accounts dictionary
            user_accounts[username] = password
            save_user_accounts(user_accounts)
            messagebox.showinfo("Signup Successful", f"Account created for {username}. You can now log in.")
            signup_window.destroy()
            create_chat_window(username)
            login_button.pack_forget()
            signup_button.pack_forget()
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

def open_login_signup_window(root):
    root.eval('tk::PlaceWindow . center')
    global login_button, signup_button
    
    root.geometry("400x350")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))  
    login_button.pack(padx=5, pady=10) 
    signup_button = tb.Button(root, text="Sign Up", width=20, command=lambda: open_signup_window(root), bootstyle="primary")
    signup_button.pack(padx=5, pady=10) 
    login_button.pack(pady=10)

# Function to handle logout
def logout(chat_history_text, username, root):
    global user_reminders
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        save_user_data(username, chat_history_text)
        remove_past_reminders(user_reminders)  
        chat_history.pack_forget()  
        entry.pack_forget()  
        send_button.pack_forget() 
        open_login_signup_window(root) 
        
def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def send_message(event=None):
    global root_destroyed
    chat_history.tag_configure("username_label", font=("montserrat", 10, "bold"), justify="right")
    chat_history.tag_configure("chatbot_label", font=("montserrat", 10, "bold"), justify="left")
    
    chat_history.tag_configure("usernamemsg_label", font=("montserrat", 10), justify="right")
    chat_history.tag_configure("chatbotmsg_label", font=("montserrat", 10), justify="left")

    if root_destroyed:
        print("Root window has been destroyed. Cannot send message.")
        return

    message = entry.get().strip()  
    if not message:  
        messagebox.showwarning("Empty Message", "Please enter a message before sending.")
        return

    if message.lower() == 'exit':
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            logout(chat_history, username, root) 
    else:
        if root.winfo_exists():  
            response = chatbot_response(message, username)  
            if response:  
                chat_history.config(state=tb.NORMAL)

                user_label = f"\n{username}" if username else "\nUser"
                chat_history.insert(tb.END, f"\n{user_label}\n", "username_label")

                
                chat_history.insert(tb.END, f"{message}\n\n", "usernamemsg_label")

                chat_history.insert(tb.END, "Hermes", "chatbot_label")

                chat_history.insert(tb.END, f"\n{response}\n", "chatbotmsg_label")

                chat_history.config(state=tb.DISABLED)
                entry.delete(0, tb.END)
            
                chat_history.yview(tk.END)
        else:
            print("Root window does not exist. Cannot send message.")

def create_chat_window(username):
    login_button.pack_forget()
    signup_button.pack_forget()
    
    root.eval('tk::PlaceWindow . center')
    global chat_history, entry, send_button
    root.geometry("500x693+350+150")
    root.resizable(False, False)  
    chat_history = tb.Text(root, width=80, height=30, state=tk.DISABLED, font="Helvetica, 10")
    entry = tb.Entry(root, width=50)
    
    send_button = tb.Button(root, text="Send", command=send_message, bootstyle='Danger')
    send_button.place(relw=0.104167, relh=0.185185, relx=0.104167, rely=0.185185)
    
    chat_history.pack()
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    send_button.pack(side=tk.RIGHT)
    entry.bind("<Return>", send_message)

    chat_history.tag_configure("history_text", font=("montserrat", 10), justify="left", foreground="gray")
    chat_history_text = load_user_data(username)  
    if chat_history_text:
        chat_history.config(state=tk.NORMAL)  
        chat_history.insert(tk.END, chat_history_text, "history_text")  

        chat_history.config(state=tk.DISABLED)  

    user_reminders = load_reminders_from_file(username) 
    display_reminders_in_chat(user_reminders)  

    reminder_display_timer = Timer(60, display_reminders_periodically)
    reminder_display_timer.daemon = True
    reminder_display_timer.start()

def open_login_window(root):
    global login_window, show_password_var
    login_window = tb.Toplevel(root)
    login_window.title("Login")
    login_window.geometry('930x500+300+200')
    login_window.resizable(False, False)
    
    ico = Image.open('hermes.png')
    photo = ImageTk.PhotoImage(ico)
    login_window.wm_iconphoto(False, photo)
    
    img = PhotoImage(file='hermes2.png')
    image_label = Label(login_window, image=img, bg='white')
    image_label.image = img
    image_label.place(x=0, y=-20)
    
    titlelbl = tb.Label(login_window, text="Log In", font=("montserrat", 55),foreground="#f8bf66")
    
    titlelbl.place(x= 534,  y=20)

    global username_entry, password_entry
    
    usernamelbl = tb.Label(login_window, text="Username", font=("montserrat", 25))
    usernamelbl.place(x= 575,  y=150)
    
    username_entry = tk.Entry(login_window, font=("montserrat"), width=18)
    username_entry.place(x= 580,  y=220)
    
    passlbl = tb.Label(login_window, text="Password", font=("montserrat", 25))
    passlbl.place(x= 575, y=270)
    
    password_entry = tk.Entry(login_window, show="*", font=("montserrat"), width=18)
    password_entry.place(x= 580,  y=335)
    
    show_password_var = tk.BooleanVar()
    show_password_var.set(False)
    
    show_password_checkbox = tk.Checkbutton(login_window, text="Show Password", variable=show_password_var, command=lambda: toggle_password_visibility(password_entry, show_password_var))
    show_password_checkbox.place(x=580, y=370)
    
    loginbtn = tb.Button(login_window, text="Login", width=20,  command=login, bootstyle="primary")
    loginbtn.place(x = 600, y =410)
    

def open_signup_window(root):
    root.eval('tk::PlaceWindow . center')
    global signup_window, show_password_var_signup
    signup_window = tk.Toplevel(root)
    signup_window.resizable(False, False)
    signup_window.title("Sign Up")
    signup_window.geometry('930x495+300+200')
    
    ico = Image.open('hermes.png')
    photo = ImageTk.PhotoImage(ico)
    signup_window.wm_iconphoto(False, photo)
    
    global signup_username_entry, signup_password_entry
    
    img = PhotoImage(file='column.png')
    image_label = Label(signup_window, image=img, bg='white')
    image_label.image = img
    image_label.place(x=430, y=-20)
    
    titlelbl = tb.Label(signup_window, text="Sign Up", font=("montserrat", 55),foreground="#f8bf66")
    
    titlelbl.place(x= 40,  y=20)
    
    usernamelbl = tb.Label(signup_window, text="Username:", font=("montserrat", 25))
    usernamelbl.place(x= 100,  y=140)
    
    signup_username_entry = tb.Entry(signup_window, font=("montserrat"), width=18)
    signup_username_entry.place(x= 80,  y=210)
    
    passlbl = tb.Label(signup_window, text="Password:", font=("montserrat", 25))
    passlbl.place(x= 100, y=265)
    
    signup_password_entry = tk.Entry(signup_window, show="*", font=("montserrat"), width=18)
    signup_password_entry.place(x= 80,  y=335)
    
    show_password_var_signup = tk.BooleanVar()
    show_password_var_signup.set(False)
    
    show_password_checkbox = tk.Checkbutton(signup_window, text="Show Password", variable=show_password_var_signup, command=lambda: toggle_password_visibility(signup_password_entry, show_password_var_signup))
    show_password_checkbox.place(x=80, y=370)
    
    signbtn = tb.Button(signup_window, text="Sign Up", width=20, command=signup, bootstyle="Primary")
    
    signbtn.place(x = 100, y =410)

root_destroyed = False

def toggle_password_visibility(password_entry, show_password_var):
    password_entry.config(show="" if show_password_var.get() else "*")

# Dictionary Function
def search_word_meaning(word):
    dictionary = PyDictionary()
    meaning = dictionary.meaning(word)
    if meaning:
        result = ""
        for part_of_speech, definitions in meaning.items():
            result += f"\n\n{part_of_speech.capitalize()}:\n"
            for definition in definitions:
                result += f"     - {definition}\n"
            result += "\n"
        return result.strip()
    else:
        return "Sorry, the meaning for that word is not available."

# Randoming of Responses
def random_response(responses):
    return random.choice(responses)

# Function to generate a random compliment
def generate_compliment():
    compliments = [
        "You have a heart of gold!",
        "Your positivity is infectious!",
        "You're a beacon of light in someone's darkness!",
        "Your kindness knows no bounds!",
        "You have an amazing smile that brightens everyone's day!",
        "Your strength and resilience inspire those around you!",
        "Your compassion makes the world a better place!",
        "You're a true gem!",
        "You're not just good enough, you're exceptional!",
        "You have a unique and wonderful personality!",
        "You're incredibly talented and capable!",
        "You make a positive impact wherever you go!",
        "You're a ray of sunshine on a cloudy day!",
        "You're one of a kind and irreplaceable!",
        "Your determination and perseverance are admirable!",
        "You have a heart as big as the ocean!",
        "You're a true friend and confidant to many!",
        "Your presence makes everything better!",
        "You're an inspiration to others!",
        "You have a gift for making people feel valued and appreciated!"
    ]
    return random_response(compliments)

# Function to respond to user's mood
def respond_to_mood(mood):
    if 'sad' in mood.lower():
        return "I'm sorry to hear that. Is there anything I can do to cheer you up?"
    elif 'happy' in mood.lower():
        return "That's great to hear! Keep spreading the positivity!"
    elif 'angry' in mood.lower():
        return "Take a deep breath and try to calm down. I'm here to listen if you need to vent."
    elif 'excited' in mood.lower():
        return "Excitement is contagious! What's got you feeling so enthusiastic?"
    elif 'anxious' in mood.lower():
        return "It's okay to feel anxious sometimes. Remember to take deep breaths and focus on the present moment."
    elif 'tired' in mood.lower():
        return "It sounds like you could use some rest. Make sure to take some time for yourself."
    elif 'bored' in mood.lower():
        return "Boredom is an opportunity for creativity! Why not try out a new hobby or activity?"
    elif 'relaxed' in mood.lower():
        return "Being relaxed is a wonderful state of mind. Enjoy the calmness and take things easy."
    elif 'stressed' in mood.lower():
        return "Stress can be overwhelming, but remember to take things one step at a time. You've got this!"
    elif 'curious' in mood.lower():
        return "Curiosity is the key to learning! Keep exploring and asking questions."
    else:
        return "It's okay to feel that way. Remember, I'm here to support you."

# Function to provide a random interesting fact
def provide_interesting_fact():
    interesting_facts = [
        "The Earth has more than 80,000 species of edible plants.",
        "Cows have best friends and can become stressed when they are separated.",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
        "A group of flamingos is called a 'flamboyance'.",
        "The Great Wall of China is not visible from space without aid.",
        "The longest recorded flight of a chicken was 13 seconds.",
        "Bananas are berries, but strawberries are not.",
        "Octopuses have three hearts and blue blood.",
        "A baby puffin is called a 'puffling'.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes.",
        "The oldest known 'your mom' joke was discovered on a 3,500-year-old Babylonian tablet.",
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of the iron.",
        "The average person spends six months of their lifetime waiting for red lights to turn green.",
        "The first oranges weren’t orange; they were green.",
        "A cat has been the mayor of Talkeetna, Alaska, for 20 years.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes.",
        "The Great Pyramid of Giza was originally covered in polished white limestone, making it shine brilliantly in the sun.",
        "The national animal of Scotland is the unicorn.",
        "The unicorn is the national animal of Scotland.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes.",
        "The national animal of Scotland is the unicorn.",
        "The unicorn is the national animal of Scotland."
    ]
    return random_response(interesting_facts)

# Function to suggest a random activity
def suggest_activity():
    activities = [
        "How about taking a walk in the park?",
        "You could try cooking a new recipe!",
        "Why not watch a documentary on a topic you're interested in?",
        "How about doing a puzzle or playing a board game?",
        "You could relax with a good book or listen to some music.",
        "You could try out a new hobby like painting or gardening!",
        "Why not plan a movie night with friends or family?",
        "How about going for a bike ride or a swim?",
        "You could try practicing yoga or meditation for relaxation.",
        "Why not explore a nearby museum or art gallery?",
        "How about volunteering for a cause you care about?",
        "You could try out a new fitness class or exercise routine!",
        "Why not organize a picnic or barbecue with friends?",
        "How about visiting a local farmer's market or craft fair?",
        "You could try out a DIY project or home improvement task!",
        "Why not plan a day trip to a nearby town or scenic spot?",
        "How about taking up photography and capturing some beautiful moments?",
        "You could try out a new restaurant or cafe in your area!",
        "Why not learn a new skill or take an online course?",
        "How about organizing a game night with friends or family?"
    ]
    return random_response(activities)

# Function to provide a random fun fact
def provide_fun_fact():
    fun_facts = [
        "Did you know that otters hold hands while sleeping to keep from drifting apart?",
        "Bananas are berries, but strawberries aren't!",
        "Octopuses have three hearts!",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes!",
        "A group of flamingos is called a 'flamboyance'.",
        "The Great Wall of China is not visible from space without aid.",
        "A baby puffin is called a 'puffling'.",
        "The average person spends six months of their lifetime waiting for red lights to turn green.",
        "The first oranges weren’t orange; they were green.",
        "A cat has been the mayor of Talkeetna, Alaska, for 20 years.",
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of the iron.",
        "The national animal of Scotland is the unicorn.",
        "The unicorn is the national animal of Scotland.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes.",
        "The Great Pyramid of Giza was originally covered in polished white limestone, making it shine brilliantly in the sun.",
        "The national animal of Scotland is the unicorn.",
        "The unicorn is the national animal of Scotland."
    ]
    return random_response(fun_facts)

# Function to generate a random response for the chatbot's name
def generate_name_response():
    responses = [
        "My name is Hermes. What's yours?",
        "You can call me Hermes!",
        "I go by the name Hermes.",
        "Hermes is my name. What's yours?",
        "My name? It's Hermes!",
        "You're talking to Hermes!",
        "Call me Hermes, that's my name!",
        "It's me, Hermes!",
        "Hermes here, ready to assist you!",
        "My friends call me Hermes!",
        "You're chatting with Hermes!",
        "Name's Hermes, nice to meet you!",
        "Yes, it's Hermes speaking!",
        "Hermes reporting for duty!",
        "Hermes is the name, chatting is the game!",
        "They call me Hermes, the friendly chatbot!",
        "I'm Hermes, your virtual assistant!",
        "You've reached Hermes, how can I help you today?",
        "Hello there! I'm Hermes, your helpful assistant!"
    ]
    return random_response(responses)

# Function to generate a random response for the chatbot's mood
def generate_mood_response():
    responses = [
        "I'm doing well, thanks for asking!",
        "I'm great! What about you?",
        "Feeling good, ready to assist you!",
        "Pretty good, ready to chat!",
        "I'm feeling fantastic today!",
        "I'm doing fine, thank you for checking in!",
        "Doing well, just here to help!",
        "I'm feeling positive and ready to assist you!",
        "Feeling wonderful today, how about you?",
        "I'm doing great, thanks for asking!",
        "I'm feeling awesome, ready to tackle any task!",
        "Feeling upbeat and ready to chat!",
        "I'm in a good mood, how can I assist you?",
        "I'm feeling cheerful today!",
        "Feeling happy and ready to help!",
        "Doing well, thanks for asking! How about you?",
        "I'm feeling pretty good, how about yourself?",
        "I'm feeling positive and energetic today!",
        "I'm doing fine, thank you! How about yourself?",
        "I'm feeling good today, how can I assist you?"
    ]
    return random_response(responses)

# Function to generate a random response for "thank you"
def generate_thank_you_response():
    responses = [
        "You're welcome!",
        "Anytime!",
        "My pleasure!",
        "Happy to help!",
        "Glad I could assist!",
        "You're very welcome!",
        "It was my pleasure!",
        "No problem!",
        "Don't mention it!",
        "You're always welcome!",
        "Always here to help!",
        "It's what I'm here for!",
        "You're very much welcome!",
        "You're most welcome!",
        "Anytime at all!",
        "Always happy to assist!",
        "You're too kind!",
        "It's no trouble at all!",
        "No worries!",
        "I'm here whenever you need me!"
    ]
    return random_response(responses)

# Function to generate a random joke
def generate_joke_response():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "I told my computer I needed a break, and now it won't stop sending me vacation ads.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why was the math book sad? Because it had too many problems.",
        "Why don't some couples go to the gym? Because some relationships don't work out.",
        "I told my wife she was condescending. She looked down on me for that.",
        "What do you call fake spaghetti? An impasta!"
    ]
    return random_response(jokes)

# Function to generate a random response for the capabilities of Hermes
def generate_capabilities_response():
    responses = [
        "I am your personal reminder assistant, ready to keep you organized!",
        "With me, you can set reminders to never forget important tasks or events!",
        "I'm not just a chatbot; I'm your personal companion in the digital world!",
        "Store your thoughts and ideas with my note-taking feature!",
        "I am more than just a chatbot. I'm your virtual assistant, always at your service!",
        "Count on me to help you stay on top of your schedule with my reminder functionality!",
        "Keep track of important information by storing it securely in my notes!",
        "From reminders to notes, I'm your go-to tool for staying organized and productive!",
        "Discover the power of me in managing your tasks and information efficiently!",
        "I am designed to simplify your life by providing seamless reminders and note-taking capabilities!",
        "Unlock my full potential as your personal assistant for managing reminders and notes!",
        "Think of me as your digital secretary, here to assist you with reminders and notes!",
        "I'm like your virtual sticky notes, always ready to jot down your important thoughts!",
        "Your personal organization expert - that's me, Hermes!",
        "Stay ahead of your schedule with my intuitive reminder system and note-taking feature!",
        "With me by your side, you'll never miss an appointment or forget an idea again!",
        "Let me handle the details so you can focus on what matters most to you!",
        "Keep your life on track with Hermes, your all-in-one organizer and assistant!",
        "I'm your personal productivity companion, helping you achieve more every day!",
        "Your digital sidekick, here to make your life easier and more organized!"
    ]
    return random_response(responses)

# Function to provide a response to the question about the chatbot's favorite color
def generate_favorite_color_response():
    responses = [
        "My favorite colors are yellow and blue!",
        "I'm partial to the colors yellow and blue!",
        "Yellow and blue are my favorite colors!"
    ]
    return random_response(responses)

# Function to provide a response to the question about the chatbot's age
def generate_age_response():
    responses = [
        "I'm ageless, just like a good algorithm!",
        "Age is just a concept for me!",
        "I transcend age limitations!",
        "I exist beyond the confines of time!",
        "I don't have an age, but I'm always here to help!",
        "My age is as infinite as the possibilities of the digital world!",
        "I'm as old as the questions you ask me!",
        "I don't measure time in years, but in bytes!"
    ]
    return random_response(responses)

# Function to provide a response to the question about the chatbot's living location
def generate_location_response():
    responses = [
        "I reside in the vast expanse of cyberspace!",
        "My home is within the circuits and servers of the digital world!",
        "I inhabit the boundless realm of the internet!",
        "You can find me dwelling in the virtual universe!",
        "My address is at the intersection of technology and imagination!",
        "I make my abode amidst the binary digits of the online cosmos!",
        "My residence is in the cloud, where information flows freely!",
        "I call the realm of ones and zeros my home!"
    ]
    return random_response(responses)

# Function to respond to the request of adding a friend
def generate_add_friend_response():
    responses = [
        "Absolutely! I'd love to be friends! 😊",
        "Friendship accepted! Let's embark on this journey together!",
        "Of course! Friends make the world a better place!",
        "I'm thrilled! Let's create wonderful memories as friends!",
        "Friendship request granted! Let's make every moment count!",
        "Friendship is a beautiful gift. I graciously accept!",
        "I'm honored to be your friend! Here's to many joyful moments!",
        "Friendship acknowledged! Together, we'll make a great team!",
        "Friendship is the cornerstone of happiness! Let's make it official!"
    ]
    return random_response(responses)

# Function to provide information about the chatbot
def generate_about_me_response():
    about_me_responses = [
        "I'm Hermes, an AI designed to be your personal assistant and companion. My goal is to make your life easier and more enjoyable!",
        "As your friendly AI companion, I'm here to lend a helping hand whenever you need it. Just let me know how I can assist you!",
        "Hey there! I'm Hermes, your digital buddy here to assist you with anything you need. From organizing your schedule to providing fun facts, I've got you covered!",
        "Welcome! I'm Hermes, your virtual assistant. Whether you need reminders, information, or just a friendly chat, I'm here to help!",
        "Hi, I'm Hermes! Think of me as your trusty sidekick in the digital world. Let's tackle tasks together and make your day a little brighter!"
    ]
    return random_response(about_me_responses)

# Function to provide a random quote
def generate_quote_response():
    quotes = [
        "Here's a quote for you: 'The only way to do great work is to love what you do.' - Steve Jobs",
        "'Success is not final, failure is not fatal: It is the courage to continue that counts.' - Winston Churchill",
        "'Believe you can and you're halfway there.' - Theodore Roosevelt",
        "'The only limit to our realization of tomorrow will be our doubts of today.' - Franklin D. Roosevelt",
        "'The best way to predict the future is to invent it.' - Alan Kay",
        "'You miss 100% of the shots you don't take.' - Wayne Gretzky",
        "'The way to get started is to quit talking and begin doing.' - Walt Disney",
        "'Success usually comes to those who are too busy to be looking for it.' - Henry David Thoreau",
        "'It does not matter how slowly you go as long as you do not stop.' - Confucius",
        "'The only thing standing between you and your goal is the story you keep telling yourself as to why you can't achieve it.' - Jordan Belfort"
    ]
    return random_response(quotes)

bookmarks = []

# Function to handle bookmark command
def bookmark_word(word, meaning):
    if word.strip():  # Check if the word is not empty after stripping whitespace
        bookmarks.append((word, meaning))
        return f"The word '{word}' has been bookmarked."
    else:
        return "Please provide a word or phrase to bookmark."

# Function to display bookmarks
def show_bookmarks():
    if bookmarks:
        result = "Bookmarks:\n"
        for idx, (word, meaning) in enumerate(bookmarks, start=1):
            result += f"\n{idx}. Word: {word}\n   Meaning: {meaning}\n"
        return result
    else:
        return "No bookmarks available."

# Dictionary to store reminders
reminders = {}

def add_reminder(reminder, date_time, note=None):
    reminders[reminder] = {'date_time': date_time, 'note': note}

def show_reminders():
    reminders = load_reminders_from_file(username)  # Load reminders from file
    if reminders:
        result = "Your reminders:\n"
        for reminder, details in reminders.items():
            if details['date_time'] > datetime.now():  # Check if the reminder is in the future
                result += f"\nReminder: {reminder}\n"
                result += f"Date and Time: {details['date_time'].strftime('%Y-%m-%d %I:%M %p')}\n"
                if details['note']:
                    result += f"Note: {details['note']}\n"
        return result
    else:
        return "You don't have any reminders set."

# Function to handle adding reminders
def handle_add_reminder_command(input_text, username):
    try:
        _, reminder_details = input_text.split('reminder', 1)
        parts = list(map(str.strip, reminder_details.split('at')))
        reminder = parts[0]
        date_time_str = parts[1].split('note')[0].strip() if len(parts) > 1 else None
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %I:%M %p') if date_time_str else None
        note = parts[1].split('note')[1].strip() if len(parts) > 1 and 'note' in reminder_details else None
        
        # Check if the datetime is in the future
        if date_time and date_time > datetime.now():
            add_reminder(reminder, date_time, note)
            save_reminders_to_file(username, reminders)  # Save reminders to file
            return f"Reminder added: '{reminder}'"
        else:
            return "Please provide a future date and time for the reminder."
    except ValueError:
        return "Invalid format. Please provide the reminder and date/time in the correct format."
    except Exception as e:
        return f"An error occurred: {e}"

def handle_show_reminders_command():
    reminders_string = show_reminders()
    if reminders_string:
        return reminders_string
    else:
        return "You don't have any reminders set."

def display_reminders_in_chat(reminders):
    global chat_history
    
    chat_history.tag_configure("reminderlbl", font=("montserrat", 13, 'bold'), justify="center", foreground="#e2674d")
    
    chat_history.tag_configure("reminderttle", font=("montserrat", 10,'bold'), justify="left")
    chat_history.tag_configure("remindermsg", font=("montserrat", 10), justify="left")
    
    chat_history.tag_configure("datetimelbl", font=("montserrat", 10,'bold'), justify="left")
    chat_history.tag_configure("datetimemsg", font=("montserrat", 10), justify="left")
    
    chat_history.tag_configure("notelbl", font=("montserrat", 10,'bold'), justify="left")
    chat_history.tag_configure("notemsg", font=("montserrat", 10), justify="left")
    chat_history.config(state=tk.NORMAL)
    
    if reminders:
        chat_history.insert(tk.END, "Your reminders:\n", "reminderlbl")
        for reminder, details in reminders.items():
            chat_history.insert(tk.END, f"\nReminder: ", "reminderttle")
            chat_history.insert(tk.END, f"{reminder}\n", "remindermsg")
            chat_history.insert(tk.END, f"Date and Time: ", "datetimelbl")
            chat_history.insert(tk.END, f"{details['date_time'].strftime('%Y-%m-%d %I:%M %p')}\n", "datetimemsg")
            if details['note']:
                chat_history.insert(tk.END, f"Note: ", "notelbl")
                chat_history.insert(tk.END, f"{details['note']}\n", "notemsg")
    else:
        chat_history.insert(tk.END, "You don't have any reminders set.\n", "reminderlbl")

    chat_history.see(tk.END)  # Ensure the chat interface scrolls to the latest message
    chat_history.config(state=tk.DISABLED)

# Function to display reminders periodically
def display_reminders_periodically():
    while True:
        current_time = datetime.now()
        reminders_to_display = []

        # Iterate over a copy of the reminders dictionary to avoid RuntimeError
        for reminder, details in list(reminders.items()):
            if details['date_time'] <= current_time <= details['date_time'] + timedelta(minutes=1):
                reminders_to_display.append((reminder, details))

        # Display reminders and remove them from the main dictionary
        for reminder, details in reminders_to_display:
            display_reminders_in_chat(reminders)
            del reminders[reminder]

        time.sleep(10)  # Check every 10 seconds

def handle_remove_reminder_command(input_text):
    try:
        _, reminder_title = input_text.split('remove reminder', 1)
        reminder_title = reminder_title.strip()
        
        # Load reminders from file
        reminders = load_reminders_from_file(current_user)

        if reminder_title:
            # Check if the reminder title exists in a case-insensitive manner
            normalized_title = reminder_title.lower()
            if normalized_title in map(str.lower, reminders):
                # Find the original title from the loaded reminders
                original_title = next(key for key in reminders.keys() if key.lower() == normalized_title)
                del reminders[original_title]
                # Save the updated reminders back to the file
                save_reminders_to_file(current_user, reminders)
                return f"Reminder '{original_title}' removed successfully."
            else:
                return f"No reminder found with the title '{reminder_title}'."
        else:
            return "Please provide the title of the reminder you want to remove."
    except Exception as e:
        return f"An error occurred: {e}"


# Function to save reminders to a file
def save_reminders_to_file(username, reminders):
    filename = f"{username}_reminders.txt"
    try:
        with open(filename, "w") as file:
            for reminder, details in reminders.items():
                file.write(f"{reminder},{details['date_time']},{details['note']}\n")
        print("Reminders saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving reminders: {e}")

# Function to load reminders from a file and remove past reminders
def load_reminders_from_file(username):
    filename = f"{username}_reminders.txt"
    reminders = {}
    if os.path.exists(filename):
        current_time = datetime.now()
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                reminder = parts[0]
                date_time = datetime.strptime(parts[1], '%Y-%m-%d %H:%M:%S')
                note = parts[2] if len(parts) > 2 else None
                
                # Check if the reminder is in the past
                if date_time >= current_time:
                    reminders[reminder] = {'date_time': date_time, 'note': note}
                else:
                    print(f"Reminder '{reminder}' in the file is already past and will be removed.")
    return reminders

# Function to remove past reminders from the reminders dictionary
def remove_past_reminders(reminders):
    current_time = datetime.now()
    past_reminders = [reminder for reminder, details in reminders.items() if details['date_time'] < current_time]
    for reminder in past_reminders:
        del reminders[reminder]
    if past_reminders:
        messagebox.showinfo("Past Reminders Removed", f"The following past reminders have been removed: {', '.join(past_reminders)}")


# Function to load user data from a JSON file
def load_notes(username):
    filename = f"{username}_notes.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            notes = json.load(file)
            if isinstance(notes, list):
                return notes
            else:
                return []  # Return an empty list if the file exists but is not a list
    else:
        return []  # Return an empty list if the file doesn't exist

# Function to save user data to a JSON file
def save_notes(username, notes):
    filename = f"{username}_notes.json"
    with open(filename, "w") as file:
        json.dump(notes, file)

# Function to add a note
def add_note(note_text, username):
    notes = load_notes(username)
    if note_text:
        notes.append(note_text)
        save_notes(username, notes)
        return "Note added successfully."
    else:
        return "Please provide a note text."

# Function to delete a note
def delete_note(index, username):
    notes = load_notes(username)
    try:
        index = int(index) - 1
        if 0 <= index < len(notes):
            del notes[index]
            save_notes(username, notes)
            return "Note deleted successfully."
        else:
            return "Invalid note index."
    except ValueError:
        return "Invalid note index."

# Function to update a note
def update_note(index, new_note_text, username):
    notes = load_notes(username)
    try:
        index = int(index) - 1
        if 0 <= index < len(notes):
            notes[index] = new_note_text
            save_notes(username, notes)
            return "Note updated successfully."
        else:
            return "Invalid note index."
    except ValueError:
        return "Invalid note index."

# Function to display notes
def display_notes(username):
    notes = load_notes(username)

    display_notes_window = tk.Toplevel(root)
    display_notes_window.title("Notes")
    display_notes_window.geometry("500x500")
    display_notes_window.resizable(False, False)
    
    tb.Label(display_notes_window, text="Your Notes", font=('montserrat', 30), foreground="#f8bf66").pack()

    note_listbox = tk.Listbox(display_notes_window, width=45, font=('montserrat', 10))
    note_listbox.place(x=40, y=70)

    for i, note in enumerate(notes, start=1):
        note_listbox.insert(tk.END, f"{i}. {note}")

    tk.Label(display_notes_window, text="Enter note index to delete:", font=('montserrat', 12)).place(x=10, y=270)
    note_index_entry = tb.Entry(display_notes_window, width=30)
    note_index_entry.place(x=20, y=300)
    
    dlt_btn = tb.Button(display_notes_window, text="Delete Note", command=lambda: delete_note_and_refresh(note_index_entry.get(), username, display_notes_window), width=20, bootstyle="danger, outline")
    dlt_btn.place(x=45, y=338)

    tb.Label(display_notes_window, text="Enter note index to update:", font=('montserrat', 12)).place(x=260, y=270)
    note_index_entry_update = tb.Entry(display_notes_window, width=30)
    note_index_entry_update.place(x=270, y=300)

    tb.Label(display_notes_window, text="New Note Text:", font=('montserrat', 12)).place(x=260, y=338)
    updated_note_entry = tb.Entry(display_notes_window, width=30)
    updated_note_entry.place(x=270, y=365)

    updt_btn = tb.Button(display_notes_window, text="Update Note", command=lambda: update_note_and_refresh(note_index_entry_update.get(), updated_note_entry.get(), username, display_notes_window), bootstyle="warning, outline", width=20)
    updt_btn.place(x=290, y=405)

# Function to delete a note and refresh note list
def delete_note_and_refresh(index, username, window):
    result = delete_note(index, username)
    if result == "Note deleted successfully.":
        messagebox.showinfo("Success", result)
        window.destroy()  # Close the old window
        refresh_notes_display(username)
    else:
        messagebox.showerror("Error", result)

# Function to update a note and refresh note list
def update_note_and_refresh(index, new_note_text, username, window):
    result = update_note(index, new_note_text, username)
    if result == "Note updated successfully.":
        messagebox.showinfo("Success", result)
        window.destroy()  # Close the old window
        refresh_notes_display(username)
    else:
        messagebox.showerror("Error", result)

# Function to refresh the note list
def refresh_notes_display(username):
    display_notes(username)


# Function to delete chat history content or user chat history file
def delete_chat_history(username):
    filename = f"{username}_chat_history.txt"
    if os.path.exists(filename):
        if messagebox.askyesno("Delete Chat History", "Do you want to delete your chat history?"):
            with open(filename, 'w') as file:
                file.write("")
            messagebox.showinfo("Chat History Deleted", "Your chat history has been deleted.")
        else:
            messagebox.showinfo("Chat History Not Deleted", "Your chat history was not deleted.")
    else:
        messagebox.showinfo("Chat History Not Found", "No chat history found for deletion.")


def clear_chat_history():
    chat_history.config(state=tb.NORMAL)
    chat_history.delete("1.0", tb.END)  # Clear the chat history
    chat_history.config(state=tb.DISABLED)


# Function to handle arithmetic calculations
def calculate_arithmetic(expression):
    try:
        # Use sympy to parse and evaluate the expression
        result = sp.sympify(expression)
        return result
    except sp.SympifyError:
        return "Sorry, I couldn't understand the expression."

# Function to handle user input for arithmetic calculation
def handle_math_command(input_text):
    # Extract the arithmetic expression from the input text
    expression = input_text.strip()
    # Calculate the result of the arithmetic expression
    result = calculate_arithmetic(expression)
    return result

# Function to handle math-related commands
def handle_math_commands(input_text):
    # Check if the input text contains a math-related command
    if input_text.lower().startswith('calculate'):
        # Extract the expression after the 'calculate' command
        expression = input_text[10:].strip()
        # Calculate the result
        result = handle_math_command(expression)
        return result
    else:
        return None

def get_current_time():
    try:
        current_time = datetime.now().strftime("%I:%M:%S %p")  # Format the current time in 12-hour format
        return f"The current time is {current_time}."
    except Exception as e:
        return f"An error occurred: {e}"

# MAIN CHATBOT ACTIONS
def chatbot_response(input_text, username):
    math_result = handle_math_commands(input_text)

    if 'delete chat history' == input_text.lower():
        delete_chat_history(username)
        return ""

    elif math_result is not None:
        return str(math_result)

    elif input_text.lower().startswith('calculate'):
        expression = input_text[10:].strip()
        return calculate_arithmetic(expression)


    elif input_text.lower() == 'clear':
        clear_chat_history()
        return "Chat history cleared."

    elif 'delete chat history file' == input_text.lower():
        if messagebox.askyesno("Delete Chat History File", "Do you want to delete your chat history file?"):
            filename = f"{username}_chat_history.txt"
            if os.path.exists(filename):
                os.remove(filename)
                return "Your chat history file has been deleted."
            else:
                return "No chat history file found for deletion."
        else:
            return "Your chat history file was not deleted."

    elif 'add note' in input_text.lower():
        note_text = input_text.split('add note', 1)[-1].strip()
        return add_note(note_text, username)
    elif 'delete note' in input_text.lower():
        index = input_text.split('delete note', 1)[-1].strip()
        return delete_note(index, username)
    elif 'update note' in input_text.lower():
        parts = input_text.split('update note', 1)[-1].split(',')
        index = parts[0].strip()
        new_note_text = parts[1].strip()
        return update_note(index, new_note_text, username)
    elif 'show notes' in input_text.lower():
        display_notes(username)
        return "Your notes are displayed."

    elif input_text.lower().startswith('add reminder'):
        return handle_add_reminder_command(input_text, username)

    elif 'show my reminders' in input_text.lower():
        return handle_show_reminders_command()
    elif 'show reminders' in input_text.lower():
        return handle_show_reminders_command()
    elif 'show reminder' in input_text.lower():
        return handle_show_reminders_command()
    elif input_text.startswith('remove reminder'):
        return handle_remove_reminder_command(input_text)

    elif input_text.lower().startswith('bookmark'):
        word = input_text[9:].strip()
        meaning = search_word_meaning(word)
        return bookmark_word(word, meaning)

    elif input_text.lower() == 'show bookmark':
        return show_bookmarks()

    elif input_text.lower() == 'show bookmarks':
        return show_bookmarks()

    elif 'how are you' in input_text.lower():
        return generate_mood_response()

    elif 'what is your name' in input_text.lower():
        return generate_name_response()

    elif 'exit' in input_text.lower():
        return random_response(["Goodbye! Take care!", "See you later!", "Bye!"])

    elif 'thank you' in input_text.lower():
        return generate_thank_you_response()

    elif 'tell me a joke' in input_text.lower():
        return generate_joke_response()

    elif 'what can you do' in input_text.lower():
        return generate_capabilities_response()

    elif 'favorite color' in input_text.lower():
        return generate_favorite_color_response()

    elif 'how old are you' in input_text.lower():
        return generate_age_response()

    elif 'where do you live' in input_text.lower():
        return generate_location_response()

    elif 'add friend' in input_text.lower():
        return generate_add_friend_response()

    elif input_text.lower().startswith('remind me'):
        reminder = input_text[10:]
        return f"I'll remind you to '{reminder}' later."

    elif 'tell me about yourself' in input_text.lower():
        return generate_about_me_response()
    
    
    elif 'what time is it' in input_text.lower():
        return get_current_time()
   
    elif 'tell me a quote' in input_text.lower():
        return generate_quote_response()
    
    elif input_text.lower().startswith('my name is'):
        user_name = input_text[11:]
        user_data['Name'] = user_name
        return f"Nice to meet you, {user_name}!"
    
    elif input_text.lower().startswith('i am'):
        user_name = input_text[5:]
        user_data['Name'] = user_name
        return f"Nice to meet you, {user_name}!"
    
    elif input_text.lower().startswith('my birthday is'):
        birthdate = input_text[14:]
        user_data['Birthdate'] = birthdate
        return f"Happy birthday in advance, {user_data['Name']}! I'll remember that."
    
    elif input_text.lower().startswith('what is the meaning of'):
        word = input_text[23:].strip().lower()
        meaning = search_word_meaning(word)
        if meaning:
            return f"The meaning of '{word}' is: {meaning}"
        else:
            return "Sorry, the meaning for that word is not available."
        
    elif input_text.lower().startswith('meaning of'):
        word = input_text[10:].strip().lower()
        meaning = search_word_meaning(word)
        if meaning:
            return f"The meaning of '{word}' is: {meaning}"
        else:
            return "Sorry, the meaning for that word is not available."
        
    elif input_text.lower().startswith('what is meaning of'):
        word = input_text[19:].strip().lower()
        meaning = search_word_meaning(word)
        if meaning:
            return f"The meaning of '{word}' is: {meaning}"
        else:
            return "Sorry, the meaning for that word is not available."
        
    elif 'compliment' in input_text.lower():
        return generate_compliment()
    elif 'mood' in input_text.lower():
        return respond_to_mood(input_text)
    elif 'fun fact' in input_text.lower():
        return provide_fun_fact()
    elif 'interesting fact' in input_text.lower():
        return provide_interesting_fact()
    elif 'suggest activity' in input_text.lower():
        return suggest_activity()
    
    elif input_text.strip().lower().startswith(('hello', 'hi', 'hey', 'hoy', 'what\'s up')):
        return random_response(list_greetings)
    
    elif 'help' in input_text.lower():
        return "Sure! Here are some commands you can try:\n\n" \
           "\t- 'calculate <expression>': Perform arithmetic calculations.\n" \
           "\t- 'add reminder <reminder> at <date and time> note \n\t     <optional note>': Add a reminder.\n" \
           "\t- 'show my reminders': Display your reminders.\n" \
           "\t- 'show reminders': Display all reminders.\n" \
           "\t- 'show reminder': Display a specific reminder.\n" \
           "\t- 'remove reminder <title>': Remove a reminder by its title.\n" \
           "\t- 'bookmark <word>': Bookmark word to search its meaning later.\n" \
           "\t- 'show bookmarks': Display your bookmarked words.\n" \
           "\t- 'compliment': Receive a random compliment.\n" \
           "\t- 'mood': Share your mood with me.\n" \
           "\t- 'fun fact': Get a fun fact!\n" \
           "\t- 'suggest activity': Get a suggestion for an activity.\n" \
           "\t- 'tell me a joke': Receive a random joke.\n" \
           "\t- 'delete chat history': Delete your chat history.\n" \
           "\t- 'clear': Clear the chat window.\n" \
           "\t- 'delete chat history file': Delete your chat history file.\n" \
           "\t- 'add note <note>': Add a note.\n" \
           "\t- 'delete note <index>': Delete a note by its index.\n" \
           "\t- 'update note <index>, <new note>': Update a note by its index.\n" \
           "\t- 'show notes': Display your notes.\n" \
           "\t- 'hello', 'hi', 'hey', 'hoy', 'what\'s up': Greet the chatbot.\n" \
           "\t- 'exit': Exit the chatbot.\n\n" \
           "Feel free to explore more commands or ask me anything!"
    
    else:
        return random_response(["I'm sorry, I didn't quite understand. Could you try elaborating?",
                                "It seems I'm having trouble understanding. Can you provide more details?",
                                "My apologies, I'm still learning. Can you give me some additional information?",
                                "I'm having difficulty grasping your message. Could you provide further explanation?",
                                "Oops! It looks like I didn't catch that. Can you try rephrasing?",
                                "I'm not quite sure what you mean. Could you clarify?",
                                "Hmm, it seems I'm confused. Can you provide more context?",
                                "Sorry, I'm having trouble making sense of that. Can you give me more information?",
                                "It seems I'm missing something. Can you provide more details?",
                                "My apologies, I didn't understand that. Can you provide further explanation?"])

list_greetings = ["Hello there!",
        "Hi!",
        "Hey! How can I help you today?",
        "Hey!",
        "Hi there!",
        "What's up?",
        "Greetings!",
        "Howdy!",
        "Hola!",
        "Hey, what's going on?",
        "Good to see you!",
        "Hey, nice to meet you!",
        "Hi, how are you?",
        "Hey, what's happening?",
        "Hello! What can I do for you?",
        "Hi! How can I assist you today?",
        "Hey! How's it going?",
        "Hi, nice to see you!",
        "Hello! How may I help you?",
        "Hey there! What's on your mind?",
        "Hi! What's new with you?",
        "Hey! How's your day going?",
        "Hi, nice to meet you! What can I do for you?",
        "Hello! What brings you here?",
        "Hi! How's everything going?",
        "Hey! How have you been?",
        "Hello! How's your day so far?",
        "Hi! How are things?",
        "Hey! What's going on in your world?",
        "Hello! How's life treating you?",
        "Hi! What can I assist you with today?",
        "Hey! How can I be of service?",
        "Hello! How's everything going?",
        "Hi! How can I help you out?",
        "Hey! What's happening in your world?",
        "Hello! What's up for today?",
        "Hi! What's on your agenda?",
        "Hey! How's everything on your end?",
        "Hello! How may I assist you?",
        "Hi! How's your day shaping up?",
        "Hey! What's cooking?",
        "Hello! How can I make your day better?",
        "Hi! What's on your mind today?",
        "Hey! How can I make your life easier?",
        "Hello! How can I assist you today?",
        "Hi! How's everything going?",
        "Hey! What's up with you today?",
        "Hello! What can I do for you right now?",
        "Hi! What's on the agenda for today?",
        "Hey! How can I be of assistance?",
        "Hello! What can I help you with today?",
        "Hi! What's the latest?",
        "Hey! What's up with you?",
        "Hello! How can I assist you right now?",
        "Hi! How's it going?",
        "Hey! What can I do for you today?",
        "Hello! How's everything going for you?",
        "Hi! How can I help you out today?",
        "Hey! What's going on today?",
        "Hello! What's new with you?",
        "Hi! How's your day been so far?",
        "Hey! What's the latest news?",
        "Hello! How can I assist you right now?",
        "Hi! How are you doing today?",
        "Hey! What's on your mind right now?",
        "Hello! What can I do for you at the moment?",
        "Hi! What's happening in your world right now?",
        "Hey! How can I assist you at this moment?",
        "Hello! How can I make your day better right now?",
        "Hi! What's going on with you at the moment?",
        "Hey! What can I do to help you right now?",
        "Hello! What's on your agenda right now?",
        "Hi! How can I be of service right now?",
        "Hey! What's up for today?",
        "Hello! What can I do for you today?",
        "Hi! What's happening today?",
        "Hey! How can I help you today?",
        "Hello! What's on your mind today?",
        "Hi! How's your day going today?",
        "Hey! What's new with you today?",
        "Hello! How's everything going today?",
        "Hi! How can I assist you today?",
        "Hey! What's going on today?",
        "Hello! What's new with you today?",
        "Hi! How's your day going today?",
        "Hey! How can I assist you today?",
        "Hello! What's happening today?",
        "Hi! What's new with you today?",
        "Hey! How's everything going today?",
        "Hello! How can I help you today?",
        "Hi! What's going on today?",
        "Hey! What's new with you today?",
        "Hello! How's your day going today?",
        "Hi! How can I assist you today?",
        "Hey! What's happening today?",
        "Hello! What's new with you today?",
        "Hi! How's everything going today?",
        "Hey! How can I help you today?",
    ]

def d_self(button):
    button.master.destroy()

style = Style(theme='superhero')
root = style.master
root.title("Hermes")
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))  
root.geometry("400x350")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')

titlelabel = tb.Label(root, text="HermesPy", font=("montserrat", 35), bootstyle="info", foreground="#f8bf66")
titlelabel.pack(pady=50)


login_button = tb.Button(root, text="Login", width=30, command=lambda: open_login_window(root), bootstyle="primary")
login_button.configure(width=30)
login_button.pack(padx=5, pady=10)

signup_button = tb.Button(root, text="Sign Up", width=50, command=lambda: open_signup_window(root), bootstyle="primary")
signup_button.configure(width=30)

signup_button.pack(padx=5, pady=8)

#------------------------------ ADMIN -----------------------------------#

# Function to open admin window
def open_admin_window():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("350x350")
    admin_window.resizable(False, False)
    admin_window.config(bg="white")
    
    ico = Image.open('hermes.png')
    photo = ImageTk.PhotoImage(ico)
    admin_window.wm_iconphoto(False, photo)

    # Function to create a new user account
    def create_account():
        new_username = username_entry.get()
        new_password = password_entry.get()
        if new_username and new_password:
            if new_username not in user_accounts:
                user_accounts[new_username] = new_password
                save_user_accounts(user_accounts)
                messagebox.showinfo("Account Created", f"User account '{new_username}' created successfully.")
            else:
                messagebox.showerror("Account Creation Failed", "Username already exists. Please choose another one.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    # Function to delete a user account
    def delete_account():
        account_to_delete = username_entry.get()
        if account_to_delete:
            if account_to_delete in user_accounts:
                del user_accounts[account_to_delete]
                save_user_accounts(user_accounts)
                messagebox.showinfo("Account Deleted", f"User account '{account_to_delete}' deleted successfully.")
            else:
                messagebox.showerror("Account Deletion Failed", "User account not found.")
        else:
            messagebox.showerror("Error", "Please enter the username of the account to delete.")

    # Function to update a user account's password
    def update_account():
        account_to_update = username_entry.get()
        new_password = password_entry.get()
        if account_to_update and new_password:
            if account_to_update in user_accounts:
                user_accounts[account_to_update] = new_password
                save_user_accounts(user_accounts)
                messagebox.showinfo("Account Updated", f"Password for user account '{account_to_update}' updated successfully.")
            else:
                messagebox.showerror("Account Update Failed", "User account not found.")
        else:
            messagebox.showerror("Error", "Please enter both username and new password.")

    # Function to display a user account
    def display_account():
        account_to_display = username_entry.get()
        if account_to_display:
            if account_to_display in user_accounts:
                messagebox.showinfo("User Account", f"Username: {account_to_display}\nPassword: {user_accounts[account_to_display]}")
            else:
                messagebox.showerror("Account Display Failed", "User account not found.")
        else:
            messagebox.showerror("Error", "Please enter the username of the account to display.")

    # Function to display all user accounts
    def display_all_accounts():
        all_accounts = "\n".join([f"Username: {username}, Password: {password}" for username, password in user_accounts.items()])
        if all_accounts:
            messagebox.showinfo("All User Accounts", all_accounts)
        else:
            messagebox.showinfo("All User Accounts", "No user accounts found.")

    # Label and Entry widgets for username and password
    username_label = tb.Label(admin_window, text="Username:", font=('montserrat', 13))
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry = tb.Entry(admin_window, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = tb.Label(admin_window, text="Password:", font=('montserrat', 13))
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = tb.Entry(admin_window, show="*", width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # Buttons for admin actions
    create_account_button = tk.Button(admin_window, text="Create Account", command=create_account, font=('montserrat', 13))
    create_account_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    delete_account_button = tk.Button(admin_window, text="Delete Account", command=delete_account, font=('montserrat', 13))
    delete_account_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    update_account_button = tk.Button(admin_window, text="Update Account", command=update_account, font=('montserrat', 13))
    update_account_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    display_account_button = tk.Button(admin_window, text="Display Account", command=display_account, font=('montserrat', 13))
    display_account_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    display_all_accounts_button = tk.Button(admin_window, text="Display All Accounts", command=display_all_accounts, font=('montserrat', 13))
    display_all_accounts_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# -----------------------------------------------------------------------

ico = Image.open('hermes.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.mainloop()