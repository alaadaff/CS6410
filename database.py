# record = {'127.0.0.1:32689':[2345627354, 6]}



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






