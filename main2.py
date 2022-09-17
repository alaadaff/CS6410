#Accept input from console for digits
#Connect to clients every 3 sec 
#Respond when clients connect 
#This part of the program will also include the threading

import threading
import socket
import os
import sys
from database import updateServer, addServer 


# Port 1: 23456
# Port 2: 52789

port2 = 52789


def server():
    '''
    Recieves data from other clients and updates record
    '''

    # print("server assigned to thread: {}".format(threading.current_thread().name))
    # print("ID of process running server: {}".format(os.getpid()))
   
    s.bind(('', PORT))
    s.listen()
    print(f"listening on: {PORT} ")

    while True:
        conn, addr = s.accept() #servers accepts or completes the connection
        if conn:
            print(f"connected to {addr}")  

        while True:
            data = conn.recv(1024) #return bytes / 3 different values (TCPIP, timeStamp, digit)
            if not data:
                break
            data = data.decode(encoding='utf-8', errors='strict') #return string
            data = data.split(",") #return list based on split values
            if data[0] in record.keys():
                updateServer(record, data[0], int(data[1]), int(data[2]))
            else:
                addServer(record, data[0], int(data[1]), int(data[2]))
            print("TCP: ", data)
        
        conn.close()
        


def client():
    """
    Accesses record and randomly selects ports to gossip to every 3 sec
    """
    if port2 != PORT:
        try:
            y.connect(('127.0.0.1', port2))  #client connects after server listens
        except ConnectionRefusedError:
            print(
                f"Connection refused!"
            )
        else:
            while True:
                y.sendall(b"127.0.0.1:32689,2345627358,8\n")
                response = y.recv(2048)
                if not response:
                    break
            y.close()

        

if __name__ == "__main__":

    #print_lock = threading.lock()
    PORT = int(sys.argv[1])
    
    record = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("ID of process running main program: {}".format(os.getpid()))

    print("Main thread name: {}".format(threading.current_thread().name))

    # creating threads
    serverThread = threading.Thread(target=server, name='serverThread')
    clientThread = threading.Thread(target=client, name='clientThread')

    # starting threads
    serverThread.start()
    clientThread.start()

    while True:
        d = input("Enter digit: ")
        if d == "end":
            # wait for threads to finish
            serverThread.join()
            clientThread.join()
                
            s.close()
        # thread 1: accept input from console

        # thread 2: accept information (server)

        # thread 3: every 3 seconds, connect to new clients from db (client)


'''
# print ID of current process
    print("ID of process running main program: {}".format(os.getpid()))
 
    # print name of main thread
    print("Main thread name: {}".format(threading.current_thread().name))
 
    # creating threads
    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2') 
 
    # starting threads
    t1.start()
    t2.start()
 
    # wait until all threads finish
    t1.join()
    t2.join()
'''