import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.60.128",8000))
chatrooms = []
JoinIDs = []

def joinChatroom(chatname,username):
	message = "JOIN_CHATROOM: %s\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: %s" %(chatname,username);
	sock.send(message)
	data = sock.recv(1024)
	if "ERROR" in data:
		print data
		exit()
	else:
		print data

def leaveChatroom(chatname,username,roomID):
	message = "LEAVE_CHATROOM: %d\nJOIN_ID: %d\nCLIENT_NAME: %s" %(roomID,joinID,username);
	sock.send(message)
	data = conn.recv(1024)
	print data
 
def message(roomID, joinID, username, message):
	message = "CHAT: %d\n JOIN_ID: %d\nCLIENT_NAME: %s\n MESSAGE: %s\n\n" %(roomID, joinID, username, message);
	sock.send(message)

def disconnect(username):
	message = "DISCONNECT: 0\n PORT: 0\nCLIENT_NAME: %s" %(username);
	sock.send(message)

joinChatroom("Avengers", "davidheg")
