from resemble_enhance.enhancer.inference import denoise, enhance
import torch
import torchaudio
import soundfile as sf
from tqdm import tqdm
from pathlib import Path

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


def denoise_and_enhance(path, solver, nfe, tau, denoising):
    """ return (sample rate, denoised
    """

    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(path)
    dwav = dwav.mean(dim=0)

    wav1, new_sr = denoise(dwav, sr, device)
    wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)

    wav1 = wav1.cpu().numpy()
    wav2 = wav2.cpu().numpy()

    return (new_sr, wav1), (new_sr, wav2)


data_dir = "../../ViTS TTS/data/wavs-old"
audios = list(Path(data_dir).rglob(f'*.wav'))
print(f"There are {len(audios)} raw audio files!")


for audio in audios:

    output = denoise_and_enhance(path  = audio,
                                 solver = "Midpoint",
                                 nfe    = 64,
                                 tau    = 0.7,
                                 denoising = True
                                 )
    
    file_name   = str(audio).split('/')[-1]
    audio_array = output[1][1]
    sample_rate = output[1][0]
    
    sf.write('wavs/'+file_name, 
             audio_array, 
             sample_rate, 
             format='wav')

audios = list(Path("wavs").rglob(f'*.wav'))

print(f"{len(audios)} audio files successfully cleaned")