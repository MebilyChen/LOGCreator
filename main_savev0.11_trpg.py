import math
import re
from random import random
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog
from datetime import datetime
import configparser

from PIL import Image, ImageTk
import json

Critical_Success = "￥￥￥ 是大成功！￥￥￥"
Extreme_Success = "（深呼吸）...极难成功！恭喜您！"
Hard_Success = "困难成功！"
Success = "鉴定成功，期待您的表现。"
Failure = "失败了，请您不要灰心..."
Fumble = "嗯...抱歉，看起来是大失败呢..."


def load_settings_avatar():
    try:
        # 尝试从JSON文件加载头像路径
        with open('avatar_settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': '', 'DiceBot': '',
                'PL 1': ''}


def load_settings_name():
    try:
        # 尝试加载姓名牌路径
        with open('name_settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': 'KP', 'DiceBot': 'DiceBot',
                'PL 1': 'PL 1'}


def load_PL_INFO():
    try:
        # 尝试加载自定义角色数值信息
        with open('pl_info.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，返回默认设置
        return {'KP': '56/100:SAN\n10/10:HP\n5/5:MP\n5/5:MOV', 'DiceBot': '56/100:SAN\n10/10:HP\n5/5:MP\n5/5:MOV',
                'PL 1': '56/100:SAN\n10/10:HP\n5/5:MP\n5/5:MOV'}


def load_role_count():
    # 从配置文件加载角色数量，默认为0
    config = configparser.ConfigParser()
    config.read('config.ini')
    return int(config.get('Settings', 'RoleCount', fallback=0))


def load_Chart():
    try:
        # 尝试加载自定义角色数值信息
        with open('pl_Chart.json', 'r', encoding='utf-8') as file:
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
            "会计": 5,
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
            "手枪": 20,
            "急救": 30,
            "历史": 5,
            "恐吓": 15,
            "跳跃": 20,
            "拉丁语": 1,
            "母语": "EDU",
            "法律": 5,
            "图书馆": 20,
            "聆听": 20,
            "锁匠": 1,
            "机械维修": 10,
            "医学": 1,
            "博物学": 10,
            "自然学": 10,
            "领航": 10,
            "神秘学": 5,
            "重型机械": 1,
            "说服": 10,
            "精神分析": 1,
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
            "炮术": 1
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
                "会计": 5,
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
                "手枪": 20,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "自然学": 10,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
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
                "炮术": 1
            }, "PL 1": {
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
                "会计": 5,
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
                "手枪": 20,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "自然学": 10,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
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
                "炮术": 1
            }, "PL 2": {
                "EDU": 0,
                "APP": 0,
                "DEX": 0,
                "STR": 0,
                "INT": 0,
                "CON": 0,
                "POW": 0,
                "SIZ": 0,
                "LUCK": 0,
                "MOV": 8,
                "HP": "(CON+SIZ)/10",
                "MP": "POW/5",
                "SAN": "POW",
                "会计": 5,
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
                "手枪": 20,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "自然学": 10,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
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
                "炮术": 1
            }, "PL 3": {
                "EDU": 0,
                "APP": 0,
                "DEX": 0,
                "STR": 0,
                "INT": 0,
                "CON": 0,
                "POW": 0,
                "SIZ": 0,
                "LUCK": 0,
                "MOV": 8,
                "HP": "(CON+SIZ)/10",
                "MP": "POW/5",
                "SAN": "POW",
                "会计": 5,
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
                "手枪": 20,
                "急救": 30,
                "历史": 5,
                "恐吓": 15,
                "跳跃": 20,
                "拉丁语": 1,
                "母语": "EDU",
                "法律": 5,
                "图书馆": 20,
                "聆听": 20,
                "锁匠": 1,
                "机械维修": 10,
                "医学": 1,
                "博物学": 10,
                "自然学": 10,
                "领航": 10,
                "神秘学": 5,
                "重型机械": 1,
                "说服": 10,
                "精神分析": 1,
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
                "炮术": 1
            }}
    except json.JSONDecodeError as e:
        print(f"Error in JSON decoding: {e}")
        print(f"Problematic data: {file.read()}")


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
    "会计": 5,
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
    "手枪": 20,
    "急救": 30,
    "历史": 5,
    "恐吓": 15,
    "跳跃": 20,
    "拉丁语": 1,
    "母语": "EDU",
    "法律": 5,
    "图书馆": 20,
    "聆听": 20,
    "锁匠": 1,
    "机械维修": 10,
    "医学": 1,
    "博物学": 10,
    "自然学": 10,
    "领航": 10,
    "神秘学": 5,
    "重型机械": 1,
    "说服": 10,
    "精神分析": 1,
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
    "炮术": 1
}

role_Chart = load_Chart()


class ChatApp:
    def __init__(self, root):

        self.root = root
        self.root.title("自嗨团 v0.33")

        # 设置图标
        self.root.iconbitmap("icon.ico")

        # 其他窗口内容
        # self.label = tk.Label(root, text="Hello, Tkinter!")

        # 绑定回车键和Alt+回车键
        root.bind("<Return>", lambda event: self.send_message(self.current_role.get()))
        root.bind("<Alt-Return>", lambda event: self.insert_newline())
        root.bind("<Control-Return>", self.newline_on_ctrl_enter)

        # 初始化角色列表
        self.role_count = load_role_count()
        self.roles = ["KP", "DiceBot", "PL 1"]

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

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")
        # 在 Text 组件中插入初始文本
        initial_text = "Updates：\n更新了TRPG掷骰模块\n退出时保存当前设置（头像、名字、PL数量）\n更新了自定义数值/笔记栏\n.st存入Json数据库\nSC\n" \
                       "\nTodo:" \
                       "\n--计算" \
                       "\n--features & bugs\n掷骰栏回车发送\n复杂掷骰算式（多个不同面骰子+常数）优化\n输出染色HTML(坑)\n\n"
        self.chat_log.insert(tk.END, initial_text)

        # 初始化输出聊天LOG按钮
        output_button = tk.Button(root, text="输出聊天LOG", command=self.output_chat_log)
        output_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # 初始化输出HTML按钮
        output_html_button = tk.Button(root, text="输出HTML(施工中)", command=self.output_html_log)
        output_html_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

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
        self.create_role_frames()
        for i in range(self.role_count):
            self.add_role_init()

        # 为每个文本框绑定焦点变化事件
        for role in self.roles:
            entry = self.role_entries[role]
            entry.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))
        for role in self.roles:
            entry_roll = self.role_entries_roll[role]
            entry_roll.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))

        # 初始化删除角色按钮
        delete_role_button = tk.Button(root, text="删除角色", command=self.delete_role)
        delete_role_button.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # 初始化添加角色按钮
        add_role_button = tk.Button(root, text="添加角色", command=self.add_role)
        add_role_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

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
                           "\n\n【全体掷骰】保持焦点在Bot消息框，点击Bot的掷骰按钮" \
                           "\n\n【暗骰】保持焦点在暗骰角色的消息框，点击Bot的掷骰按钮（公式取自暗骰角色）" \
                           "\n\n【掷骰原因】消息栏填写掷骰原因，可以包括技能文字来触发检定（例如“我使用斗殴击晕敌人”）"
            self.role_entries[role].insert(tk.END, initial_text)

        # 创建数值tag，显示数值
        role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
        SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        POW = role_Chart_detail.get("POW")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
        entry2 = tk.Text(frame, wrap=tk.WORD, width=10, height=6)
        entry2.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        value_tag = f"{role}_values_tag"
        self.role_values_tags[role] = value_tag
        entry2.tag_config(value_tag, justify=tk.LEFT)
        self.role_values_tags_text = load_PL_INFO()
        if role not in self.role_values_tags_text:
            entry2.insert(tk.END, f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV', value_tag)
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
                if ("+" or "-" or "*" or "/") in message:
                    parts = re.findall(r'([\u4e00-\u9fa5a-zA-Z\s]+)([-+*/^])(\d+)', message)
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
                SAN = role_Chart_detail.get("SAN")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                HP = role_Chart_detail.get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MP = role_Chart_detail.get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                MOV = role_Chart_detail.get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                POW = role_Chart_detail.get("POW")
                self.role_values_entry[role].insert("1.0", f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV\n===\n')
                self.role_entries[role].delete("1.0", tk.END)
                self.role_entries[role].insert(tk.END, "已录入！")
                # self.chat_log.insert(tk.END,
                # f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\nSAN:{SAN}\nHP:{HP}\nMP:{MP}\nMOV:{MOV}\n\n\n')
                self.chat_log.insert(tk.END,
                                     f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.role_entries_name[role]}】的状态：\n{self.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')

            else:
                self.chat_log.insert(tk.END, log)
                # 滚动到最底部
                self.chat_log.yview(tk.END)
                self.role_entries[role].delete("1.0", tk.END)

    def parse_input_skill(self, input_string):
        skills = {}
        # 使用正则表达式从输入字符串中提取技能和值的组合
        pattern = re.compile(r'([\u4e00-\u9fa5a-zA-Z\s]+)(\d+)')
        matches = pattern.findall(input_string)

        for match in matches:
            skill_name = match[0].strip()
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
        if old_dict["SIZ"] == 0 and old_dict["体型"] != 0:
            old_dict["EDU"] = old_dict["教育"]
            old_dict["APP"] = old_dict["外貌"]
            old_dict["DEX"] = old_dict["敏捷"]
            old_dict["STR"] = old_dict["力量"]
            old_dict["INT"] = old_dict["智力"]
            old_dict["CON"] = old_dict["体质"]
            old_dict["POW"] = old_dict["意志"]
            old_dict["SIZ"] = old_dict["体型"]
            old_dict["LUCK"] = old_dict["幸运"]
        if old_dict["SIZ"] != 0 and old_dict["体型"] == 0:
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
            # 更新当前角色名
            # if self.current_role.get() == role:
            # self.current_role.set(new_name)

            entry.grid_forget()
            label.configure(text=new_name)

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

    def send_message_on_enter(self, event, role=None):
        self.current_role.set(role)
        # 判断是否同时按下了 Ctrl 键
        if event.state - 4 == 0:  # 4 表示 Ctrl 键的状态值
            return
        # 发送消息
        current_role = role or self.current_role.get()
        self.send_message(current_role)
        self.highlight_role_frame(current_role)

    def newline_on_ctrl_enter(self, event):
        # 换行
        current_role = self.current_role.get()
        self.role_entries[current_role].insert(tk.END, "")
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
        self.role_entries_frame[self.highlighted_role.get()].config(relief=tk.SOLID)
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

    def load_and_display_avatar(self, role, frame):
        if role in self.role_avatar_paths:
            # 加载头像
            image_path = self.role_avatar_paths[role]
            if image_path:
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
            reason = self.role_entries[role].get("1.0", tk.END).strip()
            if reason == "":
                # 一系列字符串
                string_list = ["不可名状的原因", "懒得写原因", "", "", ""]
                # 从列表中随机选择一个字符串
                reason = random.choice(string_list)

            expression = self.role_entries_roll[role].get("1.0", tk.END).strip().lower()
            if expression == "":
                expression = "1d100"
            role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
            for skill in role_Chart_detail:
                if skill in reason:
                    expression = skill
                    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    log = f"{self.role_entries_name[role]} {timestamp}\n{reason}\n\n"  # 不加引号
                    self.chat_log.insert(tk.END, log)
                    # 滚动到最底部
                    self.chat_log.yview(tk.END)
                    reason = skill
            # 调用掷骰方法
            self.roll_dice(role, expression, reason)

    def roll_dice(self, role, expression, reason):
        parts_ = []
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        if role == "全员":
            for role in self.roles:
                if role != "DiceBot":
                    result = self.trpg_module.roll(expression, role)
                    parts_ = result.split('：')
                    SANC = ""
                    expressionUPP = expression.upper()
                    if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
                        expressionUPP = "1D100"
                        if ("sc" or "SC" or ".sc" or "。sc") in expression:
                            SANC = "[SAN CHECK:" + expression.split("sc")[1].upper() + "]"
                        else:
                            SANC = "[" + expression.upper() + "]"
                    if reason == "":
                        message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n({self.role_entries_name[role]}掷骰{SANC}){expressionUPP}={parts_[0]}\n\n'
                    else:
                        message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n({self.role_entries_name[role]}因【{reason}】掷骰{SANC}){expressionUPP}={parts_[0]}\n\n'
                    self.chat_log.insert(tk.END, message)
                    self.chat_log.yview(tk.END)
                    self.role_entries[role].delete("1.0", tk.END)
                    if len(parts_) > 1:
                        self.role_entries[role].insert(tk.END, parts_[1])

        else:
            if role == "DiceBot":
                pass
            else:
                result = self.trpg_module.roll(expression, role)
                parts_ = result.split('：')
                print(parts_)
                SANC = ""
                expressionUPP = expression.upper()
                if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
                    expressionUPP = "1D100"
                    if ("sc" or "SC" or ".sc" or "。sc") in expression:
                        SANC = "[SAN CHECK:" + expression.split("sc")[1].upper() + "]"
                    else:
                        SANC = "[" + expression.upper() + "]"
                if reason == "":
                    message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n({self.role_entries_name[role]}掷骰{SANC}){expressionUPP}={parts_[0]}\n\n'
                else:
                    message = f'{self.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n({self.role_entries_name[role]}因【{reason}】掷骰{SANC}){expressionUPP}={parts_[0]}\n\n'
                self.chat_log.insert(tk.END, message)
                self.chat_log.yview(tk.END)

        # 清空输入框文本
        self.role_entries[role].delete("1.0", tk.END)
        if len(parts_) > 1:
            self.role_entries[role].insert(tk.END, parts_[1])

    def roll_dice_silent(self, role, expression, reason):
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        SANC = ""
        self.role_entries[role].delete("1.0", tk.END)
        if reason == "":
            # 一系列字符串
            string_list = ["不可告人的妙计", "想到了开心的事情", "", "", ""]
            # 从列表中随机选择一个字符串
            reason = random.choice(string_list)
        if bool(pattern.search(expression)) or ("sc" or "SC" or ".sc" or "。sc") in expression:
            if ("sc" or "SC" or ".sc" or "。sc") in expression:
                SANC = "[SAN CHECK:" + expression.split("sc")[1].upper() + "]"
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

    def save_settings(self):
        # 将头像路径保存到JSON文件
        with open('avatar_settings.json', 'w') as file:
            json.dump(self.role_avatar_paths, file)
        # 将姓名牌路径保存到JSON文件
        with open('name_settings.json', 'w') as file:
            json.dump(self.role_entries_name, file)
        # 尝试保存自定义角色数值信息
        with open('pl_info.json', 'w') as file:
            json.dump(self.role_values_tags_text, file)
        # 保存自定义角色数值信息
        with open('pl_Chart.json', 'w', encoding='utf-8') as file:
            json.dump(role_Chart, file)

    def save_role_count(self):
        # 保存角色数量到配置文件
        config = configparser.ConfigParser()
        config['Settings'] = {'RoleCount': str(self.role_count)}
        with open('config.ini', 'w') as configfile:
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

    def roll(self, expression, role=None):
        if self.random_seed is not None:
            random.seed(self.random_seed)
        info = None
        sc_success = ""
        sc_fail = ""
        try:
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            pattern_user = re.compile(r'([\u4e00-\u9fa5a-zA-Z]+)(\d+)')
            part_eng = pattern_user.findall(expression)
            if ("sc" or "SC" or ".sc" or "。sc") in expression:
                print("SAN CHECK") #sc1/1d5
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

            elif bool(pattern.search(expression)) or part_eng[0][0] != "d":
                print("技能检定")
                print(part_eng[0][0])
                print(part_eng[0][1])
                if part_eng[0][1] != "":
                    expression = part_eng[0][0]
                    info = int(part_eng[0][1])
                role_Chart_detail = role_Chart.get(role, {})  # 获取 "KP" 对应的字典，如果没有则返回空字典
                if "困难" in expression or "极难" in expression:
                    print(expression)
                    parts_ = expression.split('难')
                    if parts_[0] == "极":
                        info = int(role_Chart_detail.get(parts_[1])/5)
                    if parts_[0] == "困":
                        info = int(role_Chart_detail.get(parts_[1])/2)
                else:
                    #print(expression)
                    if info == None:
                        info = role_Chart_detail.get(expression)  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                    #print(info)
                if str(info).isalpha():
                    info = role_Chart_detail.get(info)
                    #print(info)
                expression = "1d100"

            if expression == "SAN CHECK":
                # 解析表达式
                expression = "1d100"
                parts = expression.split('d')
                num_rolls = int(parts[0])
                num_faces = int(parts[1])
                # 执行掷骰
                rolls = [random.randint(1, num_faces) for _ in range(num_rolls)]
                result = sum(rolls)
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
                            HP = role_Chart[role].get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            MP = role_Chart[role].get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            MOV = role_Chart[role].get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            POW = role_Chart[role].get("POW")
                            SAN = role_Chart[role].get("SAN")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                     f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV\n===\n')
                            self.ChatApp.chat_log.insert(tk.END,
                                                      f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：\n{self.ChatApp.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                            return f"{result}/{info}={sc_success.upper()}={result2}：San Check成功，请扣除{result2}点SAN。"
                    else:
                        result2 = int(sc_success)
                        if result2 == 0:
                            return f"{result}/{info}={result2}：San Check成功！司空见惯！"
                        else:
                            role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                            HP = role_Chart[role].get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            MP = role_Chart[role].get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            MOV = role_Chart[role].get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                            POW = role_Chart[role].get("POW")
                            SAN = role_Chart[role].get("SAN")
                            self.ChatApp.role_values_entry[role].insert("1.0",
                                                                f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV\n===\n')
                            self.ChatApp.chat_log.insert(tk.END,
                                                 f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：\n{self.ChatApp.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                            return f"{result}/{info}={result2}：San Check成功，请扣除{result2}点SAN。"
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
                        HP = role_Chart[role].get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        MP = role_Chart[role].get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        MOV = role_Chart[role].get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        POW = role_Chart[role].get("POW")
                        SAN = role_Chart[role].get("SAN")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                 f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV\n===\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                  f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：\n{self.ChatApp.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                        return f"{result}/{info}={sc_fail.upper()}={result2}：San Check失败！请扣除{result2}点SAN。"
                    else:
                        result2 = int(sc_fail)
                        role_Chart[role]["SAN"] = role_Chart[role]["SAN"] - result2
                        HP = role_Chart[role].get("HP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        MP = role_Chart[role].get("MP")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        MOV = role_Chart[role].get("MOV")  # edu_value = sub_dict.get("EDU")  # 获取 "EDU" 对应的值
                        POW = role_Chart[role].get("POW")
                        SAN = role_Chart[role].get("SAN")
                        self.ChatApp.role_values_entry[role].insert("1.0",
                                                                 f'{SAN}/{POW}:SAN\n10/{HP}:HP\n5/{MP}:MP\n5/{MOV}:MOV\n===\n')
                        self.ChatApp.chat_log.insert(tk.END,
                                                  f'{self.ChatApp.role_entries_name["DiceBot"]} {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}\n【{self.ChatApp.role_entries_name[role]}】的状态[已扣除SC]：\n{self.ChatApp.role_values_entry[role].get("1.0", "5.0").strip()}\n\n')
                        return f"{result}/{info}={result2}：San Check失败！请扣除{result2}点SAN。"

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
                            print(result)
                            print(num_expression)

                            # formula_add.remove(formula_add.count() - 1)
                            if info != None:
                                info_ = info
                                info = None
                                if result <= 5 and info_ >= 50:
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
                                elif result >= 95 and info_ < 50:
                                    compare = ">"
                                    comment = Fumble
                                elif result == 100:
                                    compare = ">"
                                    comment = Fumble
                                else:
                                    compare = ">"
                                    comment = Failure
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
                if info != None:
                    info_ = info
                    info = None
                    if result <= 5 and info_ >= 50:
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
                    elif result >= 95 and info_ < 50:
                        compare = ">"
                        comment = Fumble
                    elif result == 100:
                        compare = ">"
                        comment = Fumble
                    else:
                        compare = ">"
                        comment = Failure
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
                if info != None:
                    info_ = info
                    # print(info_)
                    info = None
                    if result <= 5 and info_ >= 50:
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
                    elif result >= 95 and info_ < 50:
                        compare = ">"
                        comment = Fumble
                    elif result == 100:
                        compare = ">"
                        comment = Fumble
                    else:
                        compare = ">"
                        comment = Failure
                    # 执行算式
                    if num_rolls == 1:
                        return f"{result}/{info_}：{comment}"
                    else:
                        return f"{'+'.join(map(str, rolls))}={result}/{info_}：{comment}"
                else:
                    if num_rolls == 1:
                        return f"{result}"
                    else:
                        return f"{'+'.join(map(str, rolls))}={result}"


        except Exception as e:
            return f"Error: {e}"


class COCModule:
    def __init__(self):
        self.random_seed = None

    def roll_dice_san(self, expression):
        # 支持算式的掷骰
        if self.random_seed is not None:
            random.seed(self.random_seed)

        try:
            # 使用正则表达式分割中文、英文和数字
            parts = re.findall(r'[A-Za-z]+|\d+|[\u4e00-\u9fa5]+|[+\-*/d()]', expression)
            # 构建新的表达式，替换掉中文和英文
            num_expression = ''.join(parts)
            # 替换掷骰表达式
            num_expression = re.sub(r'(\d+)d(\d+)', lambda match: '+'.join(
                str(random.randint(1, int(match.group(2)))) for _ in range(int(match.group(1)))), num_expression)
            # 计算结果
            result = eval(num_expression)

            return result
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 捕获窗口关闭事件
    root.mainloop()
