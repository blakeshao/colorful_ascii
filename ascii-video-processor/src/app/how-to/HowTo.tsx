import React from 'react';

export const HowTo = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-md font-light">How to Use</h2>
      
      <div className="space-y-8">
        <section>
          <h3 className="text-md font-semibold mb-2">1. Upload a Video</h3>
          <p className="text-md">
            Click the file upload button to select a video file from your computer. 
            Supported formats include MP4, WebM, and MOV.
          </p>
        </section>

        <section>
          <h3 className="text-md font-semibold mb-2">2. Customize Settings</h3>
          <ul className="list-disc list-inside text-md space-y-2">
            <li>Choose a background color for your ASCII art</li>
            <li>Select a font and adjust its size</li>
            <li>Customize ASCII characters and their brightness thresholds</li>
            <li>Set colors for each ASCII character</li>
          </ul>
        </section>

        <section>
          <h3 className="text-md font-semibold mb-2">3. Process Video</h3>
          <p className="text-md">
            Click the &quot;Process Video&quot; button and wait for your ASCII art video to be generated. 
            Processing time depends on the video length and resolution.
          </p>
        </section>

        <section>
          <h3 className="text-md font-semibold mb-2">Tips</h3>
          <ul className="list-disc list-inside text-md space-y-2">
            <li>Shorter videos (under 30 seconds) process faster</li>
            <li>For best results, use videos with good contrast</li>
            <li>Experiment with different ASCII characters and thresholds</li>
            <li>Try both dark and light backgrounds</li>
          </ul>
        </section>
      </div>
    </div>
  );
};