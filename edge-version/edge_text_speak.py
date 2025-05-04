import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def remover_silencio_final(caminho_entrada, caminho_saida=None, limiar_db=-50, min_duracao_ms=300):
    audio = AudioSegment.from_file(caminho_entrada, format="mp3")
    
    # Detecta partes não silenciosas
    partes_nonsilenciosas = detect_nonsilent(audio, min_silence_len=min_duracao_ms, silence_thresh=limiar_db)

    if not partes_nonsilenciosas:
        print("⚠️ Áudio todo é considerado silêncio!")
        return

    inicio, fim = partes_nonsilenciosas[0][0], partes_nonsilenciosas[-1][1]
    audio_recortado = audio[inicio:fim]

    # Exporta
    if not caminho_saida:
        caminho_saida = caminho_entrada  # sobrescreve o original

    audio_recortado.export(caminho_saida, format="mp3")
    print(f"🧹 Silêncio final removido: novo tamanho = {len(audio_recortado)} ms")

# masculina "pt-BR-AntonioNeural"/ feminina "pt-BR-FranciscaNeural"
async def gerar_audio(texto, nome_arquivo, voz="pt-BR-FranciscaNeural"):
    communicate = edge_tts.Communicate(texto, voice=voz)
    await communicate.save(nome_arquivo)

# Rodar o código assíncrono
texto = "Olá, tudo bem? Essa é uma voz feminina do Microsoft Edge."
arquivo_saida = "fala.mp3"
voz_desejada = "pt-BR-FranciscaNeural"  # voz masculina. Feminina: "pt-BR-FranciscaNeural"

asyncio.run(gerar_audio(texto, arquivo_saida, voz_desejada))
remover_silencio_final(arquivo_saida, "sem_fim.mp3")