
# Colorful ASCII Video Converter

A web application that transforms videos into customizable ASCII art animations. Built with Next.js for the frontend and FastAPI for the backend, this tool allows users to convert their videos into unique ASCII art representations with customizable colors, characters, and fonts.

## Features

- Video to ASCII art conversion with real-time preview
- Customizable ASCII characters and their brightness thresholds
- Adjustable font settings (size and type)
- Background color customization
- Support for multiple video formats (MP4, AVI, MOV, MKV, GIF)
- Gallery of example conversions with reusable configurations
- Two rendering methods: luminance-based and edge detection

## Tech Stack

### Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- OpenCV (cv2)
- Pillow
- NumPy
- Python 3.x

## Getting Started

### Prerequisites

- Node.js (Latest LTS version recommended)
- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/blakeshao/colorful_ascii.git
cd ascii-video-converter
```

2. Install frontend dependencies:

```bash
npm install
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

4. Run the application:

```bash
npm run dev
```

This will start both:
- Frontend server at http://localhost:3000
- Backend server at http://localhost:8000

## Usage

1. Upload a video (supported formats: MP4, AVI, MOV, MKV, GIF)
2. Customize your ASCII art settings:
   - Choose background color
   - Select font and size
   - Configure ASCII characters and their thresholds
   - Set colors for each ASCII character
3. Click "Process Video" and wait for the conversion
4. View and download your ASCII art video

## Environment Variables

Create a `.env` file in the root directory:

```bash
env
NEXT_PUBLIC_API_URL=http://localhost:8000
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- Video processing using [OpenCV](https://opencv.org/)