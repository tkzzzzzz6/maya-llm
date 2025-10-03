#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型加载和管理
Model Loading and Management
"""

import gradio as gr
from funasr import AutoModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from modelscope.pipelines import pipeline
from modelscope import snapshot_download

from .config import MODEL_CONFIG, VOICEPRINT_DIR
from .memory import ChatMemory
import os

class MayaModels:
    """模型管理类"""
    
    def __init__(self):
        """初始化模型管理器"""
        self.models_loaded = False
        self.asr_model = None
        self.llm_model = None
        self.llm_tokenizer = None
        self.sv_pipeline = None
        self.memory = ChatMemory(max_length=512)
        
        # 确保声纹目录存在
        os.makedirs(VOICEPRINT_DIR, exist_ok=True)
        
    def load_models(self, progress=gr.Progress()):
        """
        加载所有模型（生成器函数，用于流式更新状态）
        
        Yields:
            str: 加载状态信息
        """
        if self.models_loaded:
            yield "✅ 模型已加载完成"
            return
        
        try:
            # 1. 加载 SenseVoice ASR 模型
            yield "📥 正在加载语音识别模型 (SenseVoice)..."
            if progress:
                progress(0.2)
            
            self.asr_model = AutoModel(
                model=MODEL_CONFIG["asr"]["model_id"],
                trust_remote_code=MODEL_CONFIG["asr"]["trust_remote_code"]
            )
            
            # 2. 加载 CAM++ 声纹识别模型
            yield "📥 正在加载声纹识别模型 (CAM++)..."
            if progress:
                progress(0.4)
            
            self.sv_pipeline = pipeline(
                task=MODEL_CONFIG["sv"]["task"],
                model=MODEL_CONFIG["sv"]["model_id"],
                model_revision=MODEL_CONFIG["sv"]["model_revision"]
            )
            
            # 3. 加载 Qwen2.5 大语言模型
            yield "📥 正在加载大语言模型 (Qwen2.5-1.5B)..."
            if progress:
                progress(0.6)
            
            qwen_local_dir = snapshot_download(
                model_id=MODEL_CONFIG["llm"]["model_id"]
            )
            
            yield "🔄 初始化大语言模型..."
            if progress:
                progress(0.8)
            
            self.llm_model = AutoModelForCausalLM.from_pretrained(
                qwen_local_dir,
                torch_dtype=MODEL_CONFIG["llm"]["torch_dtype"],
                device_map=MODEL_CONFIG["llm"]["device_map"],
                trust_remote_code=MODEL_CONFIG["llm"]["trust_remote_code"]
            )
            
            self.llm_tokenizer = AutoTokenizer.from_pretrained(
                qwen_local_dir,
                trust_remote_code=MODEL_CONFIG["llm"]["trust_remote_code"]
            )
            
            if progress:
                progress(1.0)
            
            self.models_loaded = True
            yield "✅ 所有模型加载成功！可以开始对话了"
            
        except Exception as e:
            yield f"❌ 模型加载失败: {str(e)}"
    
    def is_loaded(self):
        """检查模型是否已加载"""
        return self.models_loaded
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory.clear()

# 创建全局模型实例
maya_models = MayaModels()

