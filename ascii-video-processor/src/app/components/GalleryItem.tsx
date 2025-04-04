'use client';


import { useEffect, useState } from 'react';

interface GalleryItemProps {
  videoName: string;
  onSelect?: () => void;
}

export default function GalleryItem({ videoName, onSelect }: GalleryItemProps) {
  const videoUrl =  `/gallery-videos/${videoName}`;
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return (
    <div 
      className="border border-foreground bg-background/10 cursor-pointer hover:bg-foreground/50 transition-colors aspect-square relative"
      onClick={() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        onSelect?.();
      }}
    >
      {isMounted && (
        <>
          <video
            src={videoUrl}
            className="w-full h-full object-cover"
            autoPlay
            muted
            loop
            playsInline
            controls
          />
          <div className="absolute inset-0 opacity-0 bg-foreground/50 hover:opacity-100 transition-opacity flex items-center justify-center">
            <p className="text-background font-medium">Click to apply config</p>
          </div>
        </>
      )}
    </div>
  );
}