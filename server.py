import socket
import threading
import os
import sys

run = True
max = 10
address = "10.62.0.213"
port = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
threadpool = []
numberofThreads = 0
chatnames= []
usersInChats = [[]]
messages = []
clients = []

def sortThreadPool():
    i = 0
    for thread in threadpool:
        if(not thread.isAlive()):
            threadpool.pop(i)
            global numberofThreads
            numberofThreads = numberofThreads - 1
            i = i + 1
    threadpool.sort()

def removeUserFromChatroom(roomref, joinID):
    for user in usersInChats[roomref]:
        if user == joinID:
            user = None
            #Add message to queue stating user has left chat
    filter(None, usersInChats[roomref])

def addUserToChatroom(roomref, joinID):
    usersInChats[roomref].append(joinID)
    #Add message to queue stating user has joined chat

def createChatroom(name):
    chatname.append(name)
    chatname.append([])

def leaveChatroom(conn,data):
        messageContents = data.split("\n")
        i = messageContents[0].split(" ")[1]
        if chats[i] == None:
            conn.send(" ERROR_CODE: 2 \nERROR_DESCRIPTION: Chatroom does not exist")
        else:
                

def findChatroom(name):
    i = 0
    for chat in chatnames:
        if  chat == name:
            return i
        i = i + 1
    return -1

def joinChatroom(conn,data):
    messageContents = data.split("\n")
    i = findChatroom(messageContents[0].split(" ")[1])
    if i == -1:
        createChatroom(messageContents[0].split(" ")[1])
        i = findChatroom(messageContents[0].split(" ")[1])
    id = len(clients) + 1
    addUserToChatroom(i,id)
    message = "JOINED_CHATROOM: %s\nSERVER_IP: 0\nPORT: 0\nROOM_REF: %s\n JOIN_ID: %s" %(messageContents[0].split(" ")[1],i,id);
    conn.send(message)
    #Send error message if already in chatroom

def sendMessage(data):
   

def handleClient(conn,addr):
    receiving = True
    while receiving:
        data = conn.recv(1024)
        if "JOIN" in data:
            joinChatroom(conn,data)
        elif data == "KILL_SERVICE\n":
            sock.close()
            os._exit(1)
        elif "LEAVE" in data:
            leaveChatroom(conn,data)
        elif "MESSAGE" in data:
            sendMessage(conn,data)

sock.bind((address,port))
print "Socket created at IP:%s and port:%d, now listening for clients" %(address,port)
sock.listen(5)
while run:
    print numberofThreads
    if numberofThreads < max:
        conn,addr = sock.accept()
        threadpool.append(threading.Thread(target = handleClient, args =(conn,addr,)))
        threadpool[numberofThreads].start()
        global numberofThreads
        numberofThreads = numberofThreads + 1
    else:
        print "There are no free threads"
    threading.Thread(target = sortThreadPool).start()
