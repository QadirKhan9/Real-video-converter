import { useState } from 'react';

const API_URL = 'https://qadirk-real-video-converter.hf.space';

export default function App() {
  const [mode, setMode] = useState('mp4-to-mkv');
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('Choose an MP4 file to convert to MKV.');
  const [isLoading, setIsLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [downloadName, setDownloadName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setIsLoading(true);
    setStatus('Uploading and converting...');
    setDownloadUrl('');
    setDownloadName('');

    const formData = new FormData();
    formData.append('file', file);

    const endpoint = mode === 'mp4-to-mkv' ? '/convert' : '/convert-mkv-to-mp4';
    const targetLabel = mode === 'mp4-to-mkv' ? 'MKV' : 'MP4';

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Conversion failed');
      }

      const blob = await response.blob();
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `converted.${targetLabel.toLowerCase()}`;
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="?([^";]+)"?/);
        if (match) filename = match[1];
      }

      const fileUrl = window.URL.createObjectURL(blob);
      setStatus(`Done! Your file is ready as ${targetLabel}.`);
      setDownloadUrl(fileUrl);
      setDownloadName(filename);
    } catch (err) {
      setStatus('Conversion failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!downloadUrl) return;

    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = downloadName || 'converted.file';
    document.body.appendChild(link);
    link.click();
    link.remove();
    setStatus('Download complete.');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-4">
      <div className="w-full max-w-2xl rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-black/40">
        <div className="mb-8">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Video Converter</p>
          <h1 className="mt-3 text-4xl font-semibold">Convert media formats in seconds</h1>
          <p className="mt-3 text-slate-400">Upload your video, let FFmpeg do the work, and download the converted file.</p>
        </div>

        <div className="mb-6 flex rounded-xl border border-slate-800 bg-slate-950/70 p-1">
          {[
            { id: 'mp4-to-mkv', label: 'MP4 → MKV' },
            { id: 'mkv-to-mp4', label: 'MKV → MP4' },
          ].map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => {
                setMode(tab.id);
                setFile(null);
                setDownloadUrl('');
                setDownloadName('');
                setStatus(tab.id === 'mp4-to-mkv' ? 'Choose an MP4 file to convert to MKV.' : 'Choose an MKV file to convert to MP4.');
              }}
              className={`flex-1 rounded-lg px-4 py-2 text-sm font-semibold transition ${mode === tab.id ? 'bg-cyan-500 text-slate-950' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-800/70 px-6 py-12 text-center transition hover:border-cyan-400 hover:bg-slate-800">
            <input
              type="file"
              accept={mode === 'mp4-to-mkv' ? 'video/mp4' : 'video/x-matroska,video/mkv'}
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <div className="rounded-full bg-cyan-500/10 p-4 text-cyan-400">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M7 16v1a2 2 0 002 2h6a2 2 0 002-2v-1M12 12V4m0 0l-3 3m3-3l3 3" />
              </svg>
            </div>
            <p className="mt-4 text-lg font-medium">{file ? file.name : mode === 'mp4-to-mkv' ? 'Drop your MP4 here' : 'Drop your MKV here'}</p>
            <p className="mt-1 text-sm text-slate-400">or click to browse</p>
          </label>

          <button
            type="submit"
            disabled={!file || isLoading}
            className="w-full rounded-xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? 'Converting...' : mode === 'mp4-to-mkv' ? 'Convert to MKV' : 'Convert to MP4'}
          </button>
        </form>

        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm text-slate-300">
          <p className="font-medium">Status</p>
          <p className="mt-1 text-slate-400">{status}</p>
          {downloadUrl && (
            <button
              type="button"
              onClick={handleDownload}
              className="mt-4 inline-flex items-center justify-center rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-300"
            >
              Download converted file
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
