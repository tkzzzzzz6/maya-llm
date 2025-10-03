# 测试文件目录

本目录包含项目的各种测试和实验性脚本。

## 文件说明

### 录音和音频测试
- **5_pyttsx3_test.py** - pyttsx3 TTS引擎测试
- **2_record_test.py** - 基础录音功能测试（注：此文件可能已移动或删除）

### 音视频录制测试
- **7.1_test_record_AV.py** - 音视频同步录制测试
- **7.2_test_record_QWen2_VL_AV.py** - QWen2-VL模型结合音视频录制测试
- **7.3_test_record_QWen2_VL_AV_TTS.py** - QWen2-VL模型结合音视频录制和TTS的完整测试

### 声纹识别测试
- **9.1_test_cam++.py** - CAM++声纹识别模型测试（使用3D-Speaker数据）

## 注意事项

1. **路径配置**: 测试文件中的输出路径已调整为相对于项目根目录（使用`../`前缀）
2. **模型路径**: 某些测试文件中包含硬编码的模型路径，运行前需要根据您的环境进行修改
3. **依赖项**: 运行测试前请确保已安装 `requirements.txt` 中的所有依赖

## 运行方式

从项目根目录运行测试：
```bash
cd maya-llm
python tests/文件名.py
```

或从tests目录运行：
```bash
cd maya-llm/tests
python 文件名.py
```

