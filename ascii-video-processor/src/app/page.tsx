'use client'

import { useState } from 'react'
import { ASCIIConfig, ASCIICharacter, RenderingMethod } from './schema'
import { FontSettings } from './components/FontSettings'
import { ASCIICharacterSettings } from './components/ASCIICharacterSettings'
import { BackgroundColorPicker } from './components/BackgroundColorPicker'
import Gallery from './components/Gallery'
import Link from 'next/link'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [processing, setProcessing] = useState(false)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [fontSize, setFontSize] = useState(15)
  const [fontPath, setFontPath] = useState('SF-Pro')
  const [backgroundColor, setBackgroundColor] = useState<[number, number, number]>([255, 255, 255])
  const [characters, setCharacters] = useState<ASCIICharacter[]>([
      { char: '.', threshold: [0, 0.2], color: [0, 0, 0] },
      { char: ':', threshold: [0.2, 0.3], color: [0, 0, 0] },
      { char: '0', threshold: [0.3, 0.4], color: [0, 0, 0] },
      { char: '+', threshold: [0.4, 0.5], color: [0, 0, 0] },
      { char: '*', threshold: [0.5, 1.0], color: [0, 0, 0] },
  ])
  const [originalColor, setOriginalColor] = useState(false)
  const [renderingMethod, setRenderingMethod] = useState<RenderingMethod>(RenderingMethod.LUMINANCE)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setProcessing(true)
    const formData = new FormData()
    formData.append('file', file)

    const chars: ASCIICharacter[] = characters

    const config: ASCIIConfig = {
      font_size: fontSize,
      font_path: fontPath,
      background_color: backgroundColor,
      characters: chars,
      original_color: originalColor,
      rendering_method: renderingMethod
    }

    formData.append('config', JSON.stringify(config))

    

    console.log('File:', file);
    console.log('Config:', config);
    console.log('FormData entries:');
    for (let pair of formData.entries()) {
      console.log(pair[0], pair[1]);
    }


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


  const handleCharacterUpdate = (index: number, field: keyof ASCIICharacter, value: any) => {
    const updatedChars = [...characters]
    if (field === 'threshold') {
      updatedChars[index].threshold = value.map(Number)
    } else if (field === 'color') {
      updatedChars[index].color = value.map(Number)
    } else {
      updatedChars[index] = { ...updatedChars[index], [field]: value }
    }
    setCharacters(updatedChars)
  }
 
  return (
    <main className="min-h-screen p-20 items-center">
     <div className="flex flex-col gap-8">
      <div>
        <div className="flex flex-row gap-2 items-baseline mb-2">
          <span className="text-md">colorful_ascii</span>
          <span className="text-xs">by Blake S.</span>
          
        </div>
        
        <div className="flex flex-col md:flex-row gap-8 h-full w-full justify-center">
          <div className="w-full md:w-3/4 flex flex-col items-center border border-1 aspect-video">
            {processing ? (
              <div className="w-full flex justify-center items-center h-full">
                <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
              </div>
            ) : videoUrl ? (
              <div className="w-full h-full flex justify-center items-center p-4">
                <video controls src={videoUrl} className="max-w-full max-h-full object-contain" />
              </div>
            ) : (
              <div className="w-full flex justify-center items-center h-full">
                <p>Upload a video to get started</p>
              </div>
            )}
          </div>

          <div className="w-full md:w-1/4">
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="mb-4">
                <Link href="/how-to" className="text-sm hover:opacity-80 underline">How to use</Link>
              </div>
              <div>
                <p className="text-sm">Upload a video</p>
                <input
                  type="file"
                  accept="video/*"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="border p-2"
                />
              </div>

              <BackgroundColorPicker
                backgroundColor={backgroundColor}
                onBackgroundColorChange={setBackgroundColor}
              />

              <FontSettings
                selectedFont={fontPath}
                fontSize={fontSize}
                onFontChange={setFontPath}
                onFontSizeChange={setFontSize}
              />

              <ASCIICharacterSettings
                asciiChars={characters}
                onCharacterUpdate={handleCharacterUpdate}
              />

              <button
                type="submit"
                disabled={!file || processing}
                className="border-2 border-foreground px-4 my-4 py-2 text-foreground disabled:opacity-50 disabled:border-opacity-50 disabled:text-opacity-50"
              >
                {processing ? 'Processing...' : 'Process Video'}
              </button>
            </form>
          </div>
        </div>
      </div>
      <div className="flex flex-col">
        <p className="text-md mb-2">Gallery</p>
        <Gallery />
      </div>
      </div>
    </main>
  )
}