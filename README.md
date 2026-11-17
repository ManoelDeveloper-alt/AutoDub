# AutoDub
## Dublagem automatica feita com python

### Versão beta 1.0 - dubloogle
- Usa a voz do google.
- No arquivo 'google_dublador.py', na pasta beta 1-0, modifique os valores de PATH_WORK, FILE_IN e FILE_OUT
- Execulte o arquivo e espere.

### Versão beta 1.0.1 - microdubbber
- Usa a voz da microsoft.
- Na pasta beta 1-0-1, abra 'edge-version', modifique o arquivo 'edge_dublador.py'
- Execulte e espere.

### versão beta 1.1 - microdubber local
- usa a voz da microsoft
- Na pasta beta 1-1 atere 'beta-1-1.py' e o execulte


#### Para instalar o ffmpeg faça:

- Linux: `sudo apt install ffmpeg` 
- Para windows vá ao [site](https://ffmpeg.org/download.html) e, após o download, adicione ele ao PATH
  - Para baixar, acesse o site e clique no simbolo do windows e selecione a opção com 'gyan.dev'
  - Vá na opção 'mirror @github' e baixe uma versão, essencial ou full, '.zip'
  - Após baixar extraia e coloque os arquivos em uma pasta como 'C:/ffmpeg/' atentando-se ao local onde a pasta 'bin' está
  - Em pesquisar digite Variaveis de ambientes e execulte 'editar as variaveis de ambientes do sistema'
  - Clique em 'Variaveis de ambientes' e em 'Variaveis do sistema' encontre e selecione a variavel path
  - Clique em editar depois em novo e adicione o caminho para a pasta bin do ffmpeg, ex: C:\ffmpeg\bin
  - Verifique a instalação digitando 'ffmpeg -version' no cmd do windows

#### Para o python:
- Instale o [python](https://www.python.org/downloads/) (foi usado a versao 3.12.7), no linux já há o python
##### blibliotecas gerais:
  - whisper: `pip install openai-whisper` (requer ffmpeg)
    - Para o whisper funcionar baixe o [Microsoft visual C++](https://aka.ms/vs/16/release/vc_redist.x64.exe)
    - Para agilizar o processo, entre no python, carregue a biblioteca whisper (import whisper) depois digite o comando `whisper.load_model("small")`, onde small é o tamanho do modelo que você pretende usar
    - Isso irá baixar o modelo
  - pydub: `pip install pydub`
##### Para beta 1.0:
- deep_translator: `pip install deep-translator`
- gtts: `pip install gtts`

##### Para beta 1.0.1:
- deep_translator: `pip install deep-translator`
- edge-tts: `pip install edge-tts`

##### Para beta 1.1:
- edge-tts: `pip install edge-tts`
- instale o Ollama usando:
    - Linux `curl -fsSL https://ollama.com/install.sh | sh` - no terminal
    - Windows `irm https://ollama.com/install.ps1 | iex` - no PowerShell
  - instale o modelo `ollama pull translategemma:4b`
- instale o request `pip install requests`