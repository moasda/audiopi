#!/usr/bin/python3

import logging
import subprocess
import time
import glob

FIRST_SONG = ""
LAST_SONG = ""
OUTPUT = "/home/pi/.moc/config"
SERVER_RUNNING = False

#function for starting mocp server
def start_server(toggleOutput=False):
    global OUTPUT
    global SERVER_RUNNING
    speaker = '/home/pi/.moc/config'
    headphones = '/home/pi/.moc/config_headphone'
    if toggleOutput == True:
        if OUTPUT == headphones:
            OUTPUT = speaker
        else:
            OUTPUT = headphones
    if SERVER_RUNNING == True:
        stop_server()
    logging.info("Start mocp server")
    subprocess.call(['mocp', '-S', '-C', OUTPUT], shell=False)
    SERVER_RUNNING = True


#function for stopping mocp server
def stop_server():
    global SERVER_RUNNING
    SERVER_RUNNING = False
    logging.info("Stop mocp server")
    subprocess.call(['mocp', '-x'], shell=False)


#function for toggling "repeat" (title)
def repeat(activate):
    logging.info("Repeat set to: "+ activate)
    #Parameter: -u=off, -o=on
    #Options: n=autonext, r=repeat, s=shuffle
    if activate == True:
        #autonext=off, repeat=on : mocp -u n -o r 
        subprocess.call(['mocp', '-u', 'n', '-o', 'r'], shell=False)
    else:
        #autonext=on, repeat=off : mocp -u n -o r 
        subprocess.call(['mocp', '-u', 'r', '-o', 'n'], shell=False)


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
    if check_is_streaming() == False:
        if check_is_current_title(LAST_SONG) == True:
            #last track is currently playing -> jump to first track
            restart_playlist()
        else:
            subprocess.call(['mocp', '-f'], shell=False)


#function for button "previous song"
def previous_song():
    logging.info("PREVIOUS Song")
    if check_is_streaming() == False:
        if check_is_current_title(FIRST_SONG) == False:
            subprocess.call(['mocp', '-r'], shell=False)


#function for button "volume up"
def volume_up():
    logging.info("VOLUME UP")
    subprocess.call(['mocp', '-v', '+5'], shell=False)


#function for button "volume down"
def volume_down():
    logging.info("VOLUME DOWN")
    subprocess.call(['mocp', '-v', '-5'], shell=False)


#function for restarting playlist (from beginning)
def restart_playlist():
    logging.info("Restart playlist")
    subprocess.call(['mocp', '-p'], shell=False)


#function for playing sounds
def play_folder(music_path):
    global FIRST_SONG
    global LAST_SONG
    logging.info("Play: " + music_path)

    #get first and last track    
    search_for = music_path + "/*.mp3"
    play_list = glob.glob(search_for)
    play_list.sort()
    if len(play_list) > 0:
        FIRST_SONG = play_list[0]
        LAST_SONG = play_list[len(play_list)-1]
    
    logging.info("First: " + FIRST_SONG[len(music_path)+1:])
    logging.info("Last: " + LAST_SONG[len(music_path)+1:])

    #Clear current playlsit
    subprocess.call(['mocp', '-c'], shell=False)
    #Create new playlist
    subprocess.call(['mocp', '-a', music_path], shell=False)
    #Start playing
    subprocess.call(['mocp', '-p'], shell=False)


#function for playing a URL (for example a radio stream)
def play_url(url):
    FIRST_SONG = ""
    LAST_SONG = ""
    logging.info("Streaming URL: " + url)
    subprocess.call(['mocp', '-c'], shell=False)
    subprocess.call(['mocp', '-a', url], shell=False)
    #Start playing
    subprocess.call(['mocp', '-p'], shell=False)


#function for playing a system sound
def play_system_sound(title):
    subprocess.call(['mocp', '-P'], shell=False)
    time.sleep(0.3)
    #play sound with 30% loudness (g) and no output (q)
    logging.info('mpg321 -q '+ title +' -g 30')
    subprocess.call(['mpg321', '-q', title, '-g', '30'], shell=False)
    time.sleep(0.1)
    subprocess.call(['mocp', '-U'], shell=False)


def check_mocp_playing():
    state = get_mocp_info('State')
    if state == 'PLAY':
        return True
    else:
        return False


def check_mocp_plause():
    state = get_mocp_info('State')
    if state == 'PAUSE':
        return True
    else:
        return False


def check_mocp_stop():
    state = get_mocp_info('State')
    if state == 'STOP':
        return True
    else:
        return False


def check_is_current_title(title):
    current_track = get_mocp_info('File')
    if current_track == title:
        return True
    else:
        return False


def check_is_streaming():
    current_track = get_mocp_info('File')
    if current_track.startswith("http"):
        return True
    else:
        return False


def get_mocp_info(option):
    mocp_info = subprocess.Popen(['mocp', '-i'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    search_for_info = option + ':'
    info = False
    for line in mocp_info.stdout:
        line = line.decode('utf-8')
        if line.startswith(search_for_info) == True:
            #Prefix equals to option - for example "File: "(6) and suffix "\n"
            info = line[len(search_for_info)+1:-1]
            break
    return info
