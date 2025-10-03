#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频处理工具
Audio Processing Utilities
"""

import wave
import os
import tempfile
import asyncio
import edge_tts
import re
from pypinyin import pinyin, Style
import langid

from .config import AUDIO_RATE, LANGUAGE_SPEAKER_MAP, DEFAULT_VOICE

def extract_chinese_and_convert_to_pinyin(input_string):
    """
    提取汉字并转换为拼音
    
    Args:
        input_string: 输入字符串
        
    Returns:
        str: 拼音字符串
    """
    chinese_characters = re.findall(r'[\u4e00-\u9fa5]', input_string)
    chinese_text = ''.join(chinese_characters)
    
    if not chinese_text:
        return ""
    
    pinyin_result = pinyin(chinese_text, style=Style.NORMAL)
    pinyin_text = ' '.join([item[0] for item in pinyin_result])
    
    return pinyin_text

def check_wake_word(text, wake_word="yaya"):
    """
    检查唤醒词（支持中英文）

    Args:
        text: 输入文本
        wake_word: 唤醒词

    Returns:
        bool: 是否包含唤醒词
    """
    if not text or not wake_word:
        return False

    # 转换为小写进行比较
    text_lower = text.lower()
    wake_word_lower = wake_word.lower()

    # 1. 直接匹配（英文或拼音）
    if wake_word_lower in text_lower:
        return True

    # 2. 拼音匹配（中文）
    text_pinyin = extract_chinese_and_convert_to_pinyin(text)
    wake_word_pinyin = extract_chinese_and_convert_to_pinyin(wake_word)

    if text_pinyin and wake_word_pinyin:
        # 去除空格进行匹配
        text_pinyin_clean = text_pinyin.replace(" ", "")
        wake_word_pinyin_clean = wake_word_pinyin.replace(" ", "")

        if wake_word_pinyin_clean in text_pinyin_clean:
            return True

    return False

def get_audio_duration(audio_file):
    """
    获取音频时长
    
    Args:
        audio_file: 音频文件路径
        
    Returns:
        float: 时长（秒）
    """
    try:
        with wave.open(audio_file, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        return duration
    except Exception as e:
        print(f"获取音频时长失败: {e}")
        return 0.0

def is_folder_empty(folder_path):
    """
    检测文件夹是否为空
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        bool: 是否为空
    """
    if not os.path.exists(folder_path):
        return True
    
    entries = os.listdir(folder_path)
    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            return False
    return True

async def text_to_speech(text, voice=None):
    """
    文字转语音（异步）
    
    Args:
        text: 文本内容
        voice: 音色名称
        
    Returns:
        str: 音频文件路径
    """
    if voice is None:
        # 自动检测语种
        language, _ = langid.classify(text)
        voice = LANGUAGE_SPEAKER_MAP.get(language, DEFAULT_VOICE)
    
    output_file = tempfile.mktemp(suffix=".mp3")
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file
    except Exception as e:
        print(f"语音合成失败: {e}")
        return None

def detect_language_and_get_voice(text):
    """
    检测语种并获取对应音色
    
    Args:
        text: 文本内容
        
    Returns:
        tuple: (language, voice)
    """
    language, confidence = langid.classify(text)
    voice = LANGUAGE_SPEAKER_MAP.get(language, DEFAULT_VOICE)
    return language, voice

