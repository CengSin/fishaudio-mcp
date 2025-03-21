#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fish Audio TTS MCP 服务使用示例
"""

import os
import time
import sys
import subprocess
from pathlib import Path

def main():
    """
    使用 MCP 服务的示例主函数
    """
    # 检查是否安装了必要的包
    try:
        import mcp
    except ImportError:
        print("未安装 mcp 包，请先运行: pip install mcp")
        return
    
    # 检查 app.py 是否存在
    if not os.path.exists("app.py"):
        print("找不到 app.py 文件，请确保它在当前目录中")
        return
    
    # 启动 MCP 服务
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
    print("\n可以使用以下命令连接到 MCP 服务:")
    print("  mcp run --file app.py")
    print("\n或者在您的应用程序中使用 MCP 客户端库连接到此服务")
    print("\n按 Ctrl+C 退出...")
    
    try:
        # 保持脚本运行直到用户按 Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止 MCP 服务...")
        server_process.terminate()
        server_process.wait()
        print("MCP 服务已停止")

if __name__ == "__main__":
    main() 