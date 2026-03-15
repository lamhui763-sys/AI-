# GitHub 上传指南

## 步骤1：安装Git

如果您的电脑上还没有安装Git，请按照以下步骤安装：

### 方法1：使用Git官方网站
1. 访问 https://git-scm.com/download/win
2. 下载Git for Windows安装程序
3. 运行安装程序，使用默认设置即可

### 方法2：使用winget（如果可用）
在命令提示符中运行：
```cmd
winget install --id Git.Git -e --source winget
```

### 验证安装
安装完成后，打开新的命令提示符并运行：
```cmd
git --version
```
应该显示Git版本信息。

## 步骤2：准备上传的文件

我已经为您准备好了需要上传的文件，并创建了`.gitignore`文件来忽略不必要的文件（如临时文件、安装脚本等）。

## 步骤3：上传代码到GitHub

### 3.1 打开命令提示符并导航到项目目录
```cmd
cd C:\Users\makai\WorkBuddy\Claw\ai-invest-tool
```

### 3.2 初始化Git仓库
```cmd
git init
```

### 3.3 添加所有文件到暂存区
```cmd
git add .
```

### 3.4 提交更改
```cmd
git commit -m "Initial commit: AI投资工具项目"
```

### 3.5 连接到GitHub远程仓库

**重要**：您提供的仓库地址 `https://github.com/lamhui763-sys/AI-` 看起来不完整。请先确认：

1. 登录到GitHub (https://github.com)
2. 创建一个新的仓库，例如命名为 `AI-invest-tool`
3. 获取完整的仓库地址，应该是：`https://github.com/lamhui763-sys/AI-invest-tool.git`

然后运行：
```cmd
git remote add origin https://github.com/lamhui763-sys/AI-invest-tool.git
```

### 3.6 推送代码到GitHub
```cmd
git branch -M main
git push -u origin main
```

## 步骤4：首次推送可能需要验证

### 情况1：使用HTTPS
如果使用HTTPS地址，GitHub可能会要求您输入用户名和密码。您可以使用：
1. **个人访问令牌**（推荐）：
   - 在GitHub设置中创建个人访问令牌
   - 使用令牌代替密码
2. **GitHub CLI**：安装GitHub CLI并使用 `gh auth login`

### 情况2：使用SSH
如果您更习惯使用SSH：
1. 生成SSH密钥：`ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 将公钥添加到GitHub账户
3. 使用SSH地址：`git@github.com:lamhui763-sys/AI-invest-tool.git`

## 项目文件说明

### 主要代码文件
- `src/` - 源代码目录
- `examples/` - 示例代码
- `tests/` - 测试文件
- `run.py` - 主运行文件
- `launcher.py` - 应用启动器
- `requirements.txt` - Python依赖

### 文档文件
- `README.md` - 项目主说明文档
- `QUICKSTART.md` - 快速开始指南
- `INSTALL_WINDOWS.md` - Windows安装指南
- `DEMO.md` - 演示说明

### 配置文件
- `config.yaml` - 配置文件

### 已忽略的文件（不会上传）
根据`.gitignore`配置，以下文件不会被上传：
- 所有`.bat`和`.ps1`安装脚本
- 所有`.txt`和`.html`说明文件
- Python缓存文件和虚拟环境
- IDE配置文件
- 临时文件

## 后续更新

上传代码后，如果您修改了代码，可以使用以下命令更新：

```cmd
git add .
git commit -m "描述您的更改"
git push
```

## 故障排除

### 错误：fatal: remote origin already exists
```cmd
git remote remove origin
git remote add origin [您的仓库地址]
```

### 错误：failed to push some refs
```cmd
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### 错误：Authentication failed
- 检查用户名和密码/令牌
- 考虑使用SSH密钥
- 使用GitHub CLI进行身份验证

## 联系支持

如果遇到问题，请检查：
1. Git是否正确安装
2. 网络连接是否正常
3. GitHub仓库地址是否正确
4. 是否有权限推送代码到该仓库