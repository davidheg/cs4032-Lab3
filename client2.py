import socket
import sys
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.60.128",8000))
chatrooms = []
JoinIDs = []

def joinChatroom(chatname,username):
	message = "JOIN_CHATROOM: %s\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: %s" %(chatname,username);
	sock.send(message)
	

def leaveChatroom(roomID,joinID,username):
	message = "LEAVE_CHATROOM: %d\nJOIN_ID: %d\nCLIENT_NAME: %s" %(roomID,joinID,username);
	sock.send(message)
 
def message(roomID, joinID, username, message):
	message = "CHAT: %d\n JOIN_ID: %d\nCLIENT_NAME: %s\n MESSAGE: %s\n\n" %(roomID, joinID, username, message);
	sock.send(message)

def disconnect(username):
	message = "DISCONNECT: 0\n PORT: 0\nCLIENT_NAME: %s" %(username);
	sock.send(message)

def receive():
	while True:
		data = sock.recv(1024)
		print data

threading.Thread(target = receive).start()
joinChatroom("room1", "client2")
time.sleep(15)