'use client';

import { ASCIIConfig } from '../schema';

interface GalleryProps {
  onConfigSelect?: (config: ASCIIConfig) => void;
}

export default function Gallery({ onConfigSelect }: GalleryProps) {
  // Create array of 9 placeholder items
  const placeholders = Array(9).fill(null);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {placeholders.map((_, i) => (
        <div 
          key={i}
          className="border border-foreground p-4 aspect-video bg-foreground/10"
        >
        </div>
      ))}
    </div>
  );
}
