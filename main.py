import threading
import socket
import random
import time
import os
import sys

import db


def server(event, lock):
    '''
    Recieves data from other clients and updates record
    '''

    while not event.is_set():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', PORT))
            s.listen()
            print(f"\nlistening on: {PORT}")
            
            while True:
                conn, addr = s.accept() #servers accepts or completes the connection
                if conn:
                    print(f"connected to {addr}")  
                    s.setblocking(True)
            
                    # with lock:
                    recordList = db.convertRecordToString(record)
                    for r in recordList:
                        conn.sendall(r.encode())
                        # response = conn.recv(2048)
                        # if not response:
                        #     print("no response from client")
                conn.close()
                


def client(event, lock):
    '''
    Accesses record, selects ports to gossip to, and sends data
    '''
    
    # while not event.is_set():

    while True:

        print("Waiting 3 seconds")
        time.sleep(3)
        
        # instantiate a socket
        y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try: 
            with lock:
                random_server = db.selectRandomPort(record, PORT)
            
            print(f"Connecting to a random port: {random_server}")
            y.connect((random_server[0], int(random_server[1])))

            data = y.recv(1024)
            while data:
                #return bytes / 3 different values (TCPIP, timeStamp, digit)
                if data:
                    data = data.decode(encoding='utf-8', errors='strict') #return string
                    data = data.split("\n") #return list based on split values
                    with lock:
                        print(f"Data received from server: {data}")
                        for d in data:
                            if d != '':
                                d_list = d.split(",")
                                if d_list[0] in record.keys():
                                    db.updateServer(record, d_list[0], int(d_list[1]), int(d_list[2]))
                                else:
                                    db.addServer(record, d_list[0], int(d_list[1]), int(d_list[2]))
                    
                data = y.recv(1024)
        
        except ConnectionRefusedError:
            print("Connection refused!")
            continue;
            
        y.close()

        
                    

        

if __name__ == "__main__":

    lock = threading.Lock()
    ipAddress = sys.argv[1] #server inputs its own ip addr / client inputs ip address it wants to connect to
    PORT = int(sys.argv[2])
    
    record = {}
    # add own tcpip to record
    db.addServer(record, ipAddress+':'+str(PORT), int(time.time()), 5)
    firstConnection = True 
    print("Record after server adds itself to db:", record)

    server_event = threading.Event() #when an event is first created it is in the not set state (False)
    client_event = threading.Event() #False
    
    # creating threads
    serverThread = threading.Thread(target=server, name='serverThread', args=(server_event,lock,))
    clientThread = threading.Thread(target=client, name='clientThread', args=(client_event,lock,))

    # starting threads
    serverThread.start()
    clientThread.start()

    while True:
        print(clientThread.is_alive()) 
        d = input("Enter IP address of new node with +IP:PORT. Or, enter digit.")
        if d:
            if d == "end":
                break     
            if d == "?":
                print(record)
            elif d[0] == "+":
                db.addServer(record, d[1:], 0, 0)
            elif int(d) in range (0,10):
                print("updating your own digit")
                # with lock:
                db.updateServer(record, ipAddress+':'+str(PORT), int(time.time()), d)
                print(record)      


    #user will input the IP address node they want to gossip with and port 
    # nodeToGossip = input("Please input IP address and port of node you want to start gossiping with: ") #string 127.0.0.1:56789

    
    
    # start program once other port has been entered
    # if nodeToGossip:
    #     gossip_client = nodeToGossip.split(":")

    # firstConnection = True #flag to connect to first node, or random node from db

    # clientThread.start()

    #check if threads are alive for debugging purposes
    


    # while True:
    #     d = input("Enter digit: ")
    #     if d:
    #         if d == "end":
    #             break     
    #         if d == "?":
    #             print(record)
    #         elif int(d) in range (0,10):
    #             print("updating your own digit")
    #             db.updateServer(record, ipAddress+':'+str(PORT), int(time.time()), d)
    #             print(record)
                 
       
    #Again check if threads are alive for debugging 
    # print(serverThread.is_alive())
    # print(clientThread.is_alive())



    server_event.set()  #changes flag to true
    client_event.set()   #true

    serverThread.join()
    clientThread.join()
    



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