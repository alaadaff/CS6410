import random
import socket

def addServer(record: dict, tcpIP: str, timeStamp: int, digit: int):
    """
    tcpIP: '1.1.1.1.:67893'
    timeStamp: time.time() 2345627354
    digit: 5
    
    return: updated record dict
    """

    # check timestamp in right format

    #todo: try catch statements for any adversarial gossip

    record[tcpIP] = [timeStamp, digit]
    


def updateServer(record: dict, tcpIP: str, timeStamp: int, digit: int):
    """
    tcpIP: '1.1.1.1.:67893'
    timeStamp: time.time() 2345627354
    digit: 7
    
    return: updated record dict
    """

    # compare server to current server info in record

    # if new digit or timestamp
    # check if timestampNEW > timestampOLD
        # update digit and timestamp
    
    currentTimestamp = record[tcpIP][0]
    currentDigit = record[tcpIP][1]
    
    #todo: try catch statements for adversarial time
    if timeStamp > currentTimestamp:
        #todo: try catch statements for adversarial digit
        record[tcpIP] = [timeStamp, digit]


def convertRecordToString(record: dict):
    """
    Returns a dictionary object as a list of string objects for sending over tcpip
    """
    final = [] # ["127.0.0.1:30000,463657697,6", "..."]
    for tcpip in record.keys():
        fullStr = str(tcpip) + "," + str(record[tcpip][0]) + "," + str(record[tcpip][1])
        final.append(fullStr)
    
    return final #final is ['127.0.0.1:56789,12345,5']


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


