import threading

from network import Network
import os
import time
from encryptor import ENCRYPTOR

programData = {"chosenContact": "","thread_stop_event": threading.Event, "chatting":False, "logged_in":False}
n = Network()
megamind = ENCRYPTOR()


def login(network, arguements):

    if not (len(arguements) == 2):
        return "Invalid login, format must be {username} {password}"

    stat = network.connect("login", arguements[0], arguements[1])

    if stat:
        programData["logged_in"] = True
        os.system('cls')
        return "Successful"
    return "Invalid username/password"


def register(network, arguements):
    if not (len(arguements) == 2):
        return "Invalid login, format must be {username} {password}"

    stat = network.connect("register", arguements[0], arguements[1])

    if stat:
        os.system('cls')
        programData["logged_in"] = True
        return "Successful"
    return "Username is already in use"


def add_contact(network, arguements):
    if not len(arguements) == 1:
        print("Invalid format, type '/add {username}' ")
    if programData["logged_in"]:
        check = network.send(["add", arguements[0]])
        return (check)
    else:
        return "Login first"

    return

def show_contacts(network):
    if programData["logged_in"]:
        contacts = network.send(["refresh"])
        return f"Your contacts: {contacts}"
    else:
        return "Login first"

def chat(network, arguements):
    if not programData["logged_in"]:
        return "Invalid, log in first"
    if not len(arguements) ==1:
        print("Invalid format, type '/chat {username}' ")

    if programData["chatting"]:
        reset_chat(network, False)


    if network.send(["contact_check", arguements[0]]):
        programData["chosenContact"] = arguements[0]
        programData["chatting"] = True
        programData["thread_stop_event"] = threading.Event()
        refresher = threading.Thread(target=receive_messages, args=(network, programData["thread_stop_event"]), daemon=True)
        refresher.start()
        os.system('cls')
        print("Now chatting with:", programData["chosenContact"] + "\n")

    else:
        print("Contact doesn't exist")
        return



def receive_messages(network, stop_event):
    last_messages_count = 0

    while not stop_event.is_set():
        messages = network.send(["retrieve", programData["chosenContact"]])

        if not isinstance(messages, dict):
            continue
        to = messages["to"]
        from_ = messages["from"]
        new_messages_count = len(to) + len(from_)

        if new_messages_count != last_messages_count:
            os.system('cls')
            last_messages_count = new_messages_count

            i, j = 0, 0

            while i < len(to) and j < len(from_):
                if to[i + 1] <= from_[j + 1]:
                    print("Me: ", megamind.kryptonite(to[i]))
                    i += 2
                else:
                    print(programData["chosenContact"] + ": ", megamind.kryptonite(from_[j]))
                    j += 2

            while i < len(to):
                print("Me: ", megamind.kryptonite(to[i]))
                i += 2
            while j < len(from_):
                print(programData["chosenContact"], ": ", megamind.kryptonite(from_[j]))
                j += 2

            time.sleep(0.1)




def reset_chat(network, bool):
    os.system('cls')
    if bool: print(f"Stopped chatting with {programData["chosenContact"]}")
    programData["thread_stop_event"].set()
    programData["chosenContact"], programData["chatting"] = "", False

def logout(network):
    os.system('cls')
    print(network.send(["logout"]))
    programData["chosenContact"], programData["thread_stop_event"], programData["chatting"], programData["logged_in"] = "",False,False,False

def parser(command):
    keyword = " "
    arguements = []
    cList = list(command)
    cList.append(" ")

    colon = False
    current_word = ""
    counter=0
    for x in range(len(cList)):
        current_letter = cList[x]
        if current_letter != " ":
            current_word += current_letter
        else:
            if current_word != "":
                arguements.append(current_word)
            current_word = ""

    keyword = arguements.pop(0)

    return keyword, arguements

def switcher(network):
    try:
        command = input("")
    except:
        print("Type letters!")

    if len(command) >1:
        if command[0] == "/":

            keyword, arguements = parser(command[1:])


            if keyword == "login" and not programData["logged_in"]:
                print(login(network, arguements))
            elif keyword == "register" and not programData["logged_in"]:
                print(register(network, arguements))

            elif keyword == "add":
                print(add_contact(network, arguements))

            elif keyword == "contacts":
                print(show_contacts(network))

            elif keyword == "chat":
                chat(network, arguements)

            elif keyword == "back" and programData["chatting"] and programData["logged_in"]:
                reset_chat(network, True)
            elif keyword == "logout" and programData["logged_in"]:
                logout(network)
            else:
                print("Invalid command!")

        elif programData["logged_in"] and programData["chatting"]:
            data = ["message", programData["chosenContact"], megamind.superman(command)]
            network.send(data)


os.system('cls')
while True:
    switcher(n)

