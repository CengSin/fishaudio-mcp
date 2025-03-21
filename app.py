#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
from pathlib import Path
from typing import Optional, Literal

from dotenv import load_dotenv
from fish_audio_sdk import Session, TTSRequest
from mcp.server.fastmcp import FastMCP

# 加载环境变量
load_dotenv()

# 获取 API Key 和 Model ID
API_KEY = os.getenv("API_KEY")
MODEL_ID = os.getenv("MODEL_ID")

# 创建 Fish Audio 会话
session = Session(API_KEY)

# 创建 MCP 服务
mcp = FastMCP("Fish Audio TTS")

@mcp.tool()
def text_to_speech(text: str, output_path: Optional[str] = None) -> str:
    """
    将文本转换为语音
    
    Args:
        text: 要转换为语音的文本
        output_path: 输出文件路径，如果不提供，将创建临时文件
        
    Returns:
        生成的音频文件路径
    """
    if not text:
        return "文本不能为空"
    
    # 如果未提供输出路径，创建临时文件
    if not output_path:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"tts_output_{hash(text)}.mp3")
    
    # 确保目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 调用 Fish Audio API 执行文本转语音
    try:
        with open(output_path, "wb") as f:
            for chunk in session.tts(TTSRequest(
                reference_id=MODEL_ID,
                text=text
            )):
                f.write(chunk)
        
        return f"成功生成语音文件：{output_path}"
    except Exception as e:
        return f"生成语音失败：{str(e)}"

@mcp.tool()
def advanced_text_to_speech(
    text: str,
    output_path: Optional[str] = None,
    format: Literal["mp3", "wav", "pcm"] = "mp3",
    mp3_bitrate: Literal[64, 128, 192] = 128,
    chunk_length: int = 200,
    normalize: bool = True,
    latency: Literal["normal", "balanced"] = "normal"
) -> str:
    """
    高级文本转语音功能，支持更多配置选项
    
    Args:
        text: 要转换为语音的文本
        output_path: 输出文件路径，如果不提供，将创建临时文件
        format: 输出音频格式 (mp3, wav, pcm)
        mp3_bitrate: MP3 比特率 (64, 128, 192 kbps)
        chunk_length: 分块长度 (100-300)
        normalize: 是否对文本进行标准化处理
        latency: 延迟模式 (normal, balanced)
        
    Returns:
        生成的音频文件路径
    """
    if not text:
        return "文本不能为空"
    
    # 验证 chunk_length 范围
    if chunk_length < 100 or chunk_length > 300:
        return "chunk_length 必须在 100 到 300 之间"
    
    # 如果未提供输出路径，创建临时文件
    if not output_path:
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"tts_output_{hash(text)}.{format}")
    else:
        # 确保文件扩展名与格式一致
        if not output_path.endswith(f".{format}"):
            output_path = f"{output_path}.{format}"
    
    # 确保目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 调用 Fish Audio API 执行文本转语音
    try:
        with open(output_path, "wb") as f:
            for chunk in session.tts(TTSRequest(
                reference_id=MODEL_ID,
                text=text,
                format=format,
                mp3_bitrate=mp3_bitrate,
                chunk_length=chunk_length,
                normalize=normalize,
                latency=latency
            )):
                f.write(chunk)
        
        return f"成功生成语音文件：{output_path}"
    except Exception as e:
        return f"生成语音失败：{str(e)}"

@mcp.tool()
def get_model_info() -> dict:
    """获取当前使用的模型信息"""
    return {
        "model_id": MODEL_ID,
        "api_key_prefix": API_KEY[:8] + "..." if API_KEY else None
    }

@mcp.tool()
def get_available_models() -> list:
    """获取可用的鱼声音模型列表"""
    model_info = [
        {"name": "Fish Speech 1.5", "id": "speech-1.5", "description": "基础文字转语音模型"},
        {"name": "Fish Speech 1.6", "id": "speech-1.6", "description": "高级文字转语音模型"},
        {"name": "Agent X0", "id": "agent-x0", "description": "特殊场景文字转语音模型"}
    ]
    return model_info

if __name__ == "__main__":
    # 启动 MCP 服务
    mcp.run() 