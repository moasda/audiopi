import subprocess

mocp_state = str( subprocess.call(['mocp', '-i', '|', 'grep', 'State'], shell=True) )

print( mocp_state )

state_play = "PLAY" in mocp_state
state_pause = "PAUSE" in mocp_state
state_stop = "STOP" in mocp_state

print( "Play: " + state_play )
print( "Pause: " + state_pause )
print( "Stop: " + state_stop )
