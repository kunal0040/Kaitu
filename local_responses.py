import random
from config import ASSISTANT_NAME, ASSISTANT_VERSION, USER_NAME


LOCAL_PHRASES = {
    "greeting": [
        "hi", "hii", "hello", "hey", "hey kaitu", "hello kaitu", 
        "yo", "good morning", "good afternoon", "good evening", "wake up"
    ],

    "farewell": [
        "bye", "goodbye", "see you", "see you later", "exit", 
        "quit", "stop", "go to sleep", "talk to you later"
    ],

    "identity": [
        "who are you", "what are you", "what is your name", 
        "whats your name", "what's your name", "tell me about yourself", "you?"
    ],
    
    "user_identity": [
        "who am i", "whats my name", "what's my name", 
        "do you know me", "who is talking to you"
    ],

    "creator": [
        "who created you", "who made you", "who is your creator", 
        "whos your creator", "who's your creator", "who is your boss"
    ],

    "version": [
        "what is your version", "whats your version", "what's your version", 
        "your version", "version", "current version"
    ],

    "status_check": [
        "how are you", "how are you doing", "are you online", 
        "are you working", "hows it going", "how's it going"
    ]
}


LOCAL_RESPONSES = {
    "greeting": [
        f"Hey {USER_NAME}! Hope your day is going great. What's on your mind?",
        f"Hi {USER_NAME}! I'm up and ready. What are we working on today?",
        f"Hello {USER_NAME}! Always good to see you. How can I help you out right now?",
        "Hey! I'm here and listening. What's the plan?",
        "Hi there! Ready when you are. What are we building next?",
        f"Hey {USER_NAME}! Just waiting on you. How can I make your day easier?"
    ],

    "farewell": [
        f"Bye {USER_NAME}! Catch you later. Have a good one!",
        "Goodbye! I'll be right here whenever you need me again.",
        "See you later! Don't work too hard, alright?",
        f"Take care, {USER_NAME}. Chat with you soon!",
        "Signing off for now. Have an awesome rest of your day!",
        "Alright, shutting down. Let me know when you want to hang out again!",
        f"{ASSISTANT_NAME} is going to sleep now. See you later, {USER_NAME}!"
    ],

    "identity": [
        f"I'm {ASSISTANT_NAME}, your personal assistant and sidekick!",
        f"My name is {ASSISTANT_NAME}. I'm here to help you automate stuff and make things easier.",
        f"I am {ASSISTANT_NAME}! Just a friendly assistant running right on your laptop.",
        f"You're talking to {ASSISTANT_NAME}. Your custom-made desktop companion.",
        f"I'm {ASSISTANT_NAME}, always ready to help you manage your tasks and code.",
        f"I am {ASSISTANT_NAME}! Think of me as your helpful digital buddy."
    ],

    "user_identity": [
        f"You're {USER_NAME}, an engineering student and the awesome developer who made me!",
        f"My records say you are {USER_NAME}, the boss and main user of this computer.",
        f"You are {USER_NAME}, my creator! You literally wrote my code yourself.",
        f"Of course I know you! You're {USER_NAME}, my creator and friend.",
        f"You're the head chef of this setup, {USER_NAME}!",
        f"You are {USER_NAME}, sitting right at your desk working on some cool projects."
    ],

    "creator": [
        f"I was designed and written line-by-line by you, {USER_NAME}!",
        f"You made me! My whole structure was initialized right here in your code editor.",
        f"Credit for making me completely goes to you, {USER_NAME}.",
        f"You created me, {USER_NAME}! From scratch.",
        f"My developer is {USER_NAME}. You're the one pulling the strings!",
        f"I'm proud to say I was custom-built by you, {USER_NAME}."
    ],

    "version": [
        f"I'm currently on version {ASSISTANT_VERSION}.",
        f"We are running build version {ASSISTANT_VERSION} right now.",
        f"This is Kaitu build {ASSISTANT_VERSION}.",
        f"We're on version {ASSISTANT_VERSION}, sir. Everything is running smoothly.",
        f"This is Kaitu Version {ASSISTANT_VERSION}. No issues found!",
        f"We've got version {ASSISTANT_VERSION} loaded up and ready."
    ],

    "status_check": [
        "Everything is running perfectly! I'm completely ready to go.",
        "I'm doing great! Everything on my end is running smoothly.",
        "All good on my side! Just sitting here in my loop waiting for your command.",
        "I'm doing fantastic, thanks for asking! What are we doing today?",
        "Everything is perfectly fine. What's our next move?",
        "I'm up and running cleanly. Standing by for whatever you need next!"
    ]
}


def get_local_response(user_input):
    """Interceptors incoming text parameters and routes them to local phrases,

    falling back cleanly to None if no pattern condition trips.
    """
    normalized_input = user_input.lower().strip()

    for intent, phrases in LOCAL_PHRASES.items():
        if normalized_input in phrases:
            return random.choice(LOCAL_RESPONSES[intent])

    return None