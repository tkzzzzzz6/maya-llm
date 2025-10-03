## 改进方案（优先级与预估收益）

本方案围绕三条主线：实时性、鲁棒性与可扩展性。结合现有脚本实现与依赖，给出工程化落地建议。

### 1. 实时性优化

- 降低端到端时延（高）
  - 将 `webrtcvad` 0.5s 窗口与 40% 激活率改为自适应门限；缩短检测窗口到 0.3s 并引入滑窗重叠，减少迟滞。
  - 合成端切换到流式接口：
    - edge-tts：采用分句流式播放，前端边播边合成；
    - CosyVoice：启用 `stream=True` 的分块推理与播放（参考 `cosyvoice.inference_sft` 的流式模式），改造 `play_audio` 支持流数据队列。
  - Qwen 端使用 KV Cache、`max_new_tokens` 动态截断，基于用户语速自适应。

- 设备与解码加速（中）
  - 固定采样率 16k，减少重采样开销；
  - Qwen2-VL 端下调 `max_pixels`、裁剪视频帧大小至 480p；
  - 使用 `bitsandbytes` 或 GPTQ 量化小模型，进一步降低显存占用。

### 2. 识别与理解鲁棒性

- VAD/ASR 增强（高）
  - 引入模型级 VAD（如 Silero VAD）对强噪音场景提升显著；
  - 加入降噪前处理（RNNoise/soxr）并在静音时自动门限提升，避免误触发。

- 指令/唤醒策略（中）
  - 统一唤醒词与命令词配置到 `config.yaml`，使用拼音匹配 + 置信度；
  - 对多说话人场景叠加声纹约束（已有 CAM++），过滤非目标说话人触发。

### 3. TTS 质量与稳定性

- edge-tts 发音人自动选择（中）
  - 将 `langid` 与 `langdetect` 融合，若冲突则回退中文；
  - 为多语种句子分句后逐句选择最优发音人，减少语速/语调突变。

- CosyVoice 流式/并发（高）
  - FastAPI 服务端支持多并发（`--max_conc`），前端以 HTTP chunked 播放；
  - 增加健康检查与负载监控（Prometheus 指标已在依赖中，可集成）。

### 4. 记忆与对话管理

- 历史记忆（中）
  - 对 `15.1_SenceVoice_kws_CAM++.py` 的队列记忆策略增加“主题窗口”与“摘要窗口”，保持近期细节与长期摘要并行。

- 打断与重入（高）
  - 通过全局播放控制信号，在检测到新片段时打断当前播放与生成（现有 `pygame.mixer.music.stop()` 已具备雏形），同时中断 LLM/TTS 生成，保障即时响应。

### 5. 多模态路径

- Qwen2-VL 优化（中）
  - 动态帧采样：根据片段时长与画面变化（SSIM/光流）自适应选择关键帧；
  - 统一帧缓存与时间码，避免音视频边界不一致带来语义偏差。

### 6. 工程化与可维护性

- 配置化/模块化（高）
  - 新增 `configs/default.yaml`：包含 ASR/LLM/TTS 选择、模型路径、VAD 参数、设备策略；
  - 抽离公共模块：`audio_io.py`、`vad.py`、`llm.py`、`tts.py`、`pipeline.py`，脚本入口仅保留参数解析与启动逻辑。

- 日志与可观测性（中）
  - 统一使用 `logging`，区分 INFO/DEBUG；
  - FastAPI 接入 Prometheus（依赖已存在），导出时延、QPS、失败率、显存利用等指标。

- 依赖与环境（中）

  - 精简 `requirements.txt` 的重复/冲突版本（如同时存在 2.3.1 与 2.5.1 的 torch 组合），按“实时最小集”和“全功能集”拆分 `requirements-min.txt` 与 `requirements-full.txt`；
  - Windows/WSL 下为 `PyAudio` 提供轮子或文档说明（管理员终端/PortAudio）。

### 7. 测试与发布

- 回归用例（中）
  - 构建最小音频样本（静音/噪声/短句/长句/多语句），校验端到端延迟与正确性；
  - 多模态场景：提供小视频样例与图像列表样例，验证帧采样策略。

- Docker 化（中）
  - 参考 `runtime/python/Dockerfile` 模板，构建 `fastapi` 与 `grpc` 两类镜像；
  - 提供 `compose.yaml` 一键起服务（含 GPU 透传与端口映射）。

### 8. 路线图（建议）

1. 短期（1-2 周）：配置化改造、VAD 自适应、edge-tts 分句流式、CosyVoice 服务化文档化；
2. 中期（3-5 周）：模块化重构、Prometheus 指标、Docker 化、量化/蒸馏小模型；
3. 长期（>2 月）：端侧部署（RNNoise/Silero VAD + 小参数 Qwen）、多说话人分离、鲁棒性评测集搭建。



