import os
import subprocess
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter # RAW waveform based separation
import speech_recognition as sr
# import ffmpeg
import wave
print('imports successful')

filename = 'twinkle_guitar'
separator = Separator('spleeter:4stems', multiprocess=False) # Separator instance
audio_loader = AudioAdapter.default()
print(audio_loader)
sample_rate = 44100 # if too slow try 22050
waveform, _ = audio_loader.load(f'{filename}.mp3', sample_rate = sample_rate, duration=95)
prediction = separator.separate_to_file(destination=f'./{filename}_vocals.wav', audio_descriptor=f'{filename}.mp3', audio_adapter=audio_loader)
# export voice to its own .wav file
# audio = {}
# print(type(prediction['vocals'].T)) # should be a numpy array

# get vocals w/ spleeter

os.replace(f'./{filename}_vocals.wav/{filename}/vocals.wav', f'Audio-to-midi-master/input/{filename}_vocals.wav')
print('moved input')

# stable version: numpy 1.16.5, scipy 1.4.1, tensorflow 2.3.0

# https://github.com/bill317996/Audio-to-midi
for x in os.walk('Audio-to-midi-master/input/'):
  print(x)
print('running model')
_output = subprocess.run(['py', 'Audio-to-midi-master/audio2midi.py', '-in', 'Audio-to-midi-master/input/', '-out', 'Audio-to-midi-master/output/'])
print('ran model')

os.replace(f'Audio-to-midi-master/output/{filename}_vocals.mid', f'./{filename}_vocals.mid')
print('moved output. can you see it?')

f = open(f'{filename}_lyrics.txt', 'w')
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
r = sr.Recognizer()
with sr.AudioFile(f'./Audio-to-midi-master/input/{filename}_vocals.wav') as source:
  # listen for data (load audio to memory)
  audio_data = r.record(source)
  # recognize (convert from speech/song to text)
  text = r.recognize_google(audio_data) # may only work for files less than ~110 seconds long, need to split otherwise
  f.write(text)
f.close()
print('printed lyrics to txt. can you see it?')