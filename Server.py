'''
Author: Kunal Kale
Date: 15-04-2021
Description: Program for Server in Single Client Server Connection 
'''

import socket
import logs

#Function to Set Server to listen
def connect():
    try:
        server = socket.socket()
        logger.info("Socket Created Successfully")    
    except socket.error as error:
        logger.error("Socket creation failed: "+error)
    ip = 'localhost'
    port = 12000
    server.bind((ip,port))
    logger.info(f"Socket binded to port {port}")
    server.listen()
    logger.info("Socket is Listening.....")
    connection,address = server.accept()
    return connection

#Function to Receive and Send messages to Server
def session():
    connection = connect()
    while(True):
        data = input('Server: ')
        connection.send(bytes(data,'utf-8'))
        recvData = connection.recv(1024).decode()
        logger.info("Client: "+recvData)
        if(recvData.upper() == 'BYE'):
            break
    connection.close()

#Driver Function
if __name__=="__main__":
    logger = logs.set_logger()
    session()