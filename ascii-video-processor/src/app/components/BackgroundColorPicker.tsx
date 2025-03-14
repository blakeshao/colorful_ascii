'use client'

import React from 'react'
import { rgbToHex, hexToRgb } from '../util'

interface BackgroundColorPickerProps {
  backgroundColor: [number, number, number]
  onBackgroundColorChange: (color: [number, number, number]) => void
}

export function BackgroundColorPicker({
  backgroundColor,
  onBackgroundColorChange,
}: BackgroundColorPickerProps) {
  

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium">
        Background Color
      </label>
      <div className="flex items-center gap-4">
        <input
          type="color"
          value={rgbToHex(backgroundColor)}
          onChange={(e) => onBackgroundColorChange(hexToRgb(e.target.value))}
          className="h-10 w-20"
        />
        <span className="text-sm">
          RGB: ({backgroundColor.join(', ')})
        </span>
      </div>
    </div>
  )
}