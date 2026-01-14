# MuleRun Multimodal API Client

Video/Image Generation Client with Gradio UI, supporting multiple AI models including Kling, Midjourney Video, Sora, Veo3, and Nano Banana Pro.

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.10+** (recommended 3.13)
- **pip** (Python package manager, usually included with Python)

### Check Installation

```bash
# Check Python version
python3 --version

# Check pip
pip --version
```

## Environment Variables

### 1. Copy the example environment file

```bash
cp .env.example .env
```

### 2. Configure your API token

Edit the `.env` file and set your MuleRun API token:

```
API_TOKEN=your-actual-api-key
```

You can obtain your API token from [MuleRun](https://mulerun.com).

> Note: You can also enter the API token directly in the web UI when the application is running.

## Quick Start

### macOS / Linux

```bash
./start.sh
```

If you encounter permission issues:

```bash
chmod +x start.sh
./start.sh
```

### Windows

Double-click `start.bat` or run in Command Prompt:

```cmd
start.bat
```

### Manual Start

If you prefer to run manually:

```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

Once started, the application will automatically open in your browser at:

```
http://127.0.0.1:7860
```

### Features

1. **Select Model**: Choose from available models (Kling, Sora, Veo3, etc.)
2. **Enter Parameters**: Fill in prompt, select options based on the model
3. **Submit Task**: Click "Submit Task" to start generation
4. **Track Progress**: View task history and poll for status updates
5. **View Results**: Preview generated videos/images directly in the UI

### Debug Mode

Enable "Debug Mode" to preview the API request before sending. This helps verify parameters are correct.

## Supported Models

| Model | Type | Description |
|-------|------|-------------|
| Kling Text-to-Video | text2video | Generate video from text prompt |
| Kling Image-to-Video | image2video | Animate an image into video |
| Midjourney Video Diffusion | text2video | MJ-style video generation |
| OpenAI Sora | text2video | OpenAI's video generation model |
| Google Veo3 | text2video | Google's video generation model |
| Nano Banana Pro (Generation) | text2image | Image generation |
| Nano Banana Pro (Edit) | image2image | Image editing |

## Dependencies

- gradio >= 4.0.0
- requests >= 2.28.0

## Troubleshooting

### Port already in use

If port 7860 is already in use, you can modify `app.py` to use a different port.

### API Token not working

- Verify your token is correct in `.env`
- Check that there are no extra spaces or quotes
- Try entering the token directly in the UI

### Tasks stuck in "pending" or "processing"

Use the "Poll Task" button to manually check the task status.
