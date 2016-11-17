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
peoplePerChat = []
numberofThreads = 0
chats= []

def sortThreadPool():
    i = 0
    for thread in threadpool:
        if(not thread.isAlive()):
            threadpool.pop(i)
            global numberofThreads
            numberofThreads = numberofThreads - 1
            i = i + 1
    threadpool.sort()


def createChatroom(name):
    i = 0
    for chat in chats:
        if chat == None:
            newChat = name
            chat = newChat
        i = i + 1
    peoplePerChat.append(0)
    return i


def findChatroom(name):
    i = 0
    for chat in chats:
        if chat == name:
            return i 
        i = i + 1 
    return -1

def joinChatroom(conn,data):
    messageContents = data.split("\n")
    i = findChatroom(messageContents[0].split(" ")[1])
    if i == -1:
        i = createChatroom(messageContents[0].split(" ")[1])
    id = peoplePerChat[i] + 1
    message = "JOINED_CHATROOM: %s\nSERVER_IP: 0\nPORT: 0\nROOM_REF: %s\n JOIN_ID: %s" %(messageContents[0].split(" ")[1],i,id);
    conn.send(message)


def handleClient(conn,addr):
    
    receiving = True
    while receiving:
        data = conn.recv(1024)
        if "JOIN" in data:
            joinChatroom(conn,data)
        elif data == "KILL_SERVICE\n:
            sock.close()
            os._exit(1)
         #elif "LEAVE" in data:
         #   leaveChatroom(conn,data)

sock.bind((address,port))
print "Socket created at IP:%s and port:%d, now listening for clients" %(address,port)
sock.listen(5)
while run:
    if numberofThreads < max:
        conn,addr = sock.accept()
        threadpool.append(threading.Thread(target = handleClient, args =(conn,addr,)))
        threadpool[numberofThreads].start()
        global numberofThreads
        numberofThreads = numberofThreads + 1
    else:
        print "There are no free threads"
    threading.Thread(target = sortThreadPool).start()