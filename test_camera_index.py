#!/usr/bin/env python3
"""
摄像头索引测试工具
用于检测系统中可用的摄像头设备及其索引

使用方法：
    python test_camera_index.py
"""

import cv2
import sys

def test_camera_indices(max_index=10):
    """
    测试从 0 到 max_index 的所有摄像头索引
    
    Args:
        max_index: 测试的最大索引值
    """
    print("=" * 60)
    print("摄像头设备检测工具")
    print("=" * 60)
    print(f"正在测试摄像头索引 0 到 {max_index}...\n")
    
    available_cameras = []
    
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                fps = cap.get(cv2.CAP_PROP_FPS)
                backend = cap.getBackendName()
                
                print(f"✓ 摄像头索引 {i} 可用")
                print(f"  分辨率: {width}x{height}")
                print(f"  帧率: {fps} FPS")
                print(f"  后端: {backend}")
                print()
                
                available_cameras.append({
                    'index': i,
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'backend': backend
                })
                
                # 显示画面预览（可选）
                cv2.imshow(f"Camera {i} Preview - Press any key to continue", frame)
                cv2.waitKey(1500)  # 显示1.5秒
                cv2.destroyAllWindows()
            else:
                print(f"✗ 摄像头索引 {i} 无法读取画面")
                print()
            
            cap.release()
        else:
            # 不打印不可用的索引，避免输出过多
            pass
    
    # 总结
    print("=" * 60)
    print("检测完成！")
    print("=" * 60)
    
    if available_cameras:
        print(f"\n找到 {len(available_cameras)} 个可用摄像头：\n")
        for cam in available_cameras:
            print(f"摄像头 {cam['index']}: {cam['width']}x{cam['height']} @ {cam['fps']}fps ({cam['backend']})")
        
        print("\n" + "=" * 60)
        print("配置建议：")
        print("=" * 60)
        
        if len(available_cameras) == 1:
            cam = available_cameras[0]
            print(f"\n在代码中使用：")
            print(f"  CAMERA_MODE = 'index'")
            print(f"  CAMERA_INDEX = {cam['index']}")
        else:
            print(f"\n在代码中使用其中一个：")
            for cam in available_cameras:
                print(f"  CAMERA_INDEX = {cam['index']}  # {cam['width']}x{cam['height']}")
    else:
        print("\n❌ 未检测到可用的摄像头设备")
        print("\n可能的原因：")
        print("  1. 没有摄像头硬件")
        print("  2. 摄像头被其他程序占用")
        print("  3. 摄像头驱动未安装")
        print("  4. 权限不足")
        print("\n解决方案：")
        print("  - 关闭可能使用摄像头的程序（Zoom、Skype等）")
        print("  - 检查设备管理器中的摄像头状态")
        print("  - 使用手机作为摄像头（参考 docs/Camera_Setup_Guide.md）")
        print("  - 或设置 CAMERA_MODE = 'disable' 禁用视频功能")
    
    print("\n" + "=" * 60)
    return available_cameras


def test_ip_camera(url):
    """
    测试IP摄像头连接
    
    Args:
        url: IP摄像头URL
    """
    print("=" * 60)
    print(f"测试IP摄像头: {url}")
    print("=" * 60)
    
    cap = cv2.VideoCapture(url)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            height, width = frame.shape[:2]
            print(f"✓ 连接成功！")
            print(f"  分辨率: {width}x{height}")
            
            # 显示预览
            cv2.imshow("IP Camera Preview - Press any key to close", frame)
            print("\n按任意键关闭预览窗口...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"✗ 无法读取画面")
        cap.release()
    else:
        print(f"✗ 连接失败")
        print("\n请检查：")
        print("  1. 手机和电脑在同一WiFi网络")
        print("  2. 手机APP已启动")
        print("  3. URL地址正确")
        print("  4. 防火墙未阻止连接")
    
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果提供了URL参数，测试IP摄像头
        url = sys.argv[1]
        test_ip_camera(url)
    else:
        # 否则测试本地摄像头索引
        test_camera_indices(max_index=10)
        
        print("\n提示：")
        print("  - 要测试IP摄像头，请运行：")
        print("    python test_camera_index.py http://192.168.1.100:8080/video")
        print("  - 详细配置指南请参考：docs/Camera_Setup_Guide.md")
        print()

