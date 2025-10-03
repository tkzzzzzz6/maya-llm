import cv2
import pyaudio
import wave
import threading
import numpy as np
import time
from queue import Queue
import webrtcvad
import os
import threading
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from funasr import AutoModel
import pygame
import edge_tts
import asyncio
from time import sleep

import langid
from langdetect import detect
from modelscope import snapshot_download

# --- 配置huggingFace国内镜像 ---
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 参数设置
AUDIO_RATE = 16000        # 音频采样率
AUDIO_CHANNELS = 1        # 单声道
CHUNK = 1024              # 音频块大小
VAD_MODE = 3              # VAD 模式 (0-3, 数字越大越敏感)
OUTPUT_DIR = "./output"   # 输出目录
NO_SPEECH_THRESHOLD = 1   # 无效语音阈值，单位：秒
audio_file_count = 0

# ========== 摄像头配置 ==========
# 摄像头模式选择：
# "default"  - 使用默认摄像头（设备索引 0）
# "index"    - 使用指定索引的摄像头（设置 CAMERA_INDEX）
# "ip"       - 使用IP摄像头/手机摄像头（设置 CAMERA_URL）
# "file"     - 使用视频文件进行测试（设置 VIDEO_FILE_PATH）
# "disable"  - 禁用视频功能（仅使用音频）
CAMERA_MODE = "default"

# 摄像头索引（当 CAMERA_MODE="index" 时使用）
# 如果有多个摄像头，可以尝试 1, 2, 3 等
CAMERA_INDEX = 0

# IP摄像头URL（当 CAMERA_MODE="ip" 时使用）
# iPhone/iPad 使用 iVCam、DroidCam、EpocCam 等软件后会提供一个URL
# 示例：
#   - "http://192.168.1.100:8080/video"  (DroidCam/IP Webcam)
#   - "http://192.168.1.100:4747/video"  (DroidCam默认)
#   - rtsp://192.168.1.100:8554/live     (RTSP流)
CAMERA_URL = "http://192.168.1.100:8080/video"

# 视频文件路径（当 CAMERA_MODE="file" 时使用，用于测试）
VIDEO_FILE_PATH = "./test_video.mp4"
# ================================

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 队列用于音频和视频同步缓存
audio_queue = Queue()
video_queue = Queue()

# 全局变量
last_active_time = time.time()
recording_active = True
segments_to_save = []
saved_intervals = []
last_vad_end_time = 0  # 上次保存的 VAD 有效段结束时间

# 初始化 WebRTC VAD
vad = webrtcvad.Vad()
vad.set_mode(VAD_MODE)

# 音频录制线程
def audio_recorder():
    global audio_queue, recording_active, last_active_time, segments_to_save, last_vad_end_time
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=AUDIO_CHANNELS,
                    rate=AUDIO_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    audio_buffer = []
    print("音频录制已开始")
    
    while recording_active:
        data = stream.read(CHUNK)
        audio_buffer.append(data)
        
        # 每 0.5 秒检测一次 VAD
        if len(audio_buffer) * CHUNK / AUDIO_RATE >= 0.5:
            # 拼接音频数据并检测 VAD
            raw_audio = b''.join(audio_buffer)
            vad_result = check_vad_activity(raw_audio)
            
            if vad_result:
                print("检测到语音活动")
                last_active_time = time.time()
                segments_to_save.append((raw_audio, time.time()))
            else:
                print("静音中...")
            
            audio_buffer = []  # 清空缓冲区
        
        # 检查无效语音时间
        if time.time() - last_active_time > NO_SPEECH_THRESHOLD:
            # 检查是否需要保存
            if segments_to_save and segments_to_save[-1][1] > last_vad_end_time:
                save_audio_video()
                last_active_time = time.time()
            else:
                pass
                # print("无新增语音段，跳过保存")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# 视频录制线程
def video_recorder():
    global video_queue, recording_active, CAMERA_MODE
    
    # 根据配置选择摄像头源
    if CAMERA_MODE == "disable":
        print("视频功能已禁用，仅使用音频模式")
        return
    
    # 初始化摄像头
    cap = None
    if CAMERA_MODE == "default":
        cap = cv2.VideoCapture(0)
        print("使用默认摄像头（索引 0）")
    elif CAMERA_MODE == "index":
        cap = cv2.VideoCapture(CAMERA_INDEX)
        print(f"使用摄像头索引: {CAMERA_INDEX}")
    elif CAMERA_MODE == "ip":
        cap = cv2.VideoCapture(CAMERA_URL)
        print(f"使用IP摄像头: {CAMERA_URL}")
        print("提示：请确保手机摄像头APP已启动并在同一网络")
    elif CAMERA_MODE == "file":
        cap = cv2.VideoCapture(VIDEO_FILE_PATH)
        print(f"使用视频文件: {VIDEO_FILE_PATH}")
    else:
        print(f"错误：未知的摄像头模式 '{CAMERA_MODE}'")
        return
    
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print(f"错误：无法打开摄像头或视频源")
        if CAMERA_MODE == "ip":
            print("请检查：")
            print("  1. 手机和电脑在同一WiFi网络")
            print("  2. 手机APP已启动（如DroidCam、iVCam等）")
            print("  3. URL地址正确")
            print("  4. 防火墙未阻止连接")
        return
    
    print("✓ 视频录制已开始")
    frame_count = 0
    error_count = 0
    max_errors = 30  # 最大连续错误次数
    
    while recording_active:
        ret, frame = cap.read()
        if ret:
            error_count = 0  # 重置错误计数
            frame_count += 1
            video_queue.put((frame, time.time()))
            
            # 实时显示摄像头画面
            cv2.imshow("Real Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 Q 键退出
                print("检测到按键 'q'，准备退出...")
                break
        else:
            error_count += 1
            if error_count >= max_errors:
                print(f"错误：连续{max_errors}次无法获取画面，停止视频录制")
                break
            if error_count == 1:
                print("警告：无法获取摄像头画面")
            time.sleep(0.1)  # 出错时稍作延迟
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"视频录制已停止（共录制 {frame_count} 帧）")

# 检测 VAD 活动
def check_vad_activity(audio_data):
    # 将音频数据分块检测，设置有效激活率rate=40%，低于此比例当作静音段
    num, rate = 0, 0.4
    step = int(AUDIO_RATE * 0.02)  # 20ms 块大小
    flag_rate = round(rate * len(audio_data) // step)

    for i in range(0, len(audio_data), step):
        chunk = audio_data[i:i + step]
        if len(chunk) == step:
            if vad.is_speech(chunk, sample_rate=AUDIO_RATE):
                num += 1

    if num > flag_rate:
        return True
    return False

# 保存音频和视频
def save_audio_video():
    pygame.mixer.init()
    global segments_to_save, video_queue, last_vad_end_time, saved_intervals

    # 全局变量，用于保存音频文件名计数
    global audio_file_count
    audio_file_count += 1
    audio_output_path = f"{OUTPUT_DIR}/audio_{audio_file_count}.wav"
    video_output_path = f"{OUTPUT_DIR}/video_{audio_file_count}.avi"

    if not segments_to_save:
        return
    
    # 用于实时打断：接收到新保存文件需求，停止当前播放的音频
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("检测到新的有效音，已停止当前音频播放")

    # 获取有效段的时间范围
    start_time = segments_to_save[0][1]
    end_time = segments_to_save[-1][1]
    
    # 检查是否与之前的片段重叠
    if saved_intervals and saved_intervals[-1][1] >= start_time:
        print("当前片段与之前片段重叠，跳过保存")
        segments_to_save.clear()
        return
    
    # 保存音频
    audio_frames = [seg[0] for seg in segments_to_save]
    wf = wave.open(audio_output_path, 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(2)  # 16-bit PCM
    wf.setframerate(AUDIO_RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()
    print(f"音频保存至 {audio_output_path}")
    
    # 保存视频
    video_frames = []
    while not video_queue.empty():
        frame, timestamp = video_queue.get()
        if start_time <= timestamp <= end_time:
            video_frames.append(frame)
    
    if video_frames:
        out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        for frame in video_frames:
            out.write(frame)
        out.release()
        print(f"视频保存至 {video_output_path}")

        # --- 直接推理会影响录制主线程，无法实现实时打断逻辑 ---
        # Inference()

        # --- 使用线程执行推理
        inference_thread = threading.Thread(target=Inference, args=(video_output_path, audio_output_path))
        inference_thread.start()
    else:
        pass
        # print("无可保存的视频帧")
    
    # 记录保存的区间
    saved_intervals.append((start_time, end_time))
    
    # 清空缓冲区
    segments_to_save.clear()

# --- 播放音频 -
def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)  # 等待音频播放结束
        print("播放完成！")
    except Exception as e:
        print(f"播放失败: {e}")
    finally:
        pygame.mixer.quit()

async def amain(TEXT, VOICE, OUTPUT_FILE) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

# -------------- Load QWen2-VL Model ------------
# 使用 ModelScope 下载 Qwen2-VL 模型
print("正在加载 Qwen2-VL-2B-Instruct 模型...")
qwen_vl_model_id = "qwen/Qwen2-VL-2B-Instruct"
qwen_vl_local_dir = snapshot_download(model_id=qwen_vl_model_id)

# default: Load the model on the available device(s)
model = Qwen2VLForConditionalGeneration.from_pretrained(
    qwen_vl_local_dir,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)

# ------- 设置分辨率，降低现存占用 -------
min_pixels = 256*28*28
max_pixels = 512*28*28
processor = AutoProcessor.from_pretrained(
    qwen_vl_local_dir,
    min_pixels=min_pixels,
    max_pixels=max_pixels,
    trust_remote_code=True
)
# --------------------------------------

# -------- SenceVoice 语音识别 --模型加载-----
# 使用 ModelScope 自动下载，支持跨平台
print("正在加载 SenseVoiceSmall 模型...")
model_dir = "iic/SenseVoiceSmall"  # ModelScope自动下载
model_senceVoice = AutoModel(model=model_dir, trust_remote_code=True,)
folder_path = "./Test_QWen2_VL/"

def Inference(TEMP_VIDEO_FILE, TEMP_AUDIO_FILE):
    
    cap = cv2.VideoCapture(TEMP_VIDEO_FILE)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # --- 设定视频截取帧时间比例
    S_index = [0.2, 0.4, 0.6, 0.8]
    frame_index = [int(total_frames * i) for i in S_index]
    # 设置视频帧位置
    for idx in frame_index:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            print(f"无法读取帧索引 {idx}")
        else:
            # 保存帧
            file_path = os.path.join(folder_path, f"captured_image{idx}.jpg")  # 设置保存路径
            cv2.imwrite(file_path, frame)

    # -------- SenceVoice 推理 --start-------
    input_file = (TEMP_AUDIO_FILE)
    res = model_senceVoice.generate(
        input=input_file,
        cache={},
        language="auto", # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=False,
    )
    # prompt = res[0]['text'].split(">")[-1]
    prompt = res[0]['text'].split(">")[-1] + "，回答简短一些，保持50字以内！"
    print("ASR OUT:", prompt)
    # ---------SenceVoice 推理--end----------

    MODE_FLAG = 0
    # -------- QWen2-VL 模型推理 --------- 多图模式
    # Messages containing a images list as a video and a text query
    if not MODE_FLAG:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": [
                            f'{os.path.join(folder_path, f"captured_image{frame_index[0]}.jpg")}',
                            f'{os.path.join(folder_path, f"captured_image{frame_index[1]}.jpg")}',
                            f'{os.path.join(folder_path, f"captured_image{frame_index[2]}.jpg")}',
                            f'{os.path.join(folder_path, f"captured_image{frame_index[3]}.jpg")}',
                        ],
                        "fps": 1.0,
                    },
                    {"type": "text", "text": f"{prompt}"},
                ],
            }
        ]

    # -------- QWen2-VL 模型推理 --------- 视频模式
    else:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": f"{TEMP_VIDEO_FILE}",
                        "max_pixels": 360 * 420,
                        "fps": 1.0,
                    },
                    {"type": "text", "text": f"{prompt}"},
                ],
            }
        ]

    # Preparation for inference
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # Inference
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    print(output_text)

    # 输入文本
    text = output_text[0]
    # 语种识别 -- langid
    language, confidence = langid.classify(text)
    # 语种识别 -- langdetect -- 没做结果对应关键词映射
    # language = detect(text)

    language_speaker = {
    "ja" : "ja-JP-NanamiNeural",            # ok
    "fr" : "fr-FR-DeniseNeural",            # ok
    "es" : "ca-ES-JoanaNeural",             # ok
    "de" : "de-DE-KatjaNeural",             # ok
    "zh" : "zh-CN-XiaoyiNeural",            # ok
    "en" : "en-US-AnaNeural",               # ok
    }

    if language not in language_speaker.keys():
        used_speaker = "zh-CN-XiaoyiNeural"
    else:
        used_speaker = language_speaker[language]
        print("检测到语种：", language, "使用音色：", language_speaker[language])

    global audio_file_count
    asyncio.run(amain(text, used_speaker, os.path.join(folder_path,f"sft_{audio_file_count}.mp3")))
    play_audio(f'{folder_path}/sft_{audio_file_count}.mp3')

    # asyncio.run(amain(text, "zh-CN-YunjianNeural", os.path.join(folder_path,"sft_0.mp3")))
    # play_audio(f'{folder_path}/sft_0.mp3')

    # asyncio.run(amain(text, "zh-CN-shaanxi-XiaoniNeural", os.path.join(folder_path,"sft_0.mp3")))
    # play_audio(f'{folder_path}/sft_0.mp3')

# 主函数
if __name__ == "__main__":
    print("\n" + "="*50)
    print("多模态语音助手启动中...")
    print("="*50)
    print(f"音频模式: 开启")
    print(f"视频模式: {'禁用' if CAMERA_MODE == 'disable' else CAMERA_MODE.upper()}")
    if CAMERA_MODE == "ip":
        print(f"摄像头URL: {CAMERA_URL}")
    print("="*50 + "\n")
    
    try:
        # 启动音频录制线程
        audio_thread = threading.Thread(target=audio_recorder)
        audio_thread.start()
        
        # 根据配置决定是否启动视频线程
        video_thread = None
        if CAMERA_MODE != "disable":
            video_thread = threading.Thread(target=video_recorder)
            video_thread.start()
        else:
            print("提示：视频功能已禁用，将仅使用音频进行纯语音对话")
        
        print("\n按 Ctrl+C 停止录制")
        print("如果开启了摄像头窗口，也可以按 'q' 键退出\n")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n录制停止中...")
        recording_active = False
        audio_thread.join()
        if video_thread is not None:
            video_thread.join()
        print("录制已停止")
