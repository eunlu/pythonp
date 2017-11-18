# -*- coding: utf-8 -*-
import numpy as np
#from numpy.random import shuffle
#from random import randint
import socket
#import time
import select
import urllib, json


questions_count=10 #kaç soruluk bir yarışma olacak
score = [0] #oyuncu skorları için liste
host = '127.0.0.1' # sistemin çalışacağı ip adresi
port = 5000 # port numarası
players = [] #oyuncu listesi
question2=[] #soru listesi
answer2 = [] #soru şıkları listesi
right_answers2 = [] #doğru cevpların listesi
question_score = [] #soru puanlarının listesi
secs = 10 # belli bir limit değilde belli bir sürede başlayacak yarışma için süre tanımı
max_players = 1 #aynı anda yarışacak kişi sayısı

# yarışma bilgilerini alacağımız link
url = "http://pendik.net/iya/api/app/soru_istek/"+str(questions_count)
response = urllib.urlopen(url)
# yarışma bilgilerinin decode edilmesi ve değişkene aktarılması
data = json.loads(response.read())
#print json.dumps(data, sort_keys=True, indent=4)


# yarışma bilgilerinin tanımlı arraylara aktarımı
for i in data:
    #print i['soru_text'],"\n\n"
    question2.append(i['soru_text'])
    answer2.append(i['soru_secenek'])
    right_answers2.append(i['soru_dogru_cevap'])
    question_score.append(i['soru_puan'])

#yarışma sırasında bir soru getirecek olan fonksiyon
def get_question (question2,k):
    print question2[k]
    return question2[k].encode('utf-8')

#yarışma sırasında bir sorunun puanını getirecek olan fonksiyon
def get_question_score (score,k):
    sc = '%s puan'%score[k]
    print sc
    return sc

#yarışma sırasında verilen cevabın doğruluğunu kontrol eden fonksiyon
def checkAnswer(answer2,agiven, qnb):
    test = False
    if agiven == right_answers2[qnb]:
        test = True
        score[0] = score[0]+1
        return test
    else:
        return test
#yarışma sırasında bir soru şıklarını getiren fonksiyon
def get_options(answer2,k):
    ret = ''
    say =0
    for i in answer2[k]:
        ret = ret+'['+str(say)+']'+i+'\n'
        say=say+1
    print ret
    return ret.encode('utf-8')

#yarışma sonunda sıralamayı ve kazananı belirleyecek olan fonmksiyon
def final_score(score):
    print("The scores are {}".format(score))

    maxi = max(score)
    if (score.count(maxi) == 1):
        print("The winner is Player {}".format(score.index(max(score)) + 1))
    else:
        winners = []
        for i in range(len(score)):
            if (score[i] == maxi):
                winners.append(i + 1)
        print("The winners are players {}".format(winners))

#yarışma sırasında yarışmacıların verdikleri cevapların 0-1-2-3 ten biri olması durumunu kontrol eden fonksiyon
def is_number(s):
    try:
        res = int(eval(str(s)))
        if type(res) == int:
            return True
    except:
        return False




# bir tane soket oluşturulması ve bağlanması 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
#oluşturulan soketin her zaman bağlı kalması ve oradan ne veri gelirlse gelsin yakalanması 
s.setblocking(0)
print('Server başladı.')





# yarışmacıların sisteme girmesi için beklenmesi 
while (len(players) < max_players):
    ready = select.select([s], [], [], 1)
    if ready[0]:
        data, addr = s.recvfrom(1024)
        print("{} bağlantı isteği gönderdi ".format(data))
        if len(players) == 0:
            players.append([data, addr,0])
            s.sendto("Oyunun başlaması bekleniyor... ", players[0][1])
        else:
            for ijk in players:
                if addr not in ijk[1]:
                    players.append([data, addr,0])
                    print("{} oyuna bağlandı".format(ijk[0]))
                    s.sendto("Oyunun başlaması bekleniyor... ", ijk[1])
                    #for ii in players:
                    #    s.sendto("{} oyuna bağlandı.".format(ii[0]), ii[1])



# yarışma başladığı bilgisinin yarışmacılara gönderilmesi 
print("Oyun başlıyor")
for i in range(len(players)):
    try:
        s.sendto("Oyun başlıyor", players[i][1])
    except:
        pass

# yarışma döngüsü
for k in range(questions_count):
    print("Soru : {}".format(k+1))
    que_s = get_question(question2,k)
    score_s = get_question_score(question_score,k)
    opt_s = get_options(answer2,k)
    for ipl in range(len(players)):
        s.sendto(que_s, players[ipl][1])
        s.sendto(score_s, players[ipl][1])
        s.sendto(opt_s, players[ipl][1])
        agv = ''
        ready = select.select([s], [], [], 20)
        if ready[0]:
            agv, addr = s.recvfrom(1024)
            agiven = int(agv)
            if is_number(agiven) == True:
                pass
            else:
                agiven = 0
            print players[ipl][0]," "+answer2[k][agiven],"cevabı verdi"
            agiven_result = checkAnswer(answer2,agiven, k)
            if agiven_result == True:
                players[ipl][2] = players[ipl][2]+question_score[k]
                dcevap_text = u'Dogru cevap verdiniz.%s puaniniz oldu'%players[ipl][2]
                s.sendto(dcevap_text,players[ipl][1])
            else:
                ycevap_text = u'Yanlis cevap verdiniz %s puaniniz var'%players[ipl][2]
                s.sendto(ycevap_text,players[ipl][1])


# yarışmacılara yarışma bitti bilgisinin gönderilmesi 
for i in range(len(players)):
    try:
        s.sendto("Oyun bitti", players[i][1])
    except:
        pass

# skor hesaplaması ve yarışmacılara sonuçların gönderilmesi 
final_score(score)
# çok yakmasın diye soketin kapatılması :)
s.close()
