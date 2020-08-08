import pyaudio
import struct
import pyautogui  # to press a button to play the game
import pvporcupine
import os
# below are the four wake word's path that I have generated 
key1 = r'Porcupine\resources\keyword_files\windows\snake_up_windows.ppn'
key2 = r'Porcupine\resources\keyword_files\windows\go_down_windows.ppn'
key3 = r'Porcupine\resources\keyword_files\windows\go_right_windows.ppn'
key4 = r'Porcupine\resources\keyword_files\windows\go_left_windows.ppn'
# this is the library path
library_path = os.getcwd()
library_path= library_path + '\Porcupine\lib\windows\\amd64\libpv_porcupine.dll'

# this is model file path can be find inside Porcupine -> lib -> common
model_file_path = r'Porcupine\lib\common\porcupine_params.pv'
keyword_file_paths = [key1, key2, key3, key4]
sensitivities = [1,0.5,0.5,0.5]
handle = pvporcupine.Porcupine(library_path, model_file_path, keyword_file_paths=keyword_file_paths, sensitivities=sensitivities)

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=handle.frame_length,input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm
 
#in this while if any of those world is going to be audible the code will press the right button 
while True:
    pcm = get_next_audio_frame()
    keyword_index = handle.process(pcm)
    if keyword_index==0:
        print("Up")
        pyautogui.press('up')
    if keyword_index==3:
        print("Left")
        pyautogui.press('left')
    if keyword_index==2:
        print("Right")
        pyautogui.press('right')
    if keyword_index==1:
        print("Down")
        pyautogui.press('down')