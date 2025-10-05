# 环境配置

1. 创建虚拟环境

```
    conda create -n chatAudio python=3.10
    conda activate chatAudio
```

2. 安装pytorch+cuda版本，本地测试2.0以上版本均可，这里安装torch=2.3.1+cuda11.8

```
    pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

    其它适合自己电脑的torch+cuda版本可在torch官网查找
    https://pytorch.org/get-started/previous-versions/
```

3. 简易版本安装，不使用cosyvoice时依赖项较少

```
    pip install edge-tts==6.1.17 funasr==1.1.12 ffmpeg==1.4 opencv-python==4.10.0.84 transformers==4.45.2 webrtcvad==2.0.10 qwen-vl-utils==0.0.8 pygame==2.6.1 langid==1.1.6 langdetect==1.0.9 accelerate==0.33.0 PyAudio==0.2.14
```

至此，不调用cosyvoice作为合成的交互可成功调用了。

4. cosyvoice依赖库

```
    conda install -c conda-forge pynini=2.1.6
    pip install WeTextProcessing --no-deps
```

5. cosyvoice其它依赖项安装（如遇到权限问题导致安装失败，以管理员形式打开终端）

```
   pip install HyperPyYAML==1.2.2 modelscope==1.15.0 onnxruntime==1.19.2 openai-whisper==20231117 importlib_resources==6.4.5 sounddevice==0.5.1 matcha-tts==0.0.7.0

    可执行验证：
    python 15.1_SenceVoice_kws_CAM++.py
```

## 结合AI前端基础版本

```bash
sh start_app.sh
```

## 新增声纹识别功能

设置固定声纹注册语音存储目录，如目录为空则自动进入声纹注册模式。默认注册语音时长大于3秒，可自定义，一般而言时长越长，声纹效果越稳定。
声纹模型采用阿里开源的CAM++，其采用3D-Speaker中文数据训练，符合中文对话需求

## 新增自由定义唤醒词功能

使用SenceVoice的语音识别能力实现，将语音识别的汉字转为拼音进行匹配。将唤醒词/指令词设置为中文对应拼音，可自由定制。15.0_SenceVoice_kws_CAM++.py中默认为'ni hao xiao qian'，15.1_SenceVoice_kws_CAM++.py中默认为'zhan qi lai'[暗影君王实在太cool辣]

## 新增对话历史内容记忆功能

通过建立user、system历史队列实现。开启新一轮对话时，首先获取历史记忆，而后拼接新的输入指令。可自由定义最大历史长度，默认为512。
