import pygetwindow as gw
import screeninfo
import logging


def get_window_position_relative_to_screen(window_title):
    """
    获取指定窗口的坐标，并将其转换为相对于屏幕左上角的坐标。

    参数:
    - window_title (str): 窗口的标题或部分标题。

    返回:
    - tuple: (screen_index, left, top, width, height) 或 None（如果未找到窗口或屏幕）。
    """
    try:
        # 获取所有与给定标题匹配的窗口
        windows = gw.getWindowsWithTitle(window_title)

        if not windows:
            logging.warning(f"未找到标题为 '{window_title}' 的窗口")
            return None

        # 获取所有显示器的信息
        monitors = screeninfo.get_monitors()

        if not monitors:
            logging.warning("未找到任何显示器")
            return None

        # 遍历所有窗口，找到第一个匹配的窗口
        for window in windows:
            window_left = window.left
            window_top = window.top
            window_width = window.width
            window_height = window.height

            # 遍历所有显示器，找到窗口所在的显示器
            for i, monitor in enumerate(monitors):
                # 检查窗口是否在当前显示器的范围内
                if (monitor.x <= window_left < monitor.x + monitor.width and
                        monitor.y <= window_top < monitor.y + monitor.height):
                    # 计算窗口相对于屏幕左上角的坐标
                    relative_left = window_left - monitor.x
                    relative_top = window_top - monitor.y

                    logging.info(
                        f"找到窗口 '{window.title}'，位于显示器 {i + 1}，坐标: ({relative_left}, {relative_top})，尺寸: {window_width}x{window_height}")
                    return (i, relative_left, relative_top, window_width, window_height)

            # 如果窗口不在任何显示器的范围内，记录警告并继续查找下一个窗口
            logging.warning(f"窗口 '{window.title}' 不在任何显示器的范围内")

        # 如果没有找到窗口所在的显示器，返回 None
        return None

    except Exception as e:
        logging.error(f"获取窗口位置时发生错误: {e}")
        return None


# 示例调用
if __name__ == "__main__":
    window_title = "精灵传说 Ver-3.0.1008 [光辉区 梦幻之吻] baodde ID-4522015"  # 请将此替换为你要查找的窗口标题
    position = get_window_position_relative_to_screen(window_title)
    if position:
        screen_index, left, top, width, height = position
        print(f"窗口 '{window_title}' 位于显示器 {screen_index + 1}，相对坐标: ({left}, {top},{left+width},{top+height})，尺寸: {width}x{height}")
    else:
        print(f"未找到窗口 '{window_title}' 或其所在显示器")

