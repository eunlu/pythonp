# -*- coding: utf-8 -*-
import socket
import threading
# import time

#aynı andan birden çok işlemi yapmak için kütüphaneyi çağıtıyoruz.
# Böylelikle bir çok işlem aynı anda çalışırken değişken değerleri üzerinden değişiklik yapabiliriz.
tEv = threading.Event()
tShutdown = threading.Event()

#server dan bir şey geldiği zaman bunu ekrana basacak aynı zamanda yarışmanın bitip bitmediğini denetleyecek olan fonksyion
def receving(name, sock):
    shutdown = False
    while not shutdown:
        try:
            data, addr = sock.recvfrom(1024)
            print(str(data))
            if '?' in data:
                tEv.set()
            if data == "Oyun bitti":  # message from server to stop
                tShutdown.set()
                shutdown = True
        except:
            pass
        finally:
            pass


#bağlacağımız server ip adresi
host = '127.0.0.1'
#bu bilgisayardan server a bağlanırken kullanacağımız port. 0= boşta uygun ne varsa onu kullan
port = 0
server = (host, 5000)

#bağlantı için bir soket yarat
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#soketi server a bağlanmak için kullan
s.bind((host, port))
#bu portu program kapatmadığı sürece açık tut başka bir şey kullanmasın
s.setblocking(0)

#serverdan gelecek veriler veya mesajlar için bir listener oluştur.
#eğer bir şey gelirse receving fonksyionunu çalıştır.
rT = threading.Thread(target=receving, args=("RecvThread", s))
#listener ı çalıştır.
rT.start()

#yarışmaya başlamak için isim
alias = raw_input("Adınız: ")

# daha sonra işlemleri json ile yapacağımız için hazırlık
# send_msg = json.dumps({'ad':alias})
send_msg = 'Adınız ? :'
#yukarıda bağlantıyı yapmıştık soket ile bu verileri gönder
s.sendto(send_msg, server)

#oyun için sonsuz döngü oluştur ve beklemeye başla
running = True
while running:
    #bir çok işi aynı andayapmaya yarayan thread kütüphanesi burada devreyee giriyor.
    #yukarısı serverdab bir şey alıp işlemek için beklerken burasıda server a birşey göndermek için beklemede
    #wait() server üzerinden bir şey gelirse birşey göndermek için wihile döngüsünün içine input eklemede kullanıyoruz
    if tEv.wait(1.0):
        tEv.clear()
        message = raw_input("")
        if message != '':
            #yazdığımız şey boş değilse server a geri gönder
            s.sendto(message, server)
    #eğer yujarıdaki fonksiyonda server dan close talimatı gelmişse burdaki döngüyüde durdurmak lazım
    if tShutdown.is_set():
        running = False

#eğer buraya kadar gelmişsek join komutu yukarıdaki thread ları kapatmak için bekliyor. içine parametre yazarsak örneğin :10 10 saniye bekleyecekti.
rT.join()
#şimdide makinede açtığımız soketleri kapatma
s.close()
