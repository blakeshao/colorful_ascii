'use client';

import GalleryItem from './GalleryItem';
import { ASCIIConfig, RenderingMethod } from '../schema';

// Define the videos statically
const defaultConfig: ASCIIConfig = {
  font_size: 30,
  font_path: 'SF-Pro',
  background_color: [255, 255, 255],
  characters: [
    { char: '.', threshold: [0, 0.2], color: [0, 0, 0] },
    { char: ':', threshold: [0.2, 0.3], color: [0, 0, 0] },
    { char: '0', threshold: [0.3, 0.4], color: [0, 0, 0] },
    { char: '+', threshold: [0.4, 0.5], color: [0, 0, 0] },
    { char: '*', threshold: [0.5, 1.0], color: [0, 0, 0] },
  ],
  original_color: false,
  rendering_method: RenderingMethod.LUMINANCE
}

const galleryVideos = [
  {name: 'sample1.mp4',
  config: defaultConfig,
  },

  // Add all your video filenames here
];

export default function Gallery({ setAllConfig }: { setAllConfig: (config: ASCIIConfig) => void }) {
  // Use a default config for gallery items

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {galleryVideos.map((video) => (
        <GalleryItem
          key={video.name}
          videoName={video.name}
          onSelect={() => setAllConfig(video.config)}
        />
      ))}
    </div>
  );
}