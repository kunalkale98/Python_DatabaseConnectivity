'''
Author: Kunal Kale
Date: 20-04-2021
Description: Multi client chat application with one server and database implementation  
'''

import os
import threading
import socket
import logs
from dotenv import *

#logger implementation
logger = logs.set_logger()

#load environment variables
load_dotenv(find_dotenv())

#Connection to server
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
name = input('Enter Name: ')

#Function to receive messages from Server
def client_receive():
    while(True):
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'name':
                client.send(name.encode('utf-8'))
            else:
                logger.info(message)
        except:
            logger.error('Error!')
            client.close()
            break

#Function to send messages to Server
def client_send():
    while(True):
        message = f'{name}: {input("")}'
        logger.info(message)
        client.send(message.encode('utf-8'))

#Implementing multi threading for making it multi client
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()