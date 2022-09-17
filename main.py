#Accept input from console for digits
#Connect to clients every 3 sec 
#Respond when clients connect 
#This part of the program will also include the threading

import threading
import socket


print_lock = threading.lock()

def Client():
    """
    
    """


def main():

    host = ""
    port = 35678

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(3)

    # thread 1: accept input from console

    # thread 2: accept information (server)

    # thread 3: every 3 seconds, connect to new clients from db (client)


