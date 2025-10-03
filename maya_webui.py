#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻鸭语音助手 Web UI
Maya Voice Assistant - Modern Web Interface

功能特性：
- 🎙️ 语音识别 (SenseVoice)
- 🔑 关键词唤醒 (KWS) 
- 👤 声纹识别 (CAM++)
- 🤖 智能对话 (Qwen2.5)
- 🔊 语音合成 (Edge TTS)
- 💾 对话记忆
"""

import gradio as gr
import numpy as np
import torch
import wave
import os
import tempfile
import asyncio
from datetime import datetime
from funasr import AutoModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from modelscope.pipelines import pipeline
from modelscope import snapshot_download
import edge_tts
import pygame
import time
import re
from pypinyin import pinyin, Style
import langid

# ========== 配置 ==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 全局变量
audio_file_count = 0
conversation_history = []

# ========== 工具函数 ==========

def extract_chinese_and_convert_to_pinyin(input_string):
    """提取汉字并转换为拼音"""
    chinese_characters = re.findall(r'[\u4e00-\u9fa5]', input_string)
    chinese_text = ''.join(chinese_characters)
    pinyin_result = pinyin(chinese_text, style=Style.NORMAL)
    pinyin_text = ' '.join([item[0] for item in pinyin_result])
    return pinyin_text

def is_folder_empty(folder_path):
    """检测文件夹是否为空"""
    if not os.path.exists(folder_path):
        return True
    entries = os.listdir(folder_path)
    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            return False
    return True

def format_history(history_list):
    """格式化对话历史"""
    if not history_list:
        return "暂无对话记录"
    
    formatted = []
    for i, (user_msg, bot_msg, timestamp) in enumerate(history_list, 1):
        formatted.append(f"**[{timestamp}] 对话 #{i}**")
        formatted.append(f"👤 用户: {user_msg}")
        formatted.append(f"🤖 麻鸭: {bot_msg}")
        formatted.append("---")
    return "\n".join(formatted)

async def text_to_speech(text, voice="zh-CN-XiaoyiNeural"):
    """异步文字转语音"""
    output_file = tempfile.mktemp(suffix=".mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

# ========== 对话记忆类 ==========

class ChatMemory:
    def __init__(self, max_length=2048):
        self.history = []
        self.max_length = max_length

    def add_to_history(self, user_input, model_response):
        self.history.append(f"User: {user_input}")
        self.history.append(f"Assistant: {model_response}")

    def get_context(self):
        context = "\n".join(self.history)
        if len(context) > self.max_length:
            context = context[-self.max_length:]
        return context
    
    def clear(self):
        self.history = []

# ========== 模型管理类 ==========

class MayaModels:
    def __init__(self):
        self.models_loaded = False
        self.asr_model = None
        self.llm_model = None
        self.llm_tokenizer = None
        self.sv_pipeline = None
        self.memory = ChatMemory(max_length=512)
        self.sv_enroll_dir = './SpeakerVerification_DIR/enroll_wav/'
        os.makedirs(self.sv_enroll_dir, exist_ok=True)
        os.makedirs('./output', exist_ok=True)
        
    def load_models(self, progress=gr.Progress()):
        """加载所有模型"""
        if self.models_loaded:
            return "✅ 模型已加载"
        
        try:
            # 1. 加载 SenseVoice ASR 模型
            progress(0.2, desc="加载语音识别模型 (SenseVoice)...")
            self.asr_model = AutoModel(
                model="iic/SenseVoiceSmall",
                trust_remote_code=True
            )
            
            # 2. 加载 CAM++ 声纹识别模型
            progress(0.4, desc="加载声纹识别模型 (CAM++)...")
            self.sv_pipeline = pipeline(
                task='speaker-verification',
                model='damo/speech_campplus_sv_zh-cn_16k-common',
                model_revision='v1.0.0'
            )
            
            # 3. 加载 Qwen2.5 大语言模型
            progress(0.6, desc="加载大语言模型 (Qwen2.5-1.5B)...")
            model_id = "qwen/Qwen2.5-1.5B-Instruct"
            qwen_local_dir = snapshot_download(model_id=model_id)
            
            progress(0.8, desc="初始化大语言模型...")
            self.llm_model = AutoModelForCausalLM.from_pretrained(
                qwen_local_dir,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            self.llm_tokenizer = AutoTokenizer.from_pretrained(
                qwen_local_dir,
                trust_remote_code=True
            )
            
            progress(1.0, desc="模型加载完成！")
            self.models_loaded = True
            return "✅ 所有模型加载成功！"
            
        except Exception as e:
            return f"❌ 模型加载失败: {str(e)}"

# 创建全局模型实例
maya_models = MayaModels()

# ========== 核心功能函数 ==========

def register_voiceprint(audio_file, progress=gr.Progress()):
    """声纹注册"""
    if audio_file is None:
        return "❌ 请先录制或上传音频", None
    
    try:
        progress(0.3, desc="检查音频质量...")
        
        # 检查音频长度
        with wave.open(audio_file, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        
        if duration < 3:
            return f"❌ 音频时长仅 {duration:.1f} 秒，需要至少 3 秒", None
        
        progress(0.6, desc="保存声纹特征...")
        
        # 保存声纹文件
        enroll_path = os.path.join(maya_models.sv_enroll_dir, "enroll_0.wav")
        
        # 复制音频文件
        import shutil
        shutil.copy(audio_file, enroll_path)
        
        progress(1.0, desc="声纹注册完成！")
        
        return f"✅ 声纹注册成功！音频时长: {duration:.1f} 秒", enroll_path
        
    except Exception as e:
        return f"❌ 声纹注册失败: {str(e)}", None

def speech_to_text(audio_file, progress=gr.Progress()):
    """语音识别"""
    if audio_file is None:
        return "❌ 请先录制或上传音频"
    
    if not maya_models.models_loaded:
        return "❌ 请先加载模型"
    
    try:
        progress(0.5, desc="识别中...")
        
        res = maya_models.asr_model.generate(
            input=audio_file,
            cache={},
            language="auto",
            use_itn=False,
        )
        
        text = res[0]['text'].split(">")[-1]
        progress(1.0, desc="识别完成！")
        
        return text
        
    except Exception as e:
        return f"❌ 识别失败: {str(e)}"

def verify_speaker(audio_file, threshold=0.35, progress=gr.Progress()):
    """声纹验证"""
    if audio_file is None:
        return "❌ 请先录制或上传音频", 0.0
    
    if not maya_models.models_loaded:
        return "❌ 请先加载模型", 0.0
    
    # 检查是否已注册声纹
    enroll_file = os.path.join(maya_models.sv_enroll_dir, "enroll_0.wav")
    if not os.path.exists(enroll_file):
        return "❌ 请先注册声纹", 0.0
    
    try:
        progress(0.5, desc="验证中...")
        
        sv_score = maya_models.sv_pipeline(
            [enroll_file, audio_file],
            thr=threshold
        )
        
        score = sv_score.get('score', 0.0)
        result = sv_score.get('text', 'no')
        
        progress(1.0, desc="验证完成！")
        
        if result == "yes":
            return f"✅ 声纹验证通过 (相似度: {score:.2f})", score
        else:
            return f"❌ 声纹验证失败 (相似度: {score:.2f})", score
            
    except Exception as e:
        return f"❌ 验证失败: {str(e)}", 0.0

def check_wake_word(text, wake_word="站起来"):
    """检查唤醒词"""
    text_pinyin = extract_chinese_and_convert_to_pinyin(text)
    wake_word_pinyin = extract_chinese_and_convert_to_pinyin(wake_word)
    
    wake_word_pinyin = wake_word_pinyin.replace(" ", "")
    text_pinyin = text_pinyin.replace(" ", "")
    
    if wake_word_pinyin in text_pinyin:
        return True, f"✅ 检测到唤醒词: {wake_word}"
    else:
        return False, f"❌ 未检测到唤醒词 (需要: {wake_word})"

def chat_with_maya(
    text_input=None,
    audio_input=None,
    enable_kws=True,
    wake_word="站起来",
    enable_sv=True,
    sv_threshold=0.35,
    enable_tts=True,
    system_prompt="你叫小千，是一个18岁的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。",
    progress=gr.Progress()
):
    """主对话函数"""
    global conversation_history, audio_file_count
    
    if not maya_models.models_loaded:
        return "❌ 请先加载模型", None, format_history(conversation_history)
    
    user_text = text_input
    
    # 1. 语音识别
    if audio_input is not None:
        progress(0.1, desc="语音识别中...")
        user_text = speech_to_text(audio_input)
        if user_text.startswith("❌"):
            return user_text, None, format_history(conversation_history)
    
    if not user_text or user_text.strip() == "":
        return "❌ 请输入文字或录制语音", None, format_history(conversation_history)
    
    # 2. 关键词唤醒检测
    if enable_kws:
        progress(0.2, desc="检测唤醒词...")
        kws_pass, kws_msg = check_wake_word(user_text, wake_word)
        if not kws_pass:
            return kws_msg, None, format_history(conversation_history)
    
    # 3. 声纹验证
    if enable_sv and audio_input is not None:
        progress(0.3, desc="声纹验证中...")
        sv_msg, sv_score = verify_speaker(audio_input, sv_threshold)
        if not sv_msg.startswith("✅"):
            return sv_msg, None, format_history(conversation_history)
    
    # 4. 大语言模型推理
    progress(0.5, desc="思考中...")
    
    try:
        # 获取历史对话上下文
        context = maya_models.memory.get_context()
        prompt_with_context = f"{context}\nUser: {user_text}\n" if context else user_text
        
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
        
        generated_ids = maya_models.llm_model.generate(
            **model_inputs,
            max_new_tokens=512,
        )
        
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        output_text = maya_models.llm_tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0]
        
        # 更新记忆
        maya_models.memory.add_to_history(user_text, output_text)
        
        # 保存对话历史
        timestamp = datetime.now().strftime("%H:%M:%S")
        conversation_history.append((user_text, output_text, timestamp))
        
        # 5. 语音合成
        audio_output = None
        if enable_tts:
            progress(0.8, desc="生成语音中...")
            
            # 语种识别
            language, _ = langid.classify(output_text)
            
            language_speaker = {
                "ja": "ja-JP-NanamiNeural",
                "fr": "fr-FR-DeniseNeural",
                "es": "ca-ES-JoanaNeural",
                "de": "de-DE-KatjaNeural",
                "zh": "zh-CN-XiaoyiNeural",
                "en": "en-US-AnaNeural",
            }
            
            voice = language_speaker.get(language, "zh-CN-XiaoyiNeural")
            
            audio_file_count += 1
            audio_output = asyncio.run(text_to_speech(output_text, voice))
        
        progress(1.0, desc="完成！")
        
        return output_text, audio_output, format_history(conversation_history)
        
    except Exception as e:
        return f"❌ 对话失败: {str(e)}", None, format_history(conversation_history)

def clear_history():
    """清空对话历史"""
    global conversation_history
    conversation_history = []
    maya_models.memory.clear()
    return "", format_history(conversation_history)

# ========== Gradio 界面 ==========

def create_ui():
    """创建 Gradio 界面"""
    
    # 自定义 CSS
    custom_css = """
    .gradio-container {
        font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
    }
    .header-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .header-subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        padding: 1em;
        border-radius: 10px;
        margin: 0.5em 0;
    }
    .status-box {
        padding: 1em;
        border-radius: 8px;
        margin: 0.5em 0;
        font-weight: bold;
    }
    """
    
    with gr.Blocks(css=custom_css, title="麻鸭语音助手", theme=gr.themes.Soft()) as demo:
        
        # 标题区域
        gr.HTML("""
        <div class="header-title">🦆 麻鸭语音助手</div>
        <div class="header-subtitle">Maya Voice Assistant - 基于麻鸭语料微调的智能语音助手</div>
        """)
        
        # 功能介绍
        with gr.Row():
            gr.Markdown("""
            ### ✨ 核心功能
            - 🎙️ **语音识别**: SenseVoice 高精度识别
            - 🔑 **关键词唤醒**: 自定义唤醒词，保护隐私
            - 👤 **声纹识别**: CAM++ 声纹验证，专属助手
            - 🤖 **智能对话**: Qwen2.5 大模型，上下文记忆
            - 🔊 **语音合成**: Edge TTS 多语种自然语音
            """)
        
        # 第一步：模型加载
        with gr.Tab("📦 1. 模型加载"):
            gr.Markdown("### 首次使用请先加载模型（约需1-3分钟）")
            
            load_btn = gr.Button("🚀 加载所有模型", variant="primary", size="lg")
            load_status = gr.Textbox(label="加载状态", lines=2, interactive=False)
            
            load_btn.click(
                fn=maya_models.load_models,
                outputs=load_status
            )
        
        # 第二步：声纹注册
        with gr.Tab("👤 2. 声纹注册 (可选)"):
            gr.Markdown("""
            ### 注册您的声纹，让助手只听你的指令
            - 录制或上传 **3-10秒** 的清晰语音
            - 建议说一段完整的话，如"你好，我是[你的名字]，这是我的声纹"
            """)
            
            with gr.Row():
                with gr.Column():
                    voiceprint_audio = gr.Audio(
                        source="microphone",  # Gradio 3.x 兼容
                        type="filepath",
                        label="录制或上传音频 (≥3秒)"
                    )
                    register_btn = gr.Button("✅ 注册声纹", variant="primary")
                
                with gr.Column():
                    register_status = gr.Textbox(label="注册状态", lines=2)
                    voiceprint_file = gr.File(label="已保存的声纹文件")
            
            register_btn.click(
                fn=register_voiceprint,
                inputs=voiceprint_audio,
                outputs=[register_status, voiceprint_file]
            )
        
        # 第三步：对话交互
        with gr.Tab("💬 3. 开始对话"):
            gr.Markdown("### 与麻鸭语音助手对话")
            
            with gr.Row():
                # 左侧：输入区
                with gr.Column(scale=1):
                    gr.Markdown("#### 📝 输入方式")
                    
                    text_input = gr.Textbox(
                        label="文字输入",
                        placeholder="输入您的问题...",
                        lines=3
                    )
                    
                    audio_input = gr.Audio(
                        source="microphone",  # Gradio 3.x 兼容
                        type="filepath",
                        label="语音输入"
                    )
                    
                    with gr.Accordion("⚙️ 高级设置", open=False):
                        enable_kws = gr.Checkbox(
                            label="启用关键词唤醒",
                            value=True,
                            info="需要说出唤醒词才能响应"
                        )
                        wake_word = gr.Textbox(
                            label="唤醒词",
                            value="站起来",
                            placeholder="输入唤醒词（中文）"
                        )
                        
                        enable_sv = gr.Checkbox(
                            label="启用声纹验证",
                            value=False,
                            info="仅注册用户可使用"
                        )
                        sv_threshold = gr.Slider(
                            minimum=0.1,
                            maximum=0.9,
                            value=0.35,
                            step=0.05,
                            label="声纹相似度阈值",
                            info="越高越严格"
                        )
                        
                        enable_tts = gr.Checkbox(
                            label="启用语音合成",
                            value=True,
                            info="生成语音回复"
                        )
                        
                        system_prompt = gr.Textbox(
                            label="系统提示词",
                            value="你叫小千，是一个18岁的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。",
                            lines=3
                        )
                    
                    chat_btn = gr.Button("🚀 发送", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ 清空历史", variant="secondary")
                
                # 右侧：输出区
                with gr.Column(scale=1):
                    gr.Markdown("#### 💬 助手回复")
                    
                    text_output = gr.Textbox(
                        label="文字回复",
                        lines=5,
                        interactive=False
                    )
                    
                    audio_output = gr.Audio(
                        label="语音回复",
                        autoplay=True
                    )
                    
                    history_output = gr.Markdown(
                        label="对话历史",
                        value="暂无对话记录"
                    )
            
            # 绑定事件
            chat_btn.click(
                fn=chat_with_maya,
                inputs=[
                    text_input,
                    audio_input,
                    enable_kws,
                    wake_word,
                    enable_sv,
                    sv_threshold,
                    enable_tts,
                    system_prompt
                ],
                outputs=[text_output, audio_output, history_output]
            )
            
            clear_btn.click(
                fn=clear_history,
                outputs=[text_output, history_output]
            )
        
        # 第四步：测试功能
        with gr.Tab("🔧 4. 功能测试"):
            gr.Markdown("### 单独测试各项功能")
            
            with gr.Row():
                # 语音识别测试
                with gr.Column():
                    gr.Markdown("#### 🎙️ 语音识别测试")
                    test_asr_audio = gr.Audio(
                        source="microphone",  # Gradio 3.x 兼容
                        type="filepath",
                        label="测试音频"
                    )
                    test_asr_btn = gr.Button("识别", variant="primary")
                    test_asr_output = gr.Textbox(label="识别结果", lines=3)
                    
                    test_asr_btn.click(
                        fn=speech_to_text,
                        inputs=test_asr_audio,
                        outputs=test_asr_output
                    )
                
                # 声纹验证测试
                with gr.Column():
                    gr.Markdown("#### 👤 声纹验证测试")
                    test_sv_audio = gr.Audio(
                        source="microphone",  # Gradio 3.x 兼容
                        type="filepath",
                        label="测试音频"
                    )
                    test_sv_threshold = gr.Slider(
                        minimum=0.1,
                        maximum=0.9,
                        value=0.35,
                        step=0.05,
                        label="阈值"
                    )
                    test_sv_btn = gr.Button("验证", variant="primary")
                    test_sv_output = gr.Textbox(label="验证结果", lines=3)
                    
                    test_sv_btn.click(
                        fn=verify_speaker,
                        inputs=[test_sv_audio, test_sv_threshold],
                        outputs=test_sv_output
                    )
        
        # 使用说明
        with gr.Tab("📖 使用说明"):
            gr.Markdown("""
            ## 📖 使用指南
            
            ### 快速开始（4步）
            
            #### 1️⃣ 加载模型
            - 点击"模型加载"标签页
            - 点击"加载所有模型"按钮
            - 等待1-3分钟（首次运行需要下载模型）
            
            #### 2️⃣ 注册声纹（可选）
            - 如果需要声纹验证功能，在"声纹注册"页面录制3-10秒音频
            - 点击"注册声纹"
            
            #### 3️⃣ 开始对话
            - 切换到"开始对话"标签页
            - 文字输入或语音录制您的问题
            - 确保说出唤醒词（默认"站起来"）
            - 点击"发送"
            
            #### 4️⃣ 高级设置
            - 展开"高级设置"可以：
              - 自定义唤醒词
              - 调整声纹验证阈值
              - 修改AI人设
            
            ---
            
            ### ⚙️ 功能说明
            
            #### 🔑 关键词唤醒
            - **用途**: 保护隐私，避免误触发
            - **使用**: 在对话中包含唤醒词，如"站起来，今天天气怎么样？"
            - **自定义**: 可在高级设置中修改唤醒词
            
            #### 👤 声纹识别
            - **用途**: 确保只有注册用户可以使用
            - **使用**: 注册声纹后，启用"声纹验证"，只用语音输入才会验证
            - **阈值**: 0.35为推荐值，可根据实际情况调整（越高越严格）
            
            #### 💾 对话记忆
            - 自动记住对话上下文（最近512字）
            - 支持多轮对话
            - 点击"清空历史"重置对话
            
            #### 🌍 多语言支持
            - 自动识别回复语种
            - 支持中文、英文、日语、法语、德语、西班牙语
            
            ---
            
            ### ⚠️ 常见问题
            
            **Q: 模型加载很慢？**  
            A: 首次运行需要从 ModelScope 下载模型（约2-3GB），请耐心等待。后续启动会直接使用缓存。
            
            **Q: 唤醒词不生效？**  
            A: 确保唤醒词是中文，并且在对话中包含完整的唤醒词拼音。
            
            **Q: 声纹验证总是失败？**  
            A: 尝试降低阈值，或重新注册更清晰的声纹。
            
            **Q: 没有麦克风怎么办？**  
            A: 可以使用文字输入，或上传音频文件。
            
            ---
            
            ### 🎯 使用技巧
            
            1. **仅使用文字对话**: 关闭"启用关键词唤醒"和"启用声纹验证"
            2. **公共场合使用**: 关闭"启用语音合成"，仅看文字回复
            3. **个性化AI**: 修改"系统提示词"改变AI的性格和风格
            4. **提高识别率**: 录音时保持安静环境，清晰发音
            
            ---
            
            ### 📞 技术支持
            
            - **项目地址**: GitHub / ModelScope
            - **问题反馈**: 提交 Issue
            - **技术文档**: 查看 `docs/` 目录
            
            ---
            
            🦆 **麻鸭语音助手** - 让对话更智能，更自然！
            """)
        
        # 页脚
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; padding: 1em;">
            🦆 麻鸭语音助手 v1.0 | 基于 SenseVoice + CAM++ + Qwen2.5 + Edge TTS<br>
            Powered by ModelScope & Gradio | Made with ❤️
        </div>
        """)
    
    return demo

# ========== 主函数 ==========

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="麻鸭语音助手 Web UI")
    parser.add_argument("--port", type=int, default=7860, help="端口号")
    parser.add_argument("--share", action="store_true", help="生成公网链接")
    parser.add_argument("--server-name", type=str, default="0.0.0.0", help="服务器地址")
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════╗
    ║     🦆 麻鸭语音助手 Web UI           ║
    ║   Maya Voice Assistant v1.0          ║
    ╚═══════════════════════════════════════╝
    """)
    
    demo = create_ui()
    
    # 启用队列以支持 Progress 功能
    demo.queue(concurrency_count=3, max_size=10)
    
    demo.launch(
        server_name=args.server_name,
        server_port=args.port,
        share=args.share,
        favicon_path=None,
        show_error=True
    )

