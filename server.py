# -*- coding: utf-8 -*-
import numpy as np
#from numpy.random import shuffle
#from random import randint
import socket
#import time
import select
import urllib, json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

questions_count=3
#question_done = [0] * (len(question2))
score = [0]
host = '127.0.0.1'
port = 5000
players = []
question2=[]
answer2 = []
right_answers2 = []
question_score = []
secs = 10
max_players = 1

url = "http://pendik.net/iya/api/app/soru_istek/"+str(questions_count)
response = urllib.urlopen(url)
data = json.loads(response.read())
#print json.dumps(data, sort_keys=True, indent=4)

#print data[0]['soru_text']

for i in data:
    #print i['soru_text'],"\n\n"
    question2.append(i['soru_text'])
    answer2.append(i['soru_secenek'])
    right_answers2.append(i['soru_dogru_cevap'])
    question_score.append(i['soru_puan'])

#print question2
#print answer2





# SHOW THE POSSIBLE ANSWERS
def displayA(question, answer, i):
    a = answer[i]
    order = np.arange(4)
    #shuffle(order)  # create list from 1 to 4 in different order --> to print the answers in random order
    a_display = [[a[order[0]], a[order[1]]], [a[order[2]], a[order[3]]]]
    print(a_display)


def get_question (question2,k):
    print question2[k]
    return question2[k].encode('utf-8')

# CHECK IF GOOD ANSWER OR NOT
def checkAnswer(answer2,agiven, qnb):
    test = False
    if agiven == right_answers2[qnb]:
        test = True
        score[0] = score[0]+1
        return test
    else:
        return test
def get_options(answer2,k):
    ret = ''
    say =0
    for i in answer2[k]:
        ret = ret+'['+str(say)+']'+i+'\n'
        say=say+1
    print ret
    return ret.encode('utf-8')

# END OF GAME, DISPLAY OF SCORES
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


# START THE NETWORK CODE
# host = '192.168.26.86'


# creation of socket object UDP and bind
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
# socket non blocking --> will always try to grab datas from the stream
# not block it
s.setblocking(0)

print('Server başladı.')





# WAIT FOR PLAYERS TO JOIN
while (len(players) < max_players):
    ready = select.select([s], [], [], 1)
    if ready[0]:
        data, addr = s.recvfrom(1024)
        print("{} bağlantı isteği gönderdi ".format(data))
        if len(players) == 0:
            players.append([data, addr])
            s.sendto("Oyunun başlaması bekleniyor... ", players[0][1])
        else:
            for ijk in players:
                if addr not in ijk[1]:
                    players.append([data, addr])
                    print("{} oyuna bağlandı".format(ijk[0]))
                    s.sendto("Oyunun başlaması bekleniyor... ", ijk[1])
                    #for ii in players:
                    #    s.sendto("{} oyuna bağlandı.".format(ii[0]), ii[1])

print players

# START GAME
print("Oyun başlıyor")
for i in range(len(players)):
    try:
        s.sendto("Oyun başlıyor", players[i][1])
    except:
        pass


for k in range(questions_count):
    print("Soru : {}".format(k+1))
    que_s = get_question(question2,k)
    opt_s = get_options(answer2,k)
    for ipl in range(len(players)):
        #try:
        s.sendto(que_s, players[ipl][1])
        s.sendto(opt_s, players[ipl][1])
        agiven = ""
        ready = select.select([s], [], [], 20)
        if ready[0]:
            agiven, addr = s.recvfrom(1024)
        print("{}".format(agiven))
        agiven_result = checkAnswer(answer2,agiven, k)
        if agiven_result == True:
            dcevap_text = 'Doğru cevap verdiniz'
            s.sendto(dcevap_text,players[ipl][1])
        else:
            ycevap_text = 'Yanlış cevap verdiniz'
            s.sendto(ycevap_text,players[ipl][1])

        #except:
            #pass


'''
nb = 3
for k in range(nb):
    print("Soru "+str(k+1))
    que_s = get_question(question2,k)
    opt_s = get_options(answer2,k)
    #print("ENTER FOR")
    for i in range(len(players)):
        s.sendto(que_s, players[i][1])
        s.sendto(opt_s, players[i][1])
        agiven = ""
        ready = select.select([s], [], [], 10)
        if ready[0]:
            agiven, addr = s.recvfrom(1024)
            print("agiven is : {}".format(agiven))
            checkAnswer(answer2,agiven,k)
'''

for i in range(len(players)):
    try:
        s.sendto("Oyun bitti", players[i])
    except:
        pass

final_score(score)
s.close()