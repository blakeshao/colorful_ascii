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
            <div className="flex flex-col gap-1">
              {index === 0 && <label className="block text-xs">Char</label>}
              <input
                type="text"
                value={char.char}
                onChange={(e) => onCharacterUpdate(index, 'char', e.target.value)}
                className="border p-2 w-12"
                maxLength={1}
              />
            </div>
            <div className="space-y-1">
              {index === 0 && <label className="block text-xs">Threshold Range</label>}
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  value={char.threshold[0]}
                  onChange={(e) => {
                    const min = Math.max(0, Math.min(1, Number(e.target.value)));
                    onCharacterUpdate(index, 'threshold', [min, char.threshold[1]]);
                    // Update previous character's upper threshold
                    if (index > 0) {
                      onCharacterUpdate(index - 1, 'threshold', [asciiChars[index - 1].threshold[0], min]);
                    }
                    
                  }}
                  className="border p-2 w-20"
                  step="0.05"
                  min={index === 0 ? 0 : asciiChars[index - 1].threshold[0]}
                  max={index === 0 ? 0 : index === asciiChars.length - 1 ? 1 : asciiChars[index + 1].threshold[0]}
                  placeholder="0.0"
                />
                <span className="text-xs">to</span>
                <input
                  type="number"
                  value={char.threshold[1]}
                  onChange={(e) => {
                    const max = Math.max(0, Math.min(1, Number(e.target.value)));
                    onCharacterUpdate(index, 'threshold', [char.threshold[0], max]);
                    // Update next character's lower threshold
                    if (index < asciiChars.length - 1) {
                      onCharacterUpdate(index + 1, 'threshold', [max, asciiChars[index + 1].threshold[1]]);
                    }
                  }}
                  className="border p-2 w-20"
                  step="0.05"
                  min={index === asciiChars.length - 1 ? 1 : asciiChars[index].threshold[0]}
                  max={index === asciiChars.length - 1 ? 1 : asciiChars[index + 1].threshold[1]}
                  placeholder="1.0"
                />
              </div>
            </div>
            <div>
              {index === 0 && <label className="block text-xs">Color</label>}
              <input
                type="color"
                value={rgbToHex(char.color)}
                onChange={(e) => {
                  const hex = e.target.value;
                  const rgb = hexToRgb(hex);
                  onCharacterUpdate(index, 'color', rgb);
                }}
                className="w-12 p-2 cursor-pointer"
                style={{ 
                  padding: 0,
                  height: '42px' // Matches the height of text inputs with border and padding
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}