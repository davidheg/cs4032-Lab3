import socket
import threading
import os
import sys

run = True
max = 10
address = "192.168.60.128"
port = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
threadpool = [] #All the client threads being used
chatThreads = []
numberofThreads = 0 #The number of client threads
chatnames= []  #List of chatsnames, sorted by their reference number
usersInChats = [[]] # List of lists of all the users in each chat, sorted by chatroom reference no
messages = [[[]]] # List of lists of messages to send to each chat, by room reference
clients = [[]] #List of clients currently connected to the server

def sortThreadPool():
    while True:
        i = 0
        for thread in threadpool:
            if(not thread.isAlive()):
                threadpool.pop(i)
                global numberofThreads
                numberofThreads = numberofThreads - 1
                i = i + 1
        threadpool.sort()

def removeUserFromChatroom(roomref, joinID):
    usersInChats[roomref][joinID] = None
    message = "User %s has left the chatroom" %(clients[joinID])
    sendMessage(roomref, joinID, message)
    filter(None, usersInChats[roomref])
    return

def addUserToChatroom(roomref, clientName):
    id = len(usersInChats[roomref]) + 1
    print "UserID %d" %(id)
    usersInChats[roomref].insert(id,clientName)
    message = "User %s has joined the chatroom" %(clientName)
    sendMessage(roomref,id,message)
    return id

def createChatroom(name):
    chatnames.append(name)
    roomref = findChatroom(name)
    usersInChats.insert(roomref, [])
    chatThreads.insert(roomref, (threading.Thread(target = handleChat, args =(roomref,))))   

def leaveChatroom(conn,data):
    messageContents = data.split("\n")
    chatroom = messageContents[0].split(" ")[1]
    joinID = messageContents[1].split(" ")[1]
    clientName = messageContents[2].split(" ")[1]
    if chats[chatroom] == None:
        conn.send("ERROR_CODE: 2 \nERROR_DESCRIPTION: Chatroom does not exist")
    else:
        removeUserFromChatroom(chatroom, joinID)
        message = "LEFT_CHATROOM: %s\nJOIN_ID: %s" %(chatroom, joinID);   
        conn.send(message)

def findChatroom(name):
    i = 0
    for chat in chatnames:
        if  chat == name:
            return i
        i = i + 1
    return -1

def joinChatroom(conn,data):
    messageContents = data.split("\n")
    chatroom = messageContents[0].split(" ")[1]
    clientName = messageContents[3].split(" ")[1]
    i = findChatroom(chatroom)
    if i == -1:
        createChatroom(chatroom)
        i = findChatroom(chatroom)
    id = addUserToChatroom(i,clientName)
    message = "JOINED_CHATROOM: %s\nSERVER_IP: 0\nPORT: 0\nROOM_REF: %s\n JOIN_ID: %s" %(chatroom,i,id);
    conn.send(message)
    if not getUserAddress(clientName):
        clients.append([clientName, conn])
        print clients

    #Send error message if already in chatroom

def sendMessage(roomref, joinID, message):
    message = [roomref,joinID,message]
    messages[roomref].append(message)
    return   

def handleChat(roomref):
    chatMessages = messages[roomref]
    while true:
        for message in chatMessages:
            userID = message[0]
            string = message[1]
            userMessage = "CHAT: %s\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(roomref,clients[roomref],string)            
            conn = getUserAddress(usersInChats[roomref][userID])
            conn.send(userMessage)
            message = None
        fliter(None,chatMessages)

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

def getUserAddress(username):
    for user in clients:
        if user:
            if user[0] == username:
                return user
    return []

def getUserInfo(roomref, joinID):
    return usersInChats[roomref][joinID]

sock.bind((address,port))
print "Socket created at IP:%s and port:%d, now listening for clients" %(address,port)
sock.listen(5)
threading.Thread(target = sortThreadPool).start()
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
