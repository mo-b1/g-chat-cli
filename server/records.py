import base64
import json
import queue
import threading
import time
from argon2 import PasswordHasher
import os

class database_manager:
    def __init__(self):
        self.data = {}
        self.file = "server/database.json"

        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self.ph = PasswordHasher()

    def _run(self):

        while True:
            func, args, result_queue = self.task_queue.get()
            try:
                result = func(*args)
                if result_queue:
                    result_queue.put(result)
            except Exception as e:
                print(f"Worker thread error: {e}")
                if result_queue:
                    result_queue.put(e)
            finally:
                self.task_queue.task_done()

    def add_task(self, func, *args, wait_for_result=True):

        result_queue = queue.Queue() if wait_for_result else None
        self.task_queue.put((func, args, result_queue))

        if result_queue is not None:
            result = result_queue.get()
            if isinstance(result, Exception):
                raise result
            return result



    #-----------------------database management functions---------------------------
    def load_data(self):
        try:
            with open(self.file, "r") as f:
                self.data = json.load(f)
        except Exception as e:
            print("Error loading data: ",e)

    def save_data(self):
        try:
            with open(self.file, "w") as f:
                json.dump(self.data,f)
        except Exception as e:
            print("Error saving server data: ", e)

    def update(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def new_user(self, name, password):
        if name not in self.data:
            self.data[name] = {"password": self.ph.hash(password), "contacts": {}}
            self.save_data()
            return True
        return False

    def validator(self, name, password):
        if name in self.data:
            return self.ph.verify(self.data[name]["password"], password)


    def save_message(self, sender, receiver, message, time):
        if sender in self.data and receiver in self.data:
            if receiver in self.data[sender]["contacts"]:
                self.data[sender]["contacts"][receiver]["to"].append(message)
                self.data[sender]["contacts"][receiver]["to"].append(time)
            if sender in self.data[receiver]["contacts"]:
                self.data[receiver]["contacts"][sender]["from"].append(message)
                self.data[receiver]["contacts"][sender]["from"].append(time)
        self.save_data()

    def remove_contact(self, user, contact):
        del self.data[user]["contacts"][contact]
        self.save_data()

    def add_contact(self, user, contact):
        if  contact == user:
            return "Can't add yourself"
        if contact not in self.data:
            return f"{contact} doesn't exist"
        if contact not in self.data[user]["contacts"]:
            self.data[user]["contacts"][contact] = {}
            self.data[user]["contacts"][contact] = {}
            self.data[user]["contacts"][contact]["to"] = []
            self.data[user]["contacts"][contact]["from"] = []
            self.save_data()
            return f"Successfully added {contact}!"
        return "Already added!"




    def is_Contact (self, user, name):
        if name in self.data[user]["contacts"]:
            return True
        else:
            return False

    def retrieve_messages(self, user, contact):
        if contact in self.data[user]["contacts"]:
            return self.data[user]["contacts"][contact]
        else:
            return "Contact doesn't exist"


    def retrieve_contacts(self,user):
        try:
            contacts = [contact for contact in self.data[user]["contacts"]]
        except Exception as e:
            print("Error retrieving contacts: ", e)
        if len(contacts) == 0:
            return "No contacts"
        else:
            return contacts

    def retrieve_all_users(self):
        return [user for user in self.data]
