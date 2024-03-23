import math
import os
import re
import shutil
import subprocess
from random import random
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, simpledialog, messagebox
from datetime import datetime, timedelta
import configparser
import imageio

from PIL import Image, ImageTk, ImageSequence
import json
import pygame
import apng

import win32gui
import win32con
import win32api


# import logging

# logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为 DEBUG

def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 创建成功")
    except FileExistsError:
        print(f"文件夹 '{folder_path}' 已经存在")

audio_list = {}
babel_on = False
frame_Map = 0
frames_map = {}
current_frame_map = {}
Is_fill = False
Is_square = False

def play_audio(file_path, name, loops = -1):
    if file_path:
        pygame.mixer.init()
        #pygame.mixer.music.load(file_path)
        #pygame.mixer.music.play(loops = loops)
        sound = pygame.mixer.Sound(file_path)
        sound.play(loops = loops)
        if loops == -1:
            audio_list[name] = sound

def kill_audio(name):
    audio_list[name].stop()
    audio_list.pop(name)

# 例子：创建名为 'my_folder' 的文件夹在当前工作目录下
create_folder('AppSettings')
create_folder('Bots')
create_folder('GameSaves')
create_folder('Images')
create_folder('Images/AvatarImages')
create_folder('Images/IconImages')
create_folder('Images/SheetImages')
create_folder('Images/BattleImages')
create_folder('ReplayResources')
create_folder('ReplayResources/BG')
create_folder('ReplayResources/BGM')
create_folder('ReplayResources/SE')
create_folder('ReplayResources/HandOut')

# 便于直接编辑的一系列字符串
string_list_Critical_Success = ["￥.。.￥。￥.。\n是大成功！\n.￥.。.￥。.￥。", "这次是大成功！/微笑"]
string_list_Extreme_Success = ["（深呼吸）...极难成功！恭喜您！", "极难成功！恭喜您。"]
string_list_Hard_Success = ["困难成功！"]
string_list_Success = ["检定成功，期待您的表现。", "检定成功，请多加利用/微笑"]
string_list_Failure = ["失败了，请您不要灰心..."]
string_list_Fumble = ["嗯...抱歉，看起来是大失败呢..."]

# timer计算
place = "某地"
weather = "晴"
time = datetime.now().strftime("%H:%M")
date = datetime.now().strftime("%Y/%m/%d %A")
# 自动Timer计算
_secondsTime = 0
time_3s = ["斗殴", "闪避", "斧头", "连枷", "矛", "剑", "鞭子", "弓", "手枪", "机枪", "步枪", "霰弹枪", "步枪/霰弹枪", "冲锋枪", "急救",
           "困难跳跃", "跳跃", "攀爬", "困难攀爬", "妙手", "投掷", "困难投掷"]
time_1min = ["链锯", "困难急救", "极难跳跃", "极难攀爬", "困难妙手", "极难投掷", "困难潜行", "重武器", "火焰喷射器", "锁匠"]
time_5min = ["困难侦查", "困难聆听", "困难心理学", "恐吓", "说服", "魅惑", "话术", "医学", "极难急救", "困难锁匠", "领航",
             "极难妙手", "极难潜行"]
time_10min = ["表演", "美术", "写作", "书法", "舞蹈", "歌剧", "声乐", "摄影", "极难聆听", "极难心理学", "困难恐吓", "困难说服", "困难魅惑", "困难话术",
              "极难急救", "困难锁匠", "困难领航"]
time_30min = ["极难话术", "困难医学", "极难领航", "精神分析", "困难追踪", "图书馆", "计算机", "电脑", "困难会计", "木匠", "厨艺", "雕塑", "伪造", "陶艺", "极难侦查"]
time_1h = ["困难表演", "困难美术", "困难写作", "困难书法", "困难舞蹈", "困难歌剧", "困难声乐", "困难摄影", "困难电气维修", "困难电子学", "困难机械维修", "极难锁匠",
           "困难精神分析", "困难图书馆", "困难计算机", "困难电脑", "极难会计"]
time_3h = ["极难表演", "极难书法", "极难舞蹈", "极难歌剧", "极难声乐", "极难摄影", "极难电子学", "极难电气维修", "极难医学", "极难精神分析", "极难追踪", "极难计算机", "极难电脑",
           "困难雕塑", "困难伪造", "困难陶艺", "困难木匠", "困难厨艺"]
time_12h = ["极难图书馆", "极难美术", "极难写作", "极难木匠", "极难厨艺", "极难雕塑", "极难伪造", "极难陶艺"]
time_1d = []
time_1w = []
time_skill = {"time_3s": time_3s, "time_1min": time_1min, "time_5min": time_5min, "time_10min": time_10min,
              "time_30min": time_30min,
              "time_1h": time_1h, "time_3h": time_3h, "time_12h": time_12h, "time_1d": time_1d,
              "time_1w": time_1w}

env = {"Place": place, "Weather": weather, "Time": time, "Date": date}

Fumble_SKill = 20  # 启用96以上大失败的技能水平
Critical_Success_SKill = 60  # 启用5以下大成功的技能水平

bot_personality_ = {"Critical_Success": string_list_Critical_Success, "Extreme_Success": string_list_Extreme_Success,
                    "Hard_Success": string_list_Hard_Success, "Success": string_list_Success,
                    "Failure": string_list_Failure, "Fumble": string_list_Fumble,
                    "Fumble_at_96_SKill_Level": Fumble_SKill, "Critical_at_5_SKill_Level": Critical_Success_SKill}

bot_personality_by_name_ = {"卢骰": bot_personality_, "DiceBot": bot_personality_}

Critical_Success = random.choice(bot_personality_["Critical_Success"])
Extreme_Success = random.choice(bot_personality_["Extreme_Success"])
Hard_Success = random.choice(bot_personality_["Hard_Success"])
Success = random.choice(bot_personality_["Success"])
Failure = random.choice(bot_personality_["Failure"])
Fumble = random.choice(bot_personality_["Fumble"])
Fumble_SKill = bot_personality_["Fumble_at_96_SKill_Level"]
Critical_Success_SKill = bot_personality_["Critical_at_5_SKill_Level"]


def load_settings_avatar():
    try:
        # 尝试从JSON文件加载头像路径
        with open('AppSettings/avatar_settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': '', 'DiceBot': '',
                'PL 1': ''}


def load_DiceBot_personality():
    try:
        # 尝试从JSON文件加载骰子性格路径
        with open('Bots/bot_personality_by_name.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return bot_personality_by_name_


def load_env():
    try:
        # 尝试从JSON文件加载
        with open('GameSaves/env_info.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return env


def load_settings_name():
    try:
        # 尝试加载姓名牌路径
        with open('AppSettings/name_settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': 'KP', 'DiceBot': 'DiceBot',
                'PL 1': 'PL 1'}


def load_health_data():
    try:
        # 尝试加载角色可变数值路径
        with open('GameSaves/health_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': {'HP': 0, 'MP': 0, '状态': "正常"}, 'DiceBot': {'HP': 0, 'MP': 0, '状态': "正常"},
                'PL 1': {'HP': 0, 'MP': 0, '状态': "正常"}}


def load_health_data_by_name():
    try:
        # 尝试加载角色可变数值路径
        with open('GameSaves/health_data_by_name.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': {'HP': 0, 'MP': 0, '状态': "正常"}, 'DiceBot': {'HP': 0, 'MP': 0, '状态': "正常"}}


def load_infoCanvas_data():
    try:
        # 尝试加载角色简卡图片路径
        with open('AppSettings/infoCanvas_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {}


def load_icon_data():
    try:
        # 尝试加载角色状态icon路径
        with open('GameSaves/icon_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {}


def load_infoCanvas_data_by_name():
    try:
        # 尝试加载角色简卡图片路径
        with open('AppSettings/infoCanvas_data_by_name.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {}


def load_dir_path():
    try:
        # 尝试加载角色差分目录路径
        with open('AppSettings/avatar_dir_path.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {}


def load_PL_INFO():
    try:
        # 尝试加载自定义角色数值信息
        with open('GameSaves/pl_info.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {}


def load_role_count():
    # 从配置文件加载角色数量，默认为0
    config = configparser.ConfigParser()
    config.read('AppSettings/config.ini')
    return int(config.get('Settings', 'RoleCount', fallback=0))


role_Chart_detail_demo = {
    "EDU": 0,
    "APP": 0,
    "DEX": 0,
    "STR": 0,
    "INT": 0,
    "CON": 0,
    "POW": 0,
    "SIZ": 0,
    "LUCK": 0,
    "教育": "EDU",
    "外貌": "APP",
    "敏捷": "DEX",
    "力量": "STR",
    "智力": "INT",
    "体质": "CON",
    "灵感": "INT",
    "意志": "POW",
    "体型": "SIZ",
    "幸运": "LUCK",
    "MOV": 8,
    "HP": "(CON+SIZ)/10",
    "MP": "POW/5",
    "SAN": "POW",
    "克苏鲁神话": 0,
    "克苏鲁": 0,
    "cm": 0,
    "信用": 0,
    "信用评级": 0,
    "会计": 5,
    "表演": 5,
    "美术": 5,
    "写作": 5,
    "书法": 5,
    "木匠": 5,
    "厨艺": 5,
    "舞蹈": 5,
    "歌剧": 5,
    "声乐": 5,
    "摄影": 5,
    "雕塑": 5,
    "伪造": 5,
    "陶艺": 5,
    "人类学": 1,
    "估价": 5,
    "考古学": 1,
    "魅惑": 15,
    "攀爬": 20,
    "计算机": 5,
    "计算机使用": 5,
    "电脑": 5,
    "乔装": 5,
    "闪避": "DEX/2",
    "汽车驾驶": 20,
    "电气维修": 10,
    "电子学": 1,
    "话术": 5,
    "斗殴": 25,
    "链锯": 10,
    "斧头": 25,
    "连枷": 10,
    "矛": 20,
    "剑": 20,
    "鞭子": 5,
    "弓": 15,
    "手枪": 20,
    "重武器": 10,
    "火焰喷射器": 10,
    "机枪": 10,
    "步枪": 25,
    "霰弹枪": 25,
    "步枪/霰弹枪": 25,
    "冲锋枪": 15,
    "急救": 30,
    "历史": 5,
    "恐吓": 15,
    "跳跃": 20,
    "拉丁语": 1,
    "汉语": 1,
    "日语": 1,
    "英语": 1,
    "德语": 1,
    "法语": 1,
    "西班牙语": 1,
    "意大利语": 1,
    "丹麦语": 1,
    "土著语": 1,
    "格陵兰语": 1,
    "俄语": 1,
    "母语": "EDU",
    "法律": 5,
    "图书馆": 20,
    "聆听": 20,
    "锁匠": 1,
    "机械维修": 10,
    "医学": 1,
    "博物学": 10,
    "天文学": 1,
    "生物学": 1,
    "植物学": 1,
    "化学": 1,
    "数学": 1,
    "密码学": 1,
    "工程学": 1,
    "法学": 1,
    "司法科学": 1,
    "地质学": 1,
    "气象学": 1,
    "药学": 1,
    "物理学": 1,
    "动物学": 1,
    "领航": 10,
    "神秘学": 5,
    "重型机械": 1,
    "说服": 10,
    "精神分析": 1,
    "驾驶": 1,
    "飞行器驾驶": 1,
    "船驾驶": 1,
    "心理学": 10,
    "骑术": 5,
    "科学": 1,
    "妙手": 10,
    "侦查": 25,
    "潜行": 20,
    "生存": 10,
    "游泳": 20,
    "投掷": 20,
    "追踪": 10,
    "驯兽": 5,
    "潜水": 1,
    "爆破": 1,
    "读唇": 1,
    "催眠": 1,
    "炮术": 1,
    "DB": 1,
    "#斗殴": "1D3+DB",
    "#链锯": "2D8穿",
    "#斧头": "1D8+2+DB穿",
    "#连枷": "1D8+DB",
    "#矛": "1D8+1穿",
    "#剑": "1D6+DB穿",
    "#鞭子": "1D3+DB/2",
    "#弓": "1D6+DB/2",
    "#手枪": "1D8穿",
    "#重武器": "5D10穿",
    "#火焰喷射器": "2D6+烧穿",
    "#机枪": "2D6+4穿",
    "#步枪": "1D6+1穿",
    "#霰弹枪": "4D6/2D6/1D6",
    "#冲锋枪": "1D10穿",
    "#步枪/霰弹枪": "1D6+1穿",
}


def load_Chart():
    try:
        # 尝试加载自定义角色数值信息
        with open('GameSaves/pl_Chart.json', 'r', encoding='utf-8') as file:
            # print(f"Problematic data: {file.read()}")
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {"KP": {
            "EDU": 0,
            "APP": 0,
            "DEX": 0,
            "STR": 0,
            "INT": 0,
            "CON": 0,
            "POW": 0,
            "SIZ": 0,
            "LUCK": 0,
            "教育": "EDU",
            "外貌": "APP",
            "敏捷": "DEX",
            "力量": "STR",
            "智力": "INT",
            "体质": "CON",
            "灵感": "INT",
            "意志": "POW",
            "体型": "SIZ",
            "幸运": "LUCK",
            "MOV": 8,
            "HP": "(CON+SIZ)/10",
            "MP": "POW/5",
            "SAN": "POW",
            "克苏鲁神话": 0,
            "克苏鲁": 0,
            "cm": 0,
            "信用": 0,
            "信用评级": 0,
            "会计": 5,
            "表演": 5,
            "美术": 5,
            "写作": 5,
            "书法": 5,
            "木匠": 5,
            "厨艺": 5,
            "舞蹈": 5,
            "歌剧": 5,
            "声乐": 5,
            "摄影": 5,
            "雕塑": 5,
            "伪造": 5,
            "陶艺": 5,
            "人类学": 1,
            "估价": 5,
            "考古学": 1,
            "魅惑": 15,
            "攀爬": 20,
            "计算机": 5,
            "计算机使用": 5,
            "电脑": 5,
            "乔装": 5,
            "闪避": "DEX/2",
            "汽车驾驶": 20,
            "电气维修": 10,
            "电子学": 1,
            "话术": 5,
            "斗殴": 25,
            "链锯": 10,
            "斧头": 25,
            "连枷": 10,
            "矛": 20,
            "剑": 20,
            "鞭子": 5,
            "弓": 15,
            "手枪": 20,
            "重武器": 10,
            "火焰喷射器": 10,
            "机枪": 10,
            "步枪": 25,
            "霰弹枪": 25,
            "步枪/霰弹枪": 25,
            "冲锋枪": 15,
            "急救": 30,
            "历史": 5,
            "恐吓": 15,
            "跳跃": 20,
            "拉丁语": 1,
            "汉语": 1,
            "日语": 1,
            "英语": 1,
            "德语": 1,
            "法语": 1,
            "西班牙语": 1,
            "意大利语": 1,
            "丹麦语": 1,
            "土著语": 1,
            "格陵兰语": 1,
            "俄语": 1,
            "母语": "EDU",
            "法律": 5,
            "图书馆": 20,
            "聆听": 20,
            "锁匠": 1,
            "机械维修": 10,
            "医学": 1,
            "博物学": 10,
            "天文学": 1,
            "生物学": 1,
            "植物学": 1,
            "化学": 1,
            "数学": 1,
            "密码学": 1,
            "工程学": 1,
            "法学": 1,
            "司法科学": 1,
            "地质学": 1,
            "气象学": 1,
            "药学": 1,
            "物理学": 1,
            "动物学": 1,
            "领航": 10,
            "神秘学": 5,
            "重型机械": 1,
            "说服": 10,
            "精神分析": 1,
            "驾驶": 1,
            "飞行器驾驶": 1,
            "船驾驶": 1,
            "心理学": 10,
            "骑术": 5,
            "科学": 1,
            "妙手": 10,
            "侦查": 25,
            "潜行": 20,
            "生存": 10,
            "游泳": 20,
            "投掷": 20,
            "追踪": 10,
            "驯兽": 5,
            "潜水": 1,
            "爆破": 1,
            "读唇": 1,
            "催眠": 1,
            "炮术": 1,
            "DB": 1,
            "#斗殴": "1D3+DB",
            "#链锯": "2D8穿",
            "#斧头": "1D8+2+DB穿",
            "#连枷": "1D8+DB",
            "#矛": "1D8+1穿",
            "#剑": "1D6+DB穿",
            "#鞭子": "1D3+DB/2",
            "#弓": "1D6+DB/2",
            "#手枪": "1D8穿",
            "#重武器": "5D10穿",
            "#火焰喷射器": "2D6+烧穿",
            "#机枪": "2D6+4穿",
            "#步枪": "1D6+1穿",
            "#霰弹枪": "4D6/2D6/1D6",
            "#冲锋枪": "1D10穿",
            "#步枪/霰弹枪": "1D6+1穿"
        }
            , "DiceBot": {
                "EDU": 0,
                "APP": 0,
                "DEX": 0,
                "STR": 0,
                "INT": 0,
                "CON": 0,
                "POW": 0,
                "SIZ": 0,
                "LUCK": 0,
                "教育": "EDU",
                "外貌": "APP",
                "敏捷": "DEX",
                "力量": "STR",
                "智力": "INT",
                "体质": "CON",
                "灵感": "INT",
                "意志": "POW",
                "体型": "SIZ",
                "幸运": "LUCK",
                "MOV": 8,
                "HP": "(CON+SIZ)/10",
                "MP": "POW/5",
                "SAN": "POW",
                "克苏鲁神话": 0,
                "克苏鲁": 0,
                "cm": 0,
                "信用": 0,
                "信用评级": 0,
                "会计": 5,
                "表演": 5,
                "美术": 5,
                "写作": 5,
                "书法": 5,
                "木匠": 5,
                "厨艺": 5,
                "舞蹈": 5,
                "歌剧": 5,
                "声乐": 5,
                "摄影": 5,
                "雕塑": 5,
                "伪造": 5,
                "陶艺": 5,
                "人类学": 1,
                "估价": 5,
                "考古学": 1,
                "魅惑": 15,
                "攀爬": 20,
                "计算机": 5,
                "计算机使用": 5,
                "电脑": 5,
                "乔装": 5,
                "闪避": "DEX/2",
                "汽车驾驶": 20,
                "电气维修": 10,
                "电子学": 1,
                "话术": 5,
                "斗殴": 25,
                "链锯": 10,
                "斧头": 25,
                "连枷": 10,
                "矛": 20,
                "剑": 20,
                "鞭子": 5,
                "弓": 15,
                "手枪": 20,
                "重武器": 10,
                "火焰喷射器": 10,
                "机枪": 10,
                "步枪": 25,
                "霰弹枪": 25,
                "步枪/霰弹枪": 25,
                "冲锋枪": 15,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "汉语": 1,
                "日语": 1,
                "英语": 1,
                "德语": 1,
                "法语": 1,
                "西班牙语": 1,
                "意大利语": 1,
                "丹麦语": 1,
                "土著语": 1,
                "格陵兰语": 1,
                "俄语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "天文学": 1,
                "生物学": 1,
                "植物学": 1,
                "化学": 1,
                "数学": 1,
                "密码学": 1,
                "工程学": 1,
                "法学": 1,
                "司法科学": 1,
                "地质学": 1,
                "气象学": 1,
                "药学": 1,
                "物理学": 1,
                "动物学": 1,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
                "驾驶": 1,
                "飞行器驾驶": 1,
                "船驾驶": 1,
                "心理学": 10,
                "骑术": 5,
                "科学": 1,
                "妙手": 10,
                "侦查": 25,
                "潜行": 20,
                "生存": 10,
                "游泳": 20,
                "投掷": 20,
                "追踪": 10,
                "驯兽": 5,
                "潜水": 1,
                "爆破": 1,
                "读唇": 1,
                "催眠": 1,
                "炮术": 1,
                "DB": 1,
                "#斗殴": "1D3+DB",
                "#链锯": "2D8穿",
                "#斧头": "1D8+2+DB穿",
                "#连枷": "1D8+DB",
                "#矛": "1D8+1穿",
                "#剑": "1D6+DB穿",
                "#鞭子": "1D3+DB/2",
                "#弓": "1D6+DB/2",
                "#手枪": "1D8穿",
                "#重武器": "5D10穿",
                "#火焰喷射器": "2D6+烧穿",
                "#机枪": "2D6+4穿",
                "#步枪": "1D6+1穿",
                "#霰弹枪": "4D6/2D6/1D6",
                "#冲锋枪": "1D10穿",
                "#步枪/霰弹枪": "1D6+1穿"}
            , "PL 1": {
                "EDU": 0,
                "APP": 0,
                "DEX": 0,
                "STR": 0,
                "INT": 0,
                "CON": 0,
                "POW": 0,
                "SIZ": 0,
                "LUCK": 0,
                "教育": "EDU",
                "外貌": "APP",
                "敏捷": "DEX",
                "力量": "STR",
                "智力": "INT",
                "体质": "CON",
                "灵感": "INT",
                "意志": "POW",
                "体型": "SIZ",
                "幸运": "LUCK",
                "MOV": 8,
                "HP": "(CON+SIZ)/10",
                "MP": "POW/5",
                "SAN": "POW",
                "克苏鲁神话": 0,
                "克苏鲁": 0,
                "cm": 0,
                "信用": 0,
                "信用评级": 0,
                "会计": 5,
                "表演": 5,
                "美术": 5,
                "写作": 5,
                "书法": 5,
                "木匠": 5,
                "厨艺": 5,
                "舞蹈": 5,
                "歌剧": 5,
                "声乐": 5,
                "摄影": 5,
                "雕塑": 5,
                "伪造": 5,
                "陶艺": 5,
                "人类学": 1,
                "估价": 5,
                "考古学": 1,
                "魅惑": 15,
                "攀爬": 20,
                "计算机": 5,
                "计算机使用": 5,
                "电脑": 5,
                "乔装": 5,
                "闪避": "DEX/2",
                "汽车驾驶": 20,
                "电气维修": 10,
                "电子学": 1,
                "话术": 5,
                "斗殴": 25,
                "链锯": 10,
                "斧头": 25,
                "连枷": 10,
                "矛": 20,
                "剑": 20,
                "鞭子": 5,
                "弓": 15,
                "手枪": 20,
                "重武器": 10,
                "火焰喷射器": 10,
                "机枪": 10,
                "步枪": 25,
                "霰弹枪": 25,
                "步枪/霰弹枪": 25,
                "冲锋枪": 15,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "汉语": 1,
                "日语": 1,
                "英语": 1,
                "德语": 1,
                "法语": 1,
                "西班牙语": 1,
                "意大利语": 1,
                "丹麦语": 1,
                "土著语": 1,
                "格陵兰语": 1,
                "俄语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "天文学": 1,
                "生物学": 1,
                "植物学": 1,
                "化学": 1,
                "数学": 1,
                "密码学": 1,
                "工程学": 1,
                "法学": 1,
                "司法科学": 1,
                "地质学": 1,
                "气象学": 1,
                "药学": 1,
                "物理学": 1,
                "动物学": 1,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
                "驾驶": 1,
                "飞行器驾驶": 1,
                "船驾驶": 1,
                "心理学": 10,
                "骑术": 5,
                "科学": 1,
                "妙手": 10,
                "侦查": 25,
                "潜行": 20,
                "生存": 10,
                "游泳": 20,
                "投掷": 20,
                "追踪": 10,
                "驯兽": 5,
                "潜水": 1,
                "爆破": 1,
                "读唇": 1,
                "催眠": 1,
                "炮术": 1,
                "DB": 1,
                "#斗殴": "1D3+DB",
                "#链锯": "2D8穿",
                "#斧头": "1D8+2+DB穿",
                "#连枷": "1D8+DB",
                "#矛": "1D8+1穿",
                "#剑": "1D6+DB穿",
                "#鞭子": "1D3+DB/2",
                "#弓": "1D6+DB/2",
                "#手枪": "1D8穿",
                "#重武器": "5D10穿",
                "#火焰喷射器": "2D6+烧穿",
                "#机枪": "2D6+4穿",
                "#步枪": "1D6+1穿",
                "#霰弹枪": "4D6/2D6/1D6",
                "#冲锋枪": "1D10穿",
                "#步枪/霰弹枪": "1D6+1穿"
            }}
    except json.JSONDecodeError as e:
        print(f"Error in JSON decoding: {e}")
        print(f"Problematic data: {file.read()}")


def load_Chart_at_name():
    try:
        # 按姓名牌加载自定义角色数值信息
        with open('GameSaves/pl_Chart_at_name.json', 'r', encoding='utf-8') as file:
            # print(f"Problematic data: {file.read()}")
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {"KP": {
            "EDU": 0,
            "APP": 0,
            "DEX": 0,
            "STR": 0,
            "INT": 0,
            "CON": 0,
            "POW": 0,
            "SIZ": 0,
            "LUCK": 0,
            "教育": "EDU",
            "外貌": "APP",
            "敏捷": "DEX",
            "力量": "STR",
            "智力": "INT",
            "体质": "CON",
            "灵感": "INT",
            "意志": "POW",
            "体型": "SIZ",
            "幸运": "LUCK",
            "MOV": 8,
            "HP": "(CON+SIZ)/10",
            "MP": "POW/5",
            "SAN": "POW",
            "克苏鲁神话": 0,
            "克苏鲁": 0,
            "cm": 0,
            "信用": 0,
            "信用评级": 0,
            "会计": 5,
            "表演": 5,
            "美术": 5,
            "写作": 5,
            "书法": 5,
            "木匠": 5,
            "厨艺": 5,
            "舞蹈": 5,
            "歌剧": 5,
            "声乐": 5,
            "摄影": 5,
            "雕塑": 5,
            "伪造": 5,
            "陶艺": 5,
            "人类学": 1,
            "估价": 5,
            "考古学": 1,
            "魅惑": 15,
            "攀爬": 20,
            "计算机": 5,
            "计算机使用": 5,
            "电脑": 5,
            "乔装": 5,
            "闪避": "DEX/2",
            "汽车驾驶": 20,
            "电气维修": 10,
            "电子学": 1,
            "话术": 5,
            "斗殴": 25,
            "链锯": 10,
            "斧头": 25,
            "连枷": 10,
            "矛": 20,
            "剑": 20,
            "鞭子": 5,
            "弓": 15,
            "手枪": 20,
            "重武器": 10,
            "火焰喷射器": 10,
            "机枪": 10,
            "步枪": 25,
            "霰弹枪": 25,
            "步枪/霰弹枪": 25,
            "冲锋枪": 15,
            "急救": 30,
            "历史": 5,
            "恐吓": 15,
            "跳跃": 20,
            "拉丁语": 1,
            "汉语": 1,
            "日语": 1,
            "英语": 1,
            "德语": 1,
            "法语": 1,
            "西班牙语": 1,
            "意大利语": 1,
            "丹麦语": 1,
            "土著语": 1,
            "格陵兰语": 1,
            "俄语": 1,
            "母语": "EDU",
            "法律": 5,
            "图书馆": 20,
            "聆听": 20,
            "锁匠": 1,
            "机械维修": 10,
            "医学": 1,
            "博物学": 10,
            "天文学": 1,
            "生物学": 1,
            "植物学": 1,
            "化学": 1,
            "数学": 1,
            "密码学": 1,
            "工程学": 1,
            "法学": 1,
            "司法科学": 1,
            "地质学": 1,
            "气象学": 1,
            "药学": 1,
            "物理学": 1,
            "动物学": 1,
            "领航": 10,
            "神秘学": 5,
            "重型机械": 1,
            "说服": 10,
            "精神分析": 1,
            "驾驶": 1,
            "飞行器驾驶": 1,
            "船驾驶": 1,
            "心理学": 10,
            "骑术": 5,
            "科学": 1,
            "妙手": 10,
            "侦查": 25,
            "潜行": 20,
            "生存": 10,
            "游泳": 20,
            "投掷": 20,
            "追踪": 10,
            "驯兽": 5,
            "潜水": 1,
            "爆破": 1,
            "读唇": 1,
            "催眠": 1,
            "炮术": 1,
            "DB": 1,
            "#斗殴": "1D3+DB",
            "#链锯": "2D8穿",
            "#斧头": "1D8+2+DB穿",
            "#连枷": "1D8+DB",
            "#矛": "1D8+1穿",
            "#剑": "1D6+DB穿",
            "#鞭子": "1D3+DB/2",
            "#弓": "1D6+DB/2",
            "#手枪": "1D8穿",
            "#重武器": "5D10穿",
            "#火焰喷射器": "2D6+烧穿",
            "#机枪": "2D6+4穿",
            "#步枪": "1D6+1穿",
            "#霰弹枪": "4D6/2D6/1D6",
            "#冲锋枪": "1D10穿",
            "#步枪/霰弹枪": "1D6+1穿",
            "_AvatarPath": ""
        }
            , "DiceBot": {
                "EDU": 0,
                "APP": 0,
                "DEX": 0,
                "STR": 0,
                "INT": 0,
                "CON": 0,
                "POW": 0,
                "SIZ": 0,
                "LUCK": 0,
                "教育": "EDU",
                "外貌": "APP",
                "敏捷": "DEX",
                "力量": "STR",
                "智力": "INT",
                "体质": "CON",
                "灵感": "INT",
                "意志": "POW",
                "体型": "SIZ",
                "幸运": "LUCK",
                "MOV": 8,
                "HP": "(CON+SIZ)/10",
                "MP": "POW/5",
                "SAN": "POW",
                "克苏鲁神话": 0,
                "克苏鲁": 0,
                "cm": 0,
                "信用": 0,
                "信用评级": 0,
                "会计": 5,
                "表演": 5,
                "美术": 5,
                "写作": 5,
                "书法": 5,
                "木匠": 5,
                "厨艺": 5,
                "舞蹈": 5,
                "歌剧": 5,
                "声乐": 5,
                "摄影": 5,
                "雕塑": 5,
                "伪造": 5,
                "陶艺": 5,
                "人类学": 1,
                "估价": 5,
                "考古学": 1,
                "魅惑": 15,
                "攀爬": 20,
                "计算机": 5,
                "计算机使用": 5,
                "电脑": 5,
                "乔装": 5,
                "闪避": "DEX/2",
                "汽车驾驶": 20,
                "电气维修": 10,
                "电子学": 1,
                "话术": 5,
                "斗殴": 25,
                "链锯": 10,
                "斧头": 25,
                "连枷": 10,
                "矛": 20,
                "剑": 20,
                "鞭子": 5,
                "弓": 15,
                "手枪": 20,
                "重武器": 10,
                "火焰喷射器": 10,
                "机枪": 10,
                "步枪": 25,
                "霰弹枪": 25,
                "步枪/霰弹枪": 25,
                "冲锋枪": 15,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "汉语": 1,
                "日语": 1,
                "英语": 1,
                "德语": 1,
                "法语": 1,
                "西班牙语": 1,
                "意大利语": 1,
                "丹麦语": 1,
                "土著语": 1,
                "格陵兰语": 1,
                "俄语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "天文学": 1,
                "生物学": 1,
                "植物学": 1,
                "化学": 1,
                "数学": 1,
                "密码学": 1,
                "工程学": 1,
                "法学": 1,
                "司法科学": 1,
                "地质学": 1,
                "气象学": 1,
                "药学": 1,
                "物理学": 1,
                "动物学": 1,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
                "驾驶": 1,
                "飞行器驾驶": 1,
                "船驾驶": 1,
                "心理学": 10,
                "骑术": 5,
                "科学": 1,
                "妙手": 10,
                "侦查": 25,
                "潜行": 20,
                "生存": 10,
                "游泳": 20,
                "投掷": 20,
                "追踪": 10,
                "驯兽": 5,
                "潜水": 1,
                "爆破": 1,
                "读唇": 1,
                "催眠": 1,
                "炮术": 1,
                "DB": 1,
                "#斗殴": "1D3+DB",
                "#链锯": "2D8穿",
                "#斧头": "1D8+2+DB穿",
                "#连枷": "1D8+DB",
                "#矛": "1D8+1穿",
                "#剑": "1D6+DB穿",
                "#鞭子": "1D3+DB/2",
                "#弓": "1D6+DB/2",
                "#手枪": "1D8穿",
                "#重武器": "5D10穿",
                "#火焰喷射器": "2D6+烧穿",
                "#机枪": "2D6+4穿",
                "#步枪": "1D6+1穿",
                "#霰弹枪": "4D6/2D6/1D6",
                "#冲锋枪": "1D10穿",
                "#步枪/霰弹枪": "1D6+1穿",
                "_AvatarPath": ""
            }
        }
    except json.JSONDecodeError as e:
        print(f"Error in JSON decoding: {e}")
        print(f"Problematic data: {file.read()}")


role_Chart = load_Chart().copy()
role_Chart_at_name = load_Chart_at_name().copy()
bot_personality_by_name = load_DiceBot_personality()
adv_comment = ""


# logging.debug("Variable value: %s", role_Chart_at_name)

class ChatApp:
    def __init__(self, root):
        self.root = root

        # 一系列字符串
        string_list_encouragement = [" - Made by 咩碳@mebily & ChatGPT", " - 人品100！这就是全部的陛下庇护！", " - 陛下所言甚是/陶醉", " - "
                                                                                                               "你生而有翼，为何竟愿一生匍匐前进，形如虫蚁？",
                                     " - 好的国王千篇一律 坏的国王万里挑一", " - 变成卢学家后能看自己的头衔互相贴贴吗", " - 导演因染新冠七天没到片场发现剧组被新来的演员带去溜冰",
                                     " - 你的Bug我的Bug好像都一样", " - 新约是不是就像陛下一样可爱", " - 傻卢，罚你一天不见陛下",
                                     " - 送你默默饮泪的泪城纪念雨景球", " - 送你向着它告白就能获得陛下碎片的勇气流星", " - 陛下正在搭建他的绝对帝国", " - 一半的陛下庇护",
                                     " - 陛下那么肥干什么，没有陛下的气质",
                                     " - 陛下很便宜的", " - 情人眼里出陛下", " - 陛下很好养活的", " - 有王吗？", " - 只能说没有陛下漂亮",
                                     ' - "你们都没有我懂陛下！"', " - 就像陛下",
                                     ' - "我是真的对陛下没感觉"',
                                     " - 曾经有一只超可爱的陛下在我面前，我却没有珍惜", " - 感觉陛下有危险！", " - 这个陛下救不了我", " - 成为陛下",
                                     ' - "有毛的都被我干掉了"', " - 陛下，本命链顶端的男人", " - 王学家和卢卢跳舞被陛下追着打",
                                     " - 陛下笑着吃了这个蛋糕，他久违的微笑也让我开心了起来", " - 下午好，今天的小骑士是要油炸呢还是要清蒸呢",
                                     " - 我需要陛下来平息我胸中怒火/翻进白宫", " - 噢可爱的生灵，请告诉我陛下为什么这么美好", " - 咩碳睡了！咩碳希望能梦到陛下！/大声",
                                     " - 有时候，只需一个代名词就能拯救别人一天的好心情。—— 王学家咩碳",
                                     " - 沃姆是不能飞的，所以你一说飞天沃姆，我想到的是被打飞的沃姆你知道吗", " - INTJ可不会被绊倒 —— 会被ENTJ绊倒",
                                     " - 我不懂，我没有背叛过陛下", " - 陛下束紧了我的缰绳，让我无法发疯", " - 陛下，您离遍布生物圈又近了一步",
                                     " - 突然感受到了人类的可爱，我祝福人类（拿着橄榄枝洒圣水）", " - 我去带陛下做核酸", " - 白宫：警惕蛾族打旧日之光牌",
                                     " - 给我一个世设，我能适配整只陛下", " - 死了也是死在陛下怀里", " - 陛下一笑倾城，圣巢虫子都跳虚空自杀以保陛下周全",
                                     " - 太久不上供 就会被踢出白宫", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "", "", "", "", ""]
        # 从列表中随机选择一个字符串
        encouragement = random.choice(string_list_encouragement)
        self.root.title("自嗨团 v1.00" + encouragement)

        # 设置图标
        self.root.iconbitmap("AppSettings/icon.ico")

        # 其他窗口内容
        # self.label = tk.Label(root, text="Hello, Tkinter!")

        # 绑定回车键和Alt+回车键
        root.bind("<Return>", lambda event: self.send_message(self.current_role.get()))
        root.bind("<Alt-Return>", lambda event: self.insert_newline())
        root.bind("<Control-Return>", self.newline_on_ctrl_enter)

        #self.chat_log_huozi = ""

        self.babel_data = {}
        self.Iconcanvas = {}
        self.Icon_on_avatar = {}
        self.canvas_icon_animate = {}
        self.image_references_on_Avatar = {}
        self.frames_avatar = {}
        self.current_frame_avatar = {}
        self.frames_icon = {}
        self.current_frame_icon = {}
        self.frames_map = {}
        self.current_frame_map = {}
        self.frames_icon_on_canvas = {}
        self.current_frame_icon_on_canvas = {}

        self.infoCanvas_data = load_infoCanvas_data()
        self.infoCanvas_data_by_name = load_infoCanvas_data_by_name()

        self.health_data = load_health_data()
        self.health_data_by_name = load_health_data_by_name()

        self.role_Icon_paths = load_icon_data()

        self.NowBGM = ["全部"]
        self.NowImage = []
        self.NowEffect = []
        self.NowDialogState = True
        self.NowCharacterEffect = []

        self.role_dir_path = load_dir_path()
        for role in self.role_dir_path:
            if "Images/AvatarImages" not in self.role_dir_path[role]:
                self.role_dir_path[role] = "Images/AvatarImages"

        # 初始化角色列表
        self.role_count = load_role_count()
        self.roles = ["KP", "DiceBot", "PL 1"]
        self.enemy_matches = {}

        # 初始化当前聚焦的头像和文本框
        self.current_role = tk.StringVar(value=self.roles[0])
        self.highlighted_role = self.current_role

        # 初始化TRPG模块
        self.trpg_module = TRPGModule(self, root)
        # self.COC_module = COCModule()
        # 添加按钮，用于展开或缩进掷骰按钮和信息面板
        toggle_button = tk.Button(self.root, text="展开/缩进\nTRPG模块", command=self.toggle_trpg)
        toggle_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.trpg_toggle = "off"

        global date
        global time
        global place
        global weather
        # 初始化时间、地点记录栏
        self.env = load_env()
        date = self.env["Date"]
        time = self.env["Time"]
        place = self.env["Place"]
        weather = self.env["Weather"]
        self.time_log = tk.Text(root, wrap=tk.WORD, width=10, height=0)
        self.time_log.grid(row=3, column=2, padx=10, pady=10, rowspan=3, sticky="nsew")
        self.time_log.insert(tk.END, "【时间】" + time.upper() + "【地点】" + place + "【天气】" + weather + "【日期】" + date)
        self.time_log.bind("<Button-3>", lambda event: self.refreshTime)

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")
        # 在 Text 组件中插入初始文本
        initial_text = "Updates：\n更新了TRPG掷骰模块:联合骰、SC、优劣势、补正骰、对抗骰、武器伤害Built-in，更新了自定义数值/笔记栏，" \
                       ".st存入Json数据库，技能成长自动判定，导出技能st，骰子性格（结果播报语句。但因为不会出现在log里，所以基本也没啥影响...），时间模块，#Armor，推理信息库" \
                       "，支持gif啦，载入新立绘时自动插入活字命令，" \
                       "巴别塔（看控制台），装载NPC模板，保留栏位名称并读取某一模板\n" \
                       "\nTodo:" \
                       "\n--计算" \
                       "\n自动加减基础数值（MP、HP）（不这么做是因为要有理由Focus再UnFocus笔记栏来保存..但已经设置了health_data了，就看怎么用方便）" \
                       "\n--features" \
                       "\n优化：NPC列表" \
                       "\n优化推理信息库-计算器直接显示在共用库栏位（新建一个Frame，避免无法发布到另一个窗口），精简框架，不要占满屏" \
                       "\n牌堆；实用命令，比如抽人 .who ABCD等 (基本坑，暂时先去用正经骰娘Bot吧)" \
                       "\n输出染色HTML，骰子性格：针对每个技能单独comment(坑)" \
                       "\n优化地图，实现实时同步数值和时间，Canvas保存" \
                       "\n--bugs\n复杂掷骰算式（多个不同面骰子+常数）优化\n补正骰优化\n对抗骰优化\n武器伤害Built-in优化\n自动加减基础数值（SAN）优化\n巴别塔新增角色BUG" \
                       "\nArmor显示优化\n小地图图形缩放BUG\n" \
                       "Tips:\n.st HP、MP时均修改的是上限，修改实时hp/mp需使用掷骰栏掷骰，或者直接修改\n使用 .st#斗殴@1D3+5 " \
                       "来载入武器伤害公式\n小地图可用于追逐、探索和战斗，更好的战斗体验可以结合CCF。小地图中的M是MOV，不是MP\nNPC活动也可以用程序多开+复制粘贴，但如此就无法无缝RP" \
                       "（而且战斗时无法触发PC的Armor显示、无法同步计算时间等），建议KP栏装载至少一个常用NPC，或者保证留有NPC栏位。\n一些复杂操作：\n[右键姓名牌] 选择简卡图片\n[" \
                       "左键头像栏] 选择头像\n[左键Icon栏] 选择状态Icon\n[右键头像栏/Icon栏] " \
                       "状态Icon叠加/撤销\n[左键@] 在Focus文本框插入@角色名\n[右键@] 插入活字命令\n如果没有头像和状态Icon，就会缩进到Frame内的左侧，左上是状态，左中是头像\n" \
                       "===以上可删除===\n\n"
        self.chat_log.insert(tk.END, initial_text)

        # 创建按钮，点击按钮时调用 open_new_window 函数
        new_window_button = tk.Button(root, text="推理信息", command=self.open_new_window)
        new_window_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # 创建按钮，点击按钮时调用 add_NPC 函数
        load_NPC_button = tk.Button(root, text="装载NPC至栏位", command=self.Add_NPC)
        load_NPC_button.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

        # 初始化输出聊天LOG按钮
        output_button = tk.Button(root, text="输出聊天LOG", command=self.output_chat_log)
        output_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # 初始化输出HTML按钮
        # output_html_button = tk.Button(root, text="输出HTML(施工中)", command=self.output_html_log)
        # output_html_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # 初始化角色对应的文字输入框、发送按钮和角色名编辑
        self.role_entries_frame = {}
        self.role_entries = {}
        self.role_entries_name = {}
        self.role_entries_roll = {}
        self.role_roll_button = {}
        self.role_values_tags = {}  # 新增保存数值的tag
        self.role_values_entry = {}
        self.role_values_tags_text = {}  # 新增保存的数值

        for role in self.roles:
            self.role_entries_name[role] = role
            self.image_references_on_Avatar[role] = []
            self.canvas_icon_animate[role] = ""
            self.frames_avatar[role] = []
            self.current_frame_avatar[role] = []
            self.frames_icon[role] = []
            self.current_frame_icon[role] = []
            self.frames_map[role] = []
            self.current_frame_map[role] = []
            self.frames_icon_on_canvas[role] = []
            self.current_frame_icon_on_canvas[role] = []
            if load_settings_name() != "":
                self.role_entries_name = load_settings_name()  # 从文件加载设置
        babel(self)

        self.create_role_frames()
        for i in range(self.role_count):
            self.add_role_init()

        # 为每个文本框绑定焦点变化事件
        for role in self.roles:
            entry = self.role_entries[role]
            entry.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))
        for role in self.roles:
            entry_roll = self.role_entries_roll[role]
            entry_roll.bind("<FocusIn>", lambda event2, role=role: self.bind_enter_to_send_roll(event2, role))

        # 初始化删除角色按钮
        delete_role_button = tk.Button(root, text="删除角色", command=self.delete_role)
        delete_role_button.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # 初始化添加角色按钮
        add_role_button = tk.Button(root, text="添加角色", command=self.add_role)
        add_role_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        for names in bot_personality_by_name:
            if names == self.role_entries_name["DiceBot"]:
                global Critical_Success
                global Extreme_Success
                global Hard_Success
                global Success
                global Failure
                global Fumble
                global Fumble_SKill
                global Critical_Success_SKill
                bot_personality = bot_personality_by_name[names]
                Critical_Success = random.choice(bot_personality["Critical_Success"])
                Extreme_Success = random.choice(bot_personality["Extreme_Success"])
                Hard_Success = random.choice(bot_personality["Hard_Success"])
                Success = random.choice(bot_personality["Success"])
                Failure = random.choice(bot_personality["Failure"])
                Fumble = random.choice(bot_personality["Fumble"])
                Fumble_SKill = bot_personality["Fumble_at_96_SKill_Level"]
                Critical_Success_SKill = bot_personality["Critical_at_5_SKill_Level"]
                self.role_entries["DiceBot"].insert("1.0", f"已录入[{names}]的性格！")
                break

    def display_image(self, file_path, text, name=None, seconds=-1):
        if file_path:
            new_window_HO = tk.Toplevel(root)
            new_window_HO.title("图片展示：" + text)
            # label = tk.Label(new_window_HO, text=text)
            # label.pack()
            image_references = []  # Add this list attribute to store references to images
            # 创建 Canvas 组件
            image = Image.open(file_path)
            # 获取图像的宽和高
            width, height = image.size
            canvas_w = int(width/3)
            canvas_h = int(height/3)
            canvas_HO = tk.Canvas(new_window_HO, width=canvas_w, height=canvas_h, bg="white")
            canvas_HO.pack(fill=tk.BOTH, expand=True)
            image = image.resize((canvas_w, canvas_h), Image.LANCZOS)  # 调整头像大小
            tk_image = ImageTk.PhotoImage(image)
            canvas_HO.create_image(canvas_w/2, canvas_h/2, image=tk_image, tags="image")
            canvas_HO.image = tk_image
            # 监听窗口大小变化事件
            #canvas_HO.bind("<Configure>", lambda event: self.resize_image(canvas_HO, tk_image))
            new_window_HO.protocol("WM_DELETE_WINDOW", lambda: self.on_kill_image(new_window_HO, text, name))

    def resize_image(self, canvas, tk_image):
        canvas.delete("image")  # 删除之前的图片
        width = canvas.winfo_width()  # 获取Canvas的新宽度
        height = canvas.winfo_height()  # 获取Canvas的新高度
        resized_image = tk_image.subsample(int(tk_image.width() / width), int(tk_image.height() / height))  # 缩放图片
        canvas.create_image(0, 0, anchor=tk.NW, image=resized_image, tags="image")  # 在Canvas上绘制调整后的图片
        canvas.image = resized_image  # 更新图片引用

    def on_kill_image(self,window, type, name):
        if type == "HandOut":
            if name in self.NowImage:
                self.NowImage.remove(name)
                content = f"【撤除图片】{name}"

                # 搜索包含 ">>>" 的行的起始索引
                start_index = "1.0"
                while True:
                    match_index = self.chat_log.search(">>>", start_index, tk.END)
                    if not match_index:
                        break
                    # 删除包含 ">>>" 的行
                    line_start = self.chat_log.index(match_index)
                    line_end = self.chat_log.index(match_index + " lineend")
                    self.chat_log.delete(line_start, line_end)
                    # 更新搜索的起始位置
                    start_index = line_end

                self.chat_log.insert(tk.END,
                                     f'活字命令 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n{content}\n\n')
                #self.chat_log_huozi = self.chat_log_huozi + f"{content}\n\n"
                self.chat_log.yview(tk.END)
        window.destroy()

    def kill_image(self,name):
        pass
        # audio_list[name].stop()
        # audio_list.pop(name)

    def refreshTime(self):
        log = self.time_log.get("1.0", tk.END)
        self.chat_log.insert(tk.END,
                             f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n{log}\n\n')
        #self.chat_log_huozi = self.chat_log_huozi + f"<{self.role_entries_name['DiceBot']}>{log}\n"
        # 滚动到最底部
        self.chat_log.yview(tk.END)

    def create_role_frames(self):
        num_cols = 3
        for idx, role in enumerate(self.roles):
            row = idx % num_cols
            col = idx // num_cols
            self.create_role_frame(role, row, col)

        # 自动调整列宽
        for i in range(num_cols + 2):
            self.root.columnconfigure(i, weight=1)

    def create_role_frame(self, role, row, col):

        if role not in role_Chart:
            role_Chart[role] = role_Chart_detail_demo.copy()

        frame = tk.LabelFrame(self.root, text=role, relief=tk.GROOVE)
        frame.grid(row=row, column=col + 2, padx=10, pady=10, sticky="nsew")
        self.role_entries_frame[role] = frame
        # 初始化头像路径
        self.role_avatar_paths = {}
        if load_settings_avatar() != "":
            self.role_avatar_paths = load_settings_avatar()  # 从文件加载设置
        # 头像点击事件
        # self.avatar_click_event = None

        # 每个角色的消息框
        entry = tk.Text(frame, wrap=tk.WORD, width=30, height=3)
        entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.role_entries[role] = entry
        # 加载并显示头像
        self.load_and_display_avatar(role, frame)
        self.load_and_display_icon(role, frame)

        if role == "DiceBot":
            # 在 Text 组件中插入初始文本
            initial_text = "复制Bot消息至此并发送，或：\n【掷骰】点击每个角色的掷骰按钮进行掷骰，公式栏填写公式或技能，留空默认1d100" \
                           "\n【优劣势】命令头部的+/-表示优劣势（++意志30）" \
                           "\n【补正骰】命令后部的+/-表示补正（意志+30）" \
                           "\n【联合骰】技能1+技能2+技能3..." \
                           "\n【对抗骰】在角色消息栏@其他对抗人 并点击掷骰" \
                           "\n【全体掷骰】保持焦点在Bot消息框，点击Bot的掷骰按钮" \
                           "\n【暗骰】保持焦点在暗骰角色的消息框，点击Bot的掷骰按钮（公式取自暗骰角色）" \
                           "\n【.st】输入后点击发送按钮或回车（而不是掷骰按钮）" \
                           "\n【掷骰原因】消息栏填写掷骰原因，可以包括技能文字点掷骰按钮来触发检定（例如“我使用r斗殴击晕敌人”）" \
                           "\n===以上可删除===\n\n"
            self.role_entries[role].insert(tk.END, initial_text)
        if role == "KP":
            initial_text = "如何创建NPC模板：" \
                           "\n0.如果巴别塔报错，先关闭巴别塔（把文件名改一下就行）" \
                           "\n1.创建新角色，更名为模板名（比如“基本怪物”、“基本人类”、“基本邪教徒”、“Muffin Stinger”（姓名也可以在创建 / 导入模板后再改））" \
                           "\n2. 。st录入数值" \
                           "\n3.重启程序（关闭程序时会自动保存）" \
                           "\n4.在KP栏把自己的名字改成模板名，会自动录入数值(即时数值例如HP、MP变化不会录入)。如果不想更改KP，新建一个NPC栏来用也行，最好不用骰子栏，会出奇怪BUG" \
                           "。或者多开程序也行，但注意一定要分开保存程序数据文件，被覆盖就会哭哭。" \
                           "\n5.如果要重新启用巴别塔，删除新创建的角色，改回第0步的文件名（除非把新添加的角色也加入巴别塔）" \
                           "\n===以上可删除===\n\n"
            self.role_entries[role].insert(tk.END, initial_text)

            # 创建数值tag，显示数值
        role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
        SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        POW = role_Chart_detail.get("POW")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        DB = role_Chart_detail.get("DB")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        if "#SAN" in role_Chart_detail:
            _SAN = role_Chart_detail.get("#SAN")
        else:
            _SAN = 100
        entry2 = tk.Text(frame, wrap=tk.WORD, width=10, height=6)
        entry2.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        value_tag = f"{role}_values_tag"
        self.role_values_tags[role] = value_tag
        entry2.tag_config(value_tag, justify=tk.LEFT)
        self.role_values_tags_text = load_PL_INFO()
        if role not in self.role_values_tags_text:
            entry2.insert(tk.END, f'{SAN}/{_SAN}:SAN\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB',
                          value_tag)
        else:
            entry2.insert(tk.END, self.role_values_tags_text[role], value_tag)
        self.role_values_entry[role] = entry2
        # 为每个文本框绑定焦点变化事件
        entry2.bind("<FocusOut>", lambda event, r=role, t=entry2: self.save_info(event, role))

        send_button = tk.Button(frame, text="发送", command=lambda role=role: self.send_message(role))
        send_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        label = tk.Label(frame, text=role, relief=tk.FLAT,
                         font=("Times New Roman", 16, "bold"))  # flat, groove, raised, ridge, solid, or sunken
        label.grid(row=0, column=1, pady=0, sticky="nsew")
        label.bind("<Button-1>", lambda event, role=role, label=label: self.edit_role_name(event, role, label))
        label.bind("<Button-3>", lambda event, role=role: self.on_avatar_click(role))
        label.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
        label.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

        if self.role_entries_name[role] != role:
            label.configure(text=self.role_entries_name[role])
            # print(self.role_entries_name[role])

        label = tk.Label(frame, text="@", relief=tk.FLAT)
        label.grid(row=2, column=0, pady=0, sticky="nsew")
        # label点击事件绑定
        label.bind("<Button-1>", lambda event, role=role: self.on_at_click(role))
        label.bind("<Button-3>", lambda event, role=role: self.on_at_right_click(role))

        # 添加选择头像按钮
        # choose_avatar_button = tk.Button(frame, text="选择简卡", command=lambda role=role: self.on_avatar_click(role))
        # choose_avatar_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # 添加保存名牌按钮
        # choose_avatar_button = tk.Button(frame, text="保存", command=lambda role=role: self.choose_avatar(role))
        # choose_avatar_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        # 添加掷骰按钮和面数输入框
        entry_roll = tk.Text(frame, wrap=tk.WORD, width=3, height=1)
        entry_roll.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.role_entries_roll[role] = entry_roll
        roll_button = tk.Button(frame, text="掷骰", command=lambda r=role: self.get_and_roll(r))
        roll_button.grid(row=2, column=2, padx=5, pady=5)
        self.role_roll_button[role] = roll_button
        # 在 Text 组件中插入初始文本
        initial_text = "1d100"
        self.role_entries_roll[role].insert(tk.END, initial_text)

    def apng_to_gif(self, apng_file, gif_file):
        # 使用 apng2gif 工具将 APNG 转换成 GIF
        subprocess.run(["apng2gif", apng_file, gif_file])
        return gif_file

    def save_info(self, event, role):
        self.role_values_tags_text[role] = self.role_values_entry[role].get("1.0", tk.END).strip()
        # print(self.role_values_entry[role].get("1.0", tk.END).strip())

    def toggle_trpg(self):
        # 展开或缩进掷骰按钮和信息面板
        if self.trpg_toggle == "off":
            for role in self.roles:
                self.role_entries_roll[role].grid_forget()  # 缩进
                self.role_roll_button[role].grid_forget()
                self.role_values_entry[role].grid_forget()
            self.trpg_toggle = "on"
        else:
            for role in self.roles:
                self.role_entries_roll[role].grid(row=0, column=2, padx=5, pady=5, sticky="nsew")  # 展开
                self.role_roll_button[role].grid(row=2, column=2, padx=5, pady=5)
                self.role_values_entry[role].grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
            self.trpg_toggle = "off"

    def send_message(self, role):
        global role_Chart_at_name

        role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
        # 搜索包含 ">>>" 的行的起始索引
        start_index = "1.0"
        while True:
            match_index = self.chat_log.search(">>>", start_index, tk.END)
            if not match_index:
                break
            # 删除包含 ">>>" 的行
            line_start = self.chat_log.index(match_index)
            line_end = self.chat_log.index(match_index + " lineend")
            self.chat_log.delete(line_start, line_end)
            # 更新搜索的起始位置
            start_index = line_end

        message = self.role_entries[role].get("1.0", tk.END).strip()
        if message:
            timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            log = f"{self.role_entries_name[role]} {timestamp}\n{message}\n\n"  # 不加引号
            if message.startswith(".st") or message.startswith("。st"):
                message = message[len("st") + 1:].strip()

                parts_skill = re.findall(r'([\u4e00-\u9fa5a-zA-Z\s]+)(\d+)', message)
                if ("+" or "-" or "*" or "/") in message and "#" not in message:
                    parts = re.findall(r'([#+]?[\u4e00-\u9fa5a-zA-Z\s]+)([-+*/^])(\d+)', message)
                    print(parts)
                    # print(str(parts[0][0]).upper())
                    if parts and len(parts) > 0 and len(parts[0]) > 0:
                        role_Chart[role][str(parts[0][0]).upper()] = eval(
                            str(role_Chart_detail[str(parts[0][0]).upper()]) + parts[0][1] + parts[0][2])
                    # print(str(parts[0][0]).upper()+":"+str(role_Chart[role][str(parts[0][0]).upper()]))
                    self.chat_log.insert(tk.END,
                                         f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的【{str(parts[0][0]).upper()}】变更为{str(role_Chart[role][str(parts[0][0]).upper()])}\n\n')
                    #self.chat_log_huozi = self.chat_log_huozi + f"<{self.role_entries_name['DiceBot']}>【{self.role_entries_name[role]}】的【{str(parts[0][0]).upper()}】变更为{str(role_Chart[role][str(parts[0][0]).upper()])}\n"
                    # 滚动到最底部
                    self.chat_log.yview(tk.END)
                else:
                    new_chart = self.parse_input_skill(message).copy()
                    print(new_chart)
                    self.update_skills(role_Chart[role], new_chart)
                    # if self.role_entries_name[role] in role_Chart_at_name:
                    role_Chart_at_name[self.role_entries_name[role]] = role_Chart[role].copy()
                    role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"] = self.role_avatar_paths[role]
                    self.save_role_skill_at_name()
                    # print(role_Chart_at_name[self.role_entries_name[role]])
                SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                POW = role_Chart_detail.get("POW")
                DB = role_Chart_detail.get("DB")
                if "#SAN" in role_Chart_detail:
                    _SAN = role_Chart_detail.get("#SAN")
                else:
                    _SAN = 100
                if "HP" in message:
                    HP_ = self.role_values_entry[role].get("2.0", "3.0").split("/")[0].strip()
                    self.role_values_entry[role].delete("2.0", "3.0")
                    self.role_values_entry[role].insert("2.0",
                                                        f'{HP_}/{HP}:HP\n')
                if "MP" in message:
                    MP_ = self.role_values_entry[role].get("3.0", "4.0").split("/")[0].strip()
                    self.role_values_entry[role].delete("3.0", "4.0")
                    self.role_values_entry[role].insert("3.0",
                                                        f'{MP_}/{MP}:MP\n')
                if "SAN" in message:
                    SAN_ = self.role_values_entry[role].get("1.0", "2.0").split("/")[0].strip()
                    #if SAN_ == 0 or SAN_ == "":
                        #SAN_ = POW
                    self.role_values_entry[role].delete("1.0", "2.0")
                    self.role_values_entry[role].insert("1.0",
                                                        f'{SAN_}/{_SAN}:SAN\n')
                if "MOV" in message:
                    MOV_ = self.role_values_entry[role].get("4.0", "5.0").split("/")[0].strip()
                    self.role_values_entry[role].delete("4.0", "5.0")
                    self.role_values_entry[role].insert("4.0",
                                                        f'{MOV_}/{MOV}:MOV\n')
                if "DB" in message:
                    self.role_values_entry[role].delete("5.0", "6.0")
                    self.role_values_entry[role].insert("5.0",
                                                        f'\n{DB}:DB\n')
                else:
                    self.role_values_entry[role].insert("1.0",
                                                        f'{SAN}/{_SAN}:SAN\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB\n===\n')
                self.role_entries[role].delete("1.0", tk.END)
                # self.chat_log.insert(tk.END, f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime(
                # "%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\nSAN:{SAN}\nHP:{HP}\nMP:{MP}\nMOV:{
                # MOV}\n\n\n')
                if parts_skill and len(parts_skill) > 0 and len(parts_skill[0]) > 0:
                    self.role_entries[role].insert(tk.END, "已录入！")
                    if "HP" in str(parts_skill[0][0]).upper() or "MP" in str(parts_skill[0][0]).upper() or "SAN" in str(
                            parts_skill[0][0]).upper() or "MOV" in str(parts_skill[0][0]).upper():
                        self.chat_log.insert(tk.END,
                                             f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\n{self.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                        #self.chat_log_huozi = self.chat_log_huozi + f"<{self.role_entries_name['DiceBot']}>【{self.role_entries_name[role]}】的状态：\n{self.role_values_entry[role].get('1.0', '5.0').strip()}\n"
                        self.chat_log.yview(tk.END)
                    else:
                        if len(parts_skill) == 1 and "#" not in message:
                            self.chat_log.insert(tk.END,
                                                 f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的【{str(parts_skill[0][0]).upper()}】成长为{str(role_Chart[role][str(parts_skill[0][0]).upper()])}！\n\n')
                        #self.chat_log_huozi = self.chat_log_huozi + f"<{self.role_entries_name['DiceBot']}>【{self.role_entries_name[role]}】的【{str(parts_skill[0][0]).upper()}】成长为{str(role_Chart[role][str(parts_skill[0][0]).upper()])}！\n"
                        self.chat_log.yview(tk.END)
                else:
                    self.role_entries[role].insert(tk.END, "已刷新！")
            else:
                fire_babel(self, role)
                self.chat_log.insert(tk.END, log)
                # 滚动到最底部
                self.chat_log.yview(tk.END)
                self.role_entries[role].delete("1.0", tk.END)

    def parse_input_skill(self, input_string):
        skills = {}
        # 使用正则表达式从输入字符串中提取技能和值的组合
        if "@" in input_string:
            input_string = input_string[1:]
            input_string = input_string.split("@")
            skill = input_string[0]
            modifier = input_string[1]
            print(skill)
            print(modifier)
            skill_name = "#" + skill.strip().upper()
            skill_value = modifier
            skills[skill_name] = skill_value
        else:
            pattern = re.compile(r'([\u4e00-\u9fa5a-zA-Z\s]+)(\d+)')
            matches = pattern.findall(input_string)
            for match in matches:
                skill_name = match[0].strip().upper()
                skill_value = int(match[1])
                skills[skill_name] = skill_value
        # print(skills)
        return skills

    def update_skills(self, old_dict, new_dict):
        for skill, value in new_dict.items():
            if skill in old_dict:
                # 如果技能已存在于旧字典中，更新数值
                old_dict[skill] = value
            else:
                # 如果技能不存在于旧字典中，将其添加到旧字典
                old_dict[skill] = value
        if (old_dict["SIZ"] == 0) and (old_dict["体型"] != 0) and (old_dict["体型"] != "SIZ"):
            old_dict["EDU"] = old_dict["教育"]
            old_dict["APP"] = old_dict["外貌"]
            old_dict["DEX"] = old_dict["敏捷"]
            old_dict["STR"] = old_dict["力量"]
            old_dict["INT"] = old_dict["智力"]
            old_dict["CON"] = old_dict["体质"]
            old_dict["POW"] = old_dict["意志"]
            old_dict["SIZ"] = old_dict["体型"]
            old_dict["LUCK"] = old_dict["幸运"]
        if old_dict["SIZ"] >= 0 and (old_dict["体型"] == "SIZ"):
            old_dict["教育"] = old_dict["EDU"]
            old_dict["外貌"] = old_dict["APP"]
            old_dict["敏捷"] = old_dict["DEX"]
            old_dict["力量"] = old_dict["STR"]
            old_dict["智力"] = old_dict["INT"]
            old_dict["体质"] = old_dict["CON"]
            old_dict["意志"] = old_dict["POW"]
            old_dict["体型"] = old_dict["SIZ"]
            old_dict["幸运"] = old_dict["LUCK"]
        old_dict["灵感"] = old_dict["智力"]
        if (old_dict["HP"] == "(CON+SIZ)/10") or (old_dict["HP"]) == 0:
            old_dict["HP"] = int((old_dict["体质"] + old_dict["体型"]) / 10)
        if (old_dict["MP"] == "POW/5") or (old_dict["MP"]) == 0:
            old_dict["MP"] = int(old_dict["意志"] / 5)
        if old_dict["SAN"] == "POW":
            old_dict["SAN"] = old_dict["意志"]
        old_dict["闪避"] = int(old_dict["敏捷"] / 2)
        old_dict["母语"] = old_dict["教育"]
        old_dict["魅力"] = old_dict["外貌"]
        old_dict["cm"] = old_dict["克苏鲁神话"]
        old_dict["克苏鲁"] = old_dict["克苏鲁神话"]
        old_dict["计算机"] = old_dict["计算机使用"]
        old_dict["电脑"] = old_dict["计算机使用"]
        old_dict["法学"] = old_dict["司法科学"]
        old_dict["霰弹枪"] = old_dict["步枪/霰弹枪"]
        old_dict["步枪"] = old_dict["步枪/霰弹枪"]
        if old_dict["信用评级"] != 0:
            old_dict["信用"] = old_dict["信用评级"]
        else:
            old_dict["信用评级"] = old_dict["信用"]
        if old_dict["MOV"] == 8:
            if (old_dict["敏捷"] < old_dict["体型"]) and (old_dict["力量"] < old_dict["体型"]):
                old_dict["MOV"] = 7
            elif (old_dict["敏捷"] > old_dict["体型"]) and (old_dict["力量"] > old_dict["体型"]):
                old_dict["MOV"] = 9
            else:
                old_dict["MOV"] = 8
            print(old_dict["MOV"])
        if old_dict["DB"] == 1:
            old_dict["DB"] = "1(+1D4)"
        if old_dict["DB"] == 2:
            old_dict["DB"] = "2(+1D6)"
        if old_dict["DB"] == -2:
            old_dict["DB"] = "-2(-2)"
        if old_dict["DB"] == -1:
            old_dict["DB"] = "-1(-1)"
        if old_dict["DB"] == 0:
            old_dict["DB"] = "0(0)"

        if old_dict["力量"] + old_dict["体型"] <= 164:
            old_dict["DB"] = "1(+1D4)"
            if old_dict["力量"] + old_dict["体型"] <= 124:
                old_dict["DB"] = "0(0)"
            if old_dict["力量"] + old_dict["体型"] <= 84:
                old_dict["DB"] = "-1(-1)"
            if old_dict["力量"] + old_dict["体型"] <= 64:
                old_dict["DB"] = "-2(-2)"
            if old_dict["力量"] + old_dict["体型"] <= 0:
                old_dict["DB"] = "0(0)"
        else:
            old_dict["DB"] = "2(+1D6)"
        if "图书馆使用" not in old_dict or old_dict["图书馆使用"] == 0:
            old_dict["图书馆使用"] = old_dict["图书馆"]
        if "图书馆使用" in old_dict and old_dict["图书馆"] == 20:
            old_dict["图书馆"] = old_dict["图书馆使用"]

        if "ARMOR" not in old_dict:
            old_dict["ARMOR"] = 0
        old_dict["#SAN"] = 100 - old_dict["克苏鲁神话"]

    def edit_role_name(self, event, role, label):
        label.config(relief=tk.GROOVE)
        entry = tk.Entry(label, width=10)
        entry.insert(0, role)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        entry.bind("<FocusOut>",
                   lambda event, role=role, entry=entry, label=label: self.update_role_name(event, role, entry, label))

    def update_role_name(self, event, role, entry, label):
        label.config(relief=tk.FLAT, font=("Times New Roman", 16, "bold"))
        new_name = entry.get().strip()
        if new_name and new_name != "":
            # 更新角色名
            index = self.roles.index(role)
            # self.roles[index] = new_name
            self.role_entries_name[role] = new_name
            babel(self)
            # 更新当前角色名
            # if self.current_role.get() == role:
            # self.current_role.set(new_name)

            entry.grid_forget()
            label.configure(text=new_name)

            if role == "DiceBot":
                # 按名牌加载Bot性格
                for names in bot_personality_by_name:
                    if names == self.role_entries_name["DiceBot"]:
                        global Critical_Success
                        global Extreme_Success
                        global Hard_Success
                        global Success
                        global Failure
                        global Fumble
                        global Fumble_SKill
                        global Critical_Success_SKill
                        bot_personality = bot_personality_by_name[names]
                        Critical_Success = random.choice(bot_personality["Critical_Success"])
                        Extreme_Success = random.choice(bot_personality["Extreme_Success"])
                        Hard_Success = random.choice(bot_personality["Hard_Success"])
                        Success = random.choice(bot_personality["Success"])
                        Failure = random.choice(bot_personality["Failure"])
                        Fumble = random.choice(bot_personality["Fumble"])
                        Fumble_SKill = bot_personality["Fumble_at_96_SKill_Level"]
                        Critical_Success_SKill = bot_personality["Critical_at_5_SKill_Level"]
                        self.role_entries["DiceBot"].insert("1.0", f"已录入[{names}]的性格！\n")
                        break

            # 按名牌加载设置
            if new_name in role_Chart_at_name and (new_name != role) and ("PL " not in new_name):
                self.infoCanvas_data[role] = self.infoCanvas_data_by_name[new_name]
                role_Chart[role] = role_Chart_at_name[new_name].copy()
                role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
                # self.role_entries[role].delete("1.0", tk.END)
                self.role_avatar_paths[role] = role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"]
                self.load_and_display_avatar(role, self.role_entries[role].master)
                SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                POW = role_Chart_detail.get("POW")
                DB = role_Chart_detail.get("DB")
                if "#SAN" in role_Chart_detail:
                    SAN_ = role_Chart_detail.get("#SAN")
                else:
                    _SAN_ = 100
                self.role_values_entry[role].insert("1.0",
                                                    f'{SAN}/{SAN_}:SAN\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB\n===\n')
                # self.role_entries[role].delete("1.0", tk.END)
                # self.role_entries[role].insert(tk.END, "已录入！")
                # self.chat_log.insert(tk.END,
                # f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\nSAN:{SAN}\nHP:{HP}\nMP:{MP}\nMOV:{MOV}\n\n\n')
                self.chat_log.insert(tk.END,
                                     f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\n{self.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                self.chat_log.yview(tk.END)
                self.role_entries[role].insert("1.0", "已加载名牌为[" + new_name + "]的角色卡！\n")
            else:
                role_Chart[role] = role_Chart_detail_demo.copy()

            # 重新创建角色框架
            # for widget in self.root.grid_slaves(column=2):
            # widget.grid_forget()

            # self.create_role_frames()

    def add_role(self):
        self.role_count += 1
        print(self.role_count)
        self.role_count = self.role_count
        new_role = f"PL {len(self.roles) - 1}"
        self.roles.append(new_role)
        if new_role not in self.role_entries_name:
            self.role_entries_name[new_role] = new_role
        elif self.role_entries_name[new_role] != new_role:
            pass

        num_cols = 3
        idx = len(self.roles) - 1
        row = idx % num_cols
        col = idx // num_cols
        self.create_role_frame(new_role, row, col)

        # 超过3列时自动换列
        if col > 2:
            self.root.columnconfigure(col + 2, weight=1)

        # 重新创建角色框架
        # for widget in self.root.grid_slaves(column=2):
        # widget.grid_forget()

        # self.create_role_frames()
        for role in self.roles:
            entry = self.role_entries[role]
            entry.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))
        for role in self.roles:
            entry_roll = self.role_entries_roll[role]
            entry_roll.bind("<FocusIn>", lambda event2, role=role: self.bind_enter_to_send_roll(event2, role))

    def add_role_init(self):
        self.role_count = self.role_count
        new_role = f"PL {len(self.roles) - 1}"
        self.roles.append(new_role)
        self.canvas_icon_animate[new_role] = ""
        self.image_references_on_Avatar[new_role] = []
        self.frames_avatar[new_role] = []
        self.current_frame_avatar[new_role] = []
        self.frames_icon[new_role] = []
        self.current_frame_icon[new_role] = []
        self.frames_map[new_role] = []
        self.current_frame_map[new_role] = []
        self.frames_icon_on_canvas[new_role] = []
        self.current_frame_icon_on_canvas[new_role] = []
        if new_role not in self.role_entries_name:
            self.role_entries_name[new_role] = new_role
        elif self.role_entries_name[new_role] != new_role:
            pass

        num_cols = 3
        idx = len(self.roles) - 1
        row = idx % num_cols
        col = idx // num_cols
        self.create_role_frame(new_role, row, col)

        # 超过3列时自动换列
        if col > 2:
            self.root.columnconfigure(col + 2, weight=1)

        # 重新创建角色框架
        # for widget in self.root.grid_slaves(column=2):
        # widget.grid_forget()

        # self.create_role_frames()
        for role in self.roles:
            entry = self.role_entries[role]
            entry.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))
        for role in self.roles:
            entry_roll = self.role_entries_roll[role]
            entry_roll.bind("<FocusIn>", lambda event2, role=role: self.bind_enter_to_send_roll(event2, role))

    def delete_role(self):
        if len(self.roles) > 3:
            self.role_count -= 1
            role_to_delete = self.roles.pop()
            self.role_entries[role_to_delete].destroy()
            # self.roles[len(self.roles)-1].destroy()
            del self.role_entries[role_to_delete]
            # del self.roles[len(self.roles)]
            self.role_entries_frame[role_to_delete].destroy()
            # 更新当前角色名
            if role_to_delete == self.current_role.get():
                self.current_role.set(self.roles[0])

            # 重新创建角色框架
            # for widget in self.root.grid_slaves(column=2):
            # widget.grid_forget()

            # self.create_role_frames()

    def insert_newline(self):
        current_text = self.role_entries[self.current_role.get()].get("1.0", tk.END)
        self.role_entries[self.current_role.get()].delete("1.0", tk.END)
        self.role_entries[self.current_role.get()].insert(tk.END, current_text)
        self.highlight_role_frame(self.current_role.get())

    def bind_enter_to_send_message(self, event, role):
        # 为当前文本框绑定回车键发送消息
        self.current_role.set(role)
        self.root.bind("<Return>", lambda event, role=role: self.send_message_on_enter(event, role))
        self.highlight_role_frame(role)

    def bind_enter_to_send_roll(self, event, role):
        # 为当前文本框绑定回车键发送消息
        self.current_role.set(role)
        self.root.bind("<Return>", lambda event, role=role: self.send_roll_on_enter(event, role))
        self.highlight_role_frame_roll(role)

    def send_message_on_enter(self, event, role=None):
        self.current_role.set(role)
        # 判断是否同时按下了 Ctrl 键
        if event.state - 4 == 0:  # 4 表示 Ctrl 键的状态值
            return
        # 发送消息
        current_role = role or self.current_role.get()
        self.send_message(current_role)
        self.highlight_role_frame(current_role)

    def send_roll_on_enter(self, event, role=None):
        self.current_role.set(role)
        # 判断是否同时按下了 Ctrl 键
        if event.state - 4 == 0:  # 4 表示 Ctrl 键的状态值
            return
        # 发送消息
        current_role = role or self.current_role.get()
        self.get_and_roll(current_role)
        self.highlight_role_frame_roll(current_role)

    def newline_on_ctrl_enter(self, event):
        # 换行
        current_role = self.current_role.get()
        self.role_entries[current_role].insert(tk.END, "")
        # self.role_entries_roll[current_role].insert(tk.END, "")
        self.highlight_role_frame(current_role)

    def highlight_role_frame(self, role):
        # 搜索包含 ">>>" 的行的起始索引
        start_index = "1.0"
        while True:
            match_index = self.chat_log.search(">>>", start_index, tk.END)
            if not match_index:
                break
            # 删除包含 ">>>" 的行
            line_start = self.chat_log.index(match_index)
            line_end = self.chat_log.index(match_index + " lineend")
            self.chat_log.delete(line_start, line_end)
            # 更新搜索的起始位置
            start_index = line_end
        current_role = self.highlighted_role.get()
        # 高亮指定角色的 Frame
        self.highlighted_role.set(role)
        self.chat_log.insert(tk.END, ">>> " + self.role_entries_name[role] + "正在输入...")
        self.chat_log.yview(tk.END)
        for role in self.roles:
            self.role_entries_frame[role].config(relief=tk.GROOVE)
            self.role_entries_roll[role].config(relief=tk.GROOVE)
        self.role_entries_frame[self.highlighted_role.get()].config(relief=tk.SOLID)
        # self.create_role_frames()

    def highlight_role_frame_roll(self, role):
        # 高亮指定角色的 Frame
        self.highlighted_role.set(role)
        for role in self.roles:
            self.role_entries_frame[role].config(relief=tk.GROOVE)
            self.role_entries_roll[role].config(relief=tk.GROOVE)
        self.role_entries_frame[self.highlighted_role.get()].config(relief=tk.SOLID)
        self.role_entries_roll[self.highlighted_role.get()].config(relief=tk.SOLID)
        # self.create_role_frames()

    def on_at_click(self, role):
        # @点击事件处理
        # self.current_at_role.set(role)
        self.avatar_click_event = role
        current_role = self.current_role.get()
        self.role_entries[current_role].insert(tk.END, "@" + self.role_entries_name[role] + " ")

    def on_at_right_click(self, role):
        # @右键事件处理
        filename_ = ""
        avatar_path = ""
        # self.current_at_role.set(role)
        self.avatar_click_event = role
        current_role = self.current_role.get()
        options = ["【背景】", "【背景】纯黑", "【BGM】", "【停止BGM】", "【音效】", "【展示图片】", "【撤除图片】", "【特效】震动", "【特效】闪屏", "【高级特效】开始",
                   "【高级特效】结束", "【改变名字】[+(之后出场角色被改成的名字, 留空为恢复)]", "【对话框特效】震动", "【隐藏/显示对话框】",
                   f"【开始角色特效】({self.role_entries_name[role]})", "【结束角色特效(连续和剪影)】", "【更换对话框样式】[+(对话框样式名, 留空为撤除样式)]",
                   "【等待】[+(秒数)]"]
        # content_ = simpledialog.askstring("Select Option", "请选择下拉项：", initialvalue=options[0], options=options)
        # 创建新的顶级窗口
        self.top_ask = tk.Toplevel(root)
        # 设置窗口标题
        self.top_ask.title("选择活字命令")
        # 创建下拉菜单
        var = tk.StringVar()
        var.set(options[0])  # 默认选择第一个选项
        dropdown = tk.OptionMenu(self.top_ask, var, *options)
        dropdown.pack(padx=10, pady=10)
        confirm_button = tk.Button(self.top_ask, text="确认", command=lambda: self.confirm_selection(var, role))
        confirm_button.pack(pady=10)

    def create_dropdown(self, role, options, title):
        self.avatar_click_event = role
        current_role = self.current_role.get()
        # 创建新的顶级窗口
        self.top_ask2 = tk.Toplevel(root)
        # 设置窗口标题
        self.top_ask2.title(title)
        # 创建下拉菜单
        var = tk.StringVar()
        var.set(options[0])  # 默认选择第一个选项
        dropdown2 = tk.OptionMenu(self.top_ask2, var, *options)
        dropdown2.pack(padx=20, pady=10)
        confirm_button2 = tk.Button(self.top_ask2, text="确认", command=lambda: self.confirm_selection2(var))
        confirm_button2.pack(pady=10)

        # 让程序等待窗口被关闭
        self.top_ask2.wait_window()
        # return str(var)

    def confirm_selection2(self, var):
        self.top_ask2.destroy()  # 销毁窗口
        self.content_ = var.get()

    def confirm_selection(self, var, role):
        self.top_ask.destroy()  # 销毁窗口
        content_ = var.get()

        if (content_ == "【背景】") or ("【BGM】" in content_) or ("音效" in content_) or ("【展示图片】" in content_):
            if "背景" in content_:
                avatar_path = filedialog.askopenfilename(
                    title="选择【背景】图片文件名",
                    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
                    initialdir="ReplayResources/BG")
                if avatar_path:
                    filename_, dotextension = os.path.splitext(os.path.basename(avatar_path))
                    content = f"【背景】{filename_}"
                    self.display_image(avatar_path,"背景图")
                    if os.path.exists(
                            'ReplayResources/BG/' + filename_ + dotextension):
                        pass
                    else:
                        shutil.copyfile(avatar_path,
                                        'ReplayResources/BG/' + filename_ + dotextension)
                else:
                    return
            elif "音效" in content_:
                avatar_path = filedialog.askopenfilename(
                    title="选择【音效】音频文件名",
                    filetypes=[("Audio files", "*.mp3;*.wav;*.ogg")],
                    initialdir="ReplayResources/SE")
                if avatar_path:
                    filename_, dotextension = os.path.splitext(os.path.basename(avatar_path))
                    play_audio(avatar_path, filename_, 0)
                    content = f"【音效】{filename_}"

                    if os.path.exists(
                            'ReplayResources/SE/' + filename_ + dotextension):
                        pass
                    else:
                        shutil.copyfile(avatar_path,
                                        'ReplayResources/SE/' + filename_ + dotextension)
                else:
                    return
            elif "BGM" in content_:
                avatar_path = filedialog.askopenfilename(
                    title="选择【BGM】音频文件名",
                    filetypes=[("Audio files", "*.mp3;*.wav;*.ogg")],
                    initialdir="ReplayResources/BGM")
                if avatar_path:
                    filename_, dotextension = os.path.splitext(os.path.basename(avatar_path))
                    self.NowBGM.append(filename_)
                    play_audio(avatar_path, filename_)
                    content = f"【BGM】{filename_}"
                    if os.path.exists(
                            'ReplayResources/BGM/' + filename_ + dotextension):
                        pass
                    else:
                        shutil.copyfile(avatar_path,
                                        'ReplayResources/BGM/' + filename_ + dotextension)
                else:
                    return
            else:
                avatar_path = filedialog.askopenfilename(
                    title="选择【展示图片】图片文件名",
                    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
                    initialdir="ReplayResources/HandOut")
                if avatar_path:
                    filename_, dotextension = os.path.splitext(os.path.basename(avatar_path))
                    if os.path.exists(
                            'ReplayResources/HandOut/' + filename_ + dotextension):
                        pass
                    else:
                        shutil.copyfile(avatar_path,
                                        'ReplayResources/HandOut/' + filename_ + dotextension)
                    self.NowImage.append(filename_)
                    content = f"【展示图片】{filename_}"
                    self.display_image(avatar_path, "HandOut", filename_)
                    content_ = simpledialog.askstring("展示秒数(0为忽略)", "请输入展示秒数(0或不输入为忽略)：")
                    if content_ == "" or content_ == "0":
                        pass
                    else:
                        content = content + "\n【等待】" + content_ + f"\n【撤除图片】{self.NowImage.pop()}"
                else:
                    return
        elif "隐藏/显示对话框" in content_:
            if self.NowDialogState:
                content = "【隐藏对话框】隐藏"
                content_ = simpledialog.askstring("隐藏秒数(0为忽略)", "请输入隐藏秒数(0或不输入为忽略)：")
                if content_ == "" or content_ == "0":
                    self.NowDialogState = False
                else:
                    content = content + "\n【等待】" + content_ + f"\n【隐藏对话框】显示"
                    self.NowDialogState = True
            else:
                content = "【隐藏对话框】显示"
                self.NowDialogState = True
        elif "恢复名字" in content_:
            content = "【改变名字】"

        elif "停止BGM" in content_:
            if len(self.NowBGM) > 1:
                self.create_dropdown(role, self.NowBGM, "请选择要停止的BGM：")
                content_ = self.content_
                if content_:
                    if content_ == "全部":
                        content = f"【停止BGM】"
                        for name in self.NowBGM:
                            if name != "全部":
                                kill_audio(name)
                        self.NowBGM.clear()
                        self.NowBGM.append("全部")
                    else:
                        kill_audio(content_)
                        content = f"【停止BGM】{content_}"
                        self.NowBGM.remove(content_)
                else:
                    return
            else:
                print("没有使用中的BGM！")
                content = f"【停止BGM】[+(BGM名称)]"

        elif "撤除图片" in content_:
            if self.NowImage:
                self.create_dropdown(role, self.NowImage, "请选择要撤除的图片：")
                content_ = self.content_
                if content_:
                    content = f"【撤除图片】{content_}"
                    self.NowImage.remove(content_)
                else:
                    return
            else:
                print("没有使用中的图片！")
                content = f"【撤除图片】[+(HandOut名称)]"
        elif "【高级特效】开始" in content_:
            _list = ["---环境---", "下雨", "下雪", "暴风雪", "大雾", "水下", "---设备---", "监控录像", "胶卷", "黑白电视", "彩色电视", "黑白电影",
                     "---故障---", "轻微故障", "中等故障", "严重故障", "---漫画---", "黑色集中线", "白色集中线", "---事件---", "幻觉", "血迹", "直面古神"]
            self.create_dropdown(role, _list, "请选择要使用的高级特效：")
            content_ = self.content_
            if content_:
                content = f"【高级特效】开始{content_}"
                self.NowEffect.append(content_)
            else:
                return
        elif "【高级特效】结束" in content_:
            if self.NowEffect:
                self.create_dropdown(role, self.NowEffect, "请选择要结束的高级特效：")
                content_ = self.content_
                if content_:
                    content = f"【高级特效】结束{content_}"
                    self.NowEffect.remove(content_)
                else:
                    return
            else:
                print("没有使用中的高级特效！")
                content = f"【高级特效】结束[+(特效名)]"
        elif "开始角色特效" in content_:
            _list = [f"({self.role_entries_name[role]})震动",
                     f"({self.role_entries_name[role]})左右震动",
                     f"({self.role_entries_name[role]})连续震动",
                     f"({self.role_entries_name[role]})剪影",
                     f"({self.role_entries_name[role]})转圈",
                     f"({self.role_entries_name[role]})连续转圈",
                     f"({self.role_entries_name[role]})跳动",
                     f"({self.role_entries_name[role]})下沉"]
            self.create_dropdown(role, _list, "请选择要进行的角色特效：")
            content_ = self.content_
            if ("连续" in content_) or ("剪影" in content_):
                self.NowCharacterEffect.append(content_)
            content = f"【角色特效】" + content_
        elif "结束角色特效" in content_:
            if self.NowCharacterEffect:
                self.create_dropdown(role, self.NowCharacterEffect, "请选择要结束的角色特效：")
                content_ = self.content_
                if content_:
                    content = f"【角色特效】" + content_.replace("连续", "结束").replace("剪影", "结束剪影")
                    self.NowCharacterEffect.remove(content_)
                else:
                    return
            else:
                content = f"【角色特效】([+(角色名)])结束[+(震动/转圈/剪影)]"
                print("没有使用中的角色特效！")
        else:
            content = content_

        # 搜索包含 ">>>" 的行的起始索引
        start_index = "1.0"
        while True:
            match_index = self.chat_log.search(">>>", start_index, tk.END)
            if not match_index:
                break
            # 删除包含 ">>>" 的行
            line_start = self.chat_log.index(match_index)
            line_end = self.chat_log.index(match_index + " lineend")
            self.chat_log.delete(line_start, line_end)
            # 更新搜索的起始位置
            start_index = line_end

        # 发布到LOG
        self.chat_log.insert(tk.END,
                             f'活字命令 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n{content}\n\n')
        self.chat_log.yview(tk.END)

    def on_avatar_right_click(self, role):
        # Icon、Avatar右击事件处理
        avatar_path = filedialog.askopenfilename(title="为【" + self.role_entries_name[role] + "】选择[会附加到头像上的]状态Icon文件",
                                                 filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.apng;*.gif")],
                                                 initialdir="Images/IconImages")
        if avatar_path:
            if os.path.exists('Images/IconImages/' + role + '-' + self.role_entries_name[role] + '.png'):
                pass
            else:
                shutil.copyfile(avatar_path,
                                'Images/IconImages/' + role + '-' + self.role_entries_name[role] + '.png')

            # 更新头像路径
            self.role_Icon_paths[role] = avatar_path
            # 加载并显示头像
            frame = self.role_entries[role].master
            self.load_and_display_icon_on_avatar(role, frame)
            self.load_and_display_icon(role, frame)
        else:
            self.role_Icon_paths[role] = ""
            frame = self.role_entries[role].master
            self.load_and_display_icon_on_avatar(role, frame)
            self.load_and_display_icon(role, frame)

    def on_avatar_click(self, role):
        # 头像点击事件处理
        # self.current_at_role.set(role)
        self.avatar_click_event = role
        current_role = self.current_role.get()
        # self.role_entries[current_role].insert(tk.END, "@" + self.role_entries_name[role] + " ")
        filename = filedialog.askopenfilename(title="为【" + self.role_entries_name[role] + "】选择简卡图片",
                                              filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.apng;*.gif")],
                                              initialdir="Images/SheetImages")
        _, extension = os.path.splitext(filename)
        filename_, dot = os.path.splitext(os.path.basename(filename))
        if extension == ".apng" or extension == ".APNG":
            filename = self.apng_to_gif(filename, _ + ".gif")
        if filename:
            if os.path.exists(
                    'Images/SheetImages/' + role + '-' + self.role_entries_name[role] + "-" + filename_ + extension):
                pass
            else:
                if os.path.exists('Images/SheetImages/' + filename_ + extension):
                    pass
                else:
                    shutil.copyfile(filename,
                                    'Images/SheetImages/' + role + '-' + self.role_entries_name[
                                        role] + '-' + filename_ + extension)
                    shutil.copyfile(filename,
                                    'Images/SheetImages/' + filename_ + extension)
            self.filename = filename
            self.infoCanvas_data[role] = filename
            if "PL " not in self.role_entries_name[role]:
                self.infoCanvas_data_by_name[self.role_entries_name[role]] = filename

    def on_Namelabel_hover(self, role):
        # print("enter"+role)
        # 头像悬停事件处理
        if role in self.infoCanvas_data and self.infoCanvas_data[role]:
            self.new_window_infoCanvas = tk.Toplevel(root)
            self.new_window_infoCanvas.title(f"{role} - {self.role_entries_name[role]}的简图")
            self.avatar_click_event = role
            current_role = self.current_role.get()

            # 创建图片对象
            self.infoimage = Image.open(self.infoCanvas_data[role])
            width, height = self.infoimage.size
            canvas_h = int(height / 2.2)
            canvas_w = int(width / 2.2)
            self.infoimage  = self.infoimage.resize((canvas_w, canvas_h), Image.LANCZOS)  # 调整头像大小
            #self.infoimage.thumbnail((width, height))
            self.infophoto = ImageTk.PhotoImage(self.infoimage)

            self.infocanvas = tk.Canvas(self.new_window_infoCanvas, width=canvas_w+5, height=canvas_h+5)
            self.infocanvas.pack()
            # 在 Canvas 上展示图片
            self.infocanvas.create_image(canvas_w / 2 +5, canvas_h / 2 +5, image=self.infophoto, tags="image")

    def on_Namelabel_unfocus(self, role):
        # print("leave" + role)
        # 头像离开悬停事件处理
        self.avatar_click_event = role
        current_role = self.current_role.get()
        self.new_window_infoCanvas.destroy()

    def output_chat_log(self):
        new_text = simpledialog.askstring("选择输出格式", "请输入输出格式(QQ/活字):", initialvalue="QQ")
        if new_text == "QQ":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"(QQ)chat_log_{timestamp}.txt"
            chat_log_content = self.chat_log.get("1.0", tk.END)
        elif new_text == "活字":
            chat_log_content_ = ""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"(活字)chat_log_{timestamp}.txt"
            chat_log_content = self.chat_log.get("1.0", tk.END)
            chat_log_content = chat_log_content.replace("\n\n\n", "\n\n")
            pattern = r'([\u4e00-\u9fa5a-zA-Z0-9\s\S]+?)\s(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2})\n([\u4e00-\u9fa5a-zA-Z0-9\s\S]+?)\n\n'
            #pattern =  r'[\u4e00-\u9fa5a-zA-Z0-9\s`~!@#$%^&*()\-_+={}\[\]|;:\'",<.>/?·！￥……（）—【】、；：‘“’”《》，。？]*\d{1,2}\/\d{1,2}\/\d{2,4}\s\d{1,2}:\d{1,2}:\d{1,2}'
            matches = re.findall(pattern, chat_log_content)
            # 输出转换后的格式
            for match in matches:
                name = match[0]
                timestamp = match[1]
                content = match[2]
                print(name)
                print(timestamp)
                print(content)
                chat_log_content_ = chat_log_content_+ f"<{name}>{content}\n"
            chat_log_content = chat_log_content_
            #for m in matches:
                #regex_pattern = r'([\u4e00-\u9fa5a-zA-Z0-9\s`~!@#$%^&*()\-_+={}\[\]|;:\'",<.>/?·！￥……（）—【】、；：‘“’”《》，。？]*)(\d{1,2}\/\d{1,2}\/\d{2,4}\s\d{1,2}:\d{1,2}:\d{1,2})'
                #match = re.search(regex_pattern, m)
                #if match:
                    # 获取捕获组的内容
                    #name = match.group(1)  # 括号内第一个捕获组的内容
                    #date_time = match.group(2)  # 括号内第二个捕获组的内容
                    #chat_log_content = chat_log_content.replace(m,f"<{name}>")
            chat_log_content = chat_log_content.replace("<活字命令>", "")
            chat_log_content = chat_log_content.replace("【差分】", "【请编辑差分】")
            chat_log_content = chat_log_content.replace("<【骰子】>", "【骰子】")

        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"(QQ)chat_log_{timestamp}.txt"
            chat_log_content = self.chat_log.get("1.0", tk.END)
        with open(filename, "w") as file:
            file.write(chat_log_content)

    def output_html_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_log_{timestamp}.html"
        chat_log_content = self.chat_log.get("1.0", tk.END)
        with open(filename, "w") as file:
            file.write(f'<html><head></head><body>{chat_log_content}</body></html>')

    def choose_Icon(self, role):
        avatar_path = filedialog.askopenfilename(title="为【" + self.role_entries_name[role] + "】选择状态Icon文件",
                                                 filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.apng;*.gif")],
                                                 initialdir="Images/IconImages")
        _, extension = os.path.splitext(avatar_path)
        filename, dot = os.path.splitext(os.path.basename(avatar_path))
        if extension == ".apng" or extension == ".APNG":
            avatar_path = self.apng_to_gif(avatar_path, _ + ".gif")
        if avatar_path:
            if os.path.exists('Images/IconImages/' + filename + extension):
                pass
            else:
                shutil.copyfile(avatar_path,
                                'Images/IconImages/' + filename + extension)

            # 更新头像路径
            self.role_Icon_paths[role] = avatar_path
            # 加载并显示头像
            frame = self.role_entries[role].master
            self.load_and_display_icon(role, frame)
        else:
            self.role_Icon_paths[role] = ""
            frame = self.role_entries[role].master
            self.load_and_display_icon(role, frame)

    def choose_avatar(self, role):
        if role in self.role_dir_path:
            initDir = self.role_dir_path[role]
        else:
            initDir = "Images/AvatarImages"
        avatar_path = filedialog.askopenfilename(title="为【" + self.role_entries_name[role] + "】选择头像文件",
                                                 filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.apng;*.gif")],
                                                 initialdir=initDir)
        if avatar_path:
            _, extension = os.path.splitext(avatar_path)
            filename, dot = os.path.splitext(os.path.basename(avatar_path))
            self.role_dir_path[role] = os.path.dirname(avatar_path)
            if extension == ".apng" or extension == ".APNG":
                avatar_path = self.apng_to_gif(avatar_path, _ + ".gif")
            if os.path.exists(
                    'Images/AvatarImages/' + role + '-' + self.role_entries_name[role] + '-' + filename + extension):
                pass
            else:
                if os.path.exists('Images/AvatarImages/' + filename + extension):
                    pass
                else:
                    shutil.copyfile(avatar_path,
                                    'Images/AvatarImages/' + role + '-' + self.role_entries_name[
                                        role] + '-' + filename + extension)
                    shutil.copyfile(avatar_path,
                                    'Images/AvatarImages/' + filename + extension)
            # 发布到LOG
            # 搜索包含 ">>>" 的行的起始索引
            start_index = "1.0"
            while True:
                match_index = self.chat_log.search(">>>", start_index, tk.END)
                if not match_index:
                    break
                # 删除包含 ">>>" 的行
                line_start = self.chat_log.index(match_index)
                line_end = self.chat_log.index(match_index + " lineend")
                self.chat_log.delete(line_start, line_end)
                # 更新搜索的起始位置
                start_index = line_end

            self.chat_log.insert(tk.END,
                                 f'活字命令 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【差分】<{self.role_entries_name[role]}({filename})>\n\n')
            self.chat_log.yview(tk.END)
            # 更新头像路径
            self.role_avatar_paths[role] = avatar_path
            # 加载并显示头像
            frame = self.role_entries[role].master
            self.load_and_display_avatar(role, frame)
        else:
            self.role_avatar_paths[role] = ""
            frame = self.role_entries[role].master
            self.load_and_display_avatar(role, frame)
        if self.role_entries_name[role] in role_Chart_at_name:
            role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"] = self.role_avatar_paths[role]

    def load_and_display_avatar(self, role, frame):
        self.Avatar = ""
        if role in self.role_avatar_paths:
            # 加载头像
            image_path = self.role_avatar_paths[role]
            if image_path:
                if self.role_entries_name[role] in role_Chart_at_name:
                    role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"] = image_path
                image = Image.open(image_path)
                image_temp = Image.open(image_path)
                # 获取图像的宽和高
                width, height = image.size

                # 根据宽高比设置头像大小
                if math.fabs(width - height) <= 10:
                    image = image.resize((50, 50), Image.LANCZOS)  # 调整头像大小
                elif math.fabs(width - height) <= 400:
                    image = image.resize((50, 80), Image.LANCZOS)
                else:
                    image = image.resize((50, 100), Image.LANCZOS)

                tk_image = ImageTk.PhotoImage(image)
                label = tk.Label(frame, image=tk_image)
                label.image = tk_image
                label.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

                # 头像点击事件绑定
                label.bind("<Button-1>", lambda event, role=role: self.choose_avatar(role))
                frame = self.role_entries[role].master
                label.bind("<Button-3>",
                           lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))

                label.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                label.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

                _, extension = os.path.splitext(image_path)
                if extension == ".gif" or extension == ".GIF":

                    # gif = imageio.mimread(image_path)
                    self.Iconcanvas[role] = tk.Canvas(frame, width=20, height=20)
                    self.Iconcanvas[role].grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

                    # self.Avatar = self.Iconcanvas[role].create_image(30, 50, image=tk_image)
                    if math.fabs(width - height) <= 10:
                        self.frames_avatar[role] = [ImageTk.PhotoImage(frame.resize((50, 50), Image.LANCZOS)) for frame
                                                    in ImageSequence.Iterator(image_temp)]
                    elif math.fabs(width - height) <= 400:
                        self.frames_avatar[role] = [ImageTk.PhotoImage(frame.resize((50, 80), Image.LANCZOS)) for frame
                                                    in ImageSequence.Iterator(image_temp)]
                    else:
                        self.frames_avatar[role] = [ImageTk.PhotoImage(frame.resize((50, 100), Image.LANCZOS)) for frame
                                                    in ImageSequence.Iterator(image_temp)]
                    # 获取 GIF 图片的所有帧

                    # self.frames_avatar[role] = image_temp
                    # self.frames_avatar[role] = []
                    # for temp_frame in ImageSequence.Iterator(image_temp):
                    # 转换为 RGBA 模式并添加到列表中
                    # frame_rgba = temp_frame.convert("RGBA")
                    # frame_rgba = ImageTk.PhotoImage(frame_rgba)
                    # self.frames_avatar[role].append(frame_rgba)

                    # 显示 GIF 图片的第一帧
                    self.current_frame_avatar[role] = self.Iconcanvas[role].create_image(0, 0, anchor=tk.NW,
                                                                                         image=self.frames_avatar[role][
                                                                                             0])
                    # 播放 GIF 动画
                    self.animate(0, self.Iconcanvas[role], self.current_frame_avatar[role], self.frames_avatar[role])

                    self.Iconcanvas[role].bind("<Button-1>", lambda event, role=role: self.choose_avatar(role))
                    self.Iconcanvas[role].bind("<Button-3>",
                                               lambda event, role=role, frame=frame: self.hide_icon_on_avatar(
                                                   role, frame))

                    self.Iconcanvas[role].bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                    self.Iconcanvas[role].bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

                else:
                    self.Iconcanvas[role] = tk.Canvas(frame, width=20, height=20)
                    self.Iconcanvas[role].grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
                    self.Avatar = self.Iconcanvas[role].create_image(30, 50, image=tk_image)

                    self.Iconcanvas[role].bind("<Button-1>", lambda event, role=role: self.choose_avatar(role))
                    self.Iconcanvas[role].bind("<Button-3>",
                                               lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role,
                                                                                                              frame))

                    self.Iconcanvas[role].bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                    self.Iconcanvas[role].bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

            else:
                if self.Avatar:
                    self.Iconcanvas[role].delete(self.Avatar)
                self.Iconcanvas[role] = tk.Canvas(frame, width=0, height=0)
                self.Iconcanvas[role].grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

                self.Iconcanvas[role].bind("<Button-1>", lambda event, role=role: self.choose_avatar(role))
                self.Iconcanvas[role].bind("<Button-3>",
                                           lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))

                self.Iconcanvas[role].bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                self.Iconcanvas[role].bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

                label = tk.Label(frame)
                label.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

                label.bind("<Button-1>", lambda event, role=role: self.choose_avatar(role))
                label.bind("<Button-3>", lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))

                label.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                label.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))

    def hide_icon_on_avatar(self, role, frame):
        if role in self.Icon_on_avatar:
            self.Iconcanvas[role].delete(self.Icon_on_avatar.pop(role))
            if self.current_frame_icon_on_canvas[role]:
                self.Iconcanvas[role].delete(self.current_frame_icon_on_canvas[role])
            # self.Iconcanvas[role].delete(self.Icon_on_avatar[role])
        else:
            # self.Icon_on_avatar[role] = ""
            self.load_and_display_icon_on_avatar(role, frame)

    def load_and_display_icon_on_avatar(self, role, frame):
        if role not in self.Icon_on_avatar:
            self.Icon_on_avatar[role] = ""
        else:
            print("delete load_and_display_icon_on_avatar")
            self.Iconcanvas[role].delete(self.Icon_on_avatar[role])
        if role in self.role_Icon_paths:
            # 加载头像
            image_path = self.role_Icon_paths[role]
            if image_path:
                image = Image.open(image_path)
                image_temp = Image.open(image_path)
                # 获取图像的宽和高
                width, height = image.size
                # 根据宽高比设置头像大小
                if math.fabs(width - height) <= 10:
                    image = image.resize((50, 50), Image.LANCZOS)  # 调整头像大小
                elif math.fabs(width - height) <= 400:
                    image = image.resize((50, 80), Image.LANCZOS)
                else:
                    image = image.resize((50, 100), Image.LANCZOS)

                _, extension = os.path.splitext(image_path)
                if extension == ".gif" or extension == ".GIF":

                    # self.Avatar = self.Iconcanvas[role].create_image(30, 50, image=tk_image)
                    if math.fabs(width - height) <= 10:
                        self.frames_icon_on_canvas[role] = [ImageTk.PhotoImage(frame.resize((50, 50), Image.LANCZOS))
                                                            for frame in ImageSequence.Iterator(image_temp)]
                    elif math.fabs(width - height) <= 400:
                        self.frames_icon_on_canvas[role] = [ImageTk.PhotoImage(frame.resize((50, 80), Image.LANCZOS))
                                                            for frame in ImageSequence.Iterator(image_temp)]
                    else:
                        self.frames_icon_on_canvas[role] = [ImageTk.PhotoImage(frame.resize((50, 100), Image.LANCZOS))
                                                            for frame in ImageSequence.Iterator(image_temp)]
                    # 显示 GIF 图片的第一帧
                    self.current_frame_icon_on_canvas[role] = self.Iconcanvas[role].create_image(0, 0, anchor=tk.NW,
                                                                                                 image=
                                                                                                 self.frames_icon_on_canvas[
                                                                                                     role][
                                                                                                     0])
                    # 播放 GIF 动画
                    self.animate(0, self.Iconcanvas[role], self.current_frame_icon_on_canvas[role],
                                 self.frames_icon_on_canvas[role])
                else:
                    if self.current_frame_icon_on_canvas[role]:
                        self.Iconcanvas[role].delete(self.current_frame_icon_on_canvas[role])
                    tk_image = ImageTk.PhotoImage(image)
                    # self.Iconcanvas.create_rectangle(0, 0, 30, 30, fill="red")
                    if math.fabs(width - height) <= 10:
                        self.Icon_on_avatar[role] = self.Iconcanvas[role].create_image(20, 20, image=tk_image)
                    else:
                        self.Icon_on_avatar[role] = self.Iconcanvas[role].create_image(30, 40, image=tk_image)
                    self.image_references_on_Avatar[role].append(tk_image)

                    # elif math.fabs(width - height) <= 100:
                    # image = image.resize((20, 30), Image.LANCZOS)
                    # else:
                    # image = image.resize((10, 30), Image.LANCZOS)

                    # label3 = tk.Label(frame, image=tk_image, background = "white")
                    # label3.image = tk_image

                    # hwnd = self.Iconcanvas.winfo_id()
                    # colorkey = win32api.RGB(255, 255, 255)  # full black in COLORREF structure
                    # wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                    # new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
                    # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
                    # win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 255, win32con.LWA_COLORKEY)

            else:
                if self.Icon_on_avatar[role]:
                    self.Iconcanvas[role].delete(self.Icon_on_avatar[role])
                    # self.Iconcanvas[role].delete(self.current_frame_avatar[role])
        else:
            pass

    def animate(self, frame_index, canvas, current_frame, frames):
        # print(str(frame_index)+"/" + str(len(frames)))
        # 更新当前帧
        canvas.itemconfig(current_frame, image=frames[frame_index])
        # canvas.create_image(20, 20, anchor=tk.NW, image=frames[frame_index])
        # 循环播放下一帧
        frame_index = (frame_index + 1) % len(frames)
        self.after_id = canvas.after(50, self.animate, frame_index, canvas, current_frame, frames)

    def load_and_display_icon(self, role, frame):
        # self.Icon = ""
        if role in self.role_Icon_paths:
            # 加载头像
            image_path = self.role_Icon_paths[role]
            if image_path:
                image = Image.open(image_path)
                # 获取图像的宽和高
                width, height = image.size
                if height != width:
                    image2 = image.resize((50, 30), Image.LANCZOS)
                else:
                    image2 = image.resize((30, 30), Image.LANCZOS)

                _, extension = os.path.splitext(image_path)
                if extension == ".gif" or extension == ".GIF":
                    # print("帧数:", image.n_frames)
                    self.canvas_icon_animate[role] = tk.Canvas(frame, width=20, height=20)
                    self.canvas_icon_animate[role].grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                    # 获取 GIF 图片的所有帧
                    if height != width:
                        self.frames_icon[role] = [ImageTk.PhotoImage(frame.resize((50, 30), Image.LANCZOS)) for frame in
                                                  ImageSequence.Iterator(image)]
                    else:
                        self.frames_icon[role] = [ImageTk.PhotoImage(frame.resize((30, 30), Image.LANCZOS)) for frame in
                                                  ImageSequence.Iterator(image)]

                    # 显示 GIF 图片的第一帧
                    self.current_frame_icon[role] = self.canvas_icon_animate[role].create_image(0, 0, anchor=tk.NW,
                                                                                                image=
                                                                                                self.frames_icon[role][
                                                                                                    0])
                    # 播放 GIF 动画
                    self.animate(0, self.canvas_icon_animate[role], self.current_frame_icon[role],
                                 self.frames_icon[role])

                    self.canvas_icon_animate[role].bind("<Button-1>", lambda event, role=role: self.choose_Icon(role))
                    self.canvas_icon_animate[role].bind("<Enter>",
                                                        lambda event, role=role: self.on_Namelabel_hover(role))
                    self.canvas_icon_animate[role].bind("<Leave>",
                                                        lambda event, role=role: self.on_Namelabel_unfocus(role))
                    frame = self.role_entries[role].master
                    self.canvas_icon_animate[role].bind("<Button-3>",
                                                        lambda event, role=role, frame=frame: self.hide_icon_on_avatar(
                                                            role, frame))
                elif self.canvas_icon_animate[role]:
                    self.canvas_icon_animate[role].destroy()
                    # 根据宽高比设置头像大小
                    # if width >= 100:
                    # image = image.resize((50, 50), Image.LANCZOS)  # 调整头像大小

                    # elif math.fabs(width - height) <= 100:
                    # image = image.resize((20, 30), Image.LANCZOS)
                    # else:
                    # image = image.resize((10, 30), Image.LANCZOS)
                    # tk_image = ImageTk.PhotoImage(image)
                    tk_image2 = ImageTk.PhotoImage(image2)
                    label2 = tk.Label(frame, image=tk_image2)
                    label2.image = tk_image2

                    # self.Icon = self.Iconcanvas.create_image(200, 200, image=tk_image)

                    # 头像点击事件绑定
                    label2.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                    label2.bind("<Button-1>", lambda event, role=role: self.choose_Icon(role))
                    label2.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                    label2.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))
                    frame = self.role_entries[role].master
                    label2.bind("<Button-3>",
                                lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))
                else:
                    tk_image2 = ImageTk.PhotoImage(image2)
                    label2 = tk.Label(frame, image=tk_image2)
                    label2.image = tk_image2

                    # self.Icon = self.Iconcanvas.create_image(200, 200, image=tk_image)

                    # 头像点击事件绑定
                    label2.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                    label2.bind("<Button-1>", lambda event, role=role: self.choose_Icon(role))
                    label2.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                    label2.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))
                    frame = self.role_entries[role].master
                    label2.bind("<Button-3>",
                                lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))
                # label2.bind("<Button-3>", lambda event, role=role: self.on_avatar_right_click(role))

            else:
                if self.canvas_icon_animate[role]:
                    self.canvas_icon_animate[role].destroy()
                label2 = tk.Label(frame)
                # if self.Icon:
                # self.Iconcanvas.delete(self.Icon)
                label2.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                label2.bind("<Button-1>", lambda event, role=role: self.choose_Icon(role))
                label2.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
                label2.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))
                frame = self.role_entries[role].master
                label2.bind("<Button-3>",
                            lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))
                # label2.bind("<Button-3>", lambda event, role=role: self.on_avatar_right_click(role))
        else:
            label2 = tk.Label(frame)
            label2.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            label2.bind("<Button-1>", lambda event, role=role: self.choose_Icon(role))
            label2.bind("<Enter>", lambda event, role=role: self.on_Namelabel_hover(role))
            label2.bind("<Leave>", lambda event, role=role: self.on_Namelabel_unfocus(role))
            frame = self.role_entries[role].master
            label2.bind("<Button-3>",
                        lambda event, role=role, frame=frame: self.hide_icon_on_avatar(role, frame))
            # label2.bind("<Button-3>", lambda event, role=role: self.on_avatar_right_click(role))

    def get_and_roll(self, role):
        # 搜索包含 ">>>" 的行的起始索引
        start_index = "1.0"
        while True:
            match_index = self.chat_log.search(">>>", start_index, tk.END)
            if not match_index:
                break
            # 删除包含 ">>>" 的行
            line_start = self.chat_log.index(match_index)
            line_end = self.chat_log.index(match_index + " lineend")
            self.chat_log.delete(line_start, line_end)
            # 更新搜索的起始位置
            start_index = line_end
        if self.role_entries_roll[role].get("1.0", tk.END).strip() != "":
            text = self.role_entries_roll[role].get("1.0", tk.END).strip()
            self.role_entries_roll[self.current_role.get()].delete("1.0", tk.END)
            self.role_entries_roll[self.current_role.get()].insert(tk.END, text)
        current_role = self.current_role.get()
        if role == "DiceBot":
            if current_role != "DiceBot":
                if self.role_entries_roll[role].get("1.0", tk.END).strip() != "":
                    self.roll_dice_silent(current_role,
                                          self.role_entries_roll[current_role].get("1.0", tk.END).strip().lower(),
                                          self.role_entries[current_role].get("1.0", tk.END).strip())
                else:
                    self.roll_dice_silent(current_role, "1d100",
                                          self.role_entries[current_role].get("1.0", tk.END).strip())
            else:
                if self.role_entries_roll[role].get("1.0", tk.END).strip() != "":
                    self.roll_dice("全员", self.role_entries_roll[role].get("1.0", tk.END).strip().lower(),
                                   self.role_entries[current_role].get("1.0", tk.END).strip())
                else:
                    self.roll_dice("全员", "1d100", self.role_entries[current_role].get("1.0", tk.END).strip())
        else:
            # 获取相应角色的输入框文本
            enemy_matches = None
            reason = self.role_entries[role].get("1.0", tk.END).strip()
            if "@" in reason:
                print("对抗骰")
                pattern = r"@[\w\s]+"
                enemy_matches = re.findall(pattern, reason)
                enemy_matches = [s.replace("@", "").strip() for s in enemy_matches]
                print(enemy_matches)
                reason = reason.replace("@", "对抗").strip()
                reason = reason.replace(" 对抗", "，对抗")
            if reason == "":
                # 一系列字符串
                string_list = ["不可名状的原因", "懒得写原因", "", "", ""]
                # 从列表中随机选择一个字符串
                reason = random.choice(string_list)
            role_Chart_detail = role_Chart.get(role, {}).copy()
            expression = self.role_entries_roll[role].get("1.0", tk.END).strip().lower()

            if expression == "":
                expression = "1d100"
            if enemy_matches is not None:
                for enemy in enemy_matches:
                    role_ = ""
                    for key, nickname in self.role_entries_name.items():
                        if enemy == nickname:
                            role_ = key
                    expression_ = self.role_entries_roll[role_].get("1.0", tk.END).strip()
                    if expression_ == "" or expression_ == "1d100":
                        self.enemy_matches[enemy] = expression
                    else:
                        # self.enemy_matches[enemy] = expression + self.role_entries_roll[enemy].get("1.0", tk.END).strip()
                        self.enemy_matches[enemy] = self.role_entries_roll[enemy].get("1.0", tk.END).strip()

            for skill in role_Chart_detail:
                if ("r" + skill in reason) or ("ra" + skill in reason) and ("[" not in reason):
                    reason = reason.replace("." + skill, skill)
                    reason = reason.replace("r" + skill, skill)
                    reason = reason.replace("ra" + skill, skill)
                    expression = skill
                    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    log = f"{self.role_entries_name[role]} {timestamp}\n{reason}\n\n"  # 不加引号
                    self.chat_log.insert(tk.END, log)
                    # 滚动到最底部
                    self.chat_log.yview(tk.END)
                    reason = "尝试" + skill

            if enemy_matches is not None:
                self.roll_dice(role, expression, reason)
                for enemy in self.enemy_matches:
                    role_ = ""
                    for key, nickname in self.role_entries_name.items():
                        if enemy == nickname:
                            role_ = key
                    expression_ = self.enemy_matches[enemy]
                    reason_ = f"与{self.role_entries_name[role]}对抗"
                    self.roll_dice(role_, expression_, reason_)
            else:
                self.roll_dice(role, expression, reason)

    def roll_dice(self, role, expression, reason):
        parts_ = []
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        if role == "全员":
            for role in self.roles:
                if role != "DiceBot":
                    result_ = self.trpg_module.roll(expression, role, allin=True)
                    if ("HP" in expression.upper()) or ("MP" in expression.upper()):
                        expression = ""
                        reason = ""
                        return
                    parts_ = result_.split('：')
                    SANC = ""
                    expressionUPP = expression.upper()
                    if re.compile(r'^[+\-*/]').match(expressionUPP):
                        pattern = re.compile(r'([+\-*/]+)(.*)')
                        # 使用正则表达式进行匹配
                        match = pattern.match(expressionUPP)
                        # 提取匹配的结果
                        if match:
                            expressionUPP = match.group(2)
                    if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
                        expressionUPP = "1D100"
                        if ("sc" or "SC" or ".sc" or "。sc") in expression:
                            SANC = "[SAN CHECK" + expression.split("sc")[1].upper() + "]"
                        else:
                            SANC = "[" + expression.upper() + "]"
                    result = ""
                    if len(parts_) > 1:
                        if "大成功" in parts_[1]:
                            result = "[大成功]"
                        elif "极难成功" in parts_[1]:
                            result = "[极难成功]"
                        elif "困难成功" in parts_[1]:
                            result = "[困难成功]"
                        elif "大失败" in parts_[1]:
                            result = "[大失败]"
                        elif "成功" in parts_[1]:
                            result = "[成功]"
                        elif "失败" in parts_[1]:
                            result = "[失败]"
                        else:
                            result = ""
                    if reason == "":
                        #message = f'<{self.role_entries_name["DiceBot"]}>(【{self.role_entries_name[role]}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n'
                        message = f'【骰子】 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                    else:
                        message = f'【骰子】 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】因【{reason}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                    self.chat_log.insert(tk.END, message)
                    self.chat_log.yview(tk.END)
                    self.role_entries[role].delete("1.0", tk.END)
                    self.role_entries["DiceBot"].delete("1.0", tk.END)
                    if len(parts_) > 1:
                        self.role_entries[role].insert(tk.END, parts_[1])
                        weapon_list_ = {}
                        if parts_ and "成功" in parts_[1]:
                            role_Chart_detail_ = role_Chart.get(role, {}).copy()
                            # DB_ = role_Chart_detail_["DB"]
                            for skill, value in role_Chart_detail_.items():
                                if "#" in skill:
                                    weapon_list_[skill.replace("#", "")] = value
                            for weapon, value in weapon_list_.items():
                                if weapon in expression:
                                    self.role_entries_roll[role].delete("1.0", tk.END)
                                    self.role_entries_roll[role].insert("1.0", f"{value}")
                                    self.role_entries[role].insert("1.0", f"[{weapon}]伤害\n")
                                    for role_armor in self.roles:
                                        if role_armor != role and "ARMOR:" in str(self.role_entries_roll[role_armor]):
                                            role_Chart_detail_armor = role_Chart.get(role, {}).copy()
                                            if "ARMOR" in role_Chart_detail_armor:
                                                value_armor = role_Chart_detail_armor["ARMOR"]
                                            else:
                                                value_armor = 0
                                            self.role_entries_roll[role_armor].delete("1.0", tk.END)
                                            self.role_entries_roll[role_armor].insert("1.0",
                                                                                      f"ARMOR:{value_armor}")
                            if "急救" in expression:
                                self.role_entries[role].insert("1.0", f"HP+1，若濒死请继续骰[医学]\n")
                            if "医学" in expression:
                                self.role_entries[role].insert("1.0", f"[医学]恢复1D3 HP\n")
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"1d3")
                            if "精神分析" in expression:
                                self.role_entries[role].insert("1.0", f"[精神分析]恢复1D3 SAN\n")
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"1d3")
                        if parts_ and "大失败" in parts_[1]:
                            if "精神分析" in expression:
                                self.role_entries[role].insert("1.0", f"[精神分析]损失1D6 SAN\n")
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"1d6")
                        if parts_ and "失败" in parts_[1]:
                            for weapon, value in weapon_list_.items():
                                # print(weapon_list_)
                                if weapon in expression:
                                    role_Chart_detail_armor = role_Chart.get(role, {}).copy()
                                    if "ARMOR" in role_Chart_detail_armor:
                                        value_armor = role_Chart_detail_armor["ARMOR"]
                                    else:
                                        value_armor = 0
                                    self.role_entries_roll[role].delete("1.0", tk.END)
                                    self.role_entries_roll[role].insert("1.0", f"ARMOR:{value_armor}")

        else:
            if role == "DiceBot":
                pass
            else:
                result_ = self.trpg_module.roll(expression, role)
                if ("HP" in expression.upper()) or ("MP" in expression.upper()):
                    expression = ""
                    reason = ""
                    #message = f'【骰子】 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】因【{reason}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                    #self.chat_log.insert(tk.END, message)
                    #self.chat_log.yview(tk.END)
                    return
                parts_ = result_.split('：')
                print(parts_)
                SANC = ""
                expressionUPP = expression.upper()
                if re.compile(r'^[+\-*/]').match(expressionUPP):
                    pattern = re.compile(r'([+\-*/]+)(.*)')
                    # 使用正则表达式进行匹配
                    match = pattern.match(expressionUPP)
                    # 提取匹配的结果
                    if match:
                        expressionUPP = match.group(2)
                if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
                    expressionUPP = "1D100"
                    if ("sc" or "SC" or ".sc" or "。sc") in expression:
                        SANC = "[SAN CHECK" + expression.split("sc")[1].upper() + "]"
                    else:
                        SANC = "[" + expression.upper() + "]"
                result = ""
                if len(parts_) > 1:
                    if "大成功" in parts_[1]:
                        result = "[大成功]"
                    elif "极难成功" in parts_[1]:
                        result = "[极难成功]"
                    elif "困难成功" in parts_[1]:
                        result = "[困难成功]"
                    elif "大失败" in parts_[1]:
                        result = "[大失败]"
                    elif "成功" in parts_[1]:
                        result = "[成功]"
                    elif "失败" in parts_[1]:
                        result = "[失败]"
                    else:
                        result = ""
                if reason == "":
                    message = f'【骰子】 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                else:
                    message = f'【骰子】 {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】因【{reason}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                self.chat_log.insert(tk.END, message)
                self.chat_log.yview(tk.END)

                weapon_list = {}
                if len(parts_) > 1:
                    if parts_ and "成功" in parts_[1]:
                        role_Chart_detail = role_Chart.get(role, {}).copy()
                        for skill, value in role_Chart_detail.items():
                            if "#" in skill:
                                weapon_list[skill.replace("#", "")] = value
                        for weapon, value in weapon_list.items():
                            if weapon in expression:
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"{value}")
                                # self.role_entries[role].insert(tk.END, f"{weapon}伤害")
                                for role_armor in self.roles:
                                    if role_armor != role:
                                        role_Chart_detail_armor = role_Chart.get(role, {}).copy()
                                        if "ARMOR" in role_Chart_detail_armor:
                                            value_armor = role_Chart_detail_armor["ARMOR"]
                                        else:
                                            value_armor = 0
                                        self.role_entries_roll[role_armor].delete("1.0", tk.END)
                                        self.role_entries_roll[role_armor].insert("1.0", f"ARMOR:{value_armor}")
                                break
                                # print("sadadd:" + value)
                            if "急救" in expression:
                                self.role_entries[role].insert("1.0", f"HP+1，若濒死请继续骰[医学]\n")
                            if "医学" in expression:
                                self.role_entries[role].insert("1.0", f"[医学]恢复1D3 HP\n")
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"1d3")
                            if "精神分析" in expression:
                                self.role_entries[role].insert("1.0", f"[精神分析]恢复1D3 SAN\n")
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"1d3")
                    if parts_ and "大失败" in parts_[1]:
                        if "精神分析" in expression:
                            self.role_entries[role].insert("1.0", f"[精神分析]损失1D6 SAN\n")
                            self.role_entries_roll[role].delete("1.0", tk.END)
                            self.role_entries_roll[role].insert("1.0", f"1d6")
                        for weapon, value in weapon_list.items():
                            if weapon in expression:
                                for role_armor in self.roles:
                                    if role_armor != role:
                                        role_Chart_detail_armor = role_Chart.get(role, {}).copy()
                                        if "ARMOR" in role_Chart_detail_armor:
                                            value_armor = role_Chart_detail_armor["ARMOR"]
                                        else:
                                            value_armor = 0
                                        self.role_entries_roll[role_armor].delete("1.0", tk.END)
                                        self.role_entries_roll[role_armor].insert("1.0", f"ARMOR:{value_armor}")
                    elif parts_ and "失败" in parts_[1]:
                        role_Chart_detail_armor = role_Chart.get(role, {}).copy()
                        for weapon, value in weapon_list.items():
                            if weapon in expression:
                                if "ARMOR" in role_Chart_detail_armor:
                                    value_armor = role_Chart_detail_armor["ARMOR"]
                                else:
                                    value_armor = 0
                                self.role_entries_roll[role].delete("1.0", tk.END)
                                self.role_entries_roll[role].insert("1.0", f"ARMOR:{value_armor}")

        # 清空输入框文本
        self.role_entries[role].delete("1.0", tk.END)
        if len(parts_) > 1:
            self.role_entries[role].insert(tk.END, parts_[1])

            weapon_list__ = {}
            if len(parts_) > 1:
                if parts_ and "成功" in parts_[1]:
                    role_Chart_detail__ = role_Chart.get(role, {}).copy()
                    for skill, value in role_Chart_detail__.items():
                        if "#" in skill:
                            weapon_list__[skill.replace("#", "")] = value
                    for weapon, value in weapon_list__.items():
                        if weapon in expression:
                            self.role_entries[role].insert("1.0", f"[{weapon}]伤害\n")
                            break
                    if "急救" in expression:
                        self.role_entries[role].insert("1.0", f"HP+1，若濒死请继续骰[医学]\n")
                    if "医学" in expression:
                        self.role_entries[role].insert("1.0", f"[医学]恢复1D3 HP\n")
                        self.role_entries_roll[role].delete("1.0", tk.END)
                        self.role_entries_roll[role].insert("1.0", f"1d3")
                    if "精神分析" in expression:
                        self.role_entries[role].insert("1.0", f"[精神分析]恢复1D3 SAN\n")
                        self.role_entries_roll[role].delete("1.0", tk.END)
                        self.role_entries_roll[role].insert("1.0", f"1d3")
                if parts_ and "大失败" in parts_[1]:
                    if "精神分析" in expression:
                        self.role_entries[role].insert("1.0", f"[精神分析]损失1D6 SAN\n")
                        self.role_entries_roll[role].delete("1.0", tk.END)
                        self.role_entries_roll[role].insert("1.0", f"1d6")

    def roll_dice_silent(self, role, expression, reason):
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        SANC = ""
        self.role_entries[role].delete("1.0", tk.END)
        if reason == "":
            # 一系列字符串
            string_list = ["不可告人的妙计", "想到了开心的事情", "", "", ""]
            # 从列表中随机选择一个字符串
            reason = random.choice(string_list)
        if re.compile(r'^[+\-*/]').match(expression):
            pattern = re.compile(r'([+\-*/]+)(.*)')
            # 使用正则表达式进行匹配
            match = pattern.match(expression)
            # 提取匹配的结果
            if match:
                expression = match.group(2)
        if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
            if ("sc" or "SC" or ".sc" or "。sc") in expression:
                SANC = "[SAN CHECK" + expression.split("sc")[1].upper() + "]"
            else:
                SANC = "[" + expression.upper() + "]"
        if reason == "":
            message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【暗骰】{self.role_entries_name[role]}进行了一次{SANC}暗骰。\n\n'
        else:
            message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【暗骰】{self.role_entries_name[role]}因{reason}进行了一次{SANC}暗骰。\n\n'
        self.chat_log.insert(tk.END, message)
        self.chat_log.yview(tk.END)
        result = self.trpg_module.roll(expression, role)
        self.role_entries[role].insert(tk.END, result)

    def Add_NPC(self):
        self.dialog2 = LoadNPCDialog(self.root, f"选择要加载的NPC")
        result = self.dialog2.result
        # print(result)
        if result:
            slot = result["slot"]
            for name, value in result.items():
                if name == "slot":
                    pass
                else:
                    if value == "":
                        value = name
                    self.role_entries[slot].insert("1.0", f"正在使用[{name}]的属性扮演【{value}】\n===\n")
                    if name in self.infoCanvas_data_by_name:
                        self.infoCanvas_data[slot] = self.infoCanvas_data_by_name[name]
                    else:
                        print("该模板没有简卡图片！")
                    # 按名牌加载设置
                    # print(slot)
                    role_Chart[slot] = role_Chart_at_name[name].copy()
                    SAN = role_Chart_at_name[name].get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                    HP = role_Chart_at_name[name].get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                    MP = role_Chart_at_name[name].get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                    MOV = role_Chart_at_name[name].get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                    POW = role_Chart_at_name[name].get("POW")
                    DB = role_Chart_at_name[name].get("DB")
                    if "#SAN" in role_Chart_at_name[name]:
                        SAN_ = role_Chart_at_name[name].get("#SAN")
                    else:
                        SAN_ = 100
                    self.role_values_entry[slot].insert("1.0",
                                                        f'{SAN}/{SAN_}:S\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB\n===\n')
                    self.chat_log.insert(tk.END,
                                         f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{value}】的状态：\n{self.role_values_entry[slot].get("1.0", "6.0").strip()}\n\n')
                    self.chat_log.yview(tk.END)
                # print(result)

    def set_start_point(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            x, y = event.x, event.y
            self.canvas.tag_lower(self.canvas.create_line(self.start_x, self.start_y, x, y, width=2))
            self.start_x = x
            self.start_y = y

    def set_erase_point(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def erase(self, event):
        if self.start_x is not None and self.start_y is not None:
            x, y = event.x, event.y
            self.canvas.tag_lower(self.canvas.create_line(self.start_x, self.start_y, x, y, width=5, fill="white"))
            self.start_x = x
            self.start_y = y

    def stop_drawing(self, event):
        # 鼠标松开时的事件处理函数
        self.start_x = None
        self.start_y = None

    def delete_information(self, role):
        # 获取选中的条目
        if role == "KP":
            selected_item = self.tree_main.selection()
            if selected_item is None:
                selected_item = self.tree_main.selection()
                # 如果有选中的条目
                if selected_item:
                    # 更改选中条目的背景色为红色
                    # self.tree2_list[role].item(selected_item, tags=('red_background'))
                    self.tree_main.delete(selected_item)
            if selected_item:
                # 更改选中条目的背景色为红色
                # self.tree_list[role].item(selected_item, tags=('red_background'))
                self.tree_main.delete(selected_item)
        else:
            selected_item = self.tree2_list[role].selection()
            if selected_item is None:
                selected_item = self.tree_list[role].selection()
                # 如果有选中的条目
                if selected_item:
                    # 更改选中条目的背景色为红色
                    # self.tree2_list[role].item(selected_item, tags=('red_background'))
                    self.tree_list[role].delete(selected_item)
            if selected_item:
                # 更改选中条目的背景色为红色
                # self.tree_list[role].item(selected_item, tags=('red_background'))
                self.tree2_list[role].delete(selected_item)

    def on_double_click(self, event, role=None):
        # 获取双击的条目
        item = self.tree_list[role].selection()
        if item:
            # 获取条目的值
            values = self.tree_list[role].item(item, "values")
            # 创建一个弹出对话框，让用户输入新的记忆指数
            new_memory_index = simpledialog.askinteger("修改记忆指数", f"当前记忆指数：{values[2]}\n请输入新的记忆指数：", minvalue=-5,
                                                       maxvalue=100)
            if new_memory_index is not None:
                # 更新Treeview中的值
                self.tree_list[role].item(item, values=(values[0], values[1], new_memory_index))
        sorted_ids = sorted(self.tree_list[role].get_children(), key=lambda x: self.tree_list[role].set(x, "记忆指数"),
                            reverse=True)
        # 遍历排序后的条目ID，将它们插入到新的 Treeview 中
        for item_id in sorted_ids:
            values = self.tree_list[role].item(item_id, "values")
            # 在这里进行你需要的操作，可以根据需要修改 values 的内容
            self.tree_list[role].insert("", "end", values=values)
            self.tree_list[role].delete(item_id)
            self.tree_list[role].update()

    def on_double_click2(self, event, role=None):
        # 获取双击的条目
        item = self.tree2_list[role].selection()
        if item:
            # 获取条目的值
            values = self.tree2_list[role].item(item, "values")
            # 创建一个弹出对话框，让用户输入新的记忆指数
            new_memory_index = simpledialog.askinteger("修改记忆指数", f"当前记忆指数：{values[2]}\n请输入新的记忆指数：", minvalue=-5,
                                                       maxvalue=100)
            if new_memory_index is not None:
                # 更新Treeview中的值
                self.tree2_list[role].item(item, values=(values[0], values[1], new_memory_index, values[3]))
        sorted_ids = sorted(self.tree2_list[role].get_children(), key=lambda x: self.tree2_list[role].set(x, "记忆指数"),
                            reverse=True)
        # 遍历排序后的条目ID，将它们插入到新的 Treeview 中
        for item_id in sorted_ids:
            values = self.tree2_list[role].item(item_id, "values")
            # 在这里进行你需要的操作，可以根据需要修改 values 的内容
            self.tree2_list[role].insert("", "end", values=values)
            self.tree2_list[role].delete(item_id)
            self.tree2_list[role].update()

    def edit_callback(self, new_value, item, col_id, role):
        self.tree2_list[role].set(item, col_id, new_value)
        return True

    def add_information(self, role=None):
        self.information_sources = ["来源A", "来源B", "来源C"]  # 你的信息来源列表

        self.dialog = MemoryInfoDialog(self.new_window, f"为【{self.role_entries_name[role]}】添加信息",
                                       self.information_sources,
                                       role)
        result = self.dialog.result
        if result["评分"] == "遗忘":
            self.add_inference2self2(result["信息来源"], "[该信息已遗忘 - Ignorance is a bliss.]  " + result["信息内容"],
                                     result["记忆指数"], "×", role)
        else:
            self.add_inference2self(result["信息来源"], result["信息内容"], result["记忆指数"], role)

    def forget_information(self, role):
        # 实现遗忘信息的逻辑
        # 获取所有条目的ID
        all_items = self.tree_list[role].get_children()
        # 检查是否有条目
        if all_items:
            # 获取最后一个条目的ID
            last_item = all_items[-1]
            # 使用delete方法删除最后一个条目
            self.add_inference2self2(self.tree_list[role].item(last_item, "values")[0],
                                     self.tree_list[role].item(last_item, "values")[1],
                                     self.tree_list[role].item(last_item, "values")[2], "×", role)
            self.tree_list[role].delete(last_item)

    def upload_information(self, role=None):
        list = self.tree_list[role].get_children()
        for l in list:
            self.tree_main.insert("", "end", values=(
                self.tree_list[role].item(l, "values")[0], self.tree_list[role].item(l, "values")[1],
                self.role_entries_name[role], self.thoughts[role].get("1.0", tk.END)))
            print(self.tree_list[role].item(l, "values"))
            self.tree2_list[role].insert("", "end", values=(
                self.tree_list[role].item(l, "values")[0], self.tree_list[role].item(l, "values")[1],
                self.tree_list[role].item(l, "values")[2], "√"))
            self.tree_list[role].delete(l)
            # self.add_inference2public(l["信息来源"], "关于X的信息", "想法", role)
            # self.add_inference2self2("玩家1", "关于X的信息", -4, "√", role)
        sorted_ids = sorted(self.tree2_list[role].get_children(), key=lambda x: self.tree2_list[role].set(x, "记忆指数"),
                            reverse=True)
        # 遍历排序后的条目ID，将它们插入到新的 Treeview 中
        for item_id in sorted_ids:
            values = self.tree2_list[role].item(item_id, "values")
            # 在这里进行你需要的操作，可以根据需要修改 values 的内容
            self.tree2_list[role].insert("", "end", values=values)
            self.tree2_list[role].delete(item_id)
            self.tree2_list[role].update()

    def clear_information(self, role=None):
        if role == "KP":
            self.tree_main.delete(*self.tree_main.get_children())
        else:
            self.tree_list[role].delete(*self.tree_list[role].get_children())
            self.tree2_list[role].delete(*self.tree2_list[role].get_children())

    def calculator(self):
        self.dialog = DiceRollDialog(self.new_window, f"调查进度计算器")
        result = self.dialog.result

    def expand_information(self, role=None):
        _number = 0
        for role in self.roles:
            _number += 1
            _string = "PL " + str(_number + 2)
            if role == "PL 1" or role == "PL 4" or role == "PL 7":  # 最大支持到7个PL，后续可以用算式取代
                pass
            else:
                if self.info_toggle[role] == "off":
                    if role == "KP":
                        self.tree_main.grid_forget()
                        self.info_toggle[role] = "on"
                        # self.frames["KP"].grid_forget()
                    else:
                        self.tree_list[role].grid_forget()  # 缩进
                        self.tree2_list[role].grid_forget()
                        self.info_toggle[role] = "on"
                else:
                    if role == "KP":
                        # self.frames["KP"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                        self.tree_main.grid(row=1, column=3, sticky="nsew")
                        self.KP_entry.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")
                        self.info_toggle[role] = "off"
                    else:
                        self.tree_list[role].grid(row=0, column=4, sticky="nsew")
                        self.tree2_list[role].grid(row=2, column=4, sticky="nsew")
                        self.info_toggle[role] = "off"

    def add_inference2self(self, name, info, memory_index, role=None):
        # 在Treeview中添加一行数据
        if role == None:
            return
        self.tree_list[role].insert("", "end", values=(name, info, memory_index))
        # 获取 Treeview 中所有条目的ID，并按记忆指数从大到小排序
        sorted_ids = sorted(self.tree_list[role].get_children(), key=lambda x: self.tree_list[role].set(x, "记忆指数"),
                            reverse=True)
        # 遍历排序后的条目ID，将它们插入到新的 Treeview 中
        for item_id in sorted_ids:
            values = self.tree_list[role].item(item_id, "values")
            # 在这里进行你需要的操作，可以根据需要修改 values 的内容
            self.tree_list[role].insert("", "end", values=values)
            self.tree_list[role].delete(item_id)
            self.tree_list[role].update()

    def add_inference2self2(self, name, info, memory_index, status, role=None):
        # 在Treeview中添加一行数据
        if role == None:
            return
        self.tree2_list[role].insert("", "end", values=(name, info, memory_index, status))
        sorted_ids = sorted(self.tree2_list[role].get_children(), key=lambda x: self.tree2_list[role].set(x, "记忆指数"),
                            reverse=True)
        # 遍历排序后的条目ID，将它们插入到新的 Treeview 中
        for item_id in sorted_ids:
            values = self.tree2_list[role].item(item_id, "values")
            # 在这里进行你需要的操作，可以根据需要修改 values 的内容
            self.tree2_list[role].insert("", "end", values=values)
            self.tree2_list[role].delete(item_id)
            self.tree2_list[role].update()

    def add_inference2public(self, name, info, statement, role=None):
        # 在Treeview中添加一行数据
        if role == None:
            self.tree_main.insert("", "end", values=(name, info, "未知", statement))
        else:
            self.tree_main.insert("", "end", values=(name, info, self.role_entries_name[role], statement))

    def load_treeview_data(self, treeview, filename, role=None):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data_ = json.load(file)
                if data_:
                    if role == "KP":
                        data = data_[role]
                        for item_data in data:
                            treeview.insert('', 'end', values=item_data)
                    else:
                        data = data_[role]
                        for item_data in data:
                            treeview.insert('', 'end', values=item_data)
        except FileNotFoundError:
            print(f"文件 '{filename}' 不存在")

    def on_closing_new_window(self):
        with open('GameSaves/Deduction_infos_base.json', 'w', encoding='utf-8') as file:
            data = {}
            for role in self.roles:
                value_list = []
                if role != "KP":
                    for item in self.tree2_list[role].get_children():
                        values = self.tree2_list[role].item(item, 'values')
                        value_list.append(values)
                else:
                    for item in self.tree_main.get_children():
                        values = self.tree_main.item(item, 'values')
                        value_list.append(values)
                data[role] = value_list
            json.dump(data, file, ensure_ascii=False)
        with open('GameSaves/Deduction_infos_new.json', 'w', encoding='utf-8') as file:
            data = {}
            for role in self.roles:
                value_list = []
                if role != "KP":
                    for item in self.tree_list[role].get_children():
                        values = self.tree_list[role].item(item, 'values')
                        value_list.append(values)
                    data[role] = value_list
            json.dump(data, file, ensure_ascii=False)
        # self.new_window.destroy()

    def on_closing_new_window_close(self):
        with open('GameSaves/Deduction_infos_base.json', 'w', encoding='utf-8') as file:
            data = {}
            for role in self.roles:
                value_list = []
                if role != "KP":
                    for item in self.tree2_list[role].get_children():
                        values = self.tree2_list[role].item(item, 'values')
                        value_list.append(values)
                else:
                    for item in self.tree_main.get_children():
                        values = self.tree_main.item(item, 'values')
                        value_list.append(values)
                data[role] = value_list
            json.dump(data, file, ensure_ascii=False)
        with open('GameSaves/Deduction_infos_new.json', 'w', encoding='utf-8') as file:
            data = {}
            for role in self.roles:
                value_list = []
                if role != "KP":
                    for item in self.tree_list[role].get_children():
                        values = self.tree_list[role].item(item, 'values')
                        value_list.append(values)
                    data[role] = value_list
            json.dump(data, file, ensure_ascii=False)
        self.new_window.destroy()

    # 新窗口
    def open_new_window(self):
        self.new_window = tk.Toplevel(root)
        self.new_window.title("调查模块")

        # self.new_window.grid_rowconfigure(0, weight=1)
        # self.new_window.grid_columnconfigure(0, weight=1)
        self.info_add_button = {}
        self.thoughts = {}
        self.tree_list = {}
        self.tree2_list = {}
        self.info_upload_button = {}
        self.info_delete_button = {}
        self.info_expand_button = {}
        self.info_toggle = {}
        self.frames = {}

        num_cols = 3
        for idx, role in enumerate(self.roles):
            self.info_toggle[role] = "off"
            row = idx % num_cols
            col = idx // num_cols
            # 自动调整列宽
            for i in range(num_cols + 2):
                self.new_window.columnconfigure(i, weight=1)
            if role == "KP":
                frame = tk.LabelFrame(self.new_window, text="共享库", relief=tk.GROOVE)
                frame.grid(row=row, column=col + 2, padx=5, pady=5, sticky="nsew")
                self.frames["KP"] = frame
                clearKP_button = tk.Button(frame, text="清\n空\n信\n息", bg="red", fg="black",
                                           command=lambda role=role: self.clear_information(role))
                clearKP_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
                saveKP_button = tk.Button(frame, text="保\n存\n所\n有", bg="black", fg="white",
                                          command=self.on_closing_new_window)
                saveKP_button.grid(row=0, column=2, pady=5, sticky="nsew")
                deleteKP_button = tk.Button(frame, text="删\n除\n信\n息",
                                            command=lambda role=role: self.delete_information(role))
                deleteKP_button.grid(row=1, column=2, pady=5, sticky="nsew")
                # loadKP_button = tk.Button(frame, text="读\n取", command=self.load_treeview_data)
                # loadKP_button.grid(row=1, column=2, pady=5, sticky="nsew")
                map_button = tk.Button(frame, text="绘\n制\n地\n图", bg="green", fg="white",
                                       command=self.open_new_window_map)
                map_button.grid(row=0, column=1, pady=5, sticky="nsew")
                cal_button = tk.Button(frame, text="计\n算\n器", bg="blue", fg="white", command=self.calculator)
                cal_button.grid(row=1, column=1, pady=5, sticky="nsew")
                # frame.grid_rowconfigure(0, weight=1)
                # frame.grid_columnconfigure(0, weight=1)
            else:
                if role == "DiceBot":
                    frame = tk.LabelFrame(self.new_window, text="NPC", relief=tk.GROOVE)
                    frame.grid(row=row, column=col + 2, padx=5, pady=5, sticky="nsew")
                    # frame.grid_rowconfigure(0, weight=1)
                    # frame.grid_columnconfigure(0, weight=1)
                else:
                    frame = tk.LabelFrame(self.new_window, text=f"{role} - {self.role_entries_name[role]}",
                                          relief=tk.GROOVE)
                    frame.grid(row=row, column=col + 2, padx=5, pady=5, sticky="nsew")
                self.frames[role] = frame
                # frame.grid_rowconfigure(0, weight=1)
                # frame.grid_columnconfigure(0, weight=1)

                forget_button = tk.Button(frame, text="遗\n忘\n信\n息",
                                          command=lambda role=role: self.forget_information(role))
                forget_button.grid(row=2, column=2, pady=5, sticky="nsew")
                upload_button = tk.Button(frame, text="分\n享\n信\n息",
                                          command=lambda role=role: self.upload_information(role))
                upload_button.grid(row=0, column=1, pady=5, sticky="nsew")
                add_button = tk.Button(frame, text="添\n加\n信\n息", command=lambda role=role: self.add_information(role))
                add_button.grid(row=0, column=2, pady=5, sticky="nsew")
                self.info_add_button[role] = add_button
                delete_button = tk.Button(frame, text="删\n除\n信\n息",
                                          command=lambda role=role: self.delete_information(role))
                delete_button.grid(row=2, column=1, pady=5, sticky="nsew")
                clear_button = tk.Button(frame, text="清\n空\n信\n息", bg="red", fg="black",
                                         command=lambda role=role: self.clear_information(role))
                clear_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

            expand_button = tk.Button(frame, text="展\n开\n收\n起", command=lambda role=role: self.expand_information(role))
            expand_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.info_expand_button[role] = expand_button
            # 使用style修改Treeview的样式
            style = ttk.Style()
            style.configure("Treeview", font=(None, 10), rowheight=12, height=5, sticky="nsew",
                            maxheight=5)  # 设置表头的字体大小

            if role == "KP":
                self.KP_entry = tk.Text(frame, wrap=tk.WORD, width=10, height=12)
                self.KP_entry.insert(tk.END, "← 关闭此窗口触发自动保存，也可以手动点击此按钮保存！\n此处可以自由编辑文本，对程序不存在任何影响")
                self.KP_entry.grid(row=0, column=3, padx=0, pady=0, sticky="nsew")
                # 创建Treeview
                self.tree_main = ttk.Treeview(frame, columns=("信息来源", "信息内容", "共享人", "共享想法"), show="headings",
                                              style="Treeview")
                self.tree_main.heading("信息来源", text="信息来源")
                self.tree_main.heading("信息内容", text="信息内容")
                self.tree_main.heading("共享人", text="共享人")
                self.tree_main.heading("共享想法", text="共享想法")
                self.tree_main.column("信息来源", width=100)
                self.tree_main.column("信息内容", width=200)
                self.tree_main.column("共享人", width=50)
                self.tree_main.column("共享想法", width=100)
                self.tree_main.grid(row=1, column=3, sticky="nsew")
                # 设置行和列的权重，使得Treeview可以随窗口的大小变化而调整
                self.tree_main.grid_rowconfigure(0, weight=1)
                self.load_treeview_data(self.tree_main, "GameSaves/Deduction_infos_base.json", role)
            else:
                entry2 = tk.Text(frame, wrap=tk.WORD, width=1, height=1)
                entry2.grid(row=1, column=4, padx=0, pady=0, sticky="nsew")
                self.thoughts[role] = entry2
                # 创建Treeview
                self.tree = ttk.Treeview(frame, columns=("信息来源", "信息内容", "记忆指数"), show="headings",
                                         style="Treeview")
                self.tree_list[role] = self.tree
                # 创建Treeview
                self.tree2 = ttk.Treeview(frame, columns=("信息来源", "信息内容", "记忆指数", "记忆状态"), show="headings",
                                          style="Treeview")
                self.tree2_list[role] = self.tree2
                # 添加标签以供后续使用
                self.tree2.tag_configure('red_background', background='red')
                self.tree2.bind("<Double-1>", lambda event, role=role: self.on_double_click2(event, role))
                self.tree.bind("<Double-1>", lambda event, role=role: self.on_double_click(event, role))

                # 创建Scrollbar
                # scrollbar = ttk.Scrollbar(self.new_window, orient="vertical", command=self.tree.yview)
                # 配置Treeview的yview和Scrollbar的command
                # self.tree.configure(yscrollcommand=scrollbar.set)
                # scrollbar.grid(row=0, column=1, sticky="ns")
                # self.tree.bind("<Double-1>", self.on_double_click())

                # 设置表头
                self.tree.heading("信息来源", text="来源")
                self.tree.heading("信息内容", text="内容")
                self.tree.heading("记忆指数", text="指数")
                self.tree2.heading("信息来源", text="来源")
                self.tree2.heading("信息内容", text="内容")
                self.tree2.heading("记忆指数", text="指数")
                self.tree2.heading("记忆状态", text="状态")

                # 设置列宽
                self.tree.column("信息来源", width=130)
                self.tree.column("信息内容", width=310)
                self.tree.column("记忆指数", width=10)
                self.tree2.column("信息来源", width=130)
                self.tree2.column("信息内容", width=300)
                self.tree2.column("记忆指数", width=10)
                self.tree2.column("记忆状态", width=10)

                # 将Treeview放置在窗口中，使用grid布局
                self.tree.grid(row=0, column=4, sticky="nsew")
                # 将Treeview放置在窗口中，使用grid布局
                self.tree2.grid(row=2, column=4, sticky="nsew")

                # 设置行和列的权重，使得Treeview可以随窗口的大小变化而调整
                self.tree.grid_rowconfigure(0, weight=1)
                self.tree.grid_columnconfigure(0, weight=1)
                self.tree2.grid_rowconfigure(0, weight=1)
                self.tree2.grid_columnconfigure(0, weight=1)

                self.load_treeview_data(self.tree2_list[role], "GameSaves/Deduction_infos_base.json", role)
                self.load_treeview_data(self.tree_list[role], "GameSaves/Deduction_infos_new.json", role)

                # 添加示例数据
                # self.add_inference2public("玩家1", "关于X的信息", "关于X的信息")
                if role == "DiceBot":
                    self.add_inference2self("xxx", "xxx的可能性", 0, role)
                # self.add_inference("玩家2", "关于Y的信息", 5, "√")
            # 配置可调整大小的框架
            # 绑定关闭事件
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing_new_window_close)

    # 新窗口
    def open_new_window_map(self):
        global frame_Map
        new_window = tk.Toplevel(self.new_window)
        new_window.title("简易地图")

        self.image_references = []  # Add this list attribute to store references to images

        text = self.time_log.get("1.0", tk.END).strip()
        label = tk.Label(new_window,
                         text="地图即时使用，信息不互通，关闭即销毁: [右键]绘图/副本(大小随机&透明度正负) | [右键角色/无图则❤]载入战斗图像 | [右键战斗图像]销毁 | [单击标签/❤]编辑 | [中键拖拽标签]缩放(仅限矩形和圆)")
        label.pack()

        label2 = tk.Label(new_window,
                          text=text)
        label2.pack()

        # 创建 Canvas 组件
        self.canvas = tk.Canvas(new_window, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        if os.path.exists('GameSaves/canvas_state.json'):
            # saver = CanvasSaver(self.canvas)
            # saver.load_canvas_state('GameSaves/canvas_state.json')
            # print("发现了保存State，读取旧地图...")
            pass
        else:
            print("无保存State，创建新地图...")

            # 记录鼠标位置
            self.start_x = None
            self.start_y = None

            # 绑定鼠标事件
            self.canvas.bind("<B3-Motion>", self.draw)
            self.canvas.bind("<Button-3>", self.set_start_point)

            # self.canvas.bind("<B1-Motion>", self.erase)
            # self.canvas.bind("<Button-1>", self.set_erase_point)

            self.draggable_items = {}
            radius = 0.08
            x = 100
            y = 50
            for _avatar in self.roles:
                if os.path.exists(self.role_avatar_paths[_avatar]):
                    with open(self.role_avatar_paths[_avatar], "rb") as f:
                        image = Image.open(f)
                        width, height = image.size
                        image = image.resize((int(width * radius), int(height * radius)), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        # circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='', outline="black", width=2)
                        # self.canvas.create_image(x, y, image=photo)
                        # 保持对图像的引用，防止被垃圾回收
                        # self.canvas.image = photo
                        # Keep references to all images
                        self.image_references.append(photo)
                        # Create draggable image

                    # Add label below the image
                    label_text = self.role_entries_name[
                                     _avatar] + "(" + _avatar + ")"  # You can replace this with whatever text you want
                    label_text2 = f"H{self.role_values_entry[_avatar].get('2.0', '3.0').split('/')[0].strip()} S{self.role_values_entry[_avatar].get('1.0', '2.0').split('/')[0].strip()} M{self.role_values_entry[_avatar].get('4.0', '5.0').split('/')[0].strip()}"
                    # Bind label's movement with image
                    # label_below_image_canvas = self.canvas.create_window(x-50, y+60, window=label_below_image, anchor=tk.NW)
                    _, extension = os.path.splitext(self.role_avatar_paths[_avatar])
                    if extension == ".gif" or extension == ".GIF":
                        image = Image.open(self.role_avatar_paths[_avatar])
                        width, height = image.size
                        frames_map[frame_Map] = [
                            ImageTk.PhotoImage(frame.resize((int(width * 0.25), int(height * 0.25)), Image.LANCZOS))
                            for frame
                            in ImageSequence.Iterator(image)]
                        # 显示 GIF 图片的第一帧
                        current_frame_map[frame_Map] = DraggableItem(self.canvas, x, y, 10, 10,
                                                                     image=frames_map[frame_Map][0],
                                                                     label=label_text,
                                                                     label2=label_text2, type="image_animate",
                                                                     frame=frame_Map)
                        y += 100
                        self.draggable_items[_avatar] = current_frame_map[frame_Map]
                        frame_Map += 1
                    else:
                        draggable_image = DraggableItem(self.canvas, x, y, 10, 10, image=photo, label=label_text,
                                                        label2=label_text2, type='image')
                        y += 100
                        self.draggable_items[_avatar] = draggable_image
                else:
                    label_text = self.role_entries_name[
                                     _avatar] + "(" + _avatar + ")"  # You can replace this with whatever text you want
                    label_text2 = f"H{self.role_values_entry[_avatar].get('2.0', '3.0').split('/')[0].strip()} S{self.role_values_entry[_avatar].get('1.0', '2.0').split('/')[0].strip()} M{self.role_values_entry[_avatar].get('4.0', '5.0').split('/')[0].strip()}"
                    # Bind label's movement with image
                    # label_below_image_canvas = self.canvas.create_window(x-50, y+60, window=label_below_image, anchor=tk.NW)
                    draggable_image = DraggableItem(self.canvas, x, y, 50, 50, fill='', outline='black',
                                                    label=label_text, label2=label_text2,
                                                    type='text')
                    y += 100
                    self.draggable_items[_avatar] = draggable_image
            # Create draggable rectangle
            draggable_rectangle = DraggableItem(self.canvas, 150, 50, 100, 80, fill='', outline='black', label='标签',
                                                type='rectangle')
            draggable_rectangle = DraggableItem(self.canvas, 150, 100, 100, 100, fill='', outline='black', label='标签',
                                                type='circle')
            draggable_rectangle = DraggableItem(self.canvas, 150, 150, 100, 80, fill='', outline='black', label='标签',
                                                type='oval')
            draggable_rectangle = DraggableItem(self.canvas, 150, 200, 100, 80, fill='', outline='black', label='标签',
                                                type='polygon3')
            draggable_rectangle = DraggableItem(self.canvas, 150, 250, 50, 50, fill='', outline='black', label='标签',
                                                type='polygon6')
            draggable_rectangle = DraggableItem(self.canvas, 150, 300, 50, 50, fill='', outline='black', label='标签',
                                                type='polygon8')
            draggable_rectangle = DraggableItem(self.canvas, 150, 350, 50, 50, fill='', outline='black', label='标签',
                                                type='polygon5')
            draggable_rectangle = DraggableItem(self.canvas, 150, 400, 50, 50, fill='', outline='black', label='标签',
                                                type='polygonStar')
            # draggable_rectangle = DraggableItem(self.canvas, 150, 150, 100, 80, fill='white', outline='black', label='text',
            # type='line')
            draggable_rectangle = DraggableItem(self.canvas, 150, 450, 50, 50, fill='', outline='black', label='标签',
                                                type='text')
        # 绑定关闭事件
        # new_window.protocol("WM_DELETE_WINDOW", self.on_close_map)

    def on_close_map(self):
        if messagebox.askokcancel("储存进度？", "要保存地图State吗？"):
            saver = CanvasSaver(self.canvas)
            # Save canvas state to a JSON file
            saver.save_canvas_state('GameSaves/canvas_state.json')
        else:
            if os.path.exists('GameSaves/canvas_state.json'):
                os.remove('GameSaves/canvas_state.json')

    def save_settings(self):
        # 将头像路径保存到JSON文件
        with open('AppSettings/avatar_settings.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_avatar_paths, file, ensure_ascii=False)
        # 将状态Icon路径保存到JSON文件
        with open('GameSaves/icon_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_Icon_paths, file, ensure_ascii=False)
        # 将姓名牌路径保存到JSON文件
        with open('AppSettings/name_settings.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_entries_name, file, ensure_ascii=False)
        # 将角色简卡路径保存到JSON文件
        with open('AppSettings/infoCanvas_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.infoCanvas_data, file, ensure_ascii=False)
        # 将差分目录路径保存到JSON文件
        with open('AppSettings/avatar_dir_path.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_dir_path, file, ensure_ascii=False)
        with open('AppSettings/infoCanvas_data_by_name.json', 'w', encoding='utf-8') as file:
            json.dump(self.infoCanvas_data_by_name, file, ensure_ascii=False)
        # 将角色可变数值保存到JSON文件
        with open('GameSaves/health_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.health_data, file, ensure_ascii=False)
        with open('GameSaves/health_data_by_name.json', 'w', encoding='utf-8') as file:
            json.dump(self.health_data_by_name, file, ensure_ascii=False)
        # 尝试保存自定义角色数值信息
        for role in self.role_values_tags:
            self.role_values_tags_text[role] = self.role_values_entry[role].get("1.0", tk.END).strip()
        with open('GameSaves/pl_info.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_values_tags_text, file, ensure_ascii=False)
        # 尝试保存地点时间天气信息
        with open('GameSaves/env_info.json', 'w', encoding='utf-8') as file:
            info = self.time_log.get("1.0", tk.END).strip()
            info = info.split("【时间】")[1]
            env["Date"] = info.split("【日期】")[1]
            env["Time"] = info.split("【地点】")[0]
            info = info.split("【地点】")[1]
            env["Place"] = info.split("【天气】")[0]
            info = info.split("【天气】")[1]
            env["Weather"] = info.split("【日期】")[0]
            json.dump(env, file, ensure_ascii=False)
        # 保存自定义角色数值信息
        with open('GameSaves/pl_Chart.json', 'w', encoding='utf-8') as file:
            json.dump(role_Chart, file, ensure_ascii=False)
        with open('Bots/bot_personality_by_name.json', 'w', encoding='utf-8') as file:
            json.dump(bot_personality_by_name, file, ensure_ascii=False)
        # 保存自定义角色数值信息
        with open('GameSaves/PL_Chart_Save.txt', 'w', encoding='utf-8') as txt_file:
            for role, skills in role_Chart.items():
                txt_file.write(f"【{role}】-{self.role_entries_name[role]}\n.st")
                for skill, value in skills.items():
                    if skill == "_AvatarPath" or ("#" in skill) or (skill == "DB"):
                        pass
                    else:
                        txt_file.write(f"{skill}{value} ")
                txt_file.write("\n\n\n")
        # 按姓名牌保存自定义角色数值信息
        self.save_role_skill_at_name()

    def save_role_skill_at_name(self):
        global role_Chart_at_name
        with open('GameSaves/pl_Chart_at_name.json', 'w', encoding='utf-8') as file:
            dic = role_Chart_at_name.copy()
            for role, skills in role_Chart.items():
                dicSkill = {}
                for skill, value in skills.items():
                    dicSkill[skill] = value
                dicSkill["_AvatarPath"] = ""
                if role in self.role_avatar_paths:
                    # 保存头像路径
                    dicSkill["_AvatarPath"] = self.role_avatar_paths[role]
                if "PL " not in self.role_entries_name[role]:
                    dic[self.role_entries_name[role]] = dicSkill.copy()
            json.dump(dic, file, ensure_ascii=False)

    def save_role_count(self):
        # 保存角色数量到配置文件
        config = configparser.ConfigParser()
        config['Settings'] = {'RoleCount': str(self.role_count)}
        with open('AppSettings/config.ini', 'w') as configfile:
            config.write(configfile)

    def on_closing(self):
        # 在关闭窗口前保存设置
        self.save_settings()
        # 退出时保存当前角色数量
        self.save_role_count()
        self.root.destroy()


class TRPGModule:
    def __init__(self, chat_app_instance, root):
        self.random_seed = None
        self.ChatApp = chat_app_instance
        self.root = root
        adv_comment = ""

    def skill_upgrade(self, info_, skill_name, role):
        upgrade = ""
        if "None" not in skill_name and "教育" not in skill_name and "魅力" not in skill_name and "力量" not in skill_name and "敏捷" not in skill_name and "外貌" not in skill_name and "智力" not in skill_name and "体质" not in skill_name and "灵感" not in skill_name and "意志" not in skill_name and "体型" not in skill_name and "信用" not in skill_name and "幸运" not in skill_name and "MOV" not in skill_name and "HP" not in skill_name and "MP" not in skill_name and "SAN" not in skill_name and "克苏鲁" not in skill_name and (
                f".st{skill_name}" not in self.ChatApp.role_values_entry[role].get("1.0",
                                                                                   tk.END).strip()) and skill_name != "" and "DB" not in skill_name:  # 成长检定
            # 执行d100掷骰
            rolls = [random.randint(1, 100) for _ in range(1)]
            result = sum(rolls)
            if result >= info_ or result >= 96:
                # 执行d10掷骰
                rolls = [random.randint(1, 10) for _ in range(1)]
                result2 = sum(rolls)
                upgrade = "[成长检定]【" + skill_name + "】技能获得了成长(1D100=" + str(result) + "/" + str(info_) + "):D10=" + str(
                    result2)
                result3 = role_Chart[role][skill_name] + result2
                self.ChatApp.role_values_entry[role].insert(tk.END, f'\n.st{skill_name}{str(result3)}')
            else:
                upgrade = "[成长检定]【" + skill_name + "】技能的成长检定(1D100=" + str(result) + "/" + str(info_) + ")败北了..."
        return upgrade

    def skill_check(self, info_, result):
        if result <= 5 and info_ >= Critical_Success_SKill:
            compare = "<"
            comment = Critical_Success
        elif result == 1:
            compare = "<"
            comment = Critical_Success
        elif result <= info_ // 5:
            compare = "<"
            comment = Extreme_Success
        elif result <= info_ // 2:
            compare = "<"
            comment = Hard_Success
        elif result <= info_:
            compare = "<"
            comment = Success
        elif result >= 96 and info_ < Fumble_SKill:
            compare = ">"
            comment = Fumble
        elif result == 100:
            compare = ">"
            comment = Fumble
        else:
            compare = ">"
            comment = Failure
        return comment

    def cal_advantage(self, result, advantage):
        global adv_comment
        adv_comment_1 = ""
        adv_comment_2 = ""
        if advantage is not None:
            list = []
            # 获取个位
            ones_place = result % 10
            # 获取十位
            tens_place = (result // 10) % 10
            list.append(tens_place)
            if "+" in advantage:
                for a in advantage["+"]:
                    if a == 10:
                        a = 0
                    list.append(a)
                # self.ChatApp.chat_log.insert(tk.END, f"\n优势骰：{list} = {max(list)}")
                adv_comment_1 = f"具备优势:{list}={min(list)}"
                result = ones_place + min(list) * 10
            list = [tens_place]
            if "-" in advantage:
                for a in advantage["-"]:
                    if a == 10:
                        a = 0
                    list.append(a)
                # self.ChatApp.chat_log.insert(tk.END, f"\n劣势骰：{list} = {min(list)}")
                adv_comment_2 = f"造成劣势:{list}={max(list)}"
                result = ones_place + max(list) * 10
            adv_comment = adv_comment_1 + adv_comment_2
        # if result > 100:
        # result = 100
        return result, adv_comment

    def roll(self, expression, role=None, allin=False):
        global date
        global time
        global place
        global weather
        HP_MP_check = ""
        fuhao = ""
        combine_infos = {}
        if self.random_seed is not None:
            random.seed(self.random_seed)
        info = None
        sc_success = ""
        sc_fail = ""
        skill_name = ""
        advantage = {}
        try:
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            pattern_user = re.compile(r'([\u4e00-\u9fa5a-zA-Z]+)(\d+)')
            pattern_advantage = re.compile(r'^[+\-*/]')
            pattern_combine = re.compile(r'[\u4e00-\u9fa5a-zA-Z]+[\u4e00-\u9fa5a-zA-Z]')
            part_eng = pattern_user.findall(expression)
            part_combine = pattern_combine.findall(expression)
            # print(part_eng)
            if "HP" in expression.upper() or "MP" in expression.upper():
                print("HP/MP变化")
                if "HP" in expression.upper():
                    HP_MP_check = "HP"
                elif "MP" in expression.upper():
                    HP_MP_check = "MP"
                else:
                    HP_MP_check = ""
                expression = expression.upper().replace("HP", "").replace("MP", "")
            if pattern_combine.match(expression) and len(part_combine) > 1:
                role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
                print("联合掷骰")  # 意志+斗殴+潜行
                # print(part_combine)
                for a in part_combine:
                    combine_infos[a] = role_Chart_detail[a]
                print(combine_infos)
                expression = "COMBINE CHECK"
            if pattern_advantage.match(expression) and HP_MP_check == "":
                print("优劣势掷骰")  # ++xxx
                expression_slice = expression
                matches = []
                while pattern_advantage.match(expression_slice):
                    matches.append(expression[0])
                    expression_slice = expression_slice[1:]
                # print(matches)
                for operator in matches:
                    num_operators = matches.count(operator)
                    roll_result = random.randint(1, 10)
                    # 如果运算符在字典中，将结果添加到相应的列表
                    if operator in advantage:
                        advantage[operator].append(roll_result)
                    else:
                        advantage[operator] = [roll_result]
                    expression = expression[1:]
                    print(expression)
                    print(advantage)
                # print(advantage)

            if ("sc" or "SC" or ".sc" or "。sc") in expression:
                print("SAN CHECK")  # sc1/1d5
                role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
                info = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                if info == 0:
                    info = role_Chart_detail.get("POW")
                parts_ = expression.split('sc')
                if parts_[1] == "":
                    expression = "1d100"
                else:
                    parts_ = parts_[1].split('/')
                    # print(parts_)
                    sc_success = parts_[0].replace(" ", "")
                    sc_fail = parts_[1].replace(" ", "")
                    expression = "SAN CHECK"

            elif ("san" or "San" or "SAN") in expression:
                role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
                info = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                if info == 0:
                    info = role_Chart_detail.get("POW")
                expression = "1d100"

            # elif expression == "COMBINE CHECK": # 对每个技能都掷骰的方案
            #     for a in combine_infos:
            #         expression = a
            #         info = int(combine_infos[a])
            #         if "困难" in expression or "极难" in expression:
            #             print("困难极难")
            #             print(expression)
            #             parts_ = expression.split('难')
            #             skill_name = parts_[1]
            #             if parts_[0] == "极":
            #                 info = int(combine_infos[a] / 5)
            #             if parts_[0] == "困":
            #                 info = int(combine_infos[a] / 2)
            #         # 执行掷骰
            #         rolls = [random.randint(1, 100) for _ in range(1)]
            #         result = sum(rolls)
            #         result, adv_comment = self.cal_advantage(result, advantage)
            #         if result <= 5 and info >= Critical_Success_SKill:
            #             compare = "<"
            #             comment = Critical_Success
            #             upgrade = self.skill_upgrade(0, skill_name, role)
            #         elif result == 1:
            #             compare = "<"
            #             comment = Critical_Success
            #             upgrade = self.skill_upgrade(0, skill_name, role)
            #         elif result <= info // 5:
            #             compare = "<"
            #             comment = Extreme_Success
            #             upgrade = self.skill_upgrade(info, skill_name, role)
            #         elif result <= info // 2:
            #             compare = "<"
            #             comment = Hard_Success
            #             upgrade = self.skill_upgrade(info, skill_name, role)
            #         elif result <= info:
            #             compare = "<"
            #             comment = Success
            #             upgrade = self.skill_upgrade(info, skill_name, role)
            #         elif result >= 96 and info < Fumble_SKill:
            #             compare = ">"
            #             comment = Fumble
            #             upgrade = ""
            #         elif result == 100:
            #             compare = ">"
            #             comment = Fumble
            #             upgrade = ""
            #         else:
            #             compare = ">"
            #             comment = Failure
            #             upgrade = ""
            #             # 执行算式
            #         print(f"{result}/{info}：{comment}\n\n{upgrade}")

            elif expression == "COMBINE CHECK":
                rolls = [random.randint(1, 100) for _ in range(1)]
                result = sum(rolls)
                result, adv_comment = self.cal_advantage(result, advantage)
                infos = []
                upgrades = []
                comments = []

                time_info = self.ChatApp.time_log.get("1.0", tk.END).strip()
                time_info = time_info.split("【时间】")[1]
                date = time_info.split("【日期】")[1]
                time = time_info.split("【地点】")[0]
                time_info = time_info.split("【地点】")[1]
                place = time_info.split("【天气】")[0]
                time_info = time_info.split("【天气】")[1]
                weather = time_info.split("【日期】")[0]

                # 自动计算时间
                for a in combine_infos:
                    for timer, timerlist in time_skill.items():
                        for skillname in timerlist:
                            if a == skillname:
                                if allin:
                                    if (timer == "time_3s") or (timer == "time_1min"):
                                        self.move_time_forward(timer)
                                    elif timer == "time_5min":
                                        self.move_time_forward("time_1min")
                                    elif timer == "time_10min":
                                        self.move_time_forward("time_5min")
                                    elif timer == "time_30min":
                                        self.move_time_forward("time_10min")
                                    elif timer == "time_1h":
                                        self.move_time_forward("time_30min")
                                    elif timer == "time_3h":
                                        self.move_time_forward("time_1h")
                                    elif timer == "time_12h":
                                        self.move_time_forward("time_3h")
                                    elif timer == "time_1d":
                                        self.move_time_forward("time_12h")
                                    elif timer == "time_1w":
                                        self.move_time_forward("time_1d")
                                    else:
                                        self.move_time_forward("time_5min")
                                else:
                                    self.move_time_forward(timer)
                    expression = a
                    info = combine_infos[a]
                    skill_name = a
                    if "困难" in expression or "极难" in expression:
                        print("困难极难")
                        print(expression)
                        parts_ = expression.split('难')
                        skill_name = parts_[1]
                        if parts_[0] == "极":
                            info = int(combine_infos[a] / 5)
                        if parts_[0] == "困":
                            info = int(combine_infos[a] / 2)
                    infos.append(info)
                    # 执行掷骰
                    if result <= 5 and info >= Critical_Success_SKill:
                        compare = "<"
                        comment = "大成功！！"
                        upgrade = self.skill_upgrade(0, skill_name, role)
                    elif result == 1:
                        compare = "<"
                        comment = "大成功！！"
                        upgrade = self.skill_upgrade(0, skill_name, role)
                    elif result <= info // 5:
                        compare = "<"
                        comment = "极难成功！"
                        upgrade = self.skill_upgrade(info, skill_name, role)
                    elif result <= info // 2:
                        compare = "<"
                        comment = "困难成功"
                        upgrade = self.skill_upgrade(info, skill_name, role)
                    elif result <= info:
                        compare = "<"
                        comment = "成功"
                        upgrade = self.skill_upgrade(info, skill_name, role)
                    elif result >= 96 and info < Fumble_SKill:
                        compare = ">"
                        comment = "大失败！"
                        upgrade = ""
                    elif result == 100:
                        compare = ">"
                        comment = "大失败！"
                        upgrade = ""
                    else:
                        compare = ">"
                        comment = "失败"
                        upgrade = ""
                        # 执行算式
                    upgrades.append(upgrade)
                    comments.append(comment)
                    # print(f"{result}/{info}：{comment}\n\n{upgrade}")
                str_ = '\n'.join(upgrades).strip()
                return f"{result}/{infos}:{'/'.join(comments)}：{str_}"

            elif HP_MP_check == "" and (bool(pattern.search(expression)) or part_eng[0][0] != "d"):
                expression_num = 0
                print("技能检定")
                # print(part_eng[0][0])
                # print(part_eng[0][1])
                print(expression)
                if "+" in expression or "-" in expression:
                    print("补正骰")
                    if "+" in expression:
                        expression_num = expression.split("+")[1]
                        expression = expression.split("+")[0]
                    if "-" in expression:
                        expression_num = expression.split("-")[1] * (-1)
                        expression = expression.split("-")[0]
                if part_eng and part_eng[0] and part_eng[0][1] is not None:
                    print("技能检定+数值")
                    expression = part_eng[0][0]
                    info = int(part_eng[0][1])
                    skill_name = "None"

                time_info = self.ChatApp.time_log.get("1.0", tk.END).strip()
                time_info = time_info.split("【时间】")[1]
                date = time_info.split("【日期】")[1]
                time = time_info.split("【地点】")[0]
                time_info = time_info.split("【地点】")[1]
                place = time_info.split("【天气】")[0]
                time_info = time_info.split("【天气】")[1]
                weather = time_info.split("【日期】")[0]

                # 自动计算时间

                for timer, timerlist in time_skill.items():
                    for skillname in timerlist:
                        if expression == skillname:
                            if allin:
                                if (timer == "time_3s") or (timer == "time_1min"):
                                    self.move_time_forward(timer)
                                elif timer == "time_5min":
                                    self.move_time_forward("time_1min")
                                elif timer == "time_10min":
                                    self.move_time_forward("time_5min")
                                elif timer == "time_30min":
                                    self.move_time_forward("time_10min")
                                elif timer == "time_1h":
                                    self.move_time_forward("time_30min")
                                elif timer == "time_3h":
                                    self.move_time_forward("time_1h")
                                elif timer == "time_12h":
                                    self.move_time_forward("time_3h")
                                elif timer == "time_1d":
                                    self.move_time_forward("time_12h")
                                elif timer == "time_1w":
                                    self.move_time_forward("time_1d")
                                else:
                                    self.move_time_forward("time_5min")
                            else:
                                self.move_time_forward(timer)

                role_Chart_detail = role_Chart.get(role, {}).copy()  # 获取 "KP" 对应的字典，如果没有则返回空字典
                if "困难" in expression or "极难" in expression:
                    print("困难极难")
                    print(expression)
                    parts_ = expression.split('难')
                    skill_name = parts_[1]
                    if parts_[0] == "极":
                        info = int(role_Chart_detail.get(parts_[1]) / 5)
                    if parts_[0] == "困":
                        info = int(role_Chart_detail.get(parts_[1]) / 2)
                else:
                    # print(expression)
                    if info == None:
                        if skill_name == "None":
                            skill_name = "None"
                        else:
                            skill_name = expression
                        info = role_Chart_detail.get(expression)  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        print("info == None")
                    # print(info)
                if str(info).isalpha():
                    info = role_Chart_detail.get(info)
                    # print(info)
                expression = "1d100"
                info += int(expression_num)
            if expression == "SAN CHECK":
                # 解析表达式
                expression = "1d100"
                parts = expression.split('d')
                num_rolls = int(parts[0])
                num_faces = int(parts[1])
                # 执行掷骰
                rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                result = sum(rolls)
                result, adv_comment = self.cal_advantage(result, advantage)
                if info >= result:
                    if "d" in sc_success:
                        expression = sc_success
                        parts = expression.split('d')
                        num_rolls = int(parts[0])
                        num_faces = int(parts[1])
                        # 执行掷骰
                        rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                        result2 = sum(rolls)
                        if result2 == 0:
                            return f"{result}/{info}={sc_success.upper()}={result2}：San Check成功！司空见惯！"
                        else:
                            role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                            POW = role_Chart[role].get("POW")
                            SAN = role_Chart[role].get("SAN")
                            if "#SAN" in role_Chart[role]:
                                SAN_ = role_Chart[role].get("#SAN")
                            else:
                                SAN_ = 100
                            self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                        f'{SAN}/{SAN_}:SAN\n')
                            self.ChatApp.chat_log.insert(tk.END,
                                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                            return f"{result}/{info}={sc_success.upper()}={result2}：San Check成功，扣除{result2}点SAN。"
                    else:
                        result2 = int(sc_success)
                        if result2 == 0:
                            return f"{result}/{info}={result2}：San Check成功！司空见惯！"
                        else:
                            role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                            POW = role_Chart[role].get("POW")
                            SAN = role_Chart[role].get("SAN")
                            if "#SAN" in role_Chart[role]:
                                SAN_ = role_Chart[role].get("#SAN")
                            else:
                                SAN_ = 100
                            self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                        f'{SAN}/{SAN_}:SAN\n')
                            self.ChatApp.chat_log.insert(tk.END,
                                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                            return f"{result}/{info}={result2}：San Check成功，扣除{result2}点SAN。"
                else:
                    if "d" in sc_fail:
                        expression = sc_fail
                        parts = expression.split('d')
                        num_rolls = int(parts[0])
                        num_faces = int(parts[1])
                        # 执行掷骰
                        rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                        result2 = sum(rolls)
                        role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                        POW = role_Chart[role].get("POW")
                        SAN = role_Chart[role].get("SAN")
                        if "#SAN" in role_Chart[role]:
                            SAN_ = role_Chart[role].get("#SAN")
                        else:
                            SAN_ = 100
                        self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                    f'{SAN}/{SAN_}:SAN\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                     f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                        return f"{result}/{info}={sc_fail.upper()}={result2}：San Check失败！扣除{result2}点SAN。"
                    else:
                        result2 = int(sc_fail)
                        role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                        POW = role_Chart[role].get("POW")
                        SAN = role_Chart[role].get("SAN")
                        if "#SAN" in role_Chart[role]:
                            SAN_ = role_Chart[role].get("#SAN")
                        else:
                            SAN_ = 100
                        self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                    f'{SAN}/{SAN_}:SAN\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                     f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                        return f"{result}/{info}={result2}：San Check失败！扣除{result2}点SAN。"
            if HP_MP_check != "":
                print(HP_MP_check)
                fuhao = expression[0]
                expression = expression.replace(fuhao, "").lower()
                exp = expression
                HP = role_Chart[role].get("HP")
                MP = role_Chart[role].get("MP")
                if ("+" or "-" or "*" or "/") in expression:
                    # if 有多个d
                    seen_letters = set()
                    result = 0
                    for char in expression:
                        if char.isalpha():
                            if char in seen_letters:
                                # 使用正则表达式分割中文、英文和数字
                                parts = re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fa5]+|[+\-*/d()]', expression)
                                # 构建新的表达式，替换掉中文和英文
                                num_expression = ''.join(parts)
                                # 替换掷骰表达式
                                num_expression = re.sub(r'(\d+)d(\d+)', lambda match: '+'.join(
                                    str(random.randint(1, int(match.group(2)))) for _ in range(int(match.group(1)))),
                                                        num_expression)
                                # 计算结果
                                result += eval(num_expression)
                            seen_letters.add(char)
                    # if(只有一个d)
                    # 使用正则表达式分割中文、英文和数字
                    parts = re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fa5]+|[+\-*/()]', expression)
                    # 构建算式
                    formula_dice = ''.join(parts[0:3])
                    # 解析表达式
                    parts_ = formula_dice.split('d')
                    num_rolls = int(parts_[0])
                    num_faces = int(parts_[1])
                    # 执行掷骰
                    rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                    result = sum(rolls)
                    formula_add = str(result) + parts[3] + parts[4]
                    result = eval(formula_add)
                elif "d" in expression:
                    # 解析表达式
                    parts = expression.split('d')
                    num_rolls = int(parts[0])
                    num_faces = int(parts[1])

                    # 执行掷骰
                    rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                    result = sum(rolls)
                    if num_rolls == 1:
                        exp = f"{expression}"
                    else:
                        exp = f"{'+'.join(map(str, rolls))}"
                else:
                    result = expression
                    exp = ""
                temp_HP_MP_check = HP_MP_check + "_"
                if HP_MP_check == "HP":
                    itm = self.ChatApp.role_values_entry[role].get("2.0", "3.0").split("/")[0].strip()
                else:
                    itm = self.ChatApp.role_values_entry[role].get("3.0", "4.0").split("/")[0].strip()
                if temp_HP_MP_check in role_Chart[role]:
                    if str(role_Chart[role].get(temp_HP_MP_check)) != itm:
                        role_Chart[role][temp_HP_MP_check] = itm
                    itm = eval(str(role_Chart[role].get(temp_HP_MP_check))+fuhao+str(result))
                else:
                    if HP_MP_check == "HP":
                        itm = eval(str(self.ChatApp.role_values_entry[role].get("2.0", "3.0").split("/")[0].strip())+fuhao+result)
                    else:
                        itm = eval(str(self.ChatApp.role_values_entry[role].get("3.0", "4.0").split("/")[0].strip())+fuhao+result)
                role_Chart[role][temp_HP_MP_check] = itm
                if HP_MP_check == "HP":
                    self.ChatApp.role_values_entry[role].delete("2.0", "3.0")
                    self.ChatApp.role_values_entry[role].insert("2.0",
                                                                f'{itm}/{HP}:HP\n')
                else:
                    self.ChatApp.role_values_entry[role].delete("3.0", "4.0")
                    self.ChatApp.role_values_entry[role].insert("3.0",
                                                                f'{itm}/{MP}:MP\n')
                des = f"{fuhao}{exp}={result}点{HP_MP_check}".replace("-=","减少").replace("+=", "恢复")
                des2 = "已" + des
                des2= des2.replace("已+", "已恢复").replace("已-", "已减少")
                self.ChatApp.chat_log.insert(tk.END,
                                             f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[{des2}]：\n{self.ChatApp.role_values_entry[role].get("2.0", "4.0").strip()}\n\n')
                self.ChatApp.chat_log.yview(tk.END)
                self.ChatApp.role_entries[role].insert(tk.END, des+"。")
                return

            if ("+" or "-" or "*" or "/") in expression:
                # if 有多个d
                seen_letters = set()
                for char in expression:
                    if char.isalpha():
                        if char in seen_letters:
                            # 使用正则表达式分割中文、英文和数字
                            parts = re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fa5]+|[+\-*/d()]', expression)
                            # 构建新的表达式，替换掉中文和英文
                            num_expression = ''.join(parts)
                            # 替换掷骰表达式
                            num_expression = re.sub(r'(\d+)d(\d+)', lambda match: '+'.join(
                                str(random.randint(1, int(match.group(2)))) for _ in range(int(match.group(1)))),
                                                    num_expression)
                            # 计算结果
                            result = eval(num_expression)
                            result, adv_comment = self.cal_advantage(result, advantage)
                            # print(result)
                            # print(num_expression)

                            # formula_add.remove(formula_add.count() - 1)
                            if info != None:
                                info_ = info
                                info = None
                                comment = self.skill_check(info_, result)
                                # 执行算式
                                return f"{num_expression}={result}/{info_}：{comment}"
                            else:
                                # 执行算式
                                return f"{num_expression}={result}"
                        seen_letters.add(char)

                # if(只有一个d)
                # 使用正则表达式分割中文、英文和数字
                parts = re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fa5]+|[+\-*/()]', expression)
                # 构建算式
                formula_dice = ''.join(parts[0:3])
                # 解析表达式
                parts_ = formula_dice.split('d')
                num_rolls = int(parts_[0])
                num_faces = int(parts_[1])
                # 执行掷骰
                rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                result = sum(rolls)
                formula_add = str(result) + parts[3] + parts[4]
                result = eval(formula_add)
                result, adv_comment = self.cal_advantage(result, advantage)
                if info != None:
                    info_ = info
                    info = None
                    comment = self.skill_check(info_, result)
                    # 执行算式
                    return f"{formula_add}={result}/{info_}：{comment}"
                else:
                    # 执行算式
                    return f"{formula_add}={result}"
            else:
                # 解析表达式
                parts = expression.split('d')
                num_rolls = int(parts[0])
                num_faces = int(parts[1])

                # 执行掷骰
                rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                result = sum(rolls)
                result, adv_comment = self.cal_advantage(result, advantage)
                if info != None:
                    info_ = info
                    # print(info_)
                    info = None
                    if result <= 5 and info_ >= Critical_Success_SKill:
                        compare = "<"
                        comment = Critical_Success
                        upgrade = self.skill_upgrade(0, skill_name, role)
                    elif result == 1:
                        compare = "<"
                        comment = Critical_Success
                        upgrade = self.skill_upgrade(0, skill_name, role)
                    elif result <= info_ // 5:
                        compare = "<"
                        comment = Extreme_Success
                        upgrade = self.skill_upgrade(info_, skill_name, role)
                    elif result <= info_ // 2:
                        compare = "<"
                        comment = Hard_Success
                        upgrade = self.skill_upgrade(info_, skill_name, role)
                    elif result <= info_:
                        compare = "<"
                        comment = Success
                        upgrade = self.skill_upgrade(info_, skill_name, role)
                    elif result >= 96 and info_ < Fumble_SKill:
                        compare = ">"
                        comment = Fumble
                        upgrade = ""
                    elif result == 100:
                        compare = ">"
                        comment = Fumble
                        upgrade = ""
                    else:
                        compare = ">"
                        comment = Failure
                        upgrade = ""
                    # 执行算式
                    if num_rolls == 1:
                        return f"{result}/{info_}：{comment}\n\n{upgrade}"
                    else:
                        return f"{'+'.join(map(str, rolls))}={result}/{info_}：{comment}\n\n{upgrade}"
                else:
                    if num_rolls == 1:
                        return f"{result}"
                    else:
                        return f"{'+'.join(map(str, rolls))}={result}"
        except Exception as e:
            return f"Error: {e}"

    def move_time_forward(self, timer):
        switch_dict = {
            "time_3s": self.add_time_3sec,
            "time_1min": self.add_time_1min,
            "time_5min": self.add_time_5min,
            "time_10min": self.add_time_10min,
            "time_30min": self.add_time_30min,
            "time_1h": self.add_time_1h,
            "time_3h": self.add_time_3h,
            "time_12h": self.add_time_12h,
            "time_1d": self.add_time_1d,
            "time_1w": self.add_time_1w,
        }
        # 使用 get 方法获取对应时间列表名的函数，如果不存在则返回一个默认函数
        time_function = switch_dict.get(timer, lambda: print("Invalid time list name"))
        # 执行函数
        time_function()

    def add_time_3sec(self):
        # 添加处理 time_3s 的代码
        global _secondsTime
        if _secondsTime >= 60:
            self.add_time_1min()
            _secondsTime -= 60
        else:
            _secondsTime += random.randint(1, 3)
            print(f"秒表：{_secondsTime}秒")
        # global time
        # time_format = "%H:%M"
        # base_time = datetime.strptime(time, time_format)
        # time = base_time + timedelta(seconds=3)
        # 将新时间格式化为字符串
        # time = time.strftime(time_format)
        # reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        # self.ChatApp.time_log.delete("1.0", tk.END)
        # self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        # print("Adding 1 minute")
        # if time == "23:59:57":
        # print("新的一天")
        # self.ChatApp.chat_log.insert(tk.END,
        # f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
        # 滚动到最底部
        # self.ChatApp.chat_log.yview(tk.END)

    def add_time_1min(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(minutes=1)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 1 minute")
        if int(datetime.strftime(base_time, "%H")) == 23 and int(datetime.strftime(base_time, "%M")) >= 59:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_5min(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(minutes=5)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 5 minutes")
        if int(datetime.strftime(base_time, "%H")) == 23 and int(datetime.strftime(base_time, "%M")) >= 55:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_10min(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(minutes=10)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 10 minutes")
        if int(datetime.strftime(base_time, "%H")) == 23 and int(datetime.strftime(base_time, "%M")) >= 50:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_30min(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(minutes=30)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 30 minutes")
        if int(datetime.strftime(base_time, "%H")) == 23 and int(datetime.strftime(base_time, "%M")) >= 30:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_1h(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(hours=1)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 60 minutes")
        if int(datetime.strftime(base_time, "%H")) >= 23:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_3h(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(hours=3)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 180 minutes")
        if int(datetime.strftime(base_time, "%H")) >= 21:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_12h(self):
        # 添加处理 time_1min 的代码
        global time
        time_format = "%H:%M"
        base_time = datetime.strptime(time, time_format)
        time = base_time + timedelta(hours=12)
        # 将新时间格式化为字符串
        time = time.strftime(time_format)
        reply = "【地点】" + str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【地点】")[1])
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, "【时间】" + time.upper() + reply)
        print("Adding 720 minutes")
        if int(datetime.strftime(base_time, "%H")) >= 12:
            self.add_time_1d()
            print("新的一天")
            self.ChatApp.chat_log.insert(tk.END,
                                         f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n新的一天到来了...现在是{date}\n\n')
            # 滚动到最底部
            self.ChatApp.chat_log.yview(tk.END)

    def add_time_1d(self):
        # 添加处理 time_1min 的代码
        global date
        time_format = "%Y/%m/%d %A"
        base_time = datetime.strptime(date, time_format)
        date = base_time + timedelta(days=1)
        # 将新时间格式化为字符串
        date = date.strftime(time_format)
        reply = str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【日期】")[0]) + "【日期】"
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, reply + date)
        print("Adding 1 day")

    def add_time_1w(self):
        # 添加处理 time_1min 的代码
        global date
        time_format = "%Y/%m/%d %A"
        base_time = datetime.strptime(date, time_format)
        date = base_time + timedelta(days=7)
        # 将新时间格式化为字符串
        date = date.strftime(time_format)
        reply = str(self.ChatApp.time_log.get("1.0", tk.END).strip().split("【日期】")[0]) + "【日期】"
        self.ChatApp.time_log.delete("1.0", tk.END)
        self.ChatApp.time_log.insert(tk.END, reply + date)
        print("Adding 7 days")


class DraggableItem:
    def __init__(self, canvas, x, y, width, height, fill=None, image=None, outline=None, label=None, label2=None,
                 type=None, frame=None):
        global frame_Map
        global frames_Map
        global current_frame_map
        rgba_color = "#000000"  # 黑色
        alpha = 128  # 50% 的透明度
        # self.rgba_color_with_alpha = rgba_color + "{:02x}".format(alpha)   # 添加透明度
        self.rgba_color_with_alpha = fill
        self.canvas = canvas
        self.width = width
        self.height = height
        self.anchor = None
        self.resize_anchor = None
        self.label = label
        self.label2 = label2
        self.itemType = type
        self.image_references = []
        self.frame = frame

        if image:
            self.item = canvas.create_image(x, y, image=image, tags="draggable")
            if self.itemType == "image_animate" or self.itemType == "image_temp_animate":
                # 播放 GIF 动画
                # print(current_frame_map)
                self.animate_on_map(0, self.canvas, self.item,
                                    frames_map[self.frame])
            if label is not None:
                label_below_image = tk.Label(self.canvas, text=label)
                # self.label_below_image.pack()
                # self.label_below_image.place(x=x - 50, y=y + 60)  # Adjust the position as needed
                self.label_below_image_canvas = self.canvas.create_window(x, y - 50, window=label_below_image,
                                                                          anchor=tk.NW)

                # label_below_image2 = tk.Label(self.canvas, text=label2, relief=tk.SUNKEN)
                # self.label_below_image.pack()
                # self.label_below_image.place(x=x - 50, y=y + 60)  # Adjust the position as needed
                # self.label_below_image_canvas2 = self.canvas.create_window(x - 35, y+45, window=label_below_image2,
                # anchor=tk.NW)
                self.label_below_image_canvas2 = canvas.create_text(x, y + 70, text=label2, font=("Arial", 10),
                                                                    fill="black",
                                                                    tags="draggable")
                self.label_below_image_canvas2_edit = canvas.create_text(x - 45, y + 70, text="❤", font=("Arial", 10),
                                                                         fill="black",
                                                                         tags="draggable")
                # if label2 is not None:
                # self.label_below_image_canvas = canvas.create_text(x + 50, y + 50, text=label2, font=("Arial", 5),
                # fill="black",
                # tags="draggable")
            else:
                self.label_below_image_canvas = None
                self.label_below_image_canvas2 = None
                self.label_below_image_canvas2_edit = None
        else:
            self.label_below_image_canvas2_edit = None

            if type == "rectangle":
                self.item = canvas.create_rectangle(x, y, x + width, y + height, fill=self.rgba_color_with_alpha,
                                                    outline=outline,
                                                    tags="draggable")
            elif type == "circle":
                self.item = canvas.create_oval(x, y, x + width, y + width, fill=self.rgba_color_with_alpha,
                                               outline=outline,
                                               tags="draggable")
            elif type == "oval":
                self.item = canvas.create_oval(x, y, x + width, y + height, fill=self.rgba_color_with_alpha,
                                               outline=outline,
                                               tags="draggable")
            elif type == "polygon3":
                x1 = x - width / 2
                y1 = y + height
                x2 = x + width / 2
                y2 = y + height
                points = [x, y, x1, y1, x2, y2]
                self.item = canvas.create_polygon(points, fill=self.rgba_color_with_alpha, outline=outline,
                                                  tags="draggable")
            elif type == "polygon5":
                points = []
                for i in range(5):
                    angle = math.radians(90 + i * 360 / 5)
                    points.append(x + width * math.cos(angle))
                    points.append(y + width * math.sin(angle))
                self.item = canvas.create_polygon(points, fill=self.rgba_color_with_alpha, outline=outline,
                                                  tags="draggable")
            elif type == "polygon6":
                points = []
                for i in range(6):
                    angle = math.radians(30 + i * 360 / 6)
                    points.append(x + width * math.cos(angle))
                    points.append(y + width * math.sin(angle))
                self.item = canvas.create_polygon(points, fill=self.rgba_color_with_alpha, outline=outline,
                                                  tags="draggable")
            elif type == "polygon8":
                points = []
                for i in range(8):
                    angle = math.radians(45 + i * 360 / 8)
                    points.append(x + width * math.cos(angle))
                    points.append(y + width * math.sin(angle))
                self.item = canvas.create_polygon(points, fill=self.rgba_color_with_alpha, outline=outline,
                                                  tags="draggable")
            elif type == "polygonStar":
                points = []
                for i in range(5):
                    angle = math.radians(90 + i * 360 / 5)
                    if i % 2 == 0:
                        points.append(x + width * math.cos(angle))
                        points.append(y + width * math.sin(angle))
                    else:
                        points.append(x + width / 2 * math.cos(angle))
                        points.append(y + width / 2 * math.sin(angle))
                self.item = canvas.create_polygon(points, fill=self.rgba_color_with_alpha, outline=outline,
                                                  tags="draggable")

            elif type == "line":
                self.item = canvas.create_line(x, y, x + width, y + height, fill="black",
                                               tags="draggable")

            elif type == "text":
                self.item = canvas.create_text(x + 50, y + 50, text=label, font=("Arial", 12), fill="black",
                                               tags="draggable")

            self.itemType = type
            if label is not None:
                # label_below_image = tk.Label(self.canvas, text=label)
                # self.label_below_image.pack()
                # self.label_below_image.place(x=x - 50, y=y + 60)  # Adjust the position as needed
                # self.label_below_image_canvas = self.canvas.create_window(x, y, window=label_below_image, anchor=tk.NW)
                label_below_image2 = tk.Label(self.canvas, text=label2)
                if label2 is not None:
                    self.itemType = "text_PC"
                    self.label_below_image_canvas2 = self.canvas.create_window(x + 50, y - 10,
                                                                               window=label_below_image2,
                                                                               anchor=tk.NW)
                else:
                    self.label_below_image_canvas2 = None
                if type == "text":
                    self.label_below_image_canvas = canvas.create_text(x + 30, y + 35, text="❤", font=("Arial", 10),
                                                                       fill="black",
                                                                       tags="draggable")
                else:
                    self.label_below_image_canvas = canvas.create_text(x + 10, y - 5, text=label, font=("Arial", 10),
                                                                       fill="black",
                                                                       tags="draggable")

            else:
                self.label_below_image_canvas = None
                self.label_below_image_canvas2 = None

        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.item, "<ButtonPress-3>", self.on_right_press)

        if self.label_below_image_canvas:
            self.canvas.tag_bind(self.label_below_image_canvas, "<ButtonPress-1>", self.on_tag_press)
            self.canvas.tag_bind(self.label_below_image_canvas, "<ButtonPress-2>", self.on_resize)
            self.canvas.tag_bind(self.label_below_image_canvas, "<B2-Motion>", self.on_right_drag)
        if self.label_below_image_canvas2_edit != None:
            self.canvas.tag_bind(self.label_below_image_canvas2_edit, "<ButtonPress-1>", self.on_tag_press)

    def on_tag_press(self, event):
        # 弹出输入窗口并获取用户输入的文本
        # print("text")
        if self.itemType == "image" or self.itemType == "image_temp" or self.itemType == "image_temp_animate" or self.itemType == "image_animate":
            intiText = self.label2
        else:
            intiText = "标签"
        new_text = simpledialog.askstring("Input", "Enter new text:", initialvalue=intiText)
        if new_text:
            if self.itemType == "text":
                self.canvas.itemconfig(self.item, text=new_text)
            elif self.itemType == "image" or self.itemType == "image_temp" or self.itemType == "image_temp_animate" or self.itemType == "image_animate":
                self.canvas.itemconfig(self.label_below_image_canvas2, text=new_text)
            else:
                self.canvas.itemconfig(self.label_below_image_canvas, text=new_text)

    def on_resize(self, event):
        self.resize_anchor = event.x - 100, event.y - 50
        label_coords = self.canvas.coords(self.label_below_image_canvas)
        # self.resize_anchor = (self.resize_anchor[0] + label_coords[0], self.resize_anchor[1] + label_coords[1])
        pass

    def on_right_drag(self, event):
        if self.resize_anchor:
            dx = event.x - self.resize_anchor[0]
            dy = event.y - self.resize_anchor[1]
            self.width += dx
            self.height += dy
            self.canvas.coords(self.item, self.canvas.coords(self.item)[0],
                               self.canvas.coords(self.item)[1], self.width, self.height)
            self.resize_anchor = event.x, event.y

    def apng_to_gif(self, apng_file, gif_file):
        # 使用 apng2gif 工具将 APNG 转换成 GIF
        subprocess.run(["apng2gif", apng_file, gif_file])
        return gif_file

    def animate_on_map(self, frame_index, canvas, current_frame, frames):
        # print(str(frame_index)+"/" + str(len(frames)))
        # 更新当前帧
        canvas.itemconfig(current_frame, image=frames[frame_index])
        # canvas.create_image(20, 20, anchor=tk.NW, image=frames[frame_index])
        # 循环播放下一帧
        frame_index = (frame_index + 1) % len(frames)
        self.after_id = canvas.after(50, self.animate_on_map, frame_index, canvas, current_frame, frames)

    def update_time(self, canvas, label):
        # print(str(frame_index)+"/" + str(len(frames)))
        # 更新当前帧
        # canvas.itemconfig(label, image=frames[frame_index])
        canvas.after()

    def on_right_press(self, event):
        global frame_Map
        global frames_Map
        global current_frame_map
        global Is_fill
        global Is_square
        self.anchor = event.x, event.y
        if (("polygon" in self.itemType) and self.itemType != "polygon3"):
            if Is_fill:
                draggable_rectangle = DraggableItem(self.canvas, event.x + 2, event.y + 2, random.randint(20, 150),
                                                    random.randint(20, 150), fill='white',
                                                    outline='black', label='标签', type=self.itemType)
                Is_fill = False
            else:
                if Is_square:
                    draggable_rectangle = DraggableItem(self.canvas, event.x + 2, event.y + 2, 100, 80, fill='',
                                                        outline='black', label='标签', type=self.itemType)
                    Is_square = False
                else:
                    draggable_rectangle = DraggableItem(self.canvas, event.x + 2, event.y + 2, random.randint(20, 150),
                                                        random.randint(20, 150), fill='',
                                                        outline='black', label='标签', type=self.itemType)
                    Is_square = True
                Is_fill = True
        elif self.itemType == "image_temp" or self.itemType == "image_temp_animate":
            self.canvas.delete(self.item)
            self.canvas.delete(self.label_below_image_canvas2)
            self.canvas.delete(self.label_below_image_canvas)
            self.canvas.delete(self.label_below_image_canvas2_edit)
        elif self.itemType == "image" or self.itemType == "text_PC" or self.itemType == "image_temp_animate" or self.itemType == "image_animate":
            # 创建武器选择变量
            avatar_path = filedialog.askopenfilename(title="为【" + self.label + "】选择战斗图片",
                                                     filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.apng;*.gif")],
                                                     initialdir="Images/BattleImages")
            if avatar_path:
                _, extension = os.path.splitext(avatar_path)
                filename, dot = os.path.splitext(os.path.basename(avatar_path))
                if os.path.exists(
                        'Images/BattleImages/' + filename + extension):
                    pass
                else:
                    shutil.copyfile(avatar_path,
                                    'Images/BattleImages/' + filename + extension)
                if extension == ".apng" or extension == ".APNG":
                    avatar_path = self.apng_to_gif(avatar_path, _ + ".gif")
                if extension == ".gif" or extension == ".GIF":
                    image = Image.open(avatar_path)
                    width, height = image.size
                    frames_map[frame_Map] = [
                        ImageTk.PhotoImage(frame.resize((int(width * 0.25), int(height * 0.25)), Image.LANCZOS))
                        for frame
                        in ImageSequence.Iterator(image)]
                    # 显示 GIF 图片的第一帧
                    current_frame_map[frame_Map] = DraggableItem(self.canvas, event.x, event.y, 10, 10,
                                                                 image=frames_map[frame_Map][0],
                                                                 label=self.label,
                                                                 label2=self.label2, type="image_temp_animate",
                                                                 frame=frame_Map)
                    frame_Map += 1

                else:
                    with open(avatar_path, "rb") as f:
                        image = Image.open(f)
                        width, height = image.size
                        image = image.resize((int(width * 0.25), int(height * 0.25)), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        # circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='', outline="black", width=2)
                        # self.canvas.create_image(x, y, image=photo)
                        # 保持对图像的引用，防止被垃圾回收
                        # self.canvas.image = photo
                        # Keep references to all images
                        self.image_references.append(photo)
                        # Create draggable image
                    image = tk.PhotoImage(file=avatar_path)
                    draggable_image = DraggableItem(self.canvas, event.x, event.y, 10, 10, image=photo,
                                                    label=self.label,
                                                    label2=self.label2, type="image_temp")

            # self.weapon_var = tk.StringVar(root)
            # self.weapon_var.set("请选择战斗图片")

            # 创建下拉列表
            # self.weapon_menu = tk.OptionMenu(root, self.weapon_var, "剑", "盾", "长矛")
            # self.weapon_menu.pack()

            # 创建按钮，用于确认选择
            # self.select_weapon_button = tk.Button(root, text="选择", command=self.select_weapon)
            # self.select_weapon_button.pack()

        else:
            if Is_fill:
                draggable_rectangle = DraggableItem(self.canvas, event.x + 2, event.y + 2, random.randint(20, 150), random.randint(20, 150), fill='white',
                                                    outline='black', label='标签', type=self.itemType)
                Is_fill = False
            else:
                draggable_rectangle = DraggableItem(self.canvas, event.x + 2, event.y + 2, random.randint(20, 150), random.randint(20, 150), fill='',
                                                    outline='black', label='标签', type=self.itemType)
                Is_fill = True

    def select_weapon(self, event):
        weapon = self.weapon_var.get()

        # 根据选择的武器加载相应的图片
        if weapon:
            if weapon == "剑":
                # 载入剑的图片
                image = tk.PhotoImage(file="sword.gif")
            elif weapon == "盾":
                # 载入盾的图片
                image = tk.PhotoImage(file="shield.gif")
            elif weapon == "长矛":
                # 载入长矛的图片
                image = tk.PhotoImage(file="spear.gif")
            else:
                # 默认情况下，载入默认图片
                image = tk.PhotoImage(file="default.gif")

            # 显示图片在 Canvas 上
            draggable_image = DraggableItem(self.canvas, event.x, event.y, 10, 10, image=image, label=self.label,
                                            label2=self.label2)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.anchor = event.x, event.y
        self.resize_anchor = event.x - 100, event.y - 50
        # self.canvas.tag_lift(self.item)
        # if self.label_below_image_canvas is not None:
        # self.canvas.tag_lift(self.item)

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.canvas.move(self.item, delta_x, delta_y)
        if self.label_below_image_canvas is not None:
            self.canvas.move(self.label_below_image_canvas, delta_x, delta_y)
            if self.label_below_image_canvas2 != None:
                self.canvas.move(self.label_below_image_canvas2, delta_x, delta_y)
                if self.label_below_image_canvas2_edit != None:
                    self.canvas.move(self.label_below_image_canvas2_edit, delta_x, delta_y)
        self.start_x = event.x
        self.start_y = event.y
        # dx = event.x - self.anchor[0]
        # dy = event.y - self.anchor[1]
        # self.canvas.move(self.item, dx, dy)
        self.anchor = event.x, event.y
        self.resize_anchor = event.x, event.y


class CanvasSaver:
    def __init__(self, canvas):
        self.canvas = canvas

    def save_canvas_state(self, filename):
        canvas_state = self.get_canvas_state()
        with open(filename, 'w') as f:
            json.dump(canvas_state, f)
        # self.canvas.postscript(file=filename, colormode="color")

    def load_canvas_state(self, filename):
        with open(filename, 'r') as f:
            canvas_state = json.load(f)
        self.set_canvas_state(canvas_state)

    def get_canvas_state(self):
        canvas_state = {
            'items': []
        }
        for item in self.canvas.find_all():
            item_type = self.canvas.type(item)
            item_coords = self.canvas.coords(item)

            item_tags = self.canvas.gettags(item)
            canvas_state['items'].append({
                'type': item_type,
                'coords': item_coords,
                'tags': item_tags,
            })
            if item_type in ["rectangle", "oval"]:
                fill = self.canvas.itemcget(item, "fill")
                outline = self.canvas.itemcget(item, "outline")
                # text = self.canvas.itemcget(item, "text")
                canvas_state_detail = canvas_state.get("items", {})
                canvas_state_detail["fill"] = fill
                canvas_state_detail["outline"] = outline
                # canvas_state_detail["text"] = text
        return canvas_state

    def set_canvas_state(self, canvas_state):
        self.canvas.delete('all')
        for item_data in canvas_state['items']:
            item_type = item_data['type']
            item_coords = item_data['coords']
            item_tags = item_data['tags']
            if item_type == 'image':
                # Add your handling for image items
                pass
            else:
                self.canvas.create_polygon(item_coords, tags=item_tags)


class LoadNPCDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title)
        # self.NPC_information = NPC_information
        # self.ChatApp = None
        # self.ChatApp = chat_app_instance
        # print(NPC_information)

    def body(self, master):
        role_Chart_at_name_ = load_Chart_at_name().copy()
        role_Chart_ = load_Chart().copy()
        self.npcNames = []
        self.slots = []
        for role, chart in role_Chart_at_name_.items():
            if "PL " not in role:
                self.npcNames.append(role)
        for role, chart in role_Chart_.items():
            self.slots.append(role)

        tk.Label(master, text="选择NPC：").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="使用名：").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="装载到：").grid(row=2, column=0, sticky="e")
        self.trust_var = tk.StringVar()
        self.importance_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.source_entry = tk.Entry(master, textvariable=self.source_var)

        first_roll_values = self.npcNames
        second_roll_values = self.slots
        self.first_roll_entry = ttk.Combobox(master, textvariable=self.trust_var, values=first_roll_values)
        self.second_roll_entry = ttk.Combobox(master, textvariable=self.importance_var, values=second_roll_values)

        self.first_roll_entry.grid(row=0, column=1)
        self.second_roll_entry.grid(row=2, column=1)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5)

        return self.first_roll_entry

    def apply(self):
        first_roll = self.trust_var.get()
        second_roll = self.importance_var.get()
        source = self.source_var.get()
        self.result = {}
        self.result[first_roll] = source
        if second_roll == "":
            self.result["slot"] = "KP"
        else:
            self.result["slot"] = second_roll
        # print(self.result)
        return self.result


class MemoryInfoDialog(simpledialog.Dialog):
    def __init__(self, parent, title, information_sources, role):
        # self.ChatApp = chat_app_instance
        self.information_sources = information_sources
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="信息来源：").grid(row=0, sticky="e")
        tk.Label(master, text="信息内容：").grid(row=1, sticky="e")
        tk.Label(master, text="信任度：").grid(row=2, sticky="e")
        tk.Label(master, text="重要度：").grid(row=3, sticky="e")

        self.source_var = tk.StringVar()
        self.content_var = tk.StringVar()
        self.trust_var = tk.StringVar()
        self.importance_var = tk.StringVar()

        self.source_entry = tk.Entry(master, textvariable=self.source_var)
        self.content_entry = tk.Entry(master, textvariable=self.content_var)

        trust_values = ["完全信任（0）", "基本信任（-1）", "有疑虑（-2）", "不信任（-3）", "质疑矛盾（-4）", "疑神疑鬼（-5）", "过度解读（+4）"]
        self.trust_combobox = ttk.Combobox(master, textvariable=self.trust_var, values=trust_values)

        importance_values = ["关键信息（5）", "相关信息（4）", "边缘信息（3）", "模糊信息（2）", "无用信息（1）"]
        self.importance_combobox = ttk.Combobox(master, textvariable=self.importance_var, values=importance_values)

        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        self.content_entry.grid(row=1, column=1, padx=5, pady=5)
        self.trust_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.importance_combobox.grid(row=3, column=1, padx=5, pady=5)

        return self.source_entry

    def apply(self):
        self.result = {}
        source = self.source_var.get()
        content = self.content_var.get()
        trust = int(self.trust_combobox.get().split("（")[1][:-1])  # 提取括号中的数字
        importance = int(self.importance_combobox.get().split("（")[1][:-1])  # 提取括号中的数字

        # 计算记忆指数
        memory_index = trust + importance

        # 给出评分
        if memory_index <= -1:
            rating = "遗忘"
        elif memory_index <= 0:
            rating = "无用信息"
        elif memory_index == 2:
            rating = "模糊信息"
        elif memory_index == 3:
            rating = "边缘信息"
        elif memory_index == 4:
            rating = "相关信息"
        else:
            rating = "关键信息"

        self.result["信息来源"] = source
        self.result["信息内容"] = content
        self.result["记忆指数"] = memory_index
        self.result["评分"] = rating
        print(f"信息来源: {source}, 信息内容: {content}, 信任度: {trust}, 重要度: {importance}, 记忆指数: {memory_index}, 评分: {rating}")
        return self.result


class DiceRollDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        super().__init__(parent, title)
        self.ChatApp = None
        # self.ChatApp = chat_app_instance

    def body(self, master):
        tk.Label(master, text="第一次掷骰结果：").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="第二次掷骰结果：").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="线索名（当前无效）：").grid(row=2, column=0, sticky="e")
        self.trust_var = tk.StringVar()
        self.importance_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.source_entry = tk.Entry(master, textvariable=self.source_var)

        first_roll_values = ["大失败（-20%）", "失败（10%）", "成功（100%）"]
        self.first_roll_entry = ttk.Combobox(master, textvariable=self.trust_var, values=first_roll_values)

        second_roll_values = ["放弃（0%）", "大失败（-80%）", "失败（-20%）", "成功（+20%）", "困难成功（+40%）", "极难成功（+60%）", "大成功（+100%）"]
        self.second_roll_entry = ttk.Combobox(master, textvariable=self.importance_var, values=second_roll_values)

        self.first_roll_entry.grid(row=0, column=1)
        self.second_roll_entry.grid(row=1, column=1)
        self.source_entry.grid(row=2, column=1, padx=5, pady=5)

        return self.first_roll_entry

    def apply(self):
        first_roll = self.trust_var.get()
        second_roll = self.importance_var.get()
        source = self.source_var.get()

        # 根据规则计算最后的处理方案
        result_percentage = calculate_result_percentage(first_roll, second_roll)
        final_result = calculate_final_result(result_percentage)

        # 显示最终结果
        result_text = f"结果百分比：{result_percentage}\n处理方案：{final_result}\n\n===\n根据原模组信息总结至多五个关键词，按重要度排序，发放时按重要度低到高发放。\n" \
                      f"注意给出的关键词要是可探索、结合模组剧情的关键地点、物品、事件、人物等（一般重要度较低），或者是传达一种态度和推理思路（一般重要度最高）。\n" \
                      f"如果数量不够，则不提供任何关键词（比如只有一个关键地点，则在80%以上给出）如果信息过于简短，可以提前给出全部段落，负值同理；\n如果段落总结不出关键词，可以将关键词替换为句子。\n" \
                      f"注意虚假信息和无效信息是不一样的。无效信息在0%给出，虚假信息需要起到误导PC的作用（比如新增了一个地点，新增了一个人物，关键信息错误等） "
        messagebox.showinfo("处理方案", result_text)
        # self.ChatApp.add_inference2self(source, source + "的搜查进度", result_percentage, "DiceBot")

        print(result_text)


def calculate_result_percentage(first_roll, second_roll):
    # 根据规则计算可能的结果百分比
    # 请根据实际规则进行修改
    result_percentage = 0
    match = re.search(r'（(-?\+?\d+)%）', first_roll)
    if match:
        print(match.group(1))
        first_roll = int(match.group(1))
    match2 = re.search(r'（(-?\+?\d+)%）', second_roll)
    if match2:
        second_roll = int(match2.group(1))
    result_percentage = int(first_roll) + int(second_roll)
    return result_percentage


def calculate_final_result(result_percentage):
    # 根据可能的结果百分比计算最终处理方案
    # 请根据实际规则进行修改
    if result_percentage == -100:
        final_result = "虚假全部/5假词"
    elif result_percentage == -70:
        final_result = "虚假全部，留1真词"
    elif result_percentage == -40:
        final_result = "2真词1假词"
    elif result_percentage == -20:
        final_result = "2假词/1真2假/不提供"
    elif result_percentage == -10:
        final_result = "1假词/1真1假/不提供"
    elif result_percentage == 0:
        final_result = "不提供"
    elif result_percentage == 10:
        final_result = "1关键词"
    elif result_percentage == 20:
        final_result = "2关键词"
    elif result_percentage == 30:
        final_result = "3关键词"
    elif result_percentage == 40:
        final_result = "4关键词"
    elif result_percentage == 50:
        final_result = "5关键词"
    elif result_percentage == 70:
        final_result = "完整信息隐藏2关键词"
    elif result_percentage == 80:
        final_result = "完整信息隐藏1关键词"
    else:
        final_result = "完整信息"
    return final_result


# 从文件中读取 JSON 数据

def babel(self):
    global babel_on
    try:
        # 尝试加载自定义角色数值信息
        with open('GameSaves/巴别塔.json', 'r', encoding='utf-8') as file:
            self.babel_data = json.load(file)
        babel_on = True
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        self.babel_data = {}
        babel_on = False
        print("未启用“巴别塔”模块, 配置好角色后，在GameSaves下新建以“{}”为内容的 巴别塔.json 以初始化")

    # 如果数据非空，则启用“巴别塔”模块
    if self.babel_data:
        babel_on = True
        print("启用“巴别塔”模块")
    elif babel_on == False:
        print("未启用“巴别塔”模块, 配置好角色后，在GameSaves下新建巴别塔.json以初始化")
    else:
        babel_on = False
        print("准备启用“巴别塔”模块，正在初始化，请核对 GameSaves/巴别塔.json，修改角色“母语”（{'母语':60}）为母语（{'英语':60, '母语':'英语'}），确认国籍并重启")
        self.babel_data = {}
        for role, info in role_Chart.items():
            data_ = {}
            home = -1
            for skill, percent in info.items():
                if "语" in skill:
                    if percent == "EDU":
                        data_[skill] = 0
                        data_["国籍"] = "地球"
                    else:
                        data_[skill] = percent
                        if home < int(percent):
                            data_["国籍"] = skill.replace("语", "") + "国"
            self.babel_data[self.role_entries_name[role]] = data_
        with open('GameSaves/巴别塔.json', 'w', encoding='utf-8') as file:
            json.dump(self.babel_data, file, ensure_ascii=False)


def fire_babel(self, role):
    # 在 data 中获取角色信息
    print(f"===")
    global babel_on
    role = self.role_entries_name[role]
    if babel_on:
        lan_list = {}
        dic = self.babel_data[role]
        lan_main = str(dic["母语"]).replace("0", "英语")
        for language, skill in self.babel_data[role].items():
            if language != "母语" and language != "国籍":
                if skill >= 10:
                    lan_list[language] = skill
        for role2 in self.roles:
            role2 = self.role_entries_name[role2]
            if role2 != role:
                dic2 = self.babel_data[role2]
                # self.list_skills = []
                if lan_main in dic2:
                    # self.list_skills.append(lan_main)
                    if (dic2[lan_main] + dic[lan_main] >= 60) and dic2[lan_main] >= 10:
                        print(f"[巴别塔] 【{role2}】 和 【{role}】 用 [{lan_main}] 聊得很开心！")
                    else:
                        self.best_lan = "None"
                        self.best_lan_skill = 0
                        for language, skill in self.babel_data[role2].items():
                            if language != "母语" and language != "国籍":
                                if language in lan_list:
                                    if skill + lan_list[language] >= 80 and skill >= 20:
                                        print(f"[巴别塔] 【{role2}】 和 【{role}】 用 [{language}] 聊得很开心！")
                                        self.best_lan = "GOOD"
                                        break
                                    elif skill >= 5:
                                        if self.best_lan_skill < skill:
                                            self.best_lan = language
                                            self.best_lan_skill = skill
                        if self.best_lan != "None":
                            if self.best_lan == "GOOD":
                                pass
                            elif self.best_lan_skill <= 5:
                                print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么，但知道那可能是 [{self.best_lan}]，可以去请教一下别人！")

                            elif self.best_lan_skill + lan_list[self.best_lan] >= 60 and self.best_lan_skill >= 50:
                                print(
                                    f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [母语({dic2[dic2['母语']]}): {dic2['母语']}] ！")

                            elif self.best_lan_skill + lan_list[self.best_lan] >= 40 and self.best_lan_skill >= 30:
                                print(
                                    f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [困难母语({int(dic2[dic2['母语']] / 2)}): {dic2['母语']}] ！")

                            elif self.best_lan_skill + lan_list[self.best_lan] >= 10 and self.best_lan_skill > 5:
                                print(
                                    f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [极难母语({int(dic2[dic2['母语']] / 5)}): {dic2['母语']}] ！")
                            else:
                                print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么！")
                            self.best_lan = "None"
                            self.best_lan_skill = 0
                        else:
                            print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么！")
                else:
                    self.best_lan = "None"
                    self.best_lan_skill = 0
                    for language, skill in self.babel_data[role2].items():
                        if language != "母语" and language != "国籍":
                            if language in lan_list:
                                if skill + lan_list[language] >= 80 and skill >= 20:
                                    print(f"[巴别塔] 【{role2}】 和 【{role}】 用 [{language}] 聊得很开心！")
                                    self.best_lan = "GOOD"
                                    break
                                elif skill >= 5:
                                    if self.best_lan_skill < skill:
                                        self.best_lan = language
                                        self.best_lan_skill = skill
                    if self.best_lan != "None":
                        if self.best_lan == "GOOD":
                            pass
                        elif self.best_lan_skill <= 5:
                            print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么，但知道那可能是 [{self.best_lan}]，可以去请教一下别人！")

                        elif self.best_lan_skill + lan_list[self.best_lan] >= 60 and self.best_lan_skill >= 50:
                            print(
                                f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [母语({dic2[dic2['母语']]}): {dic2['母语']}] ！")

                        elif self.best_lan_skill + lan_list[self.best_lan] >= 40 and self.best_lan_skill >= 30:
                            print(
                                f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [困难母语({int(dic2[dic2['母语']] / 2)}): {dic2['母语']}] ！")

                        elif self.best_lan_skill + lan_list[self.best_lan] >= 10 and self.best_lan_skill > 5:
                            print(
                                f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [极难母语({int(dic2[dic2['母语']] / 5)}): {dic2['母语']}] ！")
                        else:
                            print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么！")
                        self.best_lan = "None"
                        self.best_lan_skill = 0
                    else:
                        print(f"[巴别塔] 啊哦！【{role2}】 好像怎么都听不懂 【{role}】 在说什么！")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 捕获窗口关闭事件
    # root.protocol("WM_DELETE_WINDOW", self.new_window.on_closing)  # 捕获窗口关闭事件
    # root.wm_attributes('-transparentcolor', 'white')
    root.mainloop()
