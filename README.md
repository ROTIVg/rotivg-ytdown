# YouTube Downloader

Aplicativo web minimalista para download de vídeos do YouTube.

## Funcionalidades

- ✅ Download de vídeos do YouTube
- ✅ Suporte para formatos MP4, WebM e MP3
- ✅ Interface minimalista e responsiva
- ✅ API RESTful com FastAPI
- ✅ Processamento assíncrono

## Estrutura do Projeto

```
├── src/                    # Frontend React
│   ├── App.tsx            # Componente principal
│   └── ...
├── backend/               # Backend Python
│   ├── main.py           # API FastAPI
│   ├── requirements.txt  # Dependências Python
│   └── start.py         # Script para iniciar o servidor
└── README.md            # Este arquivo
```

## Instalação e Configuração

### 1. Backend (Python/FastAPI)

```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python start.py
```

O servidor estará rodando em `http://localhost:8000`

### 2. Frontend (React)

```bash
# No diretório raiz do projeto
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## Como Usar

1. **Iniciar os servidores**: Certifique-se de que tanto o backend (porta 8000) quanto o frontend (porta 5173) estejam rodando
2. **Acessar a aplicação**: Abra `http://localhost:5173` no navegador
3. **Inserir URL**: Cole o link do vídeo do YouTube no campo de texto
4. **Selecionar formato**: Escolha entre MP4, WebM ou MP3
5. **Baixar**: Clique no botão "Baixar" e aguarde o processamento

## API Endpoints

### `GET /`
- **Descrição**: Status da API
- **Resposta**: `{"message": "YouTube Downloader API", "status": "running"}`

### `POST /download`
- **Descrição**: Baixar vídeo do YouTube
- **Body**:
  ```json
  {
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "mp4|webm|mp3"
  }
  ```
- **Resposta**: Stream do arquivo para download

## Tecnologias Utilizadas

- **Frontend**: React, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: Python, FastAPI, yt-dlp
- **Ferramentas**: Vite, ESLint

## Requisitos do Sistema

- Python 3.8+
- Node.js 16+
- FFmpeg (instalado automaticamente pelo yt-dlp)

## Notas Importantes

- ⚠️ **Direitos Autorais**: Respeite os direitos autorais dos criadores de conteúdo
- ⚠️ **Uso Local**: Esta aplicação é destinada para uso local e pessoal
- ⚠️ **Dependências**: O yt-dlp pode instalar FFmpeg automaticamente quando necessário

## Troubleshooting

### Erro de CORS
Certifique-se de que o backend está configurado para aceitar requisições do frontend (já configurado nas origens permitidas).

### Erro de Download
- Verifique se a URL do YouTube é válida
- Alguns vídeos podem ter restrições de download
- Vídeos muito longos podem demorar mais para processar

### FFmpeg não encontrado
O yt-dlp instalará automaticamente o FFmpeg, mas em alguns sistemas pode ser necessário instalar manualmente:
- Windows: Baixar de https://ffmpeg.org/
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`