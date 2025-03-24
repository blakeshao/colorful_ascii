'use client';

import GalleryItem from './GalleryItem';
import { ASCIIConfig, RenderingMethod, ASCIICharacter } from '../schema';
import path from 'path';

const baseFontPath = path.join(process.cwd(), 'backend', 'fonts');
// Define the videos statically
const defaultConfig: ASCIIConfig = {
  font_size: 30,
  font_path: path.join(baseFontPath, 'SF-Pro.ttf'),
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
  {   
    name: 'boxing.mp4',
    config: {
      font_size: 30,
      font_path: path.join('KulimPark-ExtraLight'),
      background_color: [255, 255, 255] as [number, number, number],
      characters: [
        { char: '.', threshold: [0, 0.2], color: [92, 92, 92] },
        { char: ':', threshold: [0.2, 0.3], color: [92, 92, 92] },
        { char: '0', threshold: [0.3, 0.4], color: [92, 92, 92] },
        { char: '+', threshold: [0.4, 0.5], color: [92, 92, 92] },
        { char: '*', threshold: [0.5, 1.0], color: [92, 92, 92] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
  },

  {   
    name: 'gd.mp4',
    config: {
      font_size: 8,
      font_path: path.join('OCR-a'),
      background_color: [0, 0, 0] as [number, number, number],
      characters: [
        { char: 'X', threshold: [0, 0.05], color: [20, 122, 255] },
        { char: '<', threshold: [0.05, 0.25], color: [0, 255, 157] },
        { char: '?', threshold: [0.25, 0.45], color: [0, 245, 4] },
        { char: '}', threshold: [0.45, 0.65], color: [251, 255, 0] },
        { char: 'K', threshold: [0.65, 1.0], color: [255, 96, 10] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
  },

  {   
    name: 'iguana.mp4',
    config: {
      font_size: 45,
      font_path: path.join('NotoSerifSC'),
      background_color: [255, 238, 209] as [number, number, number],
      characters: [
        { char: '你', threshold: [0, 0.15], color: [6, 91, 31] },
        { char: '好', threshold: [0.15, 0.4], color: [27, 161, 68] },
        { char: '川', threshold: [0.4, 0.6], color: [58, 203, 101] },
        { char: '一', threshold: [0.6, 0.8], color: [86, 255, 128] },
        { char: '，', threshold: [0.8, 1.0], color: [133, 255, 169] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
  },

  {   
    name: 'rippling.mp4',
    config: {
      font_size: 45,
      font_path: path.join('KaiseiHarunoUmi-Regular'),
      background_color: [0, 64, 255] as [number, number, number],
      characters: [
        { char: 'ジ', threshold: [0, 0.05], color: [255, 102, 0] },
        { char: 'ケ', threshold: [0.05, 0.15], color: [255, 102, 0]},
        { char: 'ノ', threshold: [0.15, 0.25], color: [255, 133, 52]},
        { char: 'ム', threshold: [0.25, 0.35], color: [255, 133, 52]},
        { char: 'オ', threshold: [0.35, 0.4], color: [255, 163, 87]},
        { char: 'ヨ', threshold: [0.4, 0.45], color: [255, 163, 87]},
        { char: 'ビ', threshold: [0.45, 0.5], color: [247, 180,135 ] },
        { char: 'イ', threshold: [0.5, 0.55], color: [247, 180,135 ]  },
        { char: 'ガ', threshold: [0.55, 0.7], color: [255, 255, 255] },
        { char: 'バ', threshold: [0.7, 1.0], color: [255, 255, 255] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
  },

  {   
    name: 'flowers.mp4',
    config: {
      font_size: 30,
      font_path: path.join('GowunBatang-Regular'),
      background_color: [255, 255, 255] as [number, number, number],
      characters: [
        { char: '있', threshold: [0, 0.3], color: [40, 60, 130] },
        { char: '이', threshold: [0.3, 0.4], color: [40, 60, 130] },
        { char: '없', threshold: [0.4, 0.5], color: [40, 60, 130] },
        { char: ']', threshold: [0.5, 0.6], color: [40, 60, 130] },
        { char: '，', threshold: [0.6, 1.0], color: [40, 60, 130] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
  },

  {   
    name: 'jetset.mp4',
    config: {
      font_size: 10,
      font_path: path.join('KaiseiHarunoUmi-Regular'),
      background_color: [0, 133, 88] as [number, number, number],
      characters: [
        { char: 'ジ', threshold: [0, 0.05], color: [255, 255, 255] },
        { char: 'ケ', threshold: [0.05, 0.15], color: [255, 255, 255]},
        { char: 'W', threshold: [0.15, 0.25], color: [255, 255, 255]},
        { char: 'ム', threshold: [0.25, 0.35], color: [255, 255, 255]},
        { char: 'Z', threshold: [0.35, 0.4], color: [255, 255, 255]},
        { char: 'I', threshold: [0.4, 0.45], color: [255, 255, 255]},
        { char: ')', threshold: [0.45, 0.5], color: [255, 255, 255 ] },
        { char: '{', threshold: [0.5, 0.55], color: [255, 255, 255 ]  },
        { char: ';', threshold: [0.55, 0.7], color: [255, 255, 255] },
        { char: ',', threshold: [0.7, 1.0], color: [255, 255, 255] },
      ] as ASCIICharacter[],
      original_color: false,
      rendering_method: RenderingMethod.LUMINANCE

    }
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
          onSelect={() => {
            setAllConfig(video.config);
            console.log(video.config);
          }}
        />
      ))}
    </div>
  );
}