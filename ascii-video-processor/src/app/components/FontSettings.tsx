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
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/fonts`)
      .then(res => res.json())
      .then(fonts => {
        setAvailableFonts(fonts);
        // If selectedFont is not in the available fonts, add it
        if (!fonts.some((font: Font) => font.name === selectedFont)) {
          setAvailableFonts([...fonts, { name: selectedFont, value: selectedFont }]);
        }
      })
      .catch(err => console.error('Error loading fonts:', err))
      .finally(() => setIsLoading(false));
  }, [selectedFont]); // Add selectedFont as a dependency

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Font</label>
        <select
          value={selectedFont}
          onChange={(e) => onFontChange(e.target.value)}
          className="border p-2 w-full max-w-xs"
          disabled={isLoading}
        >
          {isLoading && <option value={selectedFont}>{selectedFont}</option>}
          {availableFonts.map((font) => (
            <option key={font.name} value={font.name}>
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