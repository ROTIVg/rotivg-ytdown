from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import yt_dlp
import os
import tempfile
import re
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="YouTube Downloader API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    format: str

executor = ThreadPoolExecutor(max_workers=2)

def is_valid_youtube_url(url: str) -> bool:
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(youtube_regex.match(url))

def download_video(url: str, format_type: str, temp_dir: str) -> tuple[str, str]:
    """Download video using yt-dlp"""
    
    # Configure yt-dlp options based on format
    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_type == 'mp4':
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        }
    elif format_type == 'webm':
        ydl_opts = {
            'format': 'best[ext=webm]/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        }
    else:
        raise ValueError(f"Formato não suportado: {format_type}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            
            # Clean title for filename
            clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
            
            # Download the video
            ydl.download([url])
            
            # Find the downloaded file
            for file in os.listdir(temp_dir):
                if file.endswith(('.' + format_type, '.mp4', '.webm')):
                    return os.path.join(temp_dir, file), f"{clean_title}.{format_type}"
            
            raise FileNotFoundError("Downloaded file not found")
            
    except Exception as e:
        raise Exception(f"Erro no download: {str(e)}")

async def async_download(url: str, format_type: str, temp_dir: str) -> tuple[str, str]:
    """Async wrapper for download_video"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, download_video, url, format_type, temp_dir)

@app.get("/")
async def root():
    return {"message": "YouTube Downloader API", "status": "running"}

@app.post("/download")
async def download_youtube_video(request: DownloadRequest):
    """Download YouTube video endpoint"""
    
    # Validate URL
    if not is_valid_youtube_url(request.url):
        raise HTTPException(status_code=400, detail="URL do YouTube inválida")
    
    # Validate format
    if request.format not in ['mp4', 'webm', 'mp3']:
        raise HTTPException(status_code=400, detail="Formato não suportado")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download video
        file_path, filename = await async_download(request.url, request.format, temp_dir)
        
        # Stream file response
        def iterfile():
            try:
                with open(file_path, mode="rb") as file_like:
                    yield from file_like
            finally:
                # Cleanup temp directory
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Determine media type
        media_type = {
            'mp4': 'video/mp4',
            'webm': 'video/webm',
            'mp3': 'audio/mpeg'
        }.get(request.format, 'application/octet-stream')
        
        return StreamingResponse(
            iterfile(),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\""
            }
        )
        
    except Exception as e:
        # Cleanup on error
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)