import random
from nltk.chat.util import Chat, reflections

def cht(text):
    pairs = [
        [
            r"hi|hey|hello",
            ["Hello", "Hey there"]
        ],
        [
            r"(what.*your.*name|name.*your.*what)",
            ["My name is GavetureBot. Nice to meet you!"]
        ],
        [
            r"quit",
            ["Bye, take care. It was nice talking to you!"]
        ],
        [
            r".*help.*",
            [
                "I'm not smart enough, you can type /? or /help instead",
                "Hey, if you need some help. try /? or /help",
                "Glad u ask, but i'm not as smart as chatGPT and friends. type /? or /help instead"
            ]
        ],
        [
            r"(.*)",
            [
                "Sorry, I didn't understand what you said.",
                "Sorry, i'm not really understand enough"
            ]
        ]
    ]

    random.shuffle(pairs)

    chatbot = Chat(pairs, reflections)

    response = chatbot.respond(text)
    return response