'''
This file should:
- have a function for tracking when your mic is muted on zoom
- have a function for tracking when your speaking into your system mic (for now just make sure it works for your computer mic)
- print when your mic is muted on Zoom and you are speaking for more than 2 seconds

- file should wait until the conditions (mic is closed and user has talked for 2 seconds) to send message to console
- should then run again after user remutes mic
'''

import sounddevice as sd # cross platform mic capture
#import webrtcvad #library for turning short audio frames into speech:true/false

'''
function to be called continuously with new audio frames everytime the input stream has a new block of audio
args: indata = Numpy array with audio samples
frames = number of samples delivered in this block
time = small object with timing info
status = tells if audio system had a hiccup
'''
def callback(indata, frames, time, status):
    if status:
        print("Status: ", status)
    print("Got", frames, "samples")

#16kHz mono, 20mss blocks
samplerate = 8000#how many samples per second to record, each sample is one number representing sound pressure at that instant
frame_ms = 1000#how long each block of audio should be in milliseconds
blocksize = int(samplerate * frame_ms / 1000)  #hnumber of samples per block

'''
creating an audiostream that will continously read input audio until stopped
args: samplerate
'''
with sd.InputStream(samplerate=samplerate,
                    channels=1,
                    dtype='int16',
                    blocksize=blocksize,
                    callback=callback):
    print("Recording... press Ctrl+C to stop")
    sd.sleep(10000)  # run 10 seconds, then exit