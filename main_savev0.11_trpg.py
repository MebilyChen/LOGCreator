import math
import os
import re
from random import random
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, simpledialog, messagebox
from datetime import datetime, timedelta
import configparser

from PIL import Image, ImageTk
import json


# import logging

# logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为 DEBUG

def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 创建成功")
    except FileExistsError:
        print(f"文件夹 '{folder_path}' 已经存在")

babel_on = False

# 例子：创建名为 'my_folder' 的文件夹在当前工作目录下
create_folder('AppSettings')
create_folder('Bots')
create_folder('GameSaves')

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


role_Chart = load_Chart()
role_Chart_at_name = load_Chart_at_name()
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
        self.root.title("自嗨团 v0.82" + encouragement)

        # 设置图标
        self.root.iconbitmap("AppSettings/icon.ico")

        # 其他窗口内容
        # self.label = tk.Label(root, text="Hello, Tkinter!")

        # 绑定回车键和Alt+回车键
        root.bind("<Return>", lambda event: self.send_message(self.current_role.get()))
        root.bind("<Alt-Return>", lambda event: self.insert_newline())
        root.bind("<Control-Return>", self.newline_on_ctrl_enter)

        self.babel_data = {}

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

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")
        # 在 Text 组件中插入初始文本
        initial_text = "Updates：\n更新了TRPG掷骰模块:联合骰、SC、优劣势、补正骰、对抗骰、武器伤害Built-in\n退出时保存当前设置（头像、名字、PL数量）\n更新了自定义数值/笔记栏\n.st存入Json数据库\n技能成长自动判定\n导出技能st\n骰子性格（结果播报语句。但因为不会出现在log里，所以基本也没啥影响...）\n时间模块\n#Armor\n推理信息库\n巴别塔（看控制台）\n" \
                       "\nTodo:" \
                       "\n--计算" \
                       "\n自动加减基础数值（MP、HP）（不这么做是因为要有理由Focus再UnFocus笔记栏来保存..）" \
                       "\n--features" \
                       "\n继续优化推理信息库-计算器直接显示在共用库栏位（新建一个Frame）" \
                       "\n输出染色HTML(坑)" \
                       "\n骰子性格：针对每个技能单独comment(坑)" \
                       "\n继续优化简易小地图" \
                       "\n--bugs\n复杂掷骰算式（多个不同面骰子+常数）优化\n补正骰优化\n对抗骰优化\n武器伤害Built-in优化\n自动加减基础数值（SAN）优化\nArmor显示优化\n\n" \
                       "Tips:\n在角色笔记栏中修改不会影响到角色卡数值，修改HP、MP时均修改的是上限\n使用 .st#斗殴@1D3+5 来载入武器伤害公式\n\n" \
                       "===以上可删除===\n\n"
        self.chat_log.insert(tk.END, initial_text)

        # 创建按钮，点击按钮时调用 open_new_window 函数
        new_window_button = tk.Button(root, text="推理信息", command=self.open_new_window)
        new_window_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

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
            role_Chart[role] = role_Chart_detail_demo

        frame = tk.LabelFrame(self.root, text=role, relief=tk.GROOVE)
        frame.grid(row=row, column=col + 2, padx=10, pady=10, sticky="nsew")
        self.role_entries_frame[role] = frame
        # 初始化头像路径
        self.role_avatar_paths = {}
        if load_settings_avatar() != "":
            self.role_avatar_paths = load_settings_avatar()  # 从文件加载设置
        # 头像点击事件
        # self.avatar_click_event = None

        # 加载并显示头像
        self.load_and_display_avatar(role, frame)

        # 每个角色的消息框
        entry = tk.Text(frame, wrap=tk.WORD, width=30, height=3)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.role_entries[role] = entry
        if role == "DiceBot":
            # 在 Text 组件中插入初始文本
            initial_text = "复制Bot消息至此并发送，或：\n\n【掷骰】点击每个角色的掷骰按钮进行掷骰，公式栏填写公式或技能，留空默认1d100" \
                           "\n\n【优劣势】命令头部的+/-表示优劣势（++意志30）" \
                           "\n\n【补正骰】命令后部的+/-表示补正（意志+30）" \
                           "\n\n【联合骰】技能1+技能2+技能3..." \
                           "\n\n【对抗骰】在角色消息栏@其他对抗人 并点击掷骰" \
                           "\n\n【全体掷骰】保持焦点在Bot消息框，点击Bot的掷骰按钮" \
                           "\n\n【暗骰】保持焦点在暗骰角色的消息框，点击Bot的掷骰按钮（公式取自暗骰角色）" \
                           "\n\n【.st】输入后点击发送按钮或回车（而不是掷骰按钮）" \
                           "\n\n【掷骰原因】消息栏填写掷骰原因，可以包括技能文字点掷骰按钮来触发检定（例如“我使用斗殴击晕敌人”）" \
                           "\n\n===以上可删除===\n\n"
            self.role_entries[role].insert(tk.END, initial_text)

        # 创建数值tag，显示数值
        role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
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
        entry2.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        value_tag = f"{role}_values_tag"
        self.role_values_tags[role] = value_tag
        entry2.tag_config(value_tag, justify=tk.LEFT)
        self.role_values_tags_text = load_PL_INFO()
        if role not in self.role_values_tags_text:
            entry2.insert(tk.END, f'{SAN}/{POW}/{_SAN}:S\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB',
                          value_tag)
        else:
            entry2.insert(tk.END, self.role_values_tags_text[role], value_tag)
        self.role_values_entry[role] = entry2
        # 为每个文本框绑定焦点变化事件
        entry2.bind("<FocusOut>", lambda event, r=role, t=entry2: self.save_info(event, role))

        send_button = tk.Button(frame, text="发送", command=lambda role=role: self.send_message(role))
        send_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        label = tk.Label(frame, text=role, relief=tk.FLAT,
                         font=("Times New Roman", 16, "bold"))  # flat, groove, raised, ridge, solid, or sunken
        label.grid(row=2, column=1, pady=0, sticky="nsew")
        label.bind("<Button-1>", lambda event, role=role, label=label: self.edit_role_name(event, role, label))
        if self.role_entries_name[role] != role:
            label.configure(text=self.role_entries_name[role])
            # print(self.role_entries_name[role])

        label = tk.Label(frame, text="@", relief=tk.FLAT)
        label.grid(row=2, column=0, pady=0, sticky="nsew")
        # label点击事件绑定
        label.bind("<Button-1>", lambda event, role=role: self.on_avatar_click(role))
        # 添加选择头像按钮
        choose_avatar_button = tk.Button(frame, text="选择头像", command=lambda role=role: self.choose_avatar(role))
        choose_avatar_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # 添加保存名牌按钮
        # choose_avatar_button = tk.Button(frame, text="保存", command=lambda role=role: self.choose_avatar(role))
        # choose_avatar_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        # 添加掷骰按钮和面数输入框
        entry_roll = tk.Text(frame, wrap=tk.WORD, width=3, height=1)
        entry_roll.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.role_entries_roll[role] = entry_roll
        roll_button = tk.Button(frame, text="掷骰", command=lambda r=role: self.get_and_roll(r))
        roll_button.grid(row=1, column=2, padx=5, pady=5)
        self.role_roll_button[role] = roll_button
        # 在 Text 组件中插入初始文本
        initial_text = "1d100"
        self.role_entries_roll[role].insert(tk.END, initial_text)

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
                self.role_entries_roll[role].grid(row=2, column=2, padx=5, pady=5, sticky="nsew")  # 展开
                self.role_roll_button[role].grid(row=1, column=2, padx=5, pady=5)
                self.role_values_entry[role].grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
            self.trpg_toggle = "off"

    def send_message(self, role):
        fire_babel(self, role)
        role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
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
                    # 滚动到最底部
                    self.chat_log.yview(tk.END)
                else:
                    new_chart = self.parse_input_skill(message)
                    self.update_skills(role_Chart[role], new_chart)
                    # if self.role_entries_name[role] in role_Chart_at_name:
                    role_Chart_at_name[self.role_entries_name[role]] = role_Chart[role]
                    role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"] = self.role_avatar_paths[role]
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
                    self.role_values_entry[role].delete("1.0", "2.0")
                    self.role_values_entry[role].insert("1.0",
                                                        f'{SAN_}/{POW}/{_SAN}:S\n')
                if "MOV" in message:
                    MOV_ = self.role_values_entry[role].get("4.0", "5.0").split("/")[0].strip()
                    self.role_values_entry[role].delete("4.0", "5.0")
                    self.role_values_entry[role].insert("4.0",
                                                        f'{MOV_}/{MOV}:MOV\n')
                if "DB" in message:
                    self.role_values_entry[role].delete("5.0", "6.0")
                    self.role_values_entry[role].insert("5.0",
                                                        f'\n{DB}:DB\n')
                # self.role_values_entry[role].insert("1.0",
                # f'{SAN}/{POW}/{_SAN}:S\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB\n===\n')
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
                    else:
                        if len(parts_skill) == 1 and "#" not in message:
                            self.chat_log.insert(tk.END,
                                                 f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的【{str(parts_skill[0][0]).upper()}】成长为{str(role_Chart[role][str(parts_skill[0][0]).upper()])}！\n\n')
                else:
                    self.role_entries[role].insert(tk.END, "已刷新！")
            else:
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
        print(skills)
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
            if old_dict["敏捷"] < old_dict["体型"]:
                old_dict["MOV"] = 7
            else:
                old_dict["MOV"] = 9
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
        if "图书馆使用" in old_dict and old_dict["图书馆"] == 0:
            old_dict["图书馆"] = old_dict["图书馆使用"]

        if "ARMOR" not in old_dict:
            old_dict["ARMOR"] = 0
        old_dict["#SAN"] = 100 - old_dict["克苏鲁神话"]
        self.save_role_skill_at_name()

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
                role_Chart[role] = role_Chart_at_name[new_name]
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
                # self.role_entries[role].delete("1.0", tk.END)
                self.role_avatar_paths[role] = role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"]
                self.load_and_display_avatar(role, self.role_entries[role].master)
                SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                POW = role_Chart_detail.get("POW")
                DB = role_Chart_detail.get("DB")
                SAN_ = role_Chart_detail.get("#SAN")
                self.role_values_entry[role].insert("1.0",
                                                    f'{SAN}/{POW}/{SAN_}:S\n{HP}/{HP}:HP\n{MP}/{MP}:MP\n{MOV}/{MOV}:MOV\n{DB}:DB\n===\n')
                # self.role_entries[role].delete("1.0", tk.END)
                # self.role_entries[role].insert(tk.END, "已录入！")
                # self.chat_log.insert(tk.END,
                # f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\nSAN:{SAN}\nHP:{HP}\nMP:{MP}\nMOV:{MOV}\n\n\n')
                self.chat_log.insert(tk.END,
                                     f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\n{self.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')

                self.role_entries[role].insert("1.0", "已加载名牌为[" + new_name + "]的角色卡！\n")
            else:
                role_Chart[role] = role_Chart_detail_demo

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

    def on_avatar_click(self, role):
        # 头像点击事件处理
        # self.current_at_role.set(role)
        self.avatar_click_event = role
        current_role = self.current_role.get()
        self.role_entries[current_role].insert(tk.END, "@" + self.role_entries_name[role] + " ")

    def output_chat_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_log_{timestamp}.txt"
        chat_log_content = self.chat_log.get("1.0", tk.END)
        with open(filename, "w") as file:
            file.write(chat_log_content)

    def output_html_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_log_{timestamp}.html"
        chat_log_content = self.chat_log.get("1.0", tk.END)
        with open(filename, "w") as file:
            file.write(f'<html><head></head><body>{chat_log_content}</body></html>')

    def choose_avatar(self, role):
        avatar_path = filedialog.askopenfilename(title="为【" + self.role_entries_name[role] + "】选择头像文件",
                                                 filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if avatar_path:
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
        if role in self.role_avatar_paths:
            # 加载头像
            image_path = self.role_avatar_paths[role]
            if image_path:
                if self.role_entries_name[role] in role_Chart_at_name:
                    role_Chart_at_name[self.role_entries_name[role]]["_AvatarPath"] = image_path
                image = Image.open(image_path)
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
                label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                # 头像点击事件绑定
                label.bind("<Button-1>", lambda event, role=role: self.on_avatar_click(role))
            else:
                label = tk.Label(frame)
                label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                label.bind("<Button-1>", lambda event, role=role: self.on_avatar_click(role))

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
            role_Chart_detail = role_Chart.get(role, {})
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
                for enemy in self.enemy_matches:
                    role_ = ""
                    for key, nickname in self.role_entries_name.items():
                        if enemy == nickname:
                            role_ = key
                    expression_ = self.enemy_matches[enemy]
                    reason_ = f"与{self.role_entries_name[role]}对抗"
                    self.roll_dice(role_, expression_, reason_)
            self.roll_dice(role, expression, reason)

    def roll_dice(self, role, expression, reason):
        parts_ = []
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        if role == "全员":
            for role in self.roles:
                if role != "DiceBot":
                    result_ = self.trpg_module.roll(expression, role)
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
                        message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                    else:
                        message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】因【{reason}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                    self.chat_log.insert(tk.END, message)
                    self.chat_log.yview(tk.END)
                    self.role_entries[role].delete("1.0", tk.END)
                    self.role_entries["DiceBot"].delete("1.0", tk.END)
                    if len(parts_) > 1:
                        self.role_entries[role].insert(tk.END, parts_[1])

                        weapon_list_ = {}
                        if parts_ and "成功" in parts_[1]:
                            role_Chart_detail_ = role_Chart.get(role, {})
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
                                            role_Chart_detail_armor = role_Chart.get(role, {})
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
                                    role_Chart_detail_armor = role_Chart.get(role, {})
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
                    message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                else:
                    message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n(【{self.role_entries_name[role]}】因【{reason}】掷骰{SANC}{adv_comment}){result}{expressionUPP}={parts_[0]}\n\n'
                self.chat_log.insert(tk.END, message)
                self.chat_log.yview(tk.END)

                weapon_list = {}
                if parts_ and "成功" in parts_[1]:
                    role_Chart_detail = role_Chart.get(role, {})
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
                                    role_Chart_detail_armor = role_Chart.get(role, {})
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
                                    role_Chart_detail_armor = role_Chart.get(role, {})
                                    if "ARMOR" in role_Chart_detail_armor:
                                        value_armor = role_Chart_detail_armor["ARMOR"]
                                    else:
                                        value_armor = 0
                                    self.role_entries_roll[role_armor].delete("1.0", tk.END)
                                    self.role_entries_roll[role_armor].insert("1.0", f"ARMOR:{value_armor}")
                elif parts_ and "失败" in parts_[1]:
                    role_Chart_detail_armor = role_Chart.get(role, {})
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
            if parts_ and "成功" in parts_[1]:
                role_Chart_detail__ = role_Chart.get(role, {})
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

    def set_start_point(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            x, y = event.x, event.y
            self.canvas.create_line(self.start_x, self.start_y, x, y, width=2)
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
            json.dump(data, file, ensure_ascii = False)
        with open('GameSaves/Deduction_infos_new.json', 'w', encoding='utf-8') as file:
            data = {}
            for role in self.roles:
                value_list = []
                if role != "KP":
                    for item in self.tree_list[role].get_children():
                        values = self.tree_list[role].item(item, 'values')
                        value_list.append(values)
                    data[role] = value_list
            json.dump(data, file, ensure_ascii = False)
        # self.new_window.destroy()

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
                map_button = tk.Button(frame, text="绘\n制\n地\n图", command=self.open_new_window_map)
                map_button.grid(row=0, column=1, pady=5, sticky="nsew")
                cal_button = tk.Button(frame, text="计\n算\n器", command=self.calculator)
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

    # 新窗口
    def open_new_window_map(self):
        new_window = tk.Toplevel(self.new_window)
        new_window.title("地图")
        self.image_references = []  # Add this list attribute to store references to images

        # text = self.time_log.get("1.0", tk.END).strip()
        label = tk.Label(new_window, text="地图示意窗口")
        label.pack()

        # 创建 Canvas 组件
        self.canvas = tk.Canvas(new_window, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 记录鼠标位置
        self.start_x = None
        self.start_y = None

        # 绑定鼠标事件
        self.canvas.bind("<B3-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.set_start_point)

        self.draggable_items = {}
        radius = 0.13
        x = 100
        y = 200
        for _avatar, _avatar_paths in self.role_avatar_paths.items():
            if os.path.exists(_avatar_paths):
                with open(_avatar_paths, "rb") as f:
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
                draggable_image = DraggableItem(self.canvas, x, y, 10, 10, image=photo)
                x += 100
                self.draggable_items[_avatar] = draggable_image
        # Create draggable rectangle
        draggable_rectangle = DraggableItem(self.canvas, 150, 150, 100, 80, fill='white', outline='black')

    def save_settings(self):
        # 将头像路径保存到JSON文件
        with open('AppSettings/avatar_settings.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_avatar_paths, file, ensure_ascii = False)
        # 将姓名牌路径保存到JSON文件
        with open('AppSettings/name_settings.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_entries_name, file, ensure_ascii = False)
        # 尝试保存自定义角色数值信息
        with open('GameSaves/pl_info.json', 'w', encoding='utf-8') as file:
            json.dump(self.role_values_tags_text, file, ensure_ascii = False)
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
            json.dump(env, file, ensure_ascii = False)
        # 保存自定义角色数值信息
        with open('GameSaves/pl_Chart.json', 'w', encoding='utf-8') as file:
            json.dump(role_Chart, file, ensure_ascii = False)
        with open('Bots/bot_personality_by_name.json', 'w', encoding='utf-8') as file:
            json.dump(bot_personality_by_name, file, ensure_ascii = False)
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
        with open('GameSaves/pl_Chart_at_name.json', 'w', encoding='utf-8') as file:
            dicSkill = {}
            dic = role_Chart_at_name
            for role, skills in role_Chart.items():
                for skill, value in skills.items():
                    dicSkill[skill] = value
                dicSkill["_AvatarPath"] = ""
                if role in self.role_avatar_paths:
                    # 保存头像路径
                    dicSkill["_AvatarPath"] = self.role_avatar_paths[role]
                if (self.role_entries_name[role] != role) and ("PL " not in self.role_entries_name[role]):
                    dic[self.role_entries_name[role]] = dicSkill
            json.dump(dic, file, ensure_ascii = False)

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
                upgrade = "[成长检定]【" + skill_name + "】技能的成长检定(1D100=" + str(result) + "/" + str(info_) + ")失败了..."
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

    def roll(self, expression, role=None):
        global date
        global time
        global place
        global weather
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
            if pattern_combine.match(expression) and len(part_combine) > 1:
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
                print("联合掷骰")  # 意志+斗殴+潜行
                # print(part_combine)
                for a in part_combine:
                    combine_infos[a] = role_Chart_detail[a]
                print(combine_infos)
                expression = "COMBINE CHECK"
            if pattern_advantage.match(expression):
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
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
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
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
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

            elif bool(pattern.search(expression)) or part_eng[0][0] != "d":
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
                            self.move_time_forward(timer)
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
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
                            self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                        f'{SAN}/{POW}:SAN\n')
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
                            self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                        f'{SAN}/{POW}:SAN\n')
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
                        self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                    f'{SAN}/{POW}:SAN\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                     f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                        return f"{result}/{info}={sc_fail.upper()}={result2}：San Check失败！扣除{result2}点SAN。"
                    else:
                        result2 = int(sc_fail)
                        role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                        POW = role_Chart[role].get("POW")
                        SAN = role_Chart[role].get("SAN")
                        self.ChatApp.role_values_entry[role].delete("1.0", "2.0")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                    f'{SAN}/{POW}:SAN\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                     f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：{self.ChatApp.role_values_entry[role].get("1.0", "2.0").strip()}\n\n')
                        return f"{result}/{info}={result2}：San Check失败！扣除{result2}点SAN。"

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
        if time == "00:00":
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
        if time == "00:00":
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
        if time == "00:00":
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
        if time == "00:00":
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
    def __init__(self, canvas, x, y, width, height, fill=None, image=None, outline=None):
        self.canvas = canvas
        if image:
            self.item = canvas.create_image(x, y, image=image, tags="draggable")
        else:
            self.item = canvas.create_rectangle(x, y, x + width, y + height, fill=fill, outline=outline,
                                                tags="draggable")
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.on_drag)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.canvas.move(self.item, delta_x, delta_y)
        self.start_x = event.x
        self.start_y = event.y


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
        # self.ChatApp = chat_app_instance

    def body(self, master):
        tk.Label(master, text="第一次掷骰结果：").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="第二次掷骰结果：").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="线索名：").grid(row=2, column=0, sticky="e")
        self.trust_var = tk.StringVar()
        self.importance_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.source_entry = tk.Entry(master, textvariable=self.source_var)

        first_roll_values = ["大失败（-20%）", "失败（10%）", "成功（100%）"]
        self.first_roll_entry = ttk.Combobox(master, textvariable=self.trust_var, values=first_roll_values)

        second_roll_values = ["大失败（-80%）", "失败（-20%）", "成功（+20%）", "困难成功（+40%）", "极难成功（+60%）", "大成功（+100%）"]
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
        result_text = f"结果百分比：{result_percentage}\n处理方案：{final_result}\n\n根据原模组信息总结至多五个关键词，按重要度排序，发放时按重要度低到高发放。\n" \
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
        final_result = "2假词/1真2假"
    elif result_percentage == -10:
        final_result = "1假词/1真1假"
    elif result_percentage == 0:
        final_result = "0关键词"
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
            json.dump(self.babel_data, file, ensure_ascii = False)

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
                if lan_main in dic2:
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
                                print(f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [母语({dic2[dic2['母语']]}): {dic2['母语']}] ！")

                            elif self.best_lan_skill + lan_list[self.best_lan] >= 40 and self.best_lan_skill >= 30:
                                print(f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [困难母语({int(dic2[dic2['母语']]/2)}): {dic2['母语']}] ！")

                            elif self.best_lan_skill + lan_list[self.best_lan] >= 10 and self.best_lan_skill > 5:
                                print(f"[巴别塔] 啊哦！【{role2}】 好像听不懂 【{role}】 在说什么！请掷骰 [{self.best_lan}({self.best_lan_skill})] 或 [极难母语({int(dic2[dic2['母语']]/5)}): {dic2['母语']}] ！")
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
    root.mainloop()
