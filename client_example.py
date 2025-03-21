#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fish Audio TTS MCP 客户端示例
"""

import os
import sys
import subprocess
import time

def main():
    """
    MCP 客户端示例主函数
    """
    try:
        from mcp.client import MCPClient
    except ImportError:
        print("未安装 mcp 包，请先运行: pip install mcp")
        return
    
    # 检查 app.py 是否存在
    if not os.path.exists("app.py"):
        print("找不到 app.py 文件，请确保它在当前目录中")
        return
    
    # 启动 MCP 服务（后台）
    print("启动 Fish Audio TTS MCP 服务...")
    server_process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务启动
    time.sleep(2)
    
    # 检查服务是否成功启动
    if server_process.poll() is not None:
        stdout, stderr = server_process.communicate()
        print(f"MCP 服务启动失败:\n{stderr.decode('utf-8')}")
        return
    
    print("MCP 服务已启动")
    
    try:
        # 创建 MCP 客户端
        client = MCPClient("subprocess://python app.py")
        
        # 获取模型信息
        model_info = client.call("get_model_info")
        print(f"当前使用的模型信息: {model_info}")
        
        # 获取可用的模型列表
        available_models = client.call("get_available_models")
        print("可用的模型列表:")
        for model in available_models:
            print(f"  - {model['name']} ({model['id']}): {model['description']}")
        
        # 示例 1: 基本文字转语音
        text = "你好，这是鱼声音 API 生成的语音。"
        print(f"\n示例 1: 基本文字转语音")
        print(f"转换文本: {text}")
        result = client.call("text_to_speech", {"text": text})
        print(f"结果: {result}")
        
        # 示例 2: 高级文字转语音
        text = "这是使用高级设置生成的语音，可以调整格式、比特率等参数。"
        print(f"\n示例 2: 高级文字转语音")
        print(f"转换文本: {text}")
        result = client.call("advanced_text_to_speech", {
            "text": text,
            "format": "mp3",
            "mp3_bitrate": 192,
            "chunk_length": 250,
            "normalize": True,
            "latency": "balanced"
        })
        print(f"结果: {result}")
        
        # 播放生成的音频文件
        print("\n您可以使用系统默认的音频播放器打开生成的音频文件")
        
    except Exception as e:
        print(f"调用 MCP 服务时发生错误: {str(e)}")
    finally:
        print("\n停止 MCP 服务...")
        server_process.terminate()
        server_process.wait()
        print("MCP 服务已停止")

if __name__ == "__main__":
    main() 