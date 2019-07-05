import time
import socket
import threading
from Person import Person


def receive_msg(client):
    while True:
        msg = client.recv(1024)
        if msg:
            print('Received --- {0}'.format(msg.decode('utf-8')))
        time.sleep(1)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))
print(client.recv(1024).decode('utf-8'))
bily = Person('Bily', 'male', 20)
client.send(bily.name.encode('utf-8'))
name = client.recv(1024).decode('utf-8')

t = threading.Thread(target=receive_msg, args=(client,), daemon=True)
t.start()

msg = input('write down the message you want to say to <{0}>\n'.format(name)).strip()
while True:
    client.send(msg.encode('utf-8'))
    bily.engine.say(msg)
    bily.engine.runAndWait()
    msg = input('(Stop by quit) ').strip()
    if msg.lower() == 'quit':
        bily.engine.stop()
        break

# 通知服务器，断开连接
client.send(b'exit')
client.close()
