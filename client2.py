# -*- coding: utf-8 -*-
import socket
import threading
import time

tEv = threading.Event()
tShutdown = threading.Event()

def receving(name, sock):
    shutdown = False
    while not shutdown:
        try:
            data,addr = sock.recvfrom(1024)
            print(str(data))
            if '?' in data:
                tEv.set()
            if data == "The game is finished":  # message from server to stop
                tShutdown.set()
                shutdown = True
        except:
            pass
        finally:
            pass

#host = '192.168.26.86'
host = '127.0.0.1'
port = 0 #pick any free port currently on the computer
server = (host, 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

# Start listener
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# Join the game
alias = raw_input("Adınız: ")
s.sendto(alias, server)

running = True
while running:
    if tEv.wait(1.0):
        tEv.clear()
        message = raw_input(alias + ", Cevabınız ?  ->\n ")
        if message != '':
            s.sendto(alias + ": " + message, server)
    if tShutdown.is_set():
        running = False

rT.join()
s.close()