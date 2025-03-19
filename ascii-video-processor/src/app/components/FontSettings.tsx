import React, { useEffect, useState } from 'react';

interface Font {
  name: string;
  value: string;
}

interface FontSettingsProps {
  selectedFont: string;
  fontSize: number;
  onFontChange: (font: string) => void;
  onFontSizeChange: (size: number) => void;
}

export function FontSettings({ selectedFont, fontSize, onFontChange, onFontSizeChange }: FontSettingsProps) {
  const [availableFonts, setAvailableFonts] = useState<Font[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/fonts')
      .then(res => res.json())
      .then(fonts => setAvailableFonts(fonts))
      .catch(err => console.error('Error loading fonts:', err));
    console.log('Available fonts:', availableFonts);
  }, []);


  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Font</label>
        <select
          value={selectedFont}
          onChange={(e) => onFontChange(e.target.value)}
          className="border p-2 w-full max-w-xs"
        >
          {availableFonts.map((font) => (
            <option key={font.value} value={font.value}>
              {font.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Font Size</label>
        <input
          type="number"
          value={fontSize}
          onChange={(e) => onFontSizeChange(Number(e.target.value))}
          min="8"
          max="200"
          className="border p-2 w-full max-w-xs"
        />
      </div>
    </div>
  );
}