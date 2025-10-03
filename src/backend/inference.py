#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推理逻辑
Inference Logic
"""

import os
import time
import asyncio
import shutil

from .models import maya_models
from .audio_utils import (
    get_audio_duration,
    is_folder_empty,
    check_wake_word,
    text_to_speech,
    detect_language_and_get_voice
)
from .config import VOICEPRINT_DIR, DEFAULT_SETTINGS

class InferenceEngine:
    """推理引擎类"""
    
    def __init__(self):
        """初始化推理引擎"""
        self.audio_file_count = 0
    
    def register_voiceprint(self, audio_file):
        """
        声纹注册
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            str: 注册状态消息
        """
        if audio_file is None:
            return "❌ 请先录制音频"
        
        try:
            duration = get_audio_duration(audio_file)
            
            if duration < 3:
                return f"❌ 音频时长仅 {duration:.1f} 秒，需要至少 3 秒"
            
            # 保存声纹文件
            enroll_path = os.path.join(VOICEPRINT_DIR, "enroll_0.wav")
            shutil.copy(audio_file, enroll_path)
            
            return f"✅ 声纹注册成功！音频时长: {duration:.1f} 秒"
            
        except Exception as e:
            return f"❌ 声纹注册失败: {str(e)}"
    
    def speech_to_text(self, audio_file):
        """
        语音识别
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            str: 识别结果文本
        """
        if audio_file is None:
            return ""
        
        if not maya_models.is_loaded():
            return ""
        
        try:
            res = maya_models.asr_model.generate(
                input=audio_file,
                cache={},
                language="auto",
                use_itn=False,
            )
            
            text = res[0]['text'].split(">")[-1]
            return text
            
        except Exception as e:
            print(f"语音识别失败: {e}")
            return f"识别失败: {str(e)}"
    
    def verify_speaker(self, audio_file, threshold=0.35):
        """
        声纹验证
        
        Args:
            audio_file: 音频文件路径
            threshold: 验证阈值
            
        Returns:
            tuple: (是否通过, 相似度分数)
        """
        if audio_file is None:
            return False, 0.0
        
        if not maya_models.is_loaded():
            return False, 0.0
        
        enroll_file = os.path.join(VOICEPRINT_DIR, "enroll_0.wav")
        if not os.path.exists(enroll_file):
            return False, 0.0
        
        try:
            sv_score = maya_models.sv_pipeline(
                [enroll_file, audio_file],
                thr=threshold
            )
            
            score = sv_score.get('score', 0.0)
            result = sv_score.get('text', 'no')
            
            return result == "yes", score
                
        except Exception as e:
            print(f"声纹验证失败: {e}")
            return False, 0.0
    
    def chat_respond(self, message, history, audio_input, settings):
        """
        主对话函数（流式输出）
        
        Args:
            message: 用户文字输入
            history: 对话历史
            audio_input: 语音输入
            settings: 设置字典
            
        Yields:
            tuple: (更新后的历史, 音频输出)
        """
        if not maya_models.is_loaded():
            yield history + [("系统", "❌ 请先在设置中加载模型")], None
            return
        
        # 1. 处理输入（文字或语音）
        user_text = message
        if audio_input is not None:
            asr_text = self.speech_to_text(audio_input)
            if asr_text:
                user_text = asr_text
        
        if not user_text or user_text.strip() == "":
            yield history, None
            return
        
        # 显示用户消息
        history = history + [(user_text, None)]
        yield history, None
        
        # 2. 关键词唤醒检测
        if settings.get("enable_kws", False):
            wake_word = settings.get("wake_word", "站起来")
            if not check_wake_word(user_text, wake_word):
                error_msg = f"⚠️ 未检测到唤醒词「{wake_word}」"
                history[-1] = (user_text, error_msg)
                yield history, None
                return
        
        # 3. 声纹验证
        if settings.get("enable_sv", False) and audio_input is not None:
            sv_threshold = settings.get("sv_threshold", 0.35)
            sv_pass, sv_score = self.verify_speaker(audio_input, sv_threshold)
            if not sv_pass:
                error_msg = f"⚠️ 声纹验证失败 (相似度: {sv_score:.2f})"
                history[-1] = (user_text, error_msg)
                yield history, None
                return
        
        # 4. 大语言模型推理
        try:
            context = maya_models.memory.get_context()
            prompt_with_context = f"{context}\nUser: {user_text}\n" if context else user_text
            
            system_prompt = settings.get("system_prompt", DEFAULT_SETTINGS["system_prompt"])
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_with_context},
            ]
            
            text = maya_models.llm_tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            
            model_inputs = maya_models.llm_tokenizer([text], return_tensors="pt").to(
                maya_models.llm_model.device
            )
            
            max_new_tokens = settings.get("max_new_tokens", DEFAULT_SETTINGS["max_new_tokens"])
            
            generated_ids = maya_models.llm_model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
            )
            
            generated_ids = [
                output_ids[len(input_ids):]
                for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
            
            output_text = maya_models.llm_tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0]
            
            # 流式显示回复
            history[-1] = (user_text, "")
            for i in range(0, len(output_text), 2):
                history[-1] = (user_text, output_text[:i+2])
                yield history, None
                time.sleep(0.02)
            
            history[-1] = (user_text, output_text)
            
            # 更新记忆
            maya_models.memory.add_to_history(user_text, output_text)
            
            # 5. 语音合成
            audio_output = None
            if settings.get("enable_tts", True):
                language, voice = detect_language_and_get_voice(output_text)
                self.audio_file_count += 1
                audio_output = asyncio.run(text_to_speech(output_text, voice))
            
            yield history, audio_output
            
        except Exception as e:
            error_msg = f"❌ 出错了: {str(e)}"
            history[-1] = (user_text, error_msg)
            yield history, None

# 创建全局推理引擎实例
inference_engine = InferenceEngine()

