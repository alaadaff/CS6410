# record = {'127.0.0.1:32689':[2345627354, 6]}



def addServer(record, tcpIP, timeStamp, digit):
    """
    tcpIP: '1.1.1.1.:67893'
    timeStamp: time.time() 2345627354
    digit: 5
    
    return: updated record dict
    """

    # check timestamp in right format

    #todo: try catch statements for any adversarial gossip

    record[tcpIP] = [timeStamp, digit]
    


def updateServer(record, tcpIP, timeStamp, digit):
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







