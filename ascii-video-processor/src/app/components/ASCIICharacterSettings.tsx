import React from 'react';
import { ASCIICharacter } from '../schema';
import { rgbToHex, hexToRgb } from '../util';
interface ASCIICharacterSettingsProps {
  asciiChars: ASCIICharacter[];
  onCharacterUpdate: (index: number, field: keyof ASCIICharacter, value: any) => void;
}


export function ASCIICharacterSettings({ asciiChars, onCharacterUpdate }: ASCIICharacterSettingsProps) {
  return (
    <div>
      <label className="block text-sm font-medium mb-2">ASCII Characters</label>
      <div className="space-y-2">
        {asciiChars.map((char, index) => (
          <div key={index} className="flex space-x-4 items-center">
            <input
              type="text"
              value={char.char}
              onChange={(e) => onCharacterUpdate(index, 'char', e.target.value)}
              className="border rounded p-2 w-12"
              maxLength={1}
            />
            <div>
              <label className="block text-xs">Threshold</label>
              <input
                type="text"
                value={`${char.threshold[0]}-${char.threshold[1]}`}
                onChange={(e) => {
                  const [min, max] = e.target.value.split('-').map(Number);
                  onCharacterUpdate(index, 'threshold', [min, max]);
                }}
                className="border rounded p-2 w-24"
                placeholder="0.0-1.0"
              />
            </div>
            <div>
              <label className="block text-xs">Color</label>
              <input
                type="color"
                value={rgbToHex(char.color)}
                onChange={(e) => {
                  const hex = e.target.value;
                  const rgb = hexToRgb(hex);
                  onCharacterUpdate(index, 'color', rgb);
                }}
                className="w-12 h-8 cursor-pointer"
                style={{ 
                  padding: 0,
                  border: '1px solid #ccc',
                  borderRadius: '4px'
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}