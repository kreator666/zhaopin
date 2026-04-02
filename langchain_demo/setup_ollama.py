"""
Ollama 本地模型设置助手
自动下载并配置本地开源模型
"""

import subprocess
import sys
import os


def check_ollama():
    """检查 Ollama 是否安装"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Ollama 已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    return False


def install_guide():
    """显示安装指南"""
    print("=" * 50)
    print("Ollama 未安装，请按以下步骤安装：")
    print("=" * 50)
    print()
    print("1. 访问官网下载安装包:")
    print("   https://ollama.com/download")
    print()
    print("2. Windows 用户直接下载 .exe 安装")
    print("   安装完成后重启终端")
    print()
    print("3. 验证安装:")
    print("   ollama --version")
    print()
    print("4. 下载中文模型:")
    print("   ollama pull qwen2.5:7b")
    print()
    print("5. 运行示例:")
    print("   python 05_local_model.py")
    print("=" * 50)


def download_model(model_name="qwen2.5:7b"):
    """下载模型"""
    print(f"[*] 正在下载模型 {model_name}...")
    print("[*] 这可能需要几分钟，请耐心等待...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] 模型 {model_name} 下载完成！")
            return True
    except Exception as e:
        print(f"[Error] 下载失败: {e}")
    return False


def main():
    print("[Ollama 本地模型设置助手]\n")
    
    if not check_ollama():
        install_guide()
        return
    
    # 检查可用模型
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    print("\n[*] 已安装的模型:")
    print(result.stdout)
    
    if "qwen" not in result.stdout.lower():
        print("\n[*] 未检测到中文模型，建议下载 qwen2.5:7b")
        choice = input("是否现在下载？ (y/n): ")
        if choice.lower() == 'y':
            download_model("qwen2.5:7b")
    else:
        print("[OK] 已安装中文模型，可以直接运行 05_local_model.py")


if __name__ == "__main__":
    main()
