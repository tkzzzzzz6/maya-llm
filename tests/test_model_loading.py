#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型加载测试脚本
用于诊断模型加载问题
"""

import sys
import traceback

print("=" * 60)
print("🔍 麻鸭语音助手 - 模型加载测试")
print("=" * 60)

# 测试 1: 导入基础模块
print("\n[1/6] 测试基础模块导入...")
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
    print(f"   CUDA 可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA 版本: {torch.version.cuda}")
        print(f"   GPU 数量: {torch.cuda.device_count()}")
except Exception as e:
    print(f"❌ PyTorch 导入失败: {e}")
    sys.exit(1)

try:
    import gradio as gr
    print(f"✅ Gradio {gr.__version__}")
except Exception as e:
    print(f"❌ Gradio 导入失败: {e}")

try:
    from transformers import __version__ as transformers_version
    print(f"✅ Transformers {transformers_version}")
except Exception as e:
    print(f"❌ Transformers 导入失败: {e}")

try:
    from modelscope import __version__ as modelscope_version
    print(f"✅ ModelScope {modelscope_version}")
except Exception as e:
    print(f"❌ ModelScope 导入失败: {e}")

# 测试 2: 导入项目配置
print("\n[2/6] 测试项目配置...")
try:
    from src.backend.config import MODEL_CONFIG, DEFAULT_SETTINGS
    print("✅ 配置文件加载成功")
    print(f"   ASR 模型: {MODEL_CONFIG['asr']['model_id']}")
    print(f"   LLM 模型: {MODEL_CONFIG['llm']['model_id']}")
    print(f"   SV 模型: {MODEL_CONFIG['sv']['model_id']}")
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 测试 3: 测试 ASR 模型
print("\n[3/6] 测试 ASR 模型加载...")
try:
    from funasr import AutoModel
    print("   正在加载 SenseVoice...")
    asr_model = AutoModel(
        model=MODEL_CONFIG["asr"]["model_id"],
        trust_remote_code=MODEL_CONFIG["asr"]["trust_remote_code"]
    )
    print("✅ ASR 模型加载成功")
except Exception as e:
    print(f"❌ ASR 模型加载失败: {e}")
    traceback.print_exc()

# 测试 4: 测试 SV 模型
print("\n[4/6] 测试声纹验证模型加载...")
try:
    from modelscope.pipelines import pipeline
    print("   正在加载 CAM++...")
    sv_pipeline = pipeline(
        task=MODEL_CONFIG["sv"]["task"],
        model=MODEL_CONFIG["sv"]["model_id"],
        model_revision=MODEL_CONFIG["sv"]["model_revision"]
    )
    print("✅ SV 模型加载成功")
except Exception as e:
    print(f"❌ SV 模型加载失败: {e}")
    traceback.print_exc()

# 测试 5: 测试 LLM 模型
print("\n[5/6] 测试大语言模型加载...")
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from modelscope import snapshot_download

    print("   正在下载/定位模型...")
    qwen_local_dir = snapshot_download(
        model_id=MODEL_CONFIG["llm"]["model_id"]
    )
    print(f"   模型路径: {qwen_local_dir}")

    print("   正在加载 Qwen2.5...")
    llm_model = AutoModelForCausalLM.from_pretrained(
        qwen_local_dir,
        torch_dtype=MODEL_CONFIG["llm"]["torch_dtype"],
        device_map=MODEL_CONFIG["llm"]["device_map"],
        trust_remote_code=MODEL_CONFIG["llm"]["trust_remote_code"]
    )

    llm_tokenizer = AutoTokenizer.from_pretrained(
        qwen_local_dir,
        trust_remote_code=MODEL_CONFIG["llm"]["trust_remote_code"]
    )

    print("✅ LLM 模型加载成功")
    print(f"   模型参数量: {llm_model.num_parameters() / 1e9:.2f}B")

except Exception as e:
    print(f"❌ LLM 模型加载失败: {e}")
    traceback.print_exc()

# 测试 6: 测试工具函数
print("\n[6/6] 测试辅助工具...")
try:
    from src.backend.audio_utils import check_wake_word

    # 测试唤醒词检测
    test_cases = [
        ("yaya你好", "yaya", True),
        ("你好", "yaya", False),
        ("站起来，请问", "站起来", True),
    ]

    all_pass = True
    for text, wake_word, expected in test_cases:
        result = check_wake_word(text, wake_word)
        status = "✅" if result == expected else "❌"
        print(f"   {status} 唤醒词测试: '{text}' -> {result} (期望 {expected})")
        if result != expected:
            all_pass = False

    if all_pass:
        print("✅ 工具函数测试通过")
    else:
        print("⚠️  部分工具函数测试失败")

except Exception as e:
    print(f"❌ 工具函数测试失败: {e}")
    traceback.print_exc()

# 总结
print("\n" + "=" * 60)
print("📊 测试总结")
print("=" * 60)
print("""
如果所有测试都通过，说明环境配置正确。
如果某个测试失败，请查看上面的错误信息。

常见问题：
1. 模型下载失败 → 检查网络连接和 HF_ENDPOINT 设置
2. CUDA 错误 → 检查 PyTorch 和 CUDA 版本是否匹配
3. 内存不足 → 考虑使用更小的模型或量化版本

如需帮助，请将上述完整输出发送给开发者。
""")
print("=" * 60)
