# Fish Audio Python MCP 服务

这是一个使用 Fish Audio API 实现的文字转语音 MCP 服务。通过这个服务，您可以将文本转换为自然的人声，支持多种配置选项。

## 功能特点

- 基本文字转语音：将任意文本转换为自然人声
- 高级文字转语音：支持自定义音频格式、比特率等参数
- 兼容 MCP 协议：可与支持 MCP 的应用无缝集成

## 安装依赖

```bash
pip install -r requirements.txt
```

或使用 Python 包管理工具安装：

```bash
pip install fish-audio-sdk mcp python-dotenv
```

## 配置

在项目根目录创建 `.env` 文件，包含以下内容：

```
API_KEY=your_fish_audio_api_key
MODEL_ID=your_fish_audio_model_id
```

您需要替换为您的 Fish Audio API 密钥和模型 ID。

## 使用方法

### 启动服务

```bash
python app.py
```

或使用 MCP CLI 工具：

```bash
mcp run --file app.py
```

### 运行示例

```bash
python example.py
```

### 使用 MCP 客户端调用服务

```python
# 示例代码
from mcp.client import MCPClient

client = MCPClient("subprocess://python app.py")
result = client.call("text_to_speech", {"text": "你好，世界！"})
print(result)  # 打印生成的音频文件路径
```

## API 功能说明

### text_to_speech

基本文字转语音功能。

参数：
- `text`: 要转换为语音的文本
- `output_path`（可选）: 输出文件路径，如果不提供，将创建临时文件

返回：生成的音频文件路径

### advanced_text_to_speech

高级文字转语音功能，支持更多配置选项。

参数：
- `text`: 要转换为语音的文本
- `output_path`（可选）: 输出文件路径，如果不提供，将创建临时文件
- `format`: 输出音频格式 (mp3, wav, pcm)，默认为 mp3
- `mp3_bitrate`: MP3 比特率 (64, 128, 192 kbps)，默认为 128
- `chunk_length`: 分块长度 (100-300)，默认为 200
- `normalize`: 是否对文本进行标准化处理，默认为 True
- `latency`: 延迟模式 (normal, balanced)，默认为 normal

返回：生成的音频文件路径

### get_model_info

获取当前使用的模型信息。

返回：包含模型 ID 和 API 密钥前缀的字典

### get_available_models

获取可用的 Fish Audio 模型列表。

返回：可用模型信息列表

## 许可证

MIT
