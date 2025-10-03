# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Maya-LLM (麻鸭语音助手) is a multimodal voice assistant combining:
- **ASR**: SenseVoice for speech recognition
- **LLM**: Qwen2.5-1.5B for conversational AI
- **TTS**: CosyVoice/edge-tts/pyttsx3 for speech synthesis
- **Speaker Verification**: CAM++ for voiceprint authentication
- **Multimodal**: Qwen2-VL for vision + audio interaction

## Project Structure

This codebase has been refactored from monolithic scripts into a modular architecture:

```
maya-llm/
├── src/
│   ├── backend/           # Backend logic
│   │   ├── config.py      # Configuration (paths, model IDs, defaults)
│   │   ├── models.py      # Model loading/management (ASR, LLM, SV)
│   │   ├── inference.py   # Core inference engine
│   │   ├── audio_utils.py # Audio processing utilities
│   │   └── memory.py      # Chat history management
│   └── frontend/          # Frontend UI
│       ├── ui.py          # Gradio interface
│       └── styles.py      # CSS styling
├── cosyvoice/             # CosyVoice TTS library (from FunAudioLLM)
├── third_party/           # Third-party dependencies (Matcha-TTS)
├── runtime/               # Production deployment
│   └── python/
│       ├── fastapi/       # FastAPI server for CosyVoice
│       └── grpc/          # gRPC server for CosyVoice
├── app.py                 # Main entry point (modern UI)
├── maya_webui.py          # Legacy WebUI (v1.0)
├── maya_webui_modern.py   # Modern WebUI (v2.0, monolithic)
└── tests/                 # Test scripts
```

## Development Setup

### Environment

Create conda environment:
```bash
conda create -n chatAudio python=3.10
conda activate chatAudio
```

Install PyTorch with CUDA 11.8:
```bash
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118
```

### Dependencies

**Minimal setup (without CosyVoice)**:
```bash
pip install edge-tts==6.1.17 funasr==1.1.12 ffmpeg==1.4 opencv-python==4.10.0.84 \
    transformers==4.45.2 webrtcvad==2.0.10 qwen-vl-utils==0.0.8 \
    pygame==2.6.1 langid==1.1.6 langdetect==1.0.9 accelerate==0.33.0 PyAudio==0.2.14
```

**Full setup (with CosyVoice)**:
```bash
conda install -y -c conda-forge pynini=2.1.6
pip install WeTextProcessing --no-deps
pip install HyperPyYAML==1.2.2 modelscope==1.15.0 onnxruntime==1.19.2 \
    openai-whisper==20231117 importlib_resources==6.4.5 sounddevice==0.5.1 matcha-tts==0.0.7.0
```

Or use the complete `requirements.txt` or `environment.yml`.

### Model Downloads

Models auto-download on first run via ModelScope/HuggingFace. Key models:
- ASR: `iic/SenseVoiceSmall`
- LLM: `qwen/Qwen2.5-1.5B-Instruct`
- Speaker Verification: `damo/speech_campplus_sv_zh-cn_16k-common`
- TTS: `iic/CosyVoice-300M` (optional, edge-tts is default)
- Multimodal: `Qwen/Qwen2-VL-2B-Instruct`

Set HuggingFace mirror for China: `os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'`

## Running the Application

### Modern Web UI (Recommended)

**Using modular architecture**:
```bash
python app.py
# With options:
python app.py --port 7860 --share --server-name 0.0.0.0
```

**Using startup scripts**:
```bash
# Windows
start_maya_modern.bat

# Linux/Mac
./start_maya_modern.sh
```

### Legacy Web UI

```bash
python maya_webui.py  # v1.0 traditional interface
```

### CosyVoice Deployment

Set Python path for Matcha-TTS:
```bash
export PYTHONPATH=third_party/Matcha-TTS
```

**Docker deployment**:
```bash
cd runtime/python
docker build -t cosyvoice:v1.0 .

# gRPC server
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 \
  /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/grpc && \
  python3 server.py --port 50000 --max_conc 4 --model_dir iic/CosyVoice-300M"

# FastAPI server
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 \
  /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/fastapi && \
  python3 server.py --port 50000 --model_dir iic/CosyVoice-300M"
```

## Architecture & Key Concepts

### Backend Module (`src/backend/`)

**`config.py`**: Centralized configuration
- Model IDs and paths
- Audio settings (sample rate: 16000, mono)
- TTS voice mappings (language -> edge-tts voice)
- Default system prompt and settings

**`models.py`**: Model lifecycle management
- `MayaModels` class: singleton-style manager for all models
- Loads ASR (SenseVoice), LLM (Qwen2.5), SV (CAM++)
- Manages `ChatMemory` instance for conversation history

**`inference.py`**: Core business logic
- `InferenceEngine` class handles:
  - Speaker verification enrollment/matching
  - Wake word detection (pinyin-based matching)
  - Streaming LLM inference with TextIteratorStreamer
  - Audio recording and ASR transcription
  - TTS synthesis via edge-tts or CosyVoice

**`audio_utils.py`**: Audio utilities
- Pinyin conversion for wake word matching
- Language detection (langid) for TTS voice selection
- Audio duration calculation
- edge-tts async synthesis wrapper

**`memory.py`**: Chat history
- `ChatMemory` class: stores user/assistant pairs
- Context window management (default 512 chars)
- Provides formatted context for LLM prompts

### Frontend Module (`src/frontend/`)

**`ui.py`**: Gradio interface
- ChatGPT-style chat interface with bubbles
- Streaming output support
- Settings panel (wake word, voiceprint, TTS toggle)
- Voice recording and playback

**`styles.py`**: CSS styling
- Modern gradient design
- Dark/light theme support (Gradio built-in)
- Responsive layout for mobile/tablet/desktop

### CosyVoice Library

Integrated from [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice):
- `cosyvoice/cli/cosyvoice.py`: Main inference API
- `cosyvoice/flow/`: Flow-matching TTS models
- `cosyvoice/hifigan/`: Vocoder for waveform generation
- Supports: zero-shot, SFT, instruct, cross-lingual, voice conversion modes

When using CosyVoice, always set:
```bash
export PYTHONPATH=third_party/Matcha-TTS
```

## Key Configuration Points

### Modifying Models

Edit `src/backend/config.py`:
```python
MODEL_CONFIG = {
    "llm": {
        "model_id": "your/new-model",  # Change LLM here
        ...
    }
}
```

### Adjusting System Prompt

In `src/backend/config.py`:
```python
DEFAULT_SETTINGS = {
    "system_prompt": "你叫小千...",  # Customize AI persona
    ...
}
```

### Changing Wake Word

Default is "丫丫" (yá yá). Change in UI or modify:
```python
DEFAULT_SETTINGS = {
    "wake_word": "站起来",  # "zhàn qǐ lái"
    ...
}
```

Wake word detection uses pinyin matching via `pypinyin` library.

### TTS Voice Selection

TTS auto-detects language using `langid` and maps to edge-tts voices:
```python
LANGUAGE_SPEAKER_MAP = {
    "zh": "zh-CN-XiaoyiNeural",
    "en": "en-US-AnaNeural",
    ...
}
```

## Important Implementation Details

### Speaker Verification Flow

1. **Enrollment**: User records 3-10 sec audio → saved to `./SpeakerVerification_DIR/enroll_wav/`
2. **Verification**: Live audio → CAM++ pipeline → similarity score > 0.35 threshold → pass/fail

### Wake Word Detection

Uses pinyin matching (not keyword spotting model):
1. ASR transcribes full sentence → Chinese text
2. Extract Chinese chars → convert to pinyin (pypinyin)
3. Check if wake word pinyin substring exists in transcription

Example: Wake word "站起来" (zhàn qǐ lái) matches if "zhan qi lai" found in pinyin.

### Chat Memory

Conversation history stored as alternating "User: ..." / "Assistant: ..." strings:
- Max context length: 512 chars (configurable)
- Truncates from left when exceeding limit
- Prepended to each LLM prompt as context

### Streaming LLM Inference

Uses HuggingFace `TextIteratorStreamer`:
1. Tokenize input + chat history
2. Stream generation tokens in separate thread
3. Yield decoded tokens to Gradio UI
4. Automatic typing animation effect

### Real-time VAD (Voice Activity Detection)

Legacy scripts use `webrtcvad` for real-time interrupt:
- Detection window: 500ms
- Activation threshold: 40% voiced frames
- Chunk size: 20ms

Modern UI uses simple recording start/stop.

## Testing

Run individual test scripts in `tests/`:
```bash
python tests/5_pyttsx3_test.py          # Test pyttsx3 TTS
python tests/7.1_test_record_AV.py      # Test audio/video recording
python tests/9.1_test_cam++.py          # Test CAM++ speaker verification
```

## Common Issues

### pynini Installation

Windows users: use conda-forge
```bash
conda install -y -c conda-forge pynini=2.1.6
```

### PyAudio on Windows

Requires PortAudio binary. If pip fails, use pre-built wheel or conda package.

### CosyVoice Import Errors

Always export PYTHONPATH before running:
```bash
export PYTHONPATH=third_party/Matcha-TTS
```

### Model Download Timeout

Use ModelScope mirror or set HuggingFace endpoint:
```python
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

## Git Workflow

Current branch: `main`

Key staged changes include modularization of WebUI into `src/backend/` and `src/frontend/` directories.

## References

- [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) - TTS backbone
- [FunASR/SenseVoice](https://github.com/modelscope/FunASR) - ASR
- [Qwen2.5](https://github.com/QwenLM/Qwen2.5) - LLM
- ModelScope: https://www.modelscope.cn/
- HuggingFace mirror: https://hf-mirror.com/

## File Naming Conventions

Legacy scripts follow pattern: `{number}_{components}.py`
- `13_SenceVoice_QWen2.5_edgeTTS_realTime.py`: Real-time voice chat
- `14_SenceVoice_QWen2VL_edgeTTS_realTime.py`: Multimodal (audio+video)
- `15.0_SenceVoice_kws_CAM++.py`: Wake word + speaker verification (no memory)
- `15.1_SenceVoice_kws_CAM++.py`: Same with chat history memory

Modern entry points:
- `app.py`: Modular architecture entry
- `maya_webui_modern.py`: Monolithic modern UI
- `maya_webui.py`: Legacy traditional UI
