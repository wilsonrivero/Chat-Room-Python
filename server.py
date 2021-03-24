import socket
import threading


#connection  Data
host = '192.168.1.204'
port = 5000


#starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


#list for the clients and their nicknames
clients = []
nicknames = []



#Sending  Message to all Connectec Clients
def broadcast(message):
   for client in clients:
      client.send(message)


#Hadling message from clients
def handle(client):
   while True:
      try:
         #Broadcast messages
         message = client.recv(1024)
         broadcast(message)
         
      except:
         # Removing and closing Clients
         index = clients.index(client)
         clients.remove(client)
         client.close()
         nickname = nicknames[index]
         broadcast(f'{nickname} left'.encode('ascii'))
         nicknames.remove(nickname)
         break

#Receiving / listening Function
def receive():
   while True:
      #Accept Connection
      client, address = server.accept()
      print('Connected with {}'.format(str(address)))

      # Request  And Store  Nickname
      client.send('NICK'.encode('ascii'))
      nickname = client.recv(1024).decode('ascii')
      nicknames.append(nickname)
      clients.append(client)


      #Print and broadcast Nickname
      print(f'Nickname is {nickname}')
      broadcast('{} joined!'.format(nickname).encode('ascii'))
      client.send('Connected to server'.encode('ascii'))

      # Start handling Thread for client
      thread = threading.Thread(target=handle, args=(client,))
      thread.start()



receive()