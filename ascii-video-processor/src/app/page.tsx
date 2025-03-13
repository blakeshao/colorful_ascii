'use client'

import { useState } from 'react'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [processing, setProcessing] = useState(false)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setProcessing(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/process-video', {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const blob = await response.blob();
      if (blob.size === 0) {
        throw new Error('Received empty video file');
      }
      
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);
    } catch (error) {
      console.error('Error processing video:', error);
      // You might want to show an error message to the user here
    } finally {
      setProcessing(false);
    }
  }

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">ASCII Video Processor</h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="file"
            accept="video/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="border p-2"
          />
        </div>
        
        <button
          type="submit"
          disabled={!file || processing}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
        >
          {processing ? 'Processing...' : 'Process Video'}
        </button>
      </form>

      {videoUrl && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">Processed Video:</h2>
          <video controls src={videoUrl} className="max-w-full" />
        </div>
      )}
    </main>
  )
}