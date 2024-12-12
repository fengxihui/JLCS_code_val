import base64
import json
import pydirectinput
import win32api
import win32con
import random
import pygetwindow as gw
import re
import keyboard
import cv2
import numpy as np
import sys
import logging
import os
from openai import OpenAI
import ddddocr
import pyautogui
import time
from PIL import ImageGrab
from datetime import datetime
delay=0.5

# 定义虚拟键码（VK）常量
VK_0 = 0x30  # '0' 键的虚拟键码
VK_1 = 0x31  # '1' 键的虚拟键码
VK_2 = 0x32  # '2' 键的虚拟键码
VK_3 = 0x33  # '3' 键的虚拟键码
VK_4 = 0x34  # '4' 键的虚拟键码
VK_5 = 0x35  # '5' 键的虚拟键码
VK_6 = 0x36  # '6' 键的虚拟键码
VK_7 = 0x37  # '7' 键的虚拟键码
VK_8 = 0x38  # '8' 键的虚拟键码
VK_9 = 0x39  # '9' 键的虚拟键码
VK_RETURN = 0x0D  # 回车键的虚拟键码

# 将字符映射为虚拟键码
def char_to_vk(char):
    if char.isdigit():
        return ord(char) - ord('0') + VK_0
    else:
        raise ValueError(f"无效的字符: {char}")

# 模拟按下和释放一个键
def press_key(vk_code):
    win32api.keybd_event(vk_code, 0, 0, 0)  # 按下键
    time.sleep(0.1)  # 短暂停顿
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放键
def find_fwh_image_on_screen(image_path, region,default_coords=(0, 0, 900, 300)):
    """
    在屏幕上查找与给定路径匹配的'防外挂验证'图像的位置。

    :param image_path: 包含'防外挂验证'文本的图像文件路径
    :param default_coords: 如果找不到图像时返回的默认坐标 (left, top, width, height)
    :return: 图像在屏幕上的位置 (left, top, right, bottom) 或默认坐标
    """
    try:
        # 检查图像文件是否存在
        if not os.path.exists(image_path):
            logging.error(f"图像文件 {image_path} 不存在")
            return default_coords

        # 尝试在屏幕上找到图像的位置
        # region = (837, 58, 800, 600)
        position = pyautogui.locateOnScreen(image_path, region=region,confidence=0.8)
        if position is None:
            logging.warning(f"无法找到图像 {image_path} 的位置，返回默认坐标")
            return default_coords
        else:
            left, top, width, height = position
            right = left + width
            bottom = top + height
            logging.info(f"找到图像 {image_path} 的位置: 左={left}, 上={top}, 右={right}, 下={bottom}")
            return (left, top, right, bottom)
    except pyautogui.ImageNotFoundException as e:
        logging.warning(f"图像 {image_path} 未找到: {e}")
        return default_coords
    except Exception as e:
        logging.error(f"在查找图像 {image_path} 时发生未知错误: {e}")
        raise  # 重新抛出异常，以便可以在更高层次进行处理
def capture_screen_area(left, top, right, bottom, save_folder):
    """
    截取屏幕上的指定区域，并将其保存到指定的文件夹中。

    :param left: 矩形区域的左边界坐标
    :param top: 矩形区域的上边界坐标
    :param right: 矩形区域的右边界坐标
    :param bottom: 矩形区域的下边界坐标
    :param save_folder: 保存截图的文件夹路径
    """
    # 确保保存文件夹存在
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    filename = f"result.png"
    filepath = os.path.join(save_folder, filename)

    # 截取屏幕区域
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    # 保存截图
    screenshot.save(filepath)
    print(f"Screenshot saved as {filepath}")

def extract_digits_from_image(image_path):
    try:
        # 读取并转换图像为 base64 编码
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # 根据图像的实际格式调整 MIME 类型
        mime_type = 'image/png' if image_path.lower().endswith('.png') else 'image/jpeg'
        image_url = f'data:{mime_type};base64,{image_base64}'

        client = OpenAI(
            #阿里通义
            api_key="xxxxxxxxxxx",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            # 字节豆包,字节的只试过一次，具体的模型需要自行试验
            # api_key="xxxxxxxxxxxxxxxxxxx",
            # base_url="xxxxxxxxxxxxxxxx",
        )
        completion = client.chat.completions.create(
            #通义千问
            model="qwen-vl-max-latest",
            #字节豆包
            # model="xxxxxxxxxxxxxxxxxxx",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": "图像里的数字部分是什么，请给出字符串形式，字符串两侧用!包围"},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}]
        )

        data = json.loads(completion.model_dump_json())
        content = data['choices'][0]['message']['content']
        match = re.search(r'!([^!]*)!', content)

        # 如果匹配成功，提取数字
        if match:
            number_str = re.sub(r'[^0-9]', '', match.group(1))
            return number_str
        else:
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# 使用示例
# capture_screen_area
# digits = extract_digits_from_image('gameval\\b.png')
# print(f"Extracted digits: {digits}")
def click_image_on_screen(image_path):
    # 尝试在屏幕上找到图像的位置
    position = pyautogui.locateOnScreen(image_path, confidence=0.8)

    if position is None:
        print(f"无法找到图像 {image_path} 的位置")
        return False

    # 获取图像中心点的坐标
    center = pyautogui.center(position)

    # 移动鼠标到图像中心点并点击
    pyautogui.click(center)

    return True


def click_and_type_in_search_box(image_path, text_to_type):
    try:
        # 尝试找到并点击搜索框
        if click_image_on_screen(image_path):
            time.sleep(0.5)  # 等待一段时间，确保点击生效
            print(f"已点击图像 {image_path}，准备输入文本")

            # 输入文本
            pyautogui.write(text_to_type, interval=0.1)  # 每个字符之间间隔 0.05 秒
            print(f"已输入文本: {text_to_type}")

            # 如果需要按回车键或其他键，可以使用 pyautogui.press()
            # pyautogui.press('enter')  # 模拟按下回车键

        else:
            print(f"未找到图像 {image_path}，无法输入文本")

    except pyautogui.ImageNotFoundException:
        print(f"未找到图像 {image_path}，跳过点击和输入")
def click_number_on_screen(number):
    # image_path = f'number_images/{number}.png'  # 确保路径正确指向你的模板图片
    image_path = 'gameval/write.png'
    return click_image_on_screen(image_path)


def click_image_on_screen(image_path, max_retries=3):
    """
    尝试在屏幕上找到并点击指定的图像，支持重试。

    :param image_path: 图像文件路径
    :param max_retries: 最大重试次数，默认为3次
    :return: 如果成功点击返回 True，否则返回 False
    """
    for attempt in range(max_retries):
        position = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if position is None:
            print(f"未找到图像 {image_path}，正在重试 ({attempt + 1}/{max_retries})")
            time.sleep(0.5)  # 等待一段时间再重试
        else:
            center = pyautogui.center(position)
            pyautogui.click(center)
            print(f"已点击图像 {image_path}")
            return True
    print(f"未能找到图像 {image_path}，重试次数已用尽")
    return False


def type_digit(digit, interval=0.05):
    """
    模拟键盘输入单个数字。

    :param digit: 要输入的数字字符
    :param interval: 每个字符之间的输入间隔，默认为 0.05 秒
    """
    try:
        pyautogui.write(digit, interval=interval)
        print(f"已输入数字: {digit}")
    except Exception as e:
        print(f"输入数字 {digit} 时发生错误: {e}")

def click_bb():
    #（1751，57是测得第一只bb的坐标，移动窗口就没了，也可以找图获得坐标，不过我一般不动窗口位置
    win32api.SetCursorPos((1751,57 ))
    print("鼠标已移动到出战的bb")
    time.sleep(0.5)
    # 模拟鼠标点击
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  # 按下右键
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)  # 释放右键
    print("已实现恢复HP/PP")
def click_and_type_digit(image_path, digit):
    """
    点击指定的图像，然后输入指定的数字。

    :param image_path: 搜索框图像的路径
    :param digit: 要输入的数字字符
    """
    # 找到并点击图像
    if not click_image_on_screen(image_path):
        print(f"未能成功点击图像 {image_path}，无法输入数字")
        return

    # 等待一段时间，确保点击生效
    time.sleep(delay)

    # 输入数字
    type_digit(digit)



def val_first():
    target_window_title = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    try:
        # 获取目标窗口
        target_window = gw.getWindowsWithTitle(target_window_title)[0]

        # 激活窗口
        if not target_window.isActive or target_window.isMinimized:
            target_window.activate()
            print(f"激活窗口: {target_window_title}")
            time.sleep(0.1)  # 等待窗口完全激活并获得焦点

            # 如果窗口最小化，则最大化
            if target_window.isMinimized:
                target_window.maximize()
                time.sleep(0.1)  # 再次等待确保窗口完全获得焦点

        # 确认窗口是否已激活
        if target_window.isActive:
            print("窗口已激活并获得焦点")

            # time.sleep(0.5)

        else:
            print("窗口未能激活或获得焦点")
    except IndexError:
        print(f"未找到标题为 '{target_window_title}' 的窗口")
    # click_bb()
    region = (825, 67, 800, 600)
    coords = find_fwh_image_on_screen('gameval\\locate.png',region)
    left, top, right, bottom = coords
    left = left - 130
    top = top + 62
    right = right + 117
    bottom = bottom + 160
    capture_screen_area(left, top, right, bottom, "gameval")
    default_image_path = 'gameval\\result.png'

    # 从命令行参数获取图像路径，如果没有提供则使用默认路径
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = default_image_path

    print(f"Processing image: {image_path}")
    digits = extract_digits_from_image(image_path)
    time.sleep(0.5)
    if digits and len(digits) == 3:
        print(f"Extracted digits: {digits}")
        time.sleep(0.5)
        for key in digits:
            print(f"按下 {key} 键")
            vk_code = char_to_vk(key)
            press_key(vk_code)
            time.sleep(0.1)  # 可选：添加短暂停顿，确保每个键都能被正确识别
            # 模拟按下回车键
        print("按下回车键")
        press_key(VK_RETURN)
        location = find_fwh_image_on_screen('gameval\\change.png',region)
        left1, top1, right1, bottom1 = location
        # 找不到的时候返回默认坐标，下面是为了判断是否找得到验证码图像
        if left1 != 0:
            center_xx = (left1 + right1) // 2
            center_yy = (top1 + bottom1) // 2
            win32api.SetCursorPos((center_xx, center_yy))
            print("鼠标已移动到{看不清，换一张?@__@}")
            time.sleep(0.5)
            # 模拟鼠标点击
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下左键
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放左键
            print("已实现{看不清，换一张}")
        # keyboard.press_and_release('enter')
    else:
        print("No correct digits in the image.")
        location = find_fwh_image_on_screen('gameval\\change.png',region)
        left1, top1, right1, bottom1 = location
        # 找不到的时候返回默认坐标，下面是为了判断是否找得到验证码图像
        if left1 != 0:
            center_xx = (left1 + right1) // 2
            center_yy = (top1 + bottom1) // 2
            win32api.SetCursorPos((center_xx, center_yy))
            print("鼠标已移动到{看不清，换一张?@__@}")
            time.sleep(0.5)
            # 模拟鼠标点击
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下左键
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放左键
            print("已实现{看不清，换一张}")

def val_second():
    target_window_title = "精灵传说 Ver-3.0.1008 [光辉区 梦幻之吻] name ID-xxxxxxx"
    try:
        # 获取目标窗口
        target_window = gw.getWindowsWithTitle(target_window_title)[0]

        # 激活窗口
        if not target_window.isActive or target_window.isMinimized:
            target_window.activate()
            print(f"激活窗口: {target_window_title}")
            time.sleep(0.1)  # 等待窗口完全激活并获得焦点

            # 如果窗口最小化，则最大化
            if target_window.isMinimized:
                target_window.maximize()
                time.sleep(0.1)  # 再次等待确保窗口完全获得焦点

        # 确认窗口是否已激活
        if target_window.isActive:
            print("窗口已激活并获得焦点")

            # time.sleep(0.5)

        else:
            print("窗口未能激活或获得焦点")
    except IndexError:
        print(f"未找到标题为 '{target_window_title}' 的窗口")
    # click_bb()
    region = (63, 93, 800, 600)
    coords = find_fwh_image_on_screen('gameval\\locate.png',region)
    left, top, right, bottom = coords
    left = left - 130
    top = top + 62
    right = right + 117
    bottom = bottom + 160
    capture_screen_area(left, top, right, bottom, "gameval")
    default_image_path = 'gameval\\result.png'

    # 从命令行参数获取图像路径，如果没有提供则使用默认路径
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = default_image_path

    print(f"Processing image: {image_path}")
    digits = extract_digits_from_image(image_path)

    if digits and len(digits) == 3:
        print(f"Extracted digits: {digits}")
        time.sleep(0.5)
        for key in digits:
            print(f"按下 {key} 键")
            vk_code = char_to_vk(key)
            press_key(vk_code)
            time.sleep(0.1)  # 可选：添加短暂停顿，确保每个键都能被正确识别
            # 模拟按下回车键
        print("按下回车键")
        press_key(VK_RETURN)
        location = find_fwh_image_on_screen('gameval\\change.png')
        left1, top1, right1, bottom1 = location
        # 找不到的时候返回默认坐标，下面是为了判断是否找得到验证码图像
        if left1 != 0:
            center_xx = (left1 + right1) // 2
            center_yy = (top1 + bottom1) // 2
            win32api.SetCursorPos((center_xx, center_yy))
            print("鼠标已移动到{看不清，换一张?@__@}")
            time.sleep(0.5)
            # 模拟鼠标点击
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下左键
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放左键
            print("已实现{看不清，换一张}")
        # keyboard.press_and_release('enter')
    else:
        print("No correct digits in the image.")
        location = find_fwh_image_on_screen('gameval\\change.png',region)
        left1, top1, right1, bottom1 = location
        # 找不到的时候返回默认坐标，下面是为了判断是否找得到验证码图像
        if left1 != 0:
            center_xx = (left1 + right1) // 2
            center_yy = (top1 + bottom1) // 2
            win32api.SetCursorPos((center_xx, center_yy))
            print("鼠标已移动到{看不清，换一张?@__@}")
            time.sleep(0.5)
            # 模拟鼠标点击
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下左键
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放左键
            print("已实现{看不清，换一张}")
def main():
    while True:
        val_first()
        time.sleep(3)
        val_second()
        time.sleep(3)
    # 默认图像路径
    # print("开始监控，每10秒执行一次...")
    # while True:
    #     coords =find_fwh_image_on_screen('gameval\\locate.png')
    #     left, top, right, bottom = coords
    #     left = left -130
    #     top = top + 62
    #     right = right + 117
    #     bottom = bottom + 160
    #     capture_screen_area(left,top,right,bottom, "gameval")
    #     default_image_path = 'gameval\\result.png'
    #
    #     # 从命令行参数获取图像路径，如果没有提供则使用默认路径
    #     if len(sys.argv) > 1:
    #         image_path = sys.argv[1]
    #     else:
    #         image_path = default_image_path
    #
    #     print(f"Processing image: {image_path}")
    #
    #     # 调用函数并获取结果
    #
    #     digits = extract_digits_from_image(image_path)
    #     target_window_title = "精灵传说"
    #
    #
    #     # 尝试找到并激活目标窗口864
    #
    #     try:
    #         # 获取目标窗口
    #         target_window = gw.getWindowsWithTitle(target_window_title)[0]
    #
    #         # 激活窗口
    #         if not target_window.isActive or target_window.isMinimized:
    #             target_window.activate()
    #             print(f"激活窗口: {target_window_title}")
    #             time.sleep(1)  # 等待窗口完全激活并获得焦点
    #
    #             # 如果窗口最小化，则最大化
    #             if target_window.isMinimized:
    #                 target_window.maximize()
    #                 time.sleep(1)  # 再次等待确保窗口完全获得焦点
    #
    #         # 确认窗口是否已激活
    #         if target_window.isActive:
    #             print("窗口已激活并获得焦点")
    #
    #             # time.sleep(0.5)
    #
    #         else:
    #             print("窗口未能激活或获得焦点")
    #             exit()
    #     except IndexError:
    #         print(f"未找到标题为 '{target_window_title}' 的窗口")
    #         exit()
    #
    #     # 输出结果
    #     if digits and len(digits) == 3:
    #         print(f"Extracted digits: {digits}")
    #         time.sleep(0.5)
    #         for key in digits:
    #             print(f"按下 {key} 键")
    #             vk_code = char_to_vk(key)
    #             press_key(vk_code)
    #             time.sleep(0.1)  # 可选：添加短暂停顿，确保每个键都能被正确识别
    #             # 模拟按下回车键
    #         print("按下回车键")
    #         press_key(VK_RETURN)
    #         location = find_fwh_image_on_screen('gameval\\change.png')
    #         left1, top1, right1, bottom1 = location
    #         # 找不到的时候返回默认坐标，下面是为了判断是否找得到验证码图像
    #         if left1 != 0:
    #             center_xx = (left1 + right1) // 2
    #             center_yy = (top1 + bottom1) // 2
    #             win32api.SetCursorPos((center_xx, center_yy))
    #             print("鼠标已移动到{看不清，换一张?@__@}")
    #             time.sleep(0.5)
    #             # 模拟鼠标点击
    #             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下左键
    #             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放左键
    #             print("已实现{看不清，换一张}")
    #         # keyboard.press_and_release('enter')
    #     else:
    #         print("No correct digits in the image.")
    #     print("等待10秒...")
    #     time.sleep(10)


if __name__ == "__main__":
    main()
