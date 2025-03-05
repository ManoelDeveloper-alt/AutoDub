1. Extrair audio "ffmpeg -i video.mp4 -ac 1 -ar 16000 audio.wav"
2. Modifique o nome da pasta em "config.py"
3. Executar "autoduble.py".
4. Execulte "ffmpeg -i video.mp4 -i dubbed_audio.wav -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4"
    Dentro da pasta onde está o video