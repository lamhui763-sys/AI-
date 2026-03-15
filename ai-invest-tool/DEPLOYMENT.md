# 部署指南

本指南介绍如何在不同环境中部署AI投资工具。

## 📋 目录

1. [本地部署](#本地部署)
2. [云端部署](#云端部署)
3. [Docker部署](#docker部署)
4. [生产环境配置](#生产环境配置)
5. [性能优化](#性能优化)
6. [安全配置](#安全配置)
7. [监控和维护](#监控和维护)

---

## 本地部署

### Windows部署

#### 1. 环境准备

```powershell
# 安装Python
# 下载: https://www.python.org/downloads/
# 安装时勾选 "Add Python to PATH"

# 验证安装
python --version
pip --version
```

#### 2. 项目安装

```powershell
# 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置

```powershell
# 创建配置文件
copy config.example.yaml config.yaml

# 编辑配置
notepad config.yaml

# 配置API Key
set OPENAI_API_KEY=your-key-here
```

#### 4. 运行

```powershell
# Web界面
streamlit run src/ai_inv/web_dashboard.py

# 或使用Python
python main.py
```

#### 5. 创建快捷方式

创建 `start.bat`:

```batch
@echo off
call venv\Scripts\activate
streamlit run src/ai_inv/web_dashboard.py --server.port 8501
pause
```

### macOS部署

#### 1. 环境准备

```bash
# 安装Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python
brew install python3

# 验证
python3 --version
pip3 --version
```

#### 2. 项目安装

```bash
# 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置

```bash
# 创建配置文件
cp config.example.yaml config.yaml

# 编辑配置
nano config.yaml

# 配置API Key
export OPENAI_API_KEY="your-key-here"

# 添加到shell配置
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### 4. 运行

```bash
# Web界面
streamlit run src/ai_inv/web_dashboard.py

# 或使用Python
python main.py
```

#### 5. 创建服务

创建 `start.sh`:

```bash
#!/bin/bash
source venv/bin/activate
streamlit run src/ai_inv/web_dashboard.py --server.port 8501
```

```bash
# 添加执行权限
chmod +x start.sh

# 运行
./start.sh
```

### Linux部署

#### 1. 环境准备

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# 验证
python3 --version
pip3 --version
```

#### 2. 项目安装

```bash
# 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置

```bash
# 创建配置文件
cp config.example.yaml config.yaml

# 编辑配置
nano config.yaml

# 配置API Key
export OPENAI_API_KEY="your-key-here"

# 添加到shell配置
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### 4. 运行

```bash
# Web界面
streamlit run src/ai_inv/web_dashboard.py

# 或使用Python
python main.py
```

#### 5. 创建systemd服务

创建 `/etc/systemd/system/ai-invest-tool.service`:

```ini
[Unit]
Description=AI Investment Tool
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/ai-invest-tool
Environment="PATH=/path/to/ai-invest-tool/venv/bin"
ExecStart=/path/to/ai-invest-tool/venv/bin/streamlit run src/ai_inv/web_dashboard.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable ai-invest-tool
sudo systemctl start ai-invest-tool

# 查看状态
sudo systemctl status ai-invest-tool

# 查看日志
sudo journalctl -u ai-invest-tool -f
```

---

## 云端部署

### Streamlit Cloud部署

#### 1. 准备代码

```bash
# 确保项目结构正确
ai-invest-tool/
├── src/
│   └── ai_inv/
│       └── web_dashboard.py
├── requirements.txt
├── config.yaml
└── .streamlit/
    └── config.toml
```

#### 2. 创建Streamlit配置

创建 `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#4472C4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

#### 3. 推送到GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ai-invest-tool.git
git push -u origin main
```

#### 4. 部署到Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 "New app"
3. 连接GitHub仓库
4. 选择文件: `src/ai_inv/web_dashboard.py`
5. 配置环境变量:
   - `OPENAI_API_KEY`: your-api-key
6. 点击 "Deploy"

### AWS部署

#### 1. 创建EC2实例

```bash
# 使用AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxx
```

#### 2. 连接到实例

```bash
ssh -i your-key-pair.pem ubuntu@your-instance-ip
```

#### 3. 安装环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和依赖
sudo apt install python3 python3-pip python3-venv nginx -y

# 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 4. 配置Nginx

创建 `/etc/nginx/sites-available/ai-invest-tool`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/ai-invest-tool /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

#### 5. 配置SSL（使用Let's Encrypt）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### Docker部署

详见[Docker部署](#docker部署)章节。

---

## Docker部署

### 创建Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY src/ ./src/
COPY config.yaml .

# 创建输出目录
RUN mkdir -p output/excel output/reports

# 暴露端口
EXPOSE 8501

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["streamlit", "run", "src/ai_inv/web_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 创建docker-compose.yml

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ai-invest-tool:
    build: .
    container_name: ai-invest-tool
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}
    volumes:
      - ./output:/app/output
      - ./config.yaml:/app/config.yaml
      - ./cache:/app/cache
    restart: unless-stopped
```

### 创建.env文件

创建 `.env`:

```bash
OPENAI_API_KEY=your-openai-key-here
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key-here
```

### 构建和运行

```bash
# 构建镜像
docker-compose build

# 运行容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

### Docker命令

```bash
# 构建镜像
docker build -t ai-invest-tool .

# 运行容器
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -v $(pwd)/output:/app/output \
  ai-invest-tool

# 查看日志
docker logs -f <container-id>

# 进入容器
docker exec -it <container-id> /bin/bash

# 停止容器
docker stop <container-id>

# 删除容器
docker rm <container-id>
```

---

## 生产环境配置

### 配置优化

编辑 `config.yaml`:

```yaml
# 数据源配置
data:
  source: "yfinance"
  cache_enabled: true
  cache_ttl: 3600  # 缓存1小时
  cache_dir: "cache"

# 性能配置
performance:
  max_workers: 4
  batch_size: 100
  timeout: 30

# 安全配置
security:
  rate_limit: 100  # 每分钟请求数
  max_data_rows: 10000
  enable_auth: false

# 日志配置
logging:
  level: "INFO"
  file: "logs/app.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5
```

### 环境变量

创建 `.env.production`:

```bash
# API Keys
OPENAI_API_KEY=your-production-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key

# 应用配置
APP_ENV=production
APP_PORT=8501
APP_HOST=0.0.0.0

# 数据库（如果使用）
DATABASE_URL=postgresql://user:password@localhost:5432/ai_invest

# Redis（用于缓存）
REDIS_URL=redis://localhost:6379/0

# 日志
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai-invest-tool/app.log
```

---

## 性能优化

### 数据缓存

```python
# 使用Redis缓存
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_data(key):
    data = redis_client.get(key)
    if data:
        return pickle.loads(data)
    return None

def set_cached_data(key, data, ttl=3600):
    redis_client.setex(key, ttl, pickle.dumps(data))
```

### 数据库优化

```python
# 使用SQLAlchemy连接池
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)
```

### 异步处理

```python
# 使用Celery进行异步任务
from celery import Celery

app = Celery('ai_invest', broker='redis://localhost:6379/0')

@app.task
def async_analyze_stock(symbol):
    # 耗时的分析任务
    return analyze_stock(symbol)
```

---

## 安全配置

### API Key管理

```python
# 使用环境变量
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
```

### 速率限制

```python
from functools import wraps
import time

def rate_limit(max_calls=100, period=60):
    def decorator(f):
        calls = {}
        @wraps(f)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = args[0]  # 使用用户标识
            if key in calls:
                calls[key] = [c for c in calls[key] if now - c < period]
            if len(calls.get(key, [])) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.setdefault(key, []).append(now)
            return f(*args, **kwargs)
        return wrapper
    return decorator
```

### 数据加密

```python
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 加密
encrypted_data = cipher_suite.encrypt(data.encode())

# 解密
decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
```

---

## 监控和维护

### 日志监控

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 文件处理器
handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)
```

### 健康检查

```python
def health_check():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'api_keys': check_api_keys()
    }
    return all(checks.values()), checks

def check_database():
    try:
        # 检查数据库连接
        return True
    except:
        return False

def check_redis():
    try:
        redis_client.ping()
        return True
    except:
        return False
```

### 备份策略

```bash
# 数据库备份
pg_dump -U username dbname > backup.sql

# 数据备份
tar -czf backup_$(date +%Y%m%d).tar.gz output/ cache/

# 自动备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump -U username dbname > backup/db_$DATE.sql
tar -czf backup/data_$DATE.tar.gz output/ cache/
find backup/ -name "*.sql" -mtime +7 -delete
find backup/ -name "*.tar.gz" -mtime +7 -delete
```

### 自动更新

```bash
#!/bin/bash
# update.sh

# 拉取最新代码
git pull origin main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 重启服务
sudo systemctl restart ai-invest-tool
```

### 监控工具

- **Prometheus** - 指标收集
- **Grafana** - 可视化监控
- **Sentry** - 错误追踪
- **Uptime Robot** - 可用性监控

---

## 故障排除

### 常见问题

**问题: 内存溢出**

```bash
# 解决方案
# 1. 增加swap空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 2. 限制数据量
config.yaml:
  max_data_rows: 5000
```

**问题: API请求失败**

```bash
# 解决方案
# 1. 检查网络连接
ping api.openai.com

# 2. 检查API Key
echo $OPENAI_API_KEY

# 3. 使用备用数据源
config.yaml:
  data:
    source: "alpha_vantage"
```

**问题: 性能缓慢**

```bash
# 解决方案
# 1. 启用缓存
config.yaml:
  data:
    cache_enabled: true

# 2. 使用更快的机器
# 3. 优化数据库查询
# 4. 使用CDN
```

---

## 总结

部署AI投资工具的关键步骤：

1. ✅ 选择合适的部署环境（本地/云端/Docker）
2. ✅ 配置环境和依赖
3. ✅ 设置安全和监控
4. ✅ 优化性能
5. ✅ 建立备份和恢复机制

祝您部署顺利！🚀
