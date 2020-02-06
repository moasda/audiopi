#!/usr/bin/python3

import logging
import subprocess
import time
import glob

first_song = ""
last_song = ""

#function for starting mocp server
def start_server():
    logging.info("Start mocp server")
    subprocess.call(['mocp', '-S'], shell=False)


#function for button "play/pause"
def toggle_play_pause():
    logging.info("TOGGLE Play/Pause")
    subprocess.call(['mocp', '-G'], shell=False)


#function for stopping player
def stop():
    logging.info("STOP Player")
    subprocess.call(['mocp', '-s'], shell=False)


#function for button "next song"
def next_song():
    logging.info("NEXT Song")
    subprocess.call(['mocp', '-f'], shell=False)
    ## TODO jump to first track


#function for button "previous song"
def previous_song():
    logging.info("PREVIOUS Song")
    subprocess.call(['mocp', '-r'], shell=False)
    ## TODO jump ot last track

#function for button "volume up"
def volume_up():
    logging.info("VOLUME UP")
    subprocess.call(['mocp', '-v', '+5'], shell=False)


#function for button "volume down"
def volume_down():
    logging.info("VOLUME DOWN")
    subprocess.call(['mocp', '-v', '-5'], shell=False)


#function for playing sounds
def play_folder(music_path):
    logging.info("Play: " + music_path)

    #get first and last track    
    search_for = music_path + "/*.mp3"
    play_list = glob.glob(search_for)
    if len(play_list) > 0:
        first_song = play_list[0]
        last_song = play_list[len(play_list)-1]
    
    logging.info( "First: " + first_song[len(music_path)+1:] )
    logging.info( "Last: " + last_song[len(music_path)+1:] )

    #Clear current playlsit
    subprocess.call(['mocp', '-c'], shell=False)
    #Create new playlist
    subprocess.call(['mocp', '-a', music_path], shell=False)
    #Start playing
    subprocess.call(['mocp', '-p'], shell=False)


#function for playing a system sound
def play_system_sound(title):
    subprocess.call(['mocp', '-P'], shell=False)
    time.sleep(0.5)
    subprocess.call(['mpg321', title], shell=False)
    time.sleep(0.1)
    subprocess.call(['mocp', '-U'], shell=False)


def check_mocp_playing():
    #Read status
    mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mocp_state.communicate()

    #check status
    state_play = b'PLAY' in stdout

    if state_play == True:
        return True
    else:
        return False


def check_mocp_plause():
    #Read status
    mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mocp_state.communicate()

    #check status
    state_play = b'PAUSE' in stdout

    if state_play == True:
        return True
    else:
        return False


def check_mocp_stop():
    #Read status
    mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = mocp_state.communicate()

    #check status
    state_play = b'STOP' in stdout

    if state_play == True:
        return True
    else:
        return False
