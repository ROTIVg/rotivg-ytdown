import React, { useState } from 'react';
import { Download, Link, Loader } from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('mp4');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleDownload = async () => {
    if (!url.trim()) {
      setMessage('Por favor, insira um link válido do YouTube');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          format: format
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro no download');
      }

      // Get filename from response headers or create a default one
      const contentDisposition = response.headers.get('content-disposition');
      let filename = 'video.' + format;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Create blob and download
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);

      setMessage('Download iniciado com sucesso!');
    } catch (error) {
      setMessage('Erro: ' + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-sm border p-8 w-full max-w-md">
        <div className="text-center mb-6">
          <Download className="mx-auto h-12 w-12 text-blue-600 mb-3" />
          <h1 className="text-2xl font-semibold text-gray-900">YouTube Downloader</h1>
          <p className="text-gray-600 text-sm mt-1">Baixe vídeos do YouTube de forma simples</p>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
              <Link className="inline h-4 w-4 mr-1" />
              Link do YouTube
            </label>
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="format" className="block text-sm font-medium text-gray-700 mb-2">
              Formato
            </label>
            <select
              id="format"
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              disabled={loading}
            >
              <option value="mp4">MP4 (Vídeo)</option>
              <option value="webm">WebM (Vídeo)</option>
              <option value="mp3">MP3 (Áudio)</option>
            </select>
          </div>

          <button
            onClick={handleDownload}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center text-sm font-medium transition-colors"
          >
            {loading ? (
              <>
                <Loader className="animate-spin h-4 w-4 mr-2" />
                Baixando...
              </>
            ) : (
              <>
                <Download className="h-4 w-4 mr-2" />
                Baixar
              </>
            )}
          </button>

          {message && (
            <div className={`text-center text-sm ${message.startsWith('Erro') ? 'text-red-600' : 'text-green-600'}`}>
              {message}
            </div>
          )}
        </div>

        <div className="mt-6 text-xs text-gray-500 text-center">
          <p>Respeite os direitos autorais dos criadores de conteúdo</p>
        </div>
      </div>
    </div>
  );
}

export default App;