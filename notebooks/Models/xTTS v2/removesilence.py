from pyAudioAnalysis  import (audioBasicIO      as aIO, 
                              audioSegmentation as aS)
from pydub            import AudioSegment, silence, effects
from pydub.silence    import split_on_silence
from scipy.io         import wavfile
from pesq             import pesq
from os               import listdir
from tqdm             import tqdm
from scipy.io.wavfile import read, write
from IPython.display  import Audio

import os, random, time, subprocess, pickle, wave, librosa
import matplotlib.pyplot as plt
import numpy  as np
import pandas as pd

def detect_silence(file_path, time=0.09):
    command = ['ffmpeg', '-i', file_path, '-af', f'silencedetect=n=-30dB:d={time}', '-f', 'null', '-']
    out     = subprocess.run(command, capture_output=True, text=True)
    s       = out.stderr if out.stderr else out.stdout
    k       = s.split('[silencedetect @')
    if len(k)==1:
        return None
        
    start,end=[],[]
    for i in range(1,len(k)):
        x=k[i].split(']')[1]
        if i%2==0:
            x=x.split('|')[0]
            x=x.split(':')[1].strip()
            end.append(float(x))
        else:
            x=x.split(':')[1]
            x=x.split('size')[0]
            x=x.replace('\r','')
            x=x.replace('\n','').strip()
            start.append(float(x))
    return list(zip(start,end))

def remove_silence(file_path, sil, out_path, keep_sil=0.09):
    '''
    This function removes silence from the audio.
    
    Input: 
    file_path = Input audio file path
    sil = List of silence time slots that needs to be removed
    keep_sil = Time to keep as allowed silence after removing silence
    out_path = Output path of audio file
    
    returns:
    Non - silent patches and save the new audio in out path
    '''
    rate,aud    = read(file_path)
    a           = float(keep_sil)/2
    sil_updated = [(i[0]+a,i[1]-a) for i in sil]
    
    # convert the silence patch to non-sil patches
    non_sil = []
    tmp     = 0
    ed      = len(aud)/rate
    for i in range(len(sil_updated)):
        non_sil.append((tmp,sil_updated[i][0]))
        tmp=sil_updated[i][1]
    if sil_updated[-1][1]+a/2<ed:
        non_sil.append((sil_updated[-1][1],ed))
    if non_sil[0][0]==non_sil[0][1]:
        del non_sil[0]
    
    # cut the audio
    print('slicing start')
    ans=[]
    ad=list(aud)
    for i in tqdm(non_sil):
        ans = ans+ad[int(i[0]*rate):int(i[1]*rate)]

    write(out_path,rate,np.array(ans))
    return non_sil