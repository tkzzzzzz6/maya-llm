#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端配置文件
Backend Configuration
"""

import os

# ========== 环境配置 ==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# ========== 路径配置 ==========
OUTPUT_DIR = "./output"
VOICEPRINT_DIR = './SpeakerVerification_DIR/enroll_wav/'
TEMP_AUDIO_DIR = "./Test_QWen2_VL/"

# 确保目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VOICEPRINT_DIR, exist_ok=True)
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# ========== 音频配置 ==========
AUDIO_RATE = 16000        # 音频采样率
AUDIO_CHANNELS = 1        # 单声道
CHUNK_SIZE = 1024         # 音频块大小

# ========== 模型配置 ==========
MODEL_CONFIG = {
    "asr": {
        "model_id": "iic/SenseVoiceSmall",
        "trust_remote_code": True
    },
    "sv": {
        "task": "speaker-verification",
        "model_id": "damo/speech_campplus_sv_zh-cn_16k-common",
        "model_revision": "v1.0.0"
    },
    "llm": {
        "model_id": "qwen/Qwen2.5-1.5B-Instruct",
        "torch_dtype": "auto",
        "device_map": "auto",
        "trust_remote_code": True
    }
}

# ========== 默认设置 ==========
DEFAULT_SETTINGS = {
    "enable_kws": False,
    "wake_word": "丫丫",
    "enable_sv": False,
    "sv_threshold": 0.35,
    "enable_tts": True,
    "system_prompt": "你叫小千，是一个21岁的畜牧专业的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。",
    "memory_max_length": 512,
    "max_new_tokens": 512
}

# ========== TTS 配置 ==========
LANGUAGE_SPEAKER_MAP = {
    "ja": "ja-JP-NanamiNeural",
    "fr": "fr-FR-DeniseNeural",
    "es": "ca-ES-JoanaNeural",
    "de": "de-DE-KatjaNeural",
    "zh": "zh-CN-XiaoyiNeural",
    "en": "en-US-AnaNeural",
}

DEFAULT_VOICE = "zh-CN-XiaoyiNeural"

