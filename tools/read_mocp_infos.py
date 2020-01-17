import subprocess

#mocp_state = str( subprocess.call(['mocp', '-i', '|', 'grep', 'State'], shell=False) )
mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

stdout,stderr = mocp_state.communicate()

#print( stdout.split(':')[1] )
#print( mocp_state )

#print( stdout )

state_play = b'PLAY' in stdout
state_pause = b'PAUSE' in stdout
state_stop = b'STOP' in stdout

if state_play == True:
    print( "Play: " + str(state_play) )

if state_pause == True:
    print( "Pause: " + str(state_pause) )

if state_stop == True:
    print( "Stop: " + str(state_stop) )
