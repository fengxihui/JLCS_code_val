import pygetwindow as gw
import time

target_window_title = "精灵传说"

# 获取所有与目标标题匹配的窗口
matching_windows = gw.getWindowsWithTitle(target_window_title)

if not matching_windows:
    print(f"没有找到标题为 '{target_window_title}' 的窗口。")
else:
    # 列出所有匹配的窗口及其信息
    for i, window in enumerate(matching_windows, start=1):
        print(f"窗口 {i}:")
        print(f"  Title: {window.title}")
        # print(f"  Handle: {window._hWnd}")  # 注意：_hWnd是内部属性，可能不推荐直接访问
        # print(f"  Position: ({window.left}, {window.top})")
        # print(f"  Size: ({window.width}, {window.height})")
        # print(f"  Active: {window.isActive}")
        # print(f"  Minimized: {window.isMinimized}")

    # 提示用户选择要激活的窗口
    choice = int(input("请选择要激活的窗口编号 (1, 2, 3, ...): ")) - 1

    if 0 <= choice < len(matching_windows):
        target_window = matching_windows[choice]

        # 激活选定的窗口
        if not target_window.isActive or target_window.isMinimized:
            target_window.activate()
            print(f"激活窗口: {target_window.title}")
            time.sleep(1)  # 等待窗口完全激活并获得焦点
        else:
            print(f"窗口 {target_window.title} 已经是活动窗口。")
    else:
        print("无效的选择。")