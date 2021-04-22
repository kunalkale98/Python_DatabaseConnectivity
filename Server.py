'''
Author: Kunal Kale
Date: 20-04-2021
Description: Multi client chat application with one server and database implementation  
'''

import os
import threading
import socket
import mysql.connector
import time
import logs
from dotenv import *

#logger implementation
logger = logs.set_logger()

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
port = int(os.getenv('PORT'))
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB')
    
#Server Socket Creation and set to listen
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,port))
server.listen()
logger.info("Server is Listening....")

#Server Class
class Server:
    #Constructor for Server class
    def __init__(self,db_host,db_user,db_pass,db_name,logger):
        self.conn = mysql.connector.connect(host=db_host,user=db_user,password=db_pass,database=db_name)
        self.cursor = self.conn.cursor()
        self.clients = []
        self.names = []
        self.logger = logger

    #Function to close database connection
    def close_conn(self):
        self.conn.close()

    #Function to display chat stored on database 
    def display(self):
        sql_query = "SELECT * FROM chat_data;"
        try:  
            self.cursor.execute(sql_query)
            result=self.cursor.fetchall()   
            for i in result:    
                data = i[1]
                print(data)
        except Exception:   
            self.logger.error('Error:Unable to fetch data.')

    #Function to broadcast the message to all clients
    def broadcast(self,message,connection):
        for client in self.clients:
            if(client!=connection):
                client.send(message)

    #Function to handle clients connected to the server
    def handle_client(self,client):
        while(True):
            try:
                time_stamp = time.ctime()
                message = client.recv(1024)
                data = str(message.decode('utf-8'))
                self.logger.info(data)
                self.broadcast(message,client)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                notify = f'{name} left the room'
                self.broadcast(notify.encode('utf-8'))
                self.names.remove(name)
                break
            else:
                sql_query = "INSERT INTO chat_data(chat) VALUES('{},{}');".format(time_stamp,data)
                try:
                    self.cursor.execute(sql_query)
                    self.conn.commit()
                except:
                    self.conn.rollback()
                self.display()

    #Function to receive messages from clients 
    def receive(self):
        while(True):
            connection,address = server.accept()
            connection.send("name".encode('utf-8'))
            name = connection.recv(1024).decode('utf-8')
            logger.info(f"Connected with {name}")
            connection.send("Connected to Server".encode('utf-8'))
            self.names.append(name)
            self.clients.append(connection)
            notify = f"{name} has joined the chat room"
            self.broadcast(notify.encode('utf-8'),connection)
            thread = threading.Thread(target=self.handle_client,args=(connection,))
            thread.start()

#Drivers Function
dbconn = Server(db_host,db_user,db_pass,db_name,logger)   
dbconn.receive()
dbconn.close_conn()
