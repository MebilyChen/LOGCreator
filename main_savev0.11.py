import math
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import json


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


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自嗨团 v0.21")

        # 设置图标
        self.root.iconbitmap("icon.ico")

        # 其他窗口内容
        # self.label = tk.Label(root, text="Hello, Tkinter!")

        # 绑定回车键和Alt+回车键
        root.bind("<Return>", lambda event: self.send_message(self.current_role.get()))
        root.bind("<Alt-Return>", lambda event: self.insert_newline())
        root.bind("<Control-Return>", self.newline_on_ctrl_enter)

        # 初始化角色列表
        self.roles = ["KP", "DiceBot", "PL 1"]
        # 初始化当前聚焦的头像和文本框
        self.current_role = tk.StringVar(value=self.roles[0])
        # 初始化TRPG模块
        self.trpg_module = TRPGModule()

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")

        # 初始化输出聊天LOG按钮
        output_button = tk.Button(root, text="输出聊天LOG", command=self.output_chat_log)
        output_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # 初始化输出HTML按钮
        output_html_button = tk.Button(root, text="输出HTML(施工中)", command=self.output_html_log)
        output_html_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # 初始化角色对应的文字输入框、发送按钮和角色名编辑
        self.role_entries = {}
        self.role_entries_name = {}
        for role in self.roles:
            self.role_entries_name[role] = role
            if load_settings_name() != "":
                self.role_entries_name = load_settings_name()  # 从文件加载设置
        self.create_role_frames()

        # 为每个文本框绑定焦点变化事件
        for role in self.roles:
            entry = self.role_entries[role]
            entry.bind("<FocusIn>", lambda event, role=role: self.bind_enter_to_send_message(event, role))

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

        frame = tk.LabelFrame(self.root, text=role)
        frame.grid(row=row, column=col + 2, padx=10, pady=10, sticky="nsew")

        # 初始化头像路径
        self.role_avatar_paths = {}
        if load_settings_avatar() != "":
            self.role_avatar_paths = load_settings_avatar()  # 从文件加载设置
        # 头像点击事件
        # self.avatar_click_event = None

        # 加载并显示头像
        self.load_and_display_avatar(role, frame)

        entry = tk.Text(frame, wrap=tk.WORD, width=30, height=3)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.role_entries[role] = entry

        send_button = tk.Button(frame, text="发送", command=lambda role=role: self.send_message(role))
        send_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        label = tk.Label(frame, text=role, relief=tk.SOLID)  # flat, groove, raised, ridge, solid, or sunken
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

    def send_message(self, role):
        message = self.role_entries[role].get("1.0", tk.END).strip()
        if message:
            timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            log = f"{self.role_entries_name[role]} {timestamp}\n{message}\n\n"  # 不加引号
            self.chat_log.insert(tk.END, log)
            # 滚动到最底部
            self.chat_log.yview(tk.END)
            self.role_entries[role].delete("1.0", tk.END)

    def edit_role_name(self, event, role, label):
        entry = tk.Entry(label, width=10)
        entry.insert(0, role)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        entry.bind("<FocusOut>",
                   lambda event, role=role, entry=entry, label=label: self.update_role_name(event, role, entry, label))

    def update_role_name(self, event, role, entry, label):
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
            role_to_delete = self.roles.pop()
            self.role_entries[role_to_delete].destroy()
            # self.roles[len(self.roles)-1].destroy()
            del self.role_entries[role_to_delete]
            # del self.roles[len(self.roles)]

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

    def bind_enter_to_send_message(self, event, role):
        # 为当前文本框绑定回车键发送消息
        self.current_role.set(role)
        self.root.bind("<Return>", lambda event, role=role: self.send_message_on_enter(event, role))

    def send_message_on_enter(self, event, role=None):
        self.current_role.set(role)
        # 判断是否同时按下了 Ctrl 键
        if event.state - 4 == 0:  # 4 表示 Ctrl 键的状态值
            return
        # 发送消息
        current_role = role or self.current_role.get()
        self.send_message(current_role)

    def newline_on_ctrl_enter(self, event):
        # 换行
        current_role = self.current_role.get()
        self.role_entries[current_role].insert(tk.END, "")

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

    def roll_dice(self, role, expression):
        result = self.trpg_module.roll(expression)
        message = f'{role} 掷骰: {expression}，结果: {result}\n'
        self.chat_log.insert(tk.END, message)
        self.chat_log.yview(tk.END)

    def save_settings(self):
        # 将头像路径保存到JSON文件
        with open('avatar_settings.json', 'w') as file:
            json.dump(self.role_avatar_paths, file)
        # 将姓名牌路径保存到JSON文件
        with open('name_settings.json', 'w') as file:
            json.dump(self.role_entries_name, file)

    def on_closing(self):
        # 在关闭窗口前保存设置
        self.save_settings()
        self.root.destroy()


class TRPGModule:
    def __init__(self):
        self.random_seed = None

    def roll(self, expression):
        if self.random_seed is not None:
            random.seed(self.random_seed)
        try:
            return eval(expression)
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # 捕获窗口关闭事件
    root.mainloop()
