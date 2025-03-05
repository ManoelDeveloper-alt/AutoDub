# Autor: Manoel Messias / Chat GPT
# Data: Janeiro/Fevereiro de 2025
# Descrição: Esse código permite dublar um video de ingles para portugues usando a voz do google
# Para funcionar instale:
#     - ffmpeg: sudo apt install ffmpeg  # Linux
#          - Para windows vá ao site https://ffmpeg.org/download.html e, após o download, adicione ele ao PATH
#     - whisper: pip install openai-whisper (requer ffmpeg)
#     - gtts: pip install gtts
#     - deep_translator: pip install deepl
import warnings
import whisper
import time
import os
import subprocess
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment

PATH_WORK = 'miraculous/' # pasta na qual estará os arquivos
FILE_IN   = 'video.mp4' # video em ingles
FILE_OUT  = 'output.mp4' # nome dado ao video dublado
VOLUME_BACK_SOUND = -60 # até -120db
WHISPER_MODEL = 'small' # tamanho do modelo de ia do whisper

START_TIME_OPERATION = time.time() # marcação para indicar  aduração da operação

def execultar(cmd): # função que execulta um comando de terminal (o comando deve ser uma string)
    vetor = cmd.split()
    subprocess.run(vetor, check=True, capture_output=True)

def dividir_atempo(valor):
         # função que cria um vetor de mudança de velocidade para atigir mudanças menores que 0.5
        sequencia = []
        while valor < 0.5:
            sequencia.append(0.5)
            valor /= 0.5
        sequencia.append(valor)
        return sequencia
# ===============================================================================
# ============================= EXTRAIR AUDIO ===================================
# ===============================================================================
def verify_files():
    if not os.path.exists(PATH_WORK+FILE_IN):
        print("O video não foi encotrado!")
        exit()
    files_vefify = [FILE_OUT, "audio.wav", "audio_temp_tts.mp3", "audio_temp_ajust.mp3", "dub_audio.wav"]
    for f in files_vefify:
        if os.path.exists(PATH_WORK+f):
            os.remove(PATH_WORK+f)
            print(f"Arquivo {f} excluido!")

# ===============================================================================
# ============================= EXTRAIR AUDIO ===================================
# ===============================================================================
def extrair_audio():
    try:
        execultar(f"ffmpeg -i {PATH_WORK+FILE_IN} -ac 1 -ar 16300 {PATH_WORK}audio.wav") # extrai o audio
        # ao ser extraido o arquivo temporario é criado 'audio.wav'
        print("--Audio extraido com sucesso!")
    except:
        # caso haja algum erro
        print("--Erro ao extrair o audio!")
        exit()

# ===============================================================================
# ============================= TRASCREVENDO ====================================
# ===============================================================================
def speak_to_text():
    print("--Carregando modelo...")
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead") # oculta mensagem de aviso
    model = whisper.load_model(WHISPER_MODEL)  # Carrega o modelo

    print("--Transcrevendo audio...")
    result = model.transcribe(PATH_WORK+"audio.wav", language="en",  word_timestamps=True, verbose=True) # transcreve o audio

    print("--Listando Falas...")
    english_falas = []
    for i, segment in enumerate(result["segments"]): # para cada fala achada roda uma vez
        print("----Fala ", i+1, " de ", len(result["segments"])+1)
        start = segment["start"] # tempo de inicio da fala (segundos)
        end = segment["end"] # tempo final da fala (segundos)
        text = segment["text"] # valor da fala
        english_falas.append((start, end, text))
    return english_falas

# ===============================================================================
# =============================== TRADUÇÃO ======================================
# ===============================================================================
def translate(english_falas):
    portuguese_falas = []
    for i,f in enumerate(english_falas):
        print(f"--Traduzindo: {i+1}/{len(english_falas)+1}")
        text = f[2] # pega a fala
        try:
            # tenta traduzir
            text = GoogleTranslator(source="en", target="pt").translate(text)
            portuguese_falas.append((f[0],f[1],text)) # adiciona no vetor
        except:
            print(f"**Erro ao traduzir '{text}'.")
    return portuguese_falas

# ===============================================================================
# ============================ TEXT TO SPEAK ====================================
# ===============================================================================
def text_to_speak(falas):    
    temp_audio_tts_path = PATH_WORK+"audio_temp_tts.mp3" # saida do audio gerado pelo tts
    temp_audio_ajust_path = PATH_WORK+"audio_temp_ajust.mp3" # saida do audio após ajuste de velocidade

    audio_dublado = AudioSegment.silent(duration=0) # cria um audio que será o audio dublado
    audio_original = AudioSegment.from_file(PATH_WORK+"audio.wav") # pega o audio audio_original

    for i,fala in enumerate(falas): # uma vez para cada fala
        print(f"--Fala {i+1} de {len(falas)+1}")
        # pega os dados da fala
        start = fala[0]*1000 # transforma em milessimos de segundos
        end = fala[1]*1000 # transforma em milessimos de segundos
        text = fala[2]
        # Gerar áudio da fala usando gTTS
        tts = gTTS(text, lang="pt")
        tts.save(temp_audio_tts_path) # arquivo temporario para trabalhar com o audio
        print(f"----Audio {i+1}/{len(falas)+1} criado!")

        tts_audio = AudioSegment.from_mp3(temp_audio_tts_path) # carrega o arquivo
        duration_tts = len(tts_audio)  # Pega a duração real em milissegundos

        # adiciona antes da fala o audio original, se necessário (caso haja efeitos sonoros)
        if len(audio_dublado) < (start): # se o tamanho atual do audio for menor que o inicio da fala
            part_audio = audio_original[len(audio_dublado):(start)] # pega o trecho correspondente
            audio_dublado += part_audio  # completa o trecho com o audio original
        
        # ajusta velocidade do audio para encaixar na duração da fala original
        duration_fala = end-start
        fator_velocidade = duration_tts/duration_fala # quantos tts cabem na fala?
        # por exemplo se tts for o dobro da fala, fator será 2 e tts deverá acelerar 2 vezes
        # reduzindo o seu tempo pela metade e ele terá o mesmo tamanho que fala

        # alterar a velocidade
        # o menor fator possivel é 0.5
        # se o fator for menor que isso, será feita uma sucessão de alteração na velocidade até atigir o mesmo efeito
        vetor_fator = dividir_atempo(fator_velocidade) # retorna uma sucessão de numeros ou apenas o valor passado (caso ele seja maior que 0.5)
        conjunto_fator = f"atempo={vetor_fator[0]}"
        for i in range(1, len(vetor_fator)): # caso haja mais elemento
            conjunto_fator= f"{conjunto_fator},atempo={vetor_fator[i]:2f}" # cria uma lista

        print(f"----Alterando velocidade {fator_velocidade:.2f}x")
        execultar(f"ffmpeg -i {temp_audio_tts_path} -filter:a {conjunto_fator} -vn {temp_audio_ajust_path}")

        ajust_audio = AudioSegment.from_file(temp_audio_ajust_path) # pega o audio ajustado
        start_audio_ajust = len(audio_dublado) # pega a posição onde o audio ajustado vai ser inserido
        audio_dublado += ajust_audio # adiona o audio em seu devido lugar
        # pega o som ao qual o audio ajustado está sobreescrevendo
        back_sound = audio_original[start_audio_ajust:len(ajust_audio)]
        back_sound = back_sound.apply_gain(VOLUME_BACK_SOUND) # audio baixo
        audio_dublado = audio_dublado.overlay(back_sound, position=start_audio_ajust) # sobrepõe o audio que já tinha com o audio dublado

        # Remover o arquivo temporário
        os.remove(temp_audio_tts_path)
        os.remove(temp_audio_ajust_path)

        print("----Fala adicionada")
    # após a ultima fala, preenche o audio dublado com o final do audio original
    part_audio = audio_original[len(audio_dublado):]
    audio_dublado += part_audio

    os.remove(PATH_WORK+"audio.wav") # remove o arquivo do audio original

    print("--Audio dublado!")
    audio_dublado.export(PATH_WORK+"dub_audio.wav", format="wav") 
    return PATH_WORK+"dub_audio.wav"

# ===============================================================================
# ============================ AUDIO E VIDEO ====================================
# ===============================================================================
def dublar_video(src):
    execultar(f"ffmpeg -i {PATH_WORK+FILE_IN} -i {src} -c:v copy -map 0:v:0 -map 1:a:0 -shortest {PATH_WORK+FILE_OUT}")
    os.remove(src)

# ===============================================================================
# ================================= CODIGO ======================================
# ===============================================================================
print("Preparando...")
verify_files()

print("Extraindo audio...")
extrair_audio()

print("Iniciando transcrição...")
falas_ingles = speak_to_text()

print("Traduzindo...")
falas_portugues = translate(falas_ingles)

print("Dublando...")
audio_output = text_to_speak(falas_portugues)

print("Filalizando...")
dublar_video(audio_output)

print(f"Finalizado em {((time.time())-START_TIME_OPERATION):.2f} segundos")