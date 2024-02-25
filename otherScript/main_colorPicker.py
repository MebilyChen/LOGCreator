import tkinter as tk
from tkinter import scrolledtext, filedialog, colorchooser
from datetime import datetime
from PIL import Image, ImageTk
from tkhtmlview import HTMLLabel

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多角色聊天程序")

        # 初始化角色列表
        self.roles = ["KP", "Dice", "PL1"]
        self.current_role = tk.StringVar(value=self.roles[0])
        self.role_colors = {}  # 存储每个角色的颜色

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")

        # 初始化 HTML LOG 预览
        self.html_preview = HTMLLabel(root, width=30, height=20)
        self.html_preview.grid(row=0, column=1, padx=10, pady=10, rowspan=3, sticky="nsew")

        # 初始化输出聊天LOG按钮
        output_button = tk.Button(root, text="输出聊天LOG", command=self.output_chat_log)
        output_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # 初始化输出HTML按钮
        output_html_button = tk.Button(root, text="输出HTML", command=self.output_html_log)
        output_html_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # 初始化角色对应的文字输入框、发送按钮、选择头像按钮、颜色选择按钮和角色名编辑
        self.role_entries = {}
        self.create_role_frames()

        # 初始化添加角色按钮
        add_role_button = tk.Button(root, text="添加角色", command=self.add_role)
        add_role_button.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # 初始化删除角色按钮
        delete_role_button = tk.Button(root, text="删除角色", command=self.delete_last_role)
        delete_role_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

    def create_role_frames(self):
        num_cols = 3
        for idx, role in enumerate(self.roles):
            row = idx % num_cols
            col = idx // num_cols
            self.create_role_frame(role, row, col)

        # 自动调整列宽
        for i in range(num_cols + 3):
            self.root.columnconfigure(i, weight=1)

    def create_role_frame(self, role, row, col):
        frame = tk.LabelFrame(self.root, text=role)
        frame.grid(row=row, column=col + 3, padx=10, pady=10, sticky="nsew")

        # 初始化头像路径
        self.role_avatar_paths = {}

        # 初始化颜色
        self.role_colors[role] = "black"  # 默认为黑色

        # 加载并显示头像
        self.load_and_display_avatar(role, frame)

        entry = tk.Text(frame, wrap=tk.WORD, width=30, height=3)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.role_entries[role] = entry

        send_button = tk.Button(frame, text="发送", command=lambda role=role: self.send_message(role))
        send_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 添加选择头像按钮
        choose_avatar_button = tk.Button(frame, text="选择头像", command=lambda role=role: self.choose_avatar(role))
        choose_avatar_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # 添加颜色选择按钮
        choose_color_button = tk.Button(frame, text="选择颜色", command=lambda role=role: self.choose_color(role))
        choose_color_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        label = tk.Label(frame, text=role, relief=tk.SOLID)
        label.grid(row=4, column=1, pady=5)
        label.bind("<Button-1>", lambda event, role=role, label=label: self.edit_role_name(event, role, label))

    def send_message(self, role):
        message = self.role_entries[role].get("1.0", tk.END).strip()
        if message:
            timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            color = self.role_colors.get(role, "black")
            log = f'<font color="{color}">{role} {timestamp}\n{message}</font>\n\n'
            self.chat_log.insert(tk.END, log)
            self.update_html_preview()
            self.role_entries[role].delete("1.0", tk.END)

    def edit_role_name(self, event, role, label):
        entry = tk.Entry(label, width=10)
        entry.insert(0, role)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        entry.bind("<FocusOut>", lambda event, role=role, entry=entry, label=label: self.update_role_name(role, label, entry))

    def update_role_name(self, role, label, entry):
        new_name = entry.get().strip()
        if new_name and new_name != role and not new_name.startswith("PL"):
            # 更新角色名
            self.roles[self.roles.index(role)] = new_name
            entry.grid_forget()
            label.configure(text=new_name)

    def add_role(self):
        new_role = f"PL{len(self.roles) - 2}"
        self.roles.append(new_role)

        num_cols = 3
        idx = len(self.roles) - 1
        row = idx % num_cols
        col = idx // num_cols
        self.create_role_frame(new_role, row, col)

        # 超过3列时自动换列
        if col > 2:
            self.root.columnconfigure(col + 3, weight=1)

    def delete_last_role(self):
        if len(self.roles) > 3:
            last_role = self.roles[-1]
            self.roles.pop()
            self.role_entries[last_role].master.destroy()
            del self.role_entries[last_role]

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
        self.update_html_preview()

    def update_html_preview(self):
        html_content = self.chat_log.get("1.0", tk.END)
        self.html_preview.set_html(html_content, strip=False)

    def choose_avatar(self, role):
        avatar_path = filedialog.askopenfilename(title="选择头像文件", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if avatar_path:
            # 更新头像路径
            self.role_avatar_paths[role] = avatar_path
            # 加载并显示头像
            frame = self.role_entries[role].master
            self.load_and_display_avatar(role, frame)

    def choose_color(self, role):
        color = colorchooser.askcolor()[1]  # 返回颜色的十六进制表示
        if color:
            self.role_colors[role] = color

    def load_and_display_avatar(self, role, frame):
        if role in self.role_avatar_paths:
            # 加载头像
            image_path = self.role_avatar_paths[role]
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.ANTIALIAS)  # 调整头像大小
            tk_image = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=tk_image)
            label.image = tk_image
            label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
