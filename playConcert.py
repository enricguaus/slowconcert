import sys
import os
import time
import threading
from myTwitter import Tweet
from simpleOSC import *

TEST_MODE = 1
N_DAYS    = 0.00069444 *2  #* 60 * 24* 4.5

print "--> Opens a txt converted midi file using http://flashmusicgames.com/midi/mid2txt.php"
print "    and sends data to timer"

notes  = {
0:"C_-1",   1:"C#_-1", 2:"D_-1",  3:"D#_-1",  4:"E_-1",  5:"F_-1",  6:"F#_-1",  7:"G_-1",  8:"G#_-1",  9:"A_-1", 10:"A#_-1", 11:"B_-1",
12:"C_0",  13:"C#_0", 14:"D_0", 15:"D#_0", 16:"E_0", 17:"F_0", 18:"F#_0", 19:"G_0", 20:"G#_0", 21:"A_0", 22:"A#_0", 23:"B_0",
24:"C_1",  25:"C#_1", 26:"D_1", 27:"D#_1", 28:"E_1", 29:"F_1", 30:"F#_1", 31:"G_1", 32:"G#_1", 33:"A_1", 34:"A#_1", 35:"B_1",
36:"C_2",  37:"C#_2", 38:"D_2", 39:"D#_2", 40:"E_2", 41:"F_2", 42:"F#_2", 43:"G_2", 44:"G#_2", 45:"A_2", 46:"A#_2", 47:"B_2",
48:"C_3",  49:"C#_3", 50:"D_3", 51:"D#_3", 52:"E_3", 53:"F_3", 54:"F#_3", 55:"G_3", 56:"G#_3", 57:"A_3", 58:"A#_3", 59:"B_3",
60:"C_4",  61:"C#_4", 62:"D_4", 63:"D#_4", 64:"E_4", 65:"F_4", 66:"F#_4", 67:"G_4", 68:"G#_4", 69:"A_4", 70:"A#_4", 71:"B_4",
72:"C_5",  73:"C#_5", 74:"D_5", 75:"D#_5", 76:"E_5", 77:"F_5", 78:"F#_5", 79:"G_5", 80:"G#_5", 81:"A_5", 82:"A#_5", 83:"B_5",
84:"C_6",  85:"C#_6", 86:"D_6", 87:"D#_6", 88:"E_6", 89:"F_6", 90:"F#_6", 91:"G_6", 92:"G#_6", 93:"A_6", 94:"A#_6", 95:"B_6",
96:"C_7",  97:"C#_7", 98:"D_7", 99:"D#_7",100:"E_7",101:"F_7",102:"F#_7",103:"G_7",104:"G#_7",105:"A_7",106:"A#_7",107:"B_7",
108:"C_8",109:"C#_8",110:"D_8",111:"D#_8",112:"E_8",113:"F_8",114:"F#_8",115:"G_8",116:"G#_8",117:"A_8",118:"A#_8",119:"B_8",
120:"C_9",121:"C#_9",122:"D_9",123:"D#_9",124:"E_9",125:"F_9",126:"F#_9",127:"G_9"}

myTweet=Tweet()

# ---- READING COMMAND LINE ----
if len(sys.argv) < 2:
	print "Usage:   python playConcert.py path/to/input/file "
	print "Example: python playConcert.py 01_satie_gymnopedie1.txt"
	sys.exit(-1)

inFile  = sys.argv[1]

# ---- OSC ----
ip='127.0.0.1'
#ip='192.168.1.148'
port=57120
initOSCClient(ip, port)

# ---- PROCESS ----
# Read txt file
print "--> Reading input file: " + inFile
file = open(inFile, 'r')
score={}
for line in file:
    columns = line.split(" ")
    if len(columns) >= 2:
        if columns[1] == "On":
        	if columns[4] != "v=0\n":
        		if score.has_key(columns[0]):
					new_row=[]
					new_row=score.get(columns[0])
					#new_row.append(columns[3][2:])
					new_row.append(notes[int(columns[3][2:])])
					score[columns[0]]=new_row
	        	else:
	        		row=[]
	        		row.append(notes[int(columns[3][2:])])
	        		score[columns[0]]=row

# Sort score from multiple tracks
score2=[]
for line in score.keys():
	score2.append([int(line),str(", ".join(score.get(line)))])
score2=sorted(score2)

#compute times
max_score_time=score2[len(score2)-1][0]
n_seconds = N_DAYS * 24 * 60 * 60
print "--> Read time up to " + str(max_score_time) + " to be distributed into " + str(n_seconds) + " seconds."

for note in range(len(score2)):
	act_score_time = int(score2[note][0])
	act_message    = str(score2[note][1])
	if TEST_MODE == 1:
		# This is for Twitter
		t=threading.Timer(n_seconds*act_score_time/max_score_time,myTweet.post_fake,(act_message,)).start()
		# This is for OSC
		figures=score2[note][1].split(", ")
		small_delay=0
		for figure in reversed(figures):
			midi_note=int(notes.keys()[notes.values().index(figure)]) # back process from name to midi note
			t=threading.Timer(small_delay+(n_seconds*act_score_time/max_score_time),sendOSCMsg,('/note',[int(midi_note)],)).start()
			small_delay=small_delay+0.1
	else:
		#t=threading.Timer(n_seconds*act_score_time/max_score_time,myTweet.post,(act_message,)).start()
		t=threading.Timer(n_seconds*act_score_time/max_score_time,myTweet.post_fake,(act_message,)).start()
	

