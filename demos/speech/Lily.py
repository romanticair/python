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
lily = Person('Lily', 'female', 18)
client.send(lily.name.encode('utf-8'))
name = client.recv(1024).decode('utf-8')

t = threading.Thread(target=receive_msg, args=(client,), daemon=True)
t.start()

msg = input('write down the message you want to say to <{0}>\n'.format(name)).strip()
while True:
    client.send(msg.encode('utf-8'))
    lily.engine.say(msg)
    lily.engine.runAndWait()
    msg = input('(Stop by quit) ').strip()
    if msg.lower() == 'quit':
        lily.engine.stop()
        break

client.send(b'exit')
client.close()
