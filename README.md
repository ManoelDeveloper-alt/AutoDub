# AutoDub
## Dublagem automatica feita com python

### Versão beta 1.0 - Dublagem do google
- No arquivo 'google_dublador.py' modifique os valores de PATH_WORK, FILE_IN e FILE_OUT
- Execulte o arquivo e espere.

#### Para funcionar instale:

- ffmpeg: sudo apt install ffmpeg  # Linux
  - Para windows vá ao [site](https://ffmpeg.org/download.html) e, após o download, adicione ele ao PATH
  - Para baixar, acesse o site e clique no simbolo do windows e selecione a opção com 'gyan.dev'
  - Vá na opção 'mirror @github' e baixe uma versão, essencial ou full, '.zip'
  - Após baixar extraia e coloque os arquivos em uma pasta como 'C:/ffmpeg/' atentando-se ao local onde a pasta 'bin' está
  - Em pesquisar digite Variaveis de ambientes e execulte 'editar as variaveis de ambientes do sistema'
  - Clique em 'Variaveis de ambientes' e em 'Variaveis do sistema' encontre e selecione a variavel path
  - Clique em editar depois em novo e adicione o caminho para a pasta bin do ffmpeg, ex: C:\ffmpeg\bin
  - Verifique a instalação digitando 'ffmpeg -version' no cmd do windows

- Instale o [python](https://www.python.org/downloads/) (foi usado a versao 3.12.7), no linux já há o python
  - whisper: pip install openai-whisper (requer ffmpeg)
    - Para o whisper funcionar baixe o Microsoft visual C++ (https://aka.ms/vs/16/release/vc_redist.x64.exe)
    - Para agilizar o processo, entre no python, carregue a biblioteca whisper (import whisper) depois digite o comando 'whisper.load_model("small")', onde small é o tamanho do modelo que você pretende usar
    - Isso irá baixar o modelo
  - gtts: pip install gtts
  - deep_translator: pip install deepl
