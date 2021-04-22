'''
Author: Kunal Kale
Date: 15-04-2021
Description: Program for Client in Single Client Server Connection 
'''

import socket

#Function for Client Setup
def session():
    client = socket.socket()
    ip = 'localhost'
    port = 12000
    client.connect((ip,port))
    while(True):
        recvData = client.recv(1024).decode()
        logger.info("Server: "+recvData)
        data = input("Client: ")
        client.send(bytes(data,'utf-8'))
        if(data.upper() == 'BYE'):
            break
    client.close()

#Driver Function 
if __name__=="__main__":
    logger = logs.set_logger()
    session()