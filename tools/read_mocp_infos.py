import subprocess

#Read current file
mocp_file = subprocess.Popen(['mocp', '-i', '|', 'grep', 'File'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
stdout,stderr = mocp_file.communicate()
#Decode from binary string without prefix "File: "(6) and suffix "\n"
current_track = stdout[6:-1].decode('utf-8')

print( "Aktuell: " + current_track )
print( "Vergleich: " + title )


exit(-1)

#mocp_state = str( subprocess.call(['mocp', '-i', '|', 'grep', 'State'], shell=False) )
mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'State'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

stdout,stderr = mocp_state.communicate()

#print( stdout.split(':')[1] )
#print( mocp_state )

#print( stdout )

state_play = b'PLAY' in stdout
state_pause = b'PAUSE' in stdout
state_stop = b'STOP' in stdout

print( "Play: " + str(state_play) )
print( "Pause: " + str(state_pause) )
print( "Stop: " + str(state_stop) )
