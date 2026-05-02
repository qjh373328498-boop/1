#!/usr/bin/env python3
"""
ModelScope AI 图片生成脚本
用法：
  python3 gen_image.py "<prompt>" <output_path>
  python3 gen_image.py batch.json  # 批量生成

依赖：
  pip install requests
"""

import requests
import time
import json
import sys
import os
from io import BytesIO

# ==================== 配置区 ====================

BASE_URL = "https://api-inference.modelscope.cn/"
API_KEY = "ms-cc494f31-690a-4df6-9bea-a9a0d3311c4e"  # 替换为你的 ModelScope Token
MODEL = "Tongyi-MAI/Z-Image-Turbo"  # 通义万相高速版
DEFAULT_TIMEOUT = 120  # 超时时间（秒）
DEFAULT_MAX_WORKERS = 4  # 批量生成最大并发数

# ==================== 工具函数 ====================

def get_headers():
    """获取请求头"""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true",
    }


def check_task_status(task_id: str) -> dict:
    """查询任务状态"""
    headers = get_headers()
    headers["X-ModelScope-Task-Type"] = "image_generation"
    
    response = requests.get(
        f"{BASE_URL}v1/tasks/{task_id}",
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def download_image(url: str, output_path: str):
    """下载图片并保存"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return output_path


# ==================== 核心函数 ====================

def generate_image(prompt: str, output_path: str, timeout: int = DEFAULT_TIMEOUT):
    """
    使用 ModelScope API 生成单张图片
    
    Args:
        prompt: 中文或英文提示词
        output_path: 输出文件路径
        timeout: 超时时间（秒）
    
    Returns:
        str: 输出文件路径
    
    Raises:
        TimeoutError: 生成超时
        Exception: 生成失败
    """
    headers = get_headers()
    
    print(f"🎨 开始生成：{prompt}")
    print(f"📤 输出路径：{output_path}")
    
    # 提交异步任务
    response = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers=headers,
        data=json.dumps({
            "model": MODEL,
            "prompt": prompt
        }, ensure_ascii=False).encode('utf-8'),
        timeout=30
    )
    response.raise_for_status()
    
    task_id = response.json()["task_id"]
    print(f"📋 任务 ID: {task_id}")
    
    # 轮询任务状态
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        
        if elapsed > timeout:
            raise TimeoutError(f"图片生成超时 ({timeout}s)")
        
        data = check_task_status(task_id)
        status = data.get("task_status", "UNKNOWN")
        
        print(f"⏳ [{elapsed:.0f}s] 状态：{status}")
        
        if status == "SUCCEED":
            img_url = data["output_images"][0]
            download_image(img_url, output_path)
            file_size = os.path.getsize(output_path) / 1024
            print(f"✅ 生成成功！大小：{file_size:.1f}KB")
            return output_path
            
        elif status == "FAILED":
            error_msg = data.get("error", {}).get("message", "未知错误")
            raise Exception(f"图片生成失败：{error_msg}")
        
        time.sleep(3)


def batch_generate(tasks: list, max_workers: int = DEFAULT_MAX_WORKERS):
    """
    批量生成图片
    
    Args:
        tasks: [(prompt1, output1), (prompt2, output2), ...]
        max_workers: 最大并发数
    
    Returns:
        list: 生成的文件路径列表
    """
    import concurrent.futures
    
    total = len(tasks)
    results = []
    errors = []
    
    def worker(task):
        prompt, output = task
        try:
            result = generate_image(prompt, output)
            return {"success": True, "output": result}
        except Exception as e:
            return {"success": False, "error": str(e), "prompt": prompt}
    
    print(f"\n🚀 开始批量生成：{total} 张图片")
    print(f"👷 并发数：{max_workers}")
    print("=" * 50)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, task): i for i, task in enumerate(tasks)}
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            task_index = futures[future]
            prompt = tasks[task_index][0]
            
            try:
                result = future.result()
                completed += 1
                
                if result["success"]:
                    print(f"\n✅ [{completed}/{total}] {result['output']}")
                    results.append(result['output'])
                else:
                    print(f"\n❌ [{completed}/{total}] 失败：{result['error']}")
                    errors.append({"prompt": prompt, "error": result['error']})
                    
            except Exception as e:
                print(f"\n❌ [{completed}/{total}] 异常：{e}")
                errors.append({"prompt": prompt, "error": str(e)})
    
    # 打印摘要
    print("\n" + "=" * 50)
    print(f"📊 生成摘要:")
    print(f"  成功：{len(results)}/{total}")
    print(f"  失败：{len(errors)}/{total}")
    
    if errors:
        print(f"\n⚠️ 失败详情:")
        for err in errors:
            print(f"  - {err['prompt'][:50]}... : {err['error']}")
    
    return results, errors


def load_batch_file(batch_file: str) -> list:
    """
    加载批量任务文件
    
    支持格式：
    1. [["prompt1", "output1"], ["prompt2", "output2"]]
    2. {"tasks": [["prompt1", "output1"], ...]}
    """
    with open(batch_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "tasks" in data:
        return data["tasks"]
    else:
        raise ValueError("无效的批量任务文件格式")


def generate_storyboard_images(storyboard_file: str, output_dir: str):
    """
    从分镜脚本生成图片
    
    Args:
        storyboard_file: storyboard.json 文件路径
        output_dir: 输出目录
    
    Returns:
        list: 生成的文件路径列表
    """
    with open(storyboard_file, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)
    
    tasks = []
    scenes = storyboard.get("scenes", [])
    
    for i, scene in enumerate(scenes):
        prompt = scene.get("image_prompt", "")
        output_name = f"scene_{i+1:02d}.png"
        output_path = os.path.join(output_dir, output_name)
        
        if prompt:
            tasks.append((prompt, output_path))
    
    print(f"📋 从分镜脚本提取 {len(tasks)} 个场景")
    return batch_generate(tasks)


# ==================== 命令行界面 ====================

def print_usage():
    """打印使用说明"""
    print("""
ModelScope AI 图片生成工具
==========================

用法:
  1. 单张生成:
     python3 gen_image.py "<prompt>" <output_path>
  
  2. 批量生成:
     python3 gen_image.py <batch.json>
  
  3. 从分镜生成:
     python3 gen_image.py --storyboard <storyboard.json> --output-dir <dir>

示例:
  python3 gen_image.py "一只可爱的猫" cat.png
  python3 gen_image.py tasks.json
  python3 gen_image.py --storyboard storyboard.json --output-dir images

批量任务文件格式 (batch.json):
  [
    ["提示词 1", "输出 1.png"],
    ["提示词 2", "输出 2.png"]
  ]

配置:
  编辑脚本顶部的配置区修改 API_KEY、MODEL 等参数
""")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ModelScope AI 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input", nargs="?", help="提示词或批量任务文件")
    parser.add_argument("output", nargs="?", help="输出文件路径（单张模式）")
    parser.add_argument("--storyboard", help="从分镜脚本生成图片")
    parser.add_argument("--output-dir", default=".", help="输出目录（分镜模式）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"超时时间（秒，默认:{DEFAULT_TIMEOUT}）")
    parser.add_argument("--workers", type=int, default=DEFAULT_MAX_WORKERS, help=f"并发数（默认:{DEFAULT_MAX_WORKERS}）")
    parser.add_argument("--model", default=MODEL, help=f"模型 ID（默认:{MODEL}）")
    
    args = parser.parse_args()
    
    # 分镜模式
    if args.storyboard:
        return generate_storyboard_images(args.storyboard, args.output_dir)
    
    # 单张模式：提供 prompt 和 output
    if args.input and args.output:
        return generate_image(args.input, args.output, args.timeout)
    
    # 批量模式：提供 batch.json 文件
    if args.input and args.input.endswith('.json'):
        tasks = load_batch_file(args.input)
        return batch_generate(tasks, args.workers)
    
    # 显示帮助
    print_usage()
    sys.exit(1)


if __name__ == "__main__":
    main()
