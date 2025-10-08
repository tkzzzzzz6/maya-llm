# 🔒 HTTPS + WSS 完整配置指南

## 📋 目录

1. [为什么需要 HTTPS/WSS](#为什么需要-httpswss)
2. [快速开始](#快速开始)
3. [自签名证书（开发环境）](#自签名证书开发环境)
4. [Let's Encrypt（生产环境）](#lets-encrypt生产环境)
5. [客户端配置](#客户端配置)
6. [故障排除](#故障排除)

---

## 为什么需要 HTTPS/WSS？

### 🔐 安全性

- **数据加密**：防止中间人攻击
- **身份验证**：确认服务器身份
- **数据完整性**：防止数据被篡改

### 🌐 浏览器要求

现代浏览器对某些功能有严格要求：

| 功能 | HTTP | HTTPS |
|------|------|-------|
| **麦克风访问** | ❌ 仅限 localhost | ✅ 全部域名 |
| **摄像头访问** | ❌ 仅限 localhost | ✅ 全部域名 |
| **WebSocket** | ⚠️ 不推荐 | ✅ 推荐 WSS |
| **服务工作线程** | ❌ | ✅ |
| **地理定位** | ❌ | ✅ |

**重要：** 如果您的前端不在 `localhost`，必须使用 HTTPS + WSS！

---

## 快速开始

### 📦 安装依赖

```bash
# 安装 SSL 证书生成工具
pip install pyOpenSSL

# 或使用 requirements
pip install -r ssl_requirements.txt
```

### 🚀 一键配置

**Windows:**
```bash
cd ssl_config
setup_ssl.bat
```

**Linux/macOS:**
```bash
cd ssl_config
chmod +x setup_ssl.sh
./setup_ssl.sh
```

### ▶️ 启动服务

**YAYA 语音服务 (HTTPS):**
```bash
python audio_chat_server/yaya_voice_server_https.py
```
访问: `https://localhost:5443`

**Qwen-Omni 视频服务 (HTTPS + WSS):**
```bash
python vedio_chat_server/qwen_vedio_realtime_wss.py
```
WebSocket: `wss://localhost:5444/ws/video`

---

## 自签名证书（开发环境）

### 方法一：使用配置脚本（推荐）

运行 `setup_ssl.bat` 或 `setup_ssl.sh`，选择选项 1。

### 方法二：手动生成

```bash
python ssl_config/generate_ssl_cert.py --domain localhost --days 365
```

### 方法三：自定义域名

```bash
# 为特定域名生成证书
python ssl_config/generate_ssl_cert.py --domain yourdomain.com --days 365

# 为 IP 地址生成证书
python ssl_config/generate_ssl_cert.py --domain 192.168.1.100 --days 365
```

### 📁 证书位置

```
ssl_config/
└── certs/
    ├── server.crt  # 证书文件
    └── server.key  # 私钥文件
```

### 🔧 自定义证书路径

通过环境变量指定：

**Windows (cmd):**
```cmd
set SSL_CERT_PATH=C:\path\to\your\cert.crt
set SSL_KEY_PATH=C:\path\to\your\key.key
python audio_chat_server/yaya_voice_server_https.py
```

**Windows (PowerShell):**
```powershell
$env:SSL_CERT_PATH="C:\path\to\your\cert.crt"
$env:SSL_KEY_PATH="C:\path\to\your\key.key"
python audio_chat_server/yaya_voice_server_https.py
```

**Linux/macOS:**
```bash
export SSL_CERT_PATH=/path/to/your/cert.crt
export SSL_KEY_PATH=/path/to/your/key.key
python audio_chat_server/yaya_voice_server_https.py
```

### ⚠️ 浏览器信任自签名证书

#### Chrome / Edge

1. 访问 `https://localhost:5443`
2. 看到 "您的连接不是私密连接"
3. 点击 **"高级"**
4. 点击 **"继续前往 localhost (不安全)"**

#### Firefox

1. 访问 `https://localhost:5443`
2. 点击 **"高级"**
3. 点击 **"接受风险并继续"**

#### 永久信任（推荐）

**Windows:**
1. 双击 `ssl_config/certs/server.crt`
2. 点击 **"安装证书"**
3. 选择 **"本地计算机"**
4. 选择 **"将所有证书放入下列存储"**
5. 浏览选择 **"受信任的根证书颁发机构"**
6. 完成安装

**macOS:**
```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ssl_config/certs/server.crt
```

**Linux (Ubuntu):**
```bash
sudo cp ssl_config/certs/server.crt /usr/local/share/ca-certificates/maya-llm.crt
sudo update-ca-certificates
```

---

## Let's Encrypt（生产环境）

### 🌟 推荐方案：使用 Certbot

#### 安装 Certbot

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**CentOS/RHEL:**
```bash
sudo yum install certbot python3-certbot-nginx
```

**macOS:**
```bash
brew install certbot
```

#### 获取证书

```bash
# 停止现有服务（需要使用 80 端口）
sudo certbot certonly --standalone -d yourdomain.com
```

#### 证书位置

Let's Encrypt 证书通常存放在：
```
/etc/letsencrypt/live/yourdomain.com/
├── fullchain.pem  # 证书（使用这个）
└── privkey.pem    # 私钥（使用这个）
```

#### 配置服务

```bash
export SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
export SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
python audio_chat_server/yaya_voice_server_https.py
```

#### 自动续期

Let's Encrypt 证书有效期 90 天，需要定期续期：

```bash
# 测试续期
sudo certbot renew --dry-run

# 设置定时任务
sudo crontab -e

# 添加以下行（每天凌晨 2 点检查并续期）
0 2 * * * certbot renew --quiet --post-hook "systemctl restart your-service"
```

---

## 客户端配置

### JavaScript (Web)

#### HTTPS API 调用

```javascript
// STT
const formData = new FormData();
formData.append('audio', audioBlob);

const response = await fetch('https://yourdomain.com:5443/api/speech-to-text', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log('识别结果:', result.text);
```

#### WSS WebSocket 连接

```javascript
// 连接到 WSS
const ws = new WebSocket('wss://yourdomain.com:5444/ws/video');

ws.onopen = () => {
    console.log('✅ WSS 连接已建立');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'ready') {
        console.log('会话准备就绪:', data.session_id);
    }
    else if (data.type === 'text.delta') {
        console.log('AI 响应:', data.text);
    }
    else if (data.type === 'audio.delta') {
        // 播放音频
        playAudio(data.audio);
    }
};

// 发送视频帧
function sendVideoFrame(frameBase64) {
    ws.send(JSON.stringify({
        type: 'video',
        data: frameBase64
    }));
}

// 发送音频
function sendAudio(audioBase64) {
    ws.send(JSON.stringify({
        type: 'audio',
        data: audioBase64
    }));
}
```

### Python 客户端

```python
import requests
import ssl

# 忽略自签名证书警告（仅开发环境）
session = requests.Session()
session.verify = False  # 生产环境请设为证书路径

# STT
with open('audio.wav', 'rb') as f:
    files = {'audio': f}
    response = session.post(
        'https://localhost:5443/api/speech-to-text',
        files=files
    )
    print(response.json())

# WebSocket
import websocket

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://localhost:5444/ws/video")

# 发送数据
ws.send(json.dumps({
    'type': 'video',
    'data': frame_base64
}))

# 接收数据
result = json.loads(ws.recv())
print(result)
```

---

## 故障排除

### ❌ 问题 1: 证书文件不存在

**错误信息:**
```
SSL 证书文件不存在: ./ssl_config/certs/server.crt
请运行: python ssl_config/generate_ssl_cert.py
```

**解决方案:**
```bash
python ssl_config/generate_ssl_cert.py --domain localhost
```

### ❌ 问题 2: 权限不足

**错误信息:**
```
Permission denied: './ssl_config/certs/server.key'
```

**解决方案:**

**Linux/macOS:**
```bash
chmod 600 ssl_config/certs/server.key
sudo chown $USER:$USER ssl_config/certs/*
```

**Windows:** 右键文件 → 属性 → 安全 → 编辑权限

### ❌ 问题 3: 端口被占用

**错误信息:**
```
OSError: [Errno 48] Address already in use
```

**解决方案:**

**查找占用端口的进程:**
```bash
# Linux/macOS
lsof -i :5443

# Windows
netstat -ano | findstr :5443
```

**终止进程或更改端口:**
```python
# 在代码中修改端口
app.run(host='0.0.0.0', port=5445, ssl_context=ssl_context)
```

### ❌ 问题 4: 浏览器仍显示不安全

**原因:**
- 自签名证书未添加到系统信任
- 域名不匹配（证书是 localhost，访问的是 IP）

**解决方案:**
1. 重新生成匹配域名的证书
2. 按上述步骤添加证书到系统信任
3. 重启浏览器

### ❌ 问题 5: WebSocket 连接失败

**检查清单:**
- [ ] 服务是否正常运行
- [ ] 端口是否正确（5444）
- [ ] 协议是否正确（`wss://` 而非 `ws://`）
- [ ] 防火墙是否阻止连接

**测试连接:**
```bash
# 使用 wscat 测试
npm install -g wscat
wscat -c wss://localhost:5444/ws/video
```

### ❌ 问题 6: 混合内容警告

**错误信息:**
```
Mixed Content: The page at 'https://...' was loaded over HTTPS, 
but requested an insecure resource 'http://...'.
```

**解决方案:**
确保所有资源都使用 HTTPS/WSS：
```javascript
// ❌ 错误
const ws = new WebSocket('ws://localhost:5003/ws/video');

// ✅ 正确
const ws = new WebSocket('wss://localhost:5444/ws/video');
```

---

## 环境变量总结

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ENABLE_SSL` | `true` | 启用/禁用 SSL |
| `SSL_CERT_PATH` | `./ssl_config/certs/server.crt` | 证书文件路径 |
| `SSL_KEY_PATH` | `./ssl_config/certs/server.key` | 私钥文件路径 |

### 禁用 SSL（使用 HTTP）

```bash
# Windows (cmd)
set ENABLE_SSL=false
python audio_chat_server/yaya_voice_server_https.py

# Linux/macOS
export ENABLE_SSL=false
python audio_chat_server/yaya_voice_server_https.py
```

---

## 生产环境部署建议

### 🔥 使用 Nginx 反向代理（推荐）

```nginx
# /etc/nginx/sites-available/maya-llm
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # HTTPS API
    location /api/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WSS WebSocket
    location /ws/ {
        proxy_pass http://127.0.0.1:5003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/maya-llm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 📊 优点

- ✅ 统一端口（443）
- ✅ 自动处理 SSL
- ✅ 负载均衡
- ✅ 日志记录
- ✅ 更好的性能

---

## 参考资料

- [Let's Encrypt 官网](https://letsencrypt.org/)
- [Certbot 文档](https://certbot.eff.org/)
- [MDN Web 安全](https://developer.mozilla.org/zh-CN/docs/Web/Security)
- [WebSocket Secure (WSS)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

**🎉 现在您的服务已经支持 HTTPS 和 WSS，可以安全地部署到生产环境了！**

