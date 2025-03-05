import whisper
import time
import os
import subprocess
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from config import PASTA

def dividir_atempo(valor):
        sequencia = []
        while valor < 0.5:
            sequencia.append(0.5)
            valor /= 0.5
        sequencia.append(valor)
        return sequencia

start_time_inicio = time.time()

#extrai o audio
video_input = PASTA+"video.mp4"
print("extarindo audio...")
cmd = [
    "ffmpeg", "-i", video_input, "-ac", "1",
    "-ar", "16300", PASTA+"audio.wav"
]

subprocess.run(cmd)

print("Audio extraido - V")
print("carregando modelo...")
model = whisper.load_model("small")  # Escolha o modelo adequado
print("Transcrevendo audio...")
result = model.transcribe(PASTA+"audio.wav", language="en",  word_timestamps=True)
falas = []

# Salvar como SRT
#with open(PASTA+"transcription.srt", "w", encoding="utf-8") as f:
for i, segment in enumerate(result["segments"]):
    print("Gerando falas: ", i, "/", len(result["segments"]))
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    # Traduzir para português
    try:
       text = GoogleTranslator(source="en", target="pt").translate(text)
    except:
       pass
    falas.append((start, text, end))
    #f.write(f"{i+1}\n{start:.2f} --> {end:.2f}\n{traducao}\n\n")

print("Transormando texto em voz...")
# Criar áudio final
final_audio = AudioSegment.silent(duration=0)
audio_original = AudioSegment.from_file(PASTA+"audio.wav")

index = 0
for sub in falas:
    start_time = sub[0]  
    text = sub[1]
    end_time = sub[2]

    # Gerar áudio da fala
    tts = gTTS(text, lang="pt")
    temp_audio_path = "temp_n.mp3"
    tts.save(temp_audio_path)

    speech_audio = AudioSegment.from_mp3(temp_audio_path)
    duration = len(speech_audio)  # Duração em milissegundos

    # Adicionar (silêncio) audio original se necessário para manter a sincronização
    if len(final_audio) < (start_time*1000):
        part_audio = audio_original[len(final_audio):(start_time*1000)]
        # silence_gap = AudioSegment.silent(duration=((start_time*1000) - len(final_audio)))
        final_audio += part_audio

    print("Audio criado: ", index, "/", len(falas))

    # Ajustar velocidade para encaixar no tempo
    time_fala = (end_time-start_time)*1000
    fator = time_fala/duration
    print(f"[{start_time:.2f}s - {end_time:.2f}s => {(duration/1000):.2f}] {text}")
    # alterar a velocidade
    tempo = ""
    vrg = 0

    for i in dividir_atempo(1/fator):
        if vrg>0:
            tempo= tempo+","
        tempo = tempo+f"rubberband=tempo={i:.2f}"
        vrg+=1
    cmd = [
        "ffmpeg", "-i", "temp_n.mp3", "-filter:a", tempo,
        "-vn", "temp.mp3"
    ]
    subprocess.run(cmd, check=True)
    # speech_audio = speedup(speech_audio, playback_speed=fator)
    # speech_audio = speech_audio.set_frame_rate(int(speech_audio.frame_rate * (duration/(len(speech_audio)+((start_time*1000) - len(final_audio))))))
    speech_audio = AudioSegment.from_mp3("temp.mp3")

    # Adicionar a fala no tempo correto
    inicio = len(final_audio)
    final_audio += speech_audio
    soud_fundo = audio_original[inicio:len(final_audio)]
    soud_fundo = soud_fundo.apply_gain(-60) # audio baixo
    final_audio = final_audio.overlay(soud_fundo, position=inicio)
    # após a ultima fala
    if index==len(falas)-1:
        part_audio = audio_original[len(final_audio):]
        final_audio += part_audio
    # Remover o arquivo temporário
    os.remove(temp_audio_path)
    os.remove("temp.mp3")

    print("fala adicionada: ", index, "/", len(falas))
    index += 1

# Salvar o áudio final
final_audio.export(PASTA+"dubbed_audio.wav", format="wav")
print("Voz gerada - V")
# gera o video final
audio_input = PASTA+"dubbed_audio.wav"
output_video = PASTA+"output.mp4"
print("Adicionando audio no video...")
cmd = [
    "ffmpeg", "-i", video_input, "-i", audio_input,
    "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest",
    output_video
]

subprocess.run(cmd)

print("Audio adicionado ao video...")
print("Removendo arquivos temporarios...")
#remove os audio temporario
os.remove(PASTA+"dubbed_audio.wav")
os.remove(PASTA+"audio.wav")
print("finalizado.")
print(time.time()-start_time_inicio)