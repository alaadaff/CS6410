#Accept input from console for digits
#Connect to clients every 3 sec 
#Respond when clients connect 
#This part of the program will also include the threading

import threading
import socket
import random
import time
import os
import sys

import db



def selectRandomPort(record, PORT):
    '''
    Returns a random port number from record. Ensures that it does not return the system's local port. 
    This function is called every 3 seconds
    '''
    #choose from the keys in the dict, ie. this is a list of record keys (IP/port pair) --> string var '192.68.255.255:26789'

    randomTCPIP = random.choice(list(record))   
    
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)

    myTCPIP = host_ip+':'+str(PORT)

    #if the randomizer selected myTCPIP, then run it again
    print('available records: ', record)
    while randomTCPIP == myTCPIP:  #compare string to string
        randomTCPIP = random.choice(list(record)) 
    
    tcpipToGossipTo = randomTCPIP.split(':') # e.g. [127.0.0.1, 50000]
    return tcpipToGossipTo #prints a list of strings with an IP, port format [127.0.0.1, 50000]


def server(event):
    '''
    Recieves data from other clients and updates record
    '''

    while not event.is_set():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', PORT))
            s.listen()
            print(f"listening on: {PORT} ")
            
            while True:
                conn, addr = s.accept() #servers accepts or completes the connection
                if conn:
                    print(f"connected to {addr}")  
                    s.setblocking(True)
            
                    while True:
                        print_lock.acquire()
                        recordList = db.convertRecordToString(record)
                        print_lock.release()
                        for r in recordList:
                            conn.sendall(r.encode())
                            response = conn.recv(2048)
                            if not response:
                                break
                s.close()
                


def client(event):
    '''
    Accesses record, selects ports to gossip to, and sends data
    '''
    
    # while not event.is_set():

    while True:

        print("Waiting 3 seconds")
        time.sleep(3)
        
        # instantiate a socket
        y = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        random_server = selectRandomPort(record, PORT)
        print(f"Connecting to a random port: {random_server}")
        y.connect((random_server[0], int(random_server[1])))

        while True:
            data = y.recv(1024) #return bytes / 3 different values (TCPIP, timeStamp, digit)
            if data:
                data = data.decode(encoding='utf-8', errors='strict') #return string
                data = data.split(",") #return list based on split values
                print_lock.acquire()
                if data[0] in record.keys():
                    db.updateServer(record, data[0], int(data[1]), int(data[2]))
                else:
                    db.addServer(record, data[0], int(data[1]), int(data[2]))
                print_lock.release()
                print("TCP: ", data)
        y.close()

        # except ConnectionRefusedError:
        #     print("Connection refused!")
        #     continue;
            #else:
                    

        

if __name__ == "__main__":

    print_lock = threading.Lock()
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
    serverThread = threading.Thread(target=server, name='serverThread', args=(server_event,))
    clientThread = threading.Thread(target=client, name='clientThread', args=(client_event,))

    # starting threads
    serverThread.start()


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
                #gossip_client = d[1:].split(":")
                # start program once other port has been entered
                clientThread.start()
                client_event.set()
                time.sleep(3)
                #print(serverThread.is_alive())
            elif int(d) in range (0,10):
                print("updating your own digit")
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