import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.62.0.213",8000))
currentChatroom = None 
joinID = None

def joinChatroom(chatname,username):
	message = "JOIN_CHATROOM: %s\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: %s" %(chatname,username);
	sock.send(message)
	data = conn.recv(1024)
	if "ERROR" in data:
		print data
		exit()
	else:
		print data
		messageContents = data.split("\n")
		currentChatroom = messageContents[0]
		joinID= messageContents[4]

def leaveChatroom(chatname,username):
	roomID = search(chatroomNames, chatname)
	message = "LEAVE_CHATROOM: %d\nJOIN_ID: %d\nCLIENT_NAME: %s" %(roomID,joinID,username);
	sock.send(message)
	data = conn.recv(1024)
