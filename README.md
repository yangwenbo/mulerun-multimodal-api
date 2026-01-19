# Mule Multimodal Studio

A powerful Video/Image Generation Client with Gradio Web UI, supporting multiple AI models including Kling, Midjourney, Sora, Veo3, Wan2.5/2.6, and Nano Banana Pro.

## Features

- **Multi-Site Support**: MuleRun (api.mulerun.com) and MuleRouter (api.mulerouter.ai)
- **Multiple AI Models**: 18+ models for video and image generation
- **Image URL Input**: Support direct image URLs, including Google Drive sharing links (auto-converted to direct URLs)
- **Proxy Support**: Configure HTTP/HTTPS/SOCKS5 proxy for API requests
- **Debug Mode**: Preview API requests before sending
- **Task Management**: Track task history, poll status, view results
- **Local Media Caching**: Auto-download generated media to local storage
- **Background Polling**: Automatic status updates for pending tasks

## Prerequisites

- **Python 3.10+** (recommended 3.13)
- **pip** (Python package manager)

```bash
# Check Python version
python3 --version

# Check pip
pip --version
```

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

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `API_TOKEN` | MuleRun API token (get from https://mulerun.com) |
| `MULEROUTER_API_TOKEN` | MuleRouter API token (optional) |
| `API_PROXY` | Proxy URL, e.g., `http://127.0.0.1:7890` or `socks5://127.0.0.1:1080` |

> Note: All settings can also be configured directly in the Web UI.

## Web UI Access

Once started, open in your browser:

```
http://127.0.0.1:7860
```

---

## Supported Models

### Video Generation Models

| Model | Key | Type | Site |
|-------|-----|------|------|
| Kling Text-to-Video | `kling_text2video` | text2video | MuleRun |
| Kling Image-to-Video | `kling_image2video` | image2video | MuleRun |
| Midjourney Video Diffusion | `midjourney_video` | text2video | MuleRun, MuleRouter |
| OpenAI Sora | `sora` | text2video | MuleRun |
| Google Veo3 | `veo3` | text2video | MuleRun |
| Wan2.5 Text-to-Video | `wan2_5_t2v_preview` | text2video | MuleRun |
| Wan2.5 Image-to-Video | `wan2_5_i2v_preview` | image2video | MuleRun |
| Wan2.6 Text-to-Video | `wan2_6_t2v` | text2video | MuleRouter |
| Wan2.6 Spark Text-to-Video | `wan2_6_t2v_spark` | text2video | MuleRouter |
| Wan2.6 Image-to-Video | `wan2_6_i2v` | image2video | MuleRouter |
| Wan2.6 Spark Image-to-Video | `wan2_6_i2v_spark` | image2video | MuleRouter |

### Image Generation Models

| Model | Key | Type | Site |
|-------|-----|------|------|
| Midjourney Image Generation | `midjourney_diffusion` | text2image | MuleRun, MuleRouter |
| Nano Banana Pro Generation | `nano_banana_pro_generation` | text2image | MuleRun, MuleRouter |
| Nano Banana Pro Edit | `nano_banana_pro_edit` | image2image | MuleRun, MuleRouter |
| Wan2.5 Image Generation | `wan2_5_t2i_preview` | text2image | MuleRun |
| Wan2.5 Image Edit | `wan2_5_i2i_preview` | image2image | MuleRun |
| Wan2.6 Image Generation | `wan2_6_t2i` | text2image | MuleRouter |
| Wan2.6 Image Edit | `wan2_6_i2i` | image2image | MuleRouter |

---

## AI Agent Operation Guide

This section provides step-by-step instructions for AI Agents (with vision capability) to operate this application.

### UI Layout Overview

The Web UI consists of two main sections:

```
+----------------------------------+----------------------------------------+
|         LEFT PANEL               |            RIGHT PANEL                 |
|  (Control & Parameters)          |        (Task History & Results)        |
+----------------------------------+----------------------------------------+
| - API Site selector              | - Task History table                   |
| - API Token input                |   (ID, UUID, Status, Model, etc.)      |
| - Proxy input (optional)         | - Stats badges (Pending/Processing/    |
| - Debug Mode checkbox            |   Completed/Failed counts)             |
| - Task Type radio                | - Task control row:                    |
|   (Video/Image Generation)       |   [Task ID] [Task UUID] [Poll]         |
| - Model dropdown                 |   [Detail] [Delete]                    |
| - Parameters section             | - Task Detail accordion:               |
|   (dynamic based on model)       |   - Task info (model, status, params)  |
| - Submit/Confirm/Cancel buttons  |   - Image gallery (for image results)  |
| - Result text box                |   - Video preview (for video results)  |
| - Debug preview (JSON)           |   - Result URLs                        |
+----------------------------------+----------------------------------------+
```

### Step-by-Step Operation Flow

#### Step 1: Configure API Settings

1. **Select API Site**: Click the "API Site" dropdown
   - Choose "MuleRun (api.mulerun.com)" for Kling, Sora, Veo3, Wan2.5 models
   - Choose "MuleRouter (api.mulerouter.ai)" for Wan2.6 models
   - Note: Midjourney and Nano Banana Pro are available on both sites

2. **Enter API Token**: Type your API token in the "API Token" text field
   - The token is required for all API requests

3. **Configure Proxy (Optional)**: If needed, enter proxy URL in "Proxy" field
   - Format: `http://127.0.0.1:7890` or `socks5://127.0.0.1:1080`
   - Leave empty if no proxy is needed

#### Step 2: Select Task Type and Model

1. **Select Task Type**: Click the radio button
   - "Video Generation" - for text2video and image2video models
   - "Image Generation" - for text2image and image2image models

2. **Select Model**: Click the "Select Model" dropdown
   - The available models are filtered based on the selected site and task type
   - After selection, the parameters section will update to show relevant options

#### Step 3: Fill in Parameters

Parameters vary by model. Common parameters include:

| Parameter | Description | Models |
|-----------|-------------|--------|
| **Prompt** | Text description of what to generate | All models |
| **Negative Prompt** | What to avoid in generation | Some models |
| **Input Image** | Upload image file OR enter URL | image2video, image2image |
| **Image URL** | Direct URL or Google Drive sharing link | image2video, image2image |
| **Model Version** | Specific model variant | Kling, Wan2.5 |
| **Mode** | Generation mode (std/pro) | Kling |
| **Aspect Ratio** | Output aspect ratio (16:9, 9:16, 1:1, etc.) | Video models |
| **Duration** | Video length (5s, 10s) | Video models |
| **Resolution** | Output resolution (480P, 720P, 1080P) | Some video models |
| **Size** | Image size | Image models |
| **CFG Scale** | Creativity vs prompt adherence | Some models |

**Image Input Options**:
- **File Upload**: Click the image upload area to select a local file
- **URL Input**: Enter image URL in the text field below the upload area
  - Supports direct image URLs (https://example.com/image.jpg)
  - Supports Google Drive sharing links (auto-converted to direct URLs)
  - URL input takes priority over file upload

#### Step 4: Submit Task

1. **Debug Mode (Recommended for first use)**:
   - Enable "Debug Mode" checkbox
   - Click "Submit Task" button
   - Review the JSON preview showing the exact API request
   - Click "Confirm Send" to submit, or "Cancel" to abort

2. **Normal Mode**:
   - Disable "Debug Mode" checkbox
   - Click "Submit Task" button
   - Task is submitted immediately

3. **Check Result**: The "Result" text field shows:
   - Success: "Task submitted successfully! ID: X, API Task: UUID"
   - Error: Error message with details

#### Step 5: Monitor Task Progress

1. **View Task History**: The right panel shows all tasks for the current site
   - Status indicators: Pending, Processing, Completed, Failed
   - Click "Refresh" button to update the list

2. **Poll Task Status**: To manually check a specific task:
   - Enter Task ID (number) or Task UUID in the input fields
   - Click "Poll" button
   - The task status will be updated

3. **Background Polling**: The application automatically polls pending tasks every 30 seconds

#### Step 6: View Results

1. **Select Task**: Enter the Task ID or Task UUID in the control row

2. **Click "Detail" button**: The Task Detail section expands showing:
   - Task metadata (model, status, created time, parameters)
   - For **image results**: Images displayed in the gallery
   - For **video results**: Video player with preview
   - Result URLs: Direct links to download media

3. **Download Results**:
   - Media files are auto-downloaded to `media/{task_id}/` folder
   - Or use the URLs displayed in "Result URLs" field

### Example Workflows

#### Example 1: Generate Video from Text (Kling)

```
1. Site: MuleRun
2. Task Type: Video Generation
3. Model: Kling Text-to-Video
4. Parameters:
   - Prompt: "A cat playing with a ball in a sunny garden"
   - Mode: std
   - Aspect Ratio: 16:9
   - Duration: 5
5. Click "Submit Task"
6. Wait for completion (poll or auto-refresh)
7. Click "Detail" to view video
```

#### Example 2: Generate Image from Text (Midjourney)

```
1. Site: MuleRun
2. Task Type: Image Generation
3. Model: Midjourney 图片生成
4. Parameters:
   - Prompt: "A futuristic cityscape at sunset, cyberpunk style"
   - Aspect Ratio: 16:9
5. Click "Submit Task"
6. Wait for completion
7. Click "Detail" to view images in gallery
```

#### Example 3: Image-to-Video with Google Drive Image (Wan2.6)

```
1. Site: MuleRouter
2. Task Type: Video Generation
3. Model: Wan2.6 图生视频
4. Parameters:
   - Image URL: https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing
     (Auto-converted to direct URL)
   - Prompt: "Make the character walk forward"
   - Duration: 5
   - Resolution: 720P
5. Click "Submit Task"
6. Wait for completion
7. Click "Detail" to view generated video
```

#### Example 4: Edit Image (Nano Banana Pro)

```
1. Site: MuleRouter
2. Task Type: Image Generation
3. Model: Nano Banana Pro 图片编辑
4. Parameters:
   - Image: Upload or enter URL
   - Prompt: "Remove the background and add a beach scene"
5. Click "Submit Task"
6. Wait for completion
7. Click "Detail" to view edited image
```

### Task Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| Pending | Task submitted, waiting to start | Wait or poll |
| Processing | Task is being processed | Wait or poll |
| Completed | Task finished successfully | View results |
| Failed | Task failed | Check error message |

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Please enter API Token first" | Enter valid API token |
| "Model not available for site" | Switch to correct site for the model |
| "Image is required for this model" | Upload image or enter image URL |
| Task stuck in Processing | Use "Poll" button to refresh status |
| 404 or network errors | Check proxy settings, will auto-retry |

---

## Dependencies

- gradio >= 4.0.0
- requests >= 2.28.0

## License

MIT License
