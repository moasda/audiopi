import subprocess

#Read current file
mocp_info = subprocess.Popen(['mocp', '-i'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

for line in mocp_info.stdout:
  line = line.decode('utf-8')
  if line.startswith('File') == True:
    print( line )
    break
#line = mocp_file.stdout.readline()


#print( str(test) )
#print( '\n\n' )

stdpit.stderr = mocp_info.communicate()

#Decode from binary string without prefix "File: "(6) and suffix "\n"
current_track = stdout[6:-1].decode('utf-8')

print( "Aktuell: " + str(current_track) )
#print( "Vergleich: " + title )


print("###############################")
#exit(-1)

#mocp_state = str( subprocess.call(['mocp', '-i', '|', 'grep', 'State'], shell=False) )
mocp_state = subprocess.Popen(['mocp', '-i', '|', 'grep', 'File'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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
