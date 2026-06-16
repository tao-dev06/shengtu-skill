# JOJO Code 生图 Skill

这是一个用于 JOJO Code / Codex 的图片生成 skill。它通过 OpenAI 兼容接口调用 JOJO Code 生图服务，支持输入图片描述、尺寸和输出文件名，并把生成结果保存为本地图片文件。

> 安全提醒：不要把真实 API Key 写进 README、截图、公开仓库或任何可提交文件。真实 Key 只应放在本地环境变量或私有 `.env.local` 中。

## 功能特性

- 使用 OpenAI 兼容接口：`https://api2.jojocode.com/v1`
- 默认图片模型：`gpt-image-2`
- 支持自定义图片描述：`--prompt`
- 支持自定义尺寸：`--size`
- 支持自定义输出文件名：`--output`
- 生成成功后打印本地绝对保存路径
- 自动创建输出目录
- 支持从环境变量或本地 `.env.local` 读取 `JOJO_API_KEY`

## 目录结构

```text
.
├── jojocode-imagegen/
│   ├── SKILL.md
│   ├── .env.example
│   ├── agents/
│   │   └── openai.yaml
│   └── scripts/
│       └── generate_image.py
├── outputs/
│   └── pet-dog.png
├── .gitignore
└── README.md
```

- `jojocode-imagegen/SKILL.md`：skill 的使用说明和触发描述。
- `jojocode-imagegen/scripts/generate_image.py`：实际调用 JOJO Code API 的生成脚本。
- `jojocode-imagegen/.env.example`：环境变量示例，只包含占位符。
- `outputs/pet-dog.png`：示例生成图片。

## 安装 Skill

把 `jojocode-imagegen` 文件夹复制到本机 Codex skills 目录：

```powershell
Copy-Item -Recurse -Force .\jojocode-imagegen "$env:USERPROFILE\.codex\skills\jojocode-imagegen"
```

安装后，skill 路径通常是：

```text
C:\Users\<你的用户名>\.codex\skills\jojocode-imagegen
```

## 配置 API Key

推荐使用环境变量：

```powershell
$env:JOJO_API_KEY="your_api_key_here"
```

也可以在 skill 目录中创建私有配置文件：

```powershell
Copy-Item .\jojocode-imagegen\.env.example "$env:USERPROFILE\.codex\skills\jojocode-imagegen\.env.local"
```

然后把 `.env.local` 内容改成：

```text
JOJO_API_KEY=your_api_key_here
```

请确认 `.env.local` 不会被提交到 GitHub。本仓库的 `.gitignore` 已默认忽略 `.env` 和 `.env.*`。

## 使用方式

在 skill 目录中运行：

```powershell
python scripts/generate_image.py --prompt "a cute golden retriever puppy sitting in a bright living room, soft natural light, realistic photography" --size 1024x1024 --output outputs/pet-dog.png
```

也可以使用脚本的绝对路径：

```powershell
python "$env:USERPROFILE\.codex\skills\jojocode-imagegen\scripts\generate_image.py" --prompt "a cyberpunk city at night, neon lights, cinematic style" --size 1024x1024 --output outputs/city.png
```

常用参数：

```text
--prompt  图片描述，必填
--size    图片尺寸，默认 1024x1024
--output  输出文件名或路径，必填
--model   图片模型，默认 gpt-image-2
```

生成成功后，脚本会输出类似：

```text
Saved image: C:\path\to\outputs\pet-dog.png
```

## 示例效果

![宠物狗示例](outputs/pet-dog.png)

## 常见问题

### Missing JOJO_API_KEY

说明脚本没有读取到 API Key。请检查是否已经设置环境变量 `JOJO_API_KEY`，或者是否在 skill 目录中创建了私有 `.env.local`。

### model_not_found

说明当前 Key 对应的分组没有该模型。生图 Key 通常应使用 `gpt-image-2` 或 `gpt-image-1`。

### 连接 GitHub 或 API 失败

如果本机配置了失效代理，例如 `127.0.0.1:7890`，可能会导致网络请求失败。请启动代理，或临时清除相关代理环境变量后再运行。

### 输出路径无效

请确认 `--output` 指向有效文件路径。脚本会自动创建父目录，但文件名本身仍需要合法。

## 安全检查

发布或提交前建议运行：

```powershell
$pattern = "s" + "k-"
Get-ChildItem -Recurse -File | Select-String -Pattern $pattern -SimpleMatch
```

如果命中真实 API Key，请立即移除并轮换密钥。公开仓库中只应出现占位符，例如 `your_api_key_here`。
