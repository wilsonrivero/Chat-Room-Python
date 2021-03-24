import socket
import threading


# Choosing nickname
nickname = input("What is your nickname? ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.204', 5000))


# Listening to server  and Sending Nickname
def receive():
   while True:
      try:
         #Receive message from server
         # if 'NICK' send nickname
         message =  client.recv(1024).decode('ascii')
         if message ==  'NICK':
            client.send(nickname.encode('ascii'))
         else:
            print(message)

      except:
         print('An error ocurred!')
         client.close()
         break

# Sending message to server
def write():
   while True:
      message = '{}:{}'.format(nickname, input(''))
      client.send(message.encode('ascii'))

#Start thread for listening and writing
received_thread = threading.Thread(target=receive)
received_thread.start()


wirte_thread = threading.Thread(target=write)
wirte_thread.start()