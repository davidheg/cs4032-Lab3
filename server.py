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
chatnames= []  #List of chatnames, sorted by their reference number
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
    global usersInChats
    clientName = usersInChats[roomref][joinID]
    message = "User %s has left the chatroom" %(clientName)
    global usersInChats
    usersInChats[roomref][joinID] = None
    sendMessage(roomref, clientName, message)
    global usersInChats
    usersInChats = filter(None, usersInChats[roomref])
    return

def addUserToChatroom(roomref, clientName):
    global usersInChats
    id = len(usersInChats[roomref])
    global usersInChats
    usersInChats[roomref].insert(id,clientName)
    message = "User %s has joined this chatroom" %(clientName)
    sendMessage(roomref,clientName,message)
    return id + 1


def leaveChatroom(conn,data):
    messageContents = data.split("\n")
    roomref = int(messageContents[0].split(" ")[1])
    joinID = int(messageContents[1].split(" ")[1])
    clientName = messageContents[2].split(" ")[1]
    global chatnames
    if chatnames[roomref - 1] == None:
        conn.send("ERROR_CODE: 2 \nERROR_DESCRIPTION: Chatroom does not exist")
    else:
        removeUserFromChatroom(roomref - 1, joinID - 1)
        message = "LEFT_CHATROOM: %s\nJOIN_ID: %s" %(roomref, joinID);   
        conn.send(message)

def joinChatroom(conn,data):
    messageContents = data.split("\n")
    chatroom = messageContents[0].split(" ")[1]
    clientName = messageContents[2].split(" ")[1]
    i = findChatroom(chatroom)
    if i == -1:
        createChatroom(chatroom)
        i = findChatroom(chatroom)
    id = addUserToChatroom(i - 1,clientName)
    message = "JOINED_CHATROOM: %s\nSERVER_IP: 0\nPORT: 0\nROOM_REF: %s\n JOIN_ID: %s" %(chatroom,i,id);
    conn.send(message)
    if not getUserAddress(clientName):
        global clients
        clients.append([clientName, conn])

    #Send error message if already in chatroom

def createChatroom(name):
    global chatnames
    chatnames.append(name)
    roomref = findChatroom(name) - 1
    global usersInChats
    usersInChats.insert(roomref, [])
    global messages
    messages.insert(roomref,[])
    global chatThreads
    chatThreads.insert(roomref, (threading.Thread(target = handleChat, args =(roomref,))))
    chatThreads[roomref].start() 

def findChatroom(name):
    i = 1
    global chatnames
    for chat in chatnames:
        if  chat == name:
            return i
        i = i + 1
    return -1

def sendMessage(roomref, clientName, message):
    message = [roomref + 1,clientName,message]
    global messages
    messages[roomref].append(message)

def handleChat(roomref):
    chatMessages = messages[roomref]
    while True:
        global messages
        for message in messages[roomref]:
            if message != []:
                print message
                username = message[1]
                string = message[2]
                global usersInChats
                print usersInChats
                for user in usersInChats[roomref]:
                    print user
                    if user != username:
                        userMessage = "CHAT: %s\nCLIENT_NAME: %s\nMESSAGE: %s\n\n" %(roomref + 1,user,string)  
                        conn = getUserAddress(user)
                        conn.send(userMessage)
                message = None
        messages[roomref] = filter(None,chatMessages)
       

def handleClient(conn,addr):
    receiving = True
    while receiving:
        data = conn.recv(1024)
        if "JOIN_CHATROOM" in data:
            joinChatroom(conn,data)
        elif data == "KILL_SERVICE\n":
            sock.close()
            os._exit(1)
        elif "LEAVE_CHATROOM" in data:
            leaveChatroom(conn,data)
        elif "MESSAGE" in data:
            sendUserMessage(conn,data)

def sendUserMessage (conn,data):
    return
    
def getUserAddress(username):
    global clients
    for user in clients:
        if user:
            if user[0] == username:
                return user[1]

def getUserInfo(roomref, joinID):
    global usersInChats
    return usersInChats[roomref][joinID]

sock.bind((address,port))
print "Socket created at IP:%s and port:%d, now listening for clients" %(address,port)
sock.listen(5)
threading.Thread(target = sortThreadPool).start()
while run:
    if numberofThreads < max:
        conn,addr = sock.accept()
        global threadpool
        threadpool.append(threading.Thread(target = handleClient, args =(conn,addr,)))
        threadpool[numberofThreads].start()
        global numberofThreads
        numberofThreads = numberofThreads + 1
    else:
        print "There are no free threads"
