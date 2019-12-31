
import socket
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))

print('연결확인했다.')
clientSock.send('I am a client'.encode('utf-8'))

print('메세지 전송했다.')

data = clientSock.recv(1024)
print('받은 데이터: ', data.decode('utf-8'))
