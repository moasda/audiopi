import subprocess

#mocp_state = str( subprocess.call(['mocp', '-i', '|', 'grep', 'State'], shell=False) )
mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

stdout,stderr = mocp_state.communicate()

print( stdout.split(':')[1] )
#print( mocp_state )

state_play = "PLAY" in stdout
state_pause = "PAUSE" in stdout
state_stop = "STOP" in stdout

print( "Play: " + state_play )
print( "Pause: " + state_pause )
print( "Stop: " + state_stop )
