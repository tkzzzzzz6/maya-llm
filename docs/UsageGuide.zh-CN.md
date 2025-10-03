## ASR-LLM-TTS 使用指南（Windows/WSL 优先）

本项目集成了语音识别 ASR（SenseVoice/FunASR）、大语言模型 LLM（Qwen/Qwen2.5 与 Qwen2-VL）与语音合成 TTS（CosyVoice/edge-tts/pyttsx3），支持实时单模态与音视频多模态语音交互。

- 代码根目录：`ASR-LLM-TTS`
- 关键实时脚本：
  - `13_SenceVoice_QWen2.5_edgeTTS_realTime.py`（单模态，实时，edge-tts 合成）
  - `14_SenceVoice_QWen2VL_edgeTTS_realTime.py`（音视频多模态，edge-tts 合成）
  - `10_SenceVoice_QWen2.5_cosyVoice.py`（离线/分段，CosyVoice 合成）
  - `11_SenceVoice_QWen2.5_pytts3.py`（离线/分段，pyttsx3 合成）
  - `12_SenceVoice_QWen2.5_edgeTTS.py`（离线/分段，edge-tts 合成）
- 服务入口：`runtime/python/fastapi/server.py`（CosyVoice 推理 FastAPI）


### 1. 环境准备

建议使用 Conda 和 Python 3.10，NVIDIA GPU + CUDA 环境可加速推理。系统需安装 `ffmpeg` 与音频输入设备驱动（Windows 上 `PyAudio` 依赖 PortAudio）。

1) 创建虚拟环境

```bash
conda create -n chatAudio python=3.10 -y
conda activate chatAudio
```

2) 安装 PyTorch（示例：CUDA 11.8）

```bash
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118
```

3) 快速最小依赖（不使用 CosyVoice）

```bash
pip install edge-tts==6.1.17 funasr==1.1.12 ffmpeg==1.4 opencv-python==4.10.0.84 \
            transformers==4.45.2 webrtcvad==2.0.10 qwen-vl-utils==0.0.8 \
            pygame==2.6.1 langid==1.1.6 langdetect==1.0.9 accelerate==0.33.0 PyAudio==0.2.14
```

4) 追加 CosyVoice 依赖（可选）

```bash
# 建议通过 conda 安装 pynini，pip 安装 WeTextProcessing
conda install -y -c conda-forge pynini=2.1.6
pip install WeTextProcessing --no-deps

pip install HyperPyYAML==1.2.2 modelscope==1.15.0 onnxruntime==1.19.2 \
            openai-whisper==20231117 importlib_resources==6.4.5 sounddevice==0.5.1 \
            matcha-tts==0.0.7.0
```

也可使用仓库提供的 `environment.yml` 复现环境（包含镜像源与固定版本）。


### 2. 模型与资源下载

推荐使用 ModelScope 下载加速国内访问，或配置 HuggingFace 国内镜像：

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from modelscope import snapshot_download

# SenseVoice（ASR）
sv_dir = snapshot_download('iic/SenseVoiceSmall')

# Qwen2.5（LLM）- 轻量对话
qwen_dir = snapshot_download('qwen/Qwen2.5-1.5B-Instruct')

# Qwen2-VL（多模态）
qwen_vl_dir = 'Qwen/Qwen2-VL-2B-Instruct'  # 由 Transformers 自动下载

# CosyVoice（TTS，可选）
cv_dir = snapshot_download('iic/CosyVoice-300M')
```

如需手动下载，请参考 `README.md` 中的模型链接说明。


### 3. 快速体验

1) 实时语音对话（单模态，edge-tts 合成）

```bash
python 13_SenceVoice_QWen2.5_edgeTTS_realTime.py
```

- 话筒实时采集 + WebRTC VAD 分段；
- ASR：SenseVoice；LLM：Qwen2.5-1.5B；TTS：edge-tts；
- 关键参数可在脚本顶部调整：`AUDIO_RATE`、`CHUNK`、`VAD_MODE`、`NO_SPEECH_THRESHOLD`。

2) 实时多模态（音视频 + 语言，edge-tts 合成）

```bash
python 14_SenceVoice_QWen2VL_edgeTTS_realTime.py
```

- 摄像头实时采集，VAD 触发保存音视频片段；
- ASR：SenseVoice；多模态 LLM：Qwen2-VL；TTS：edge-tts。

3) 分段/离线推理（CosyVoice 合成）

```bash
python 10_SenceVoice_QWen2.5_cosyVoice.py
```

或使用 `11_..._pytts3.py`、`12_..._edgeTTS.py` 切换不同合成后端。


### 4. 语音合成发音人与语言映射（edge-tts）

`13`/`14` 实时脚本中内置简易语言检测并映射到 `edge-tts` 发音人：

- ja → `ja-JP-NanamiNeural`
- fr → `fr-FR-DeniseNeural`
- es → `ca-ES-JoanaNeural`
- de → `de-DE-KatjaNeural`
- zh → `zh-CN-XiaoyiNeural`
- en → `en-US-AnaNeural`

如检测失败，默认中文女声。


### 5. CosyVoice FastAPI 服务

CosyVoice 提供 Web 服务封装，便于外部系统接入：

```bash
python runtime/python/fastapi/server.py --port 50000 --model_dir iic/CosyVoice-300M
```

可用接口（GET，表单参数）：

- `/inference_sft`：`tts_text`，`spk_id`
- `/inference_zero_shot`：`tts_text`，`prompt_text`，`prompt_wav`
- `/inference_cross_lingual`：`tts_text`，`prompt_wav`
- `/inference_instruct`：`tts_text`，`spk_id`，`instruct_text`

返回值为音频字节流（`StreamingResponse`），客户端可边下边播。


### 6. 常见问题（FAQ）

- PyAudio 安装/权限：使用管理员终端；必要时安装 `portaudio` 或使用预编译轮子。
- edge-tts 网络：若报错，升级至 `edge-tts==6.1.17`（已在依赖中固定）。
- 模型下载超时：优先 `modelscope.snapshot_download` 或设置 `HF_ENDPOINT` 国内镜像。
- CUDA/显存不足：选择更小的 Qwen 模型或降低 Qwen2-VL 分辨率（`min_pixels`/`max_pixels`）。
- ffmpeg 未找到：确认 `ffmpeg` 安装到 PATH。


### 7. 关键参数速览（实时脚本）

- `AUDIO_RATE=16000`、`AUDIO_CHANNELS=1`、`CHUNK=1024`
- `VAD_MODE=3`（0-3，越大越敏感）、`NO_SPEECH_THRESHOLD=1.0s`
- 多模态采样帧比例：`[0.2, 0.4, 0.6, 0.8]`
- 输出目录：`./output`、示例片段输出：`./Test_QWen2_VL/`


### 8. 参考

- 根目录 `README.md`（安装要点与更新日志）
- `README_CosyVoice.md`（CosyVoice 官方说明、部署与 Demo）



