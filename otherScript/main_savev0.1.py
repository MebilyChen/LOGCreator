import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多角色聊天程序")

        # 初始化角色列表
        self.roles = ["KP", "Dice", "PL1"]
        self.current_role = tk.StringVar(value=self.roles[0])

        # 初始化聊天LOG
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="nsew")

        # 初始化输出聊天LOG按钮
        output_button = tk.Button(root, text="输出聊天LOG", command=self.output_chat_log)
        output_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # 初始化角色对应的文字输入框、发送按钮和角色名编辑
        self.role_entries = {}
        self.create_role_frames()

        # 初始化删除角色按钮
        delete_role_button = tk.Button(root, text="删除角色", command=self.delete_role)
        delete_role_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 初始化添加角色按钮
        add_role_button = tk.Button(root, text="添加角色", command=self.add_role)
        add_role_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    def create_role_frames(self):
        for idx, role in enumerate(self.roles):
            self.create_role_frame(role, idx)

    def create_role_frame(self, role, idx):
        frame = tk.LabelFrame(self.root, text=role)
        frame.grid(row=idx, column=2, padx=10, pady=10, sticky="nsew")

        entry = tk.Text(frame, wrap=tk.WORD, width=30, height=3)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.role_entries[role] = entry

        send_button = tk.Button(frame, text="发送", command=lambda role=role: self.send_message(role))
        send_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        label = tk.Label(frame, text=role, relief=tk.SOLID)
        label.grid(row=2, column=0, pady=5)
        if role not in ["KP", "Dice", "PL1"]:
            label.bind("<Button-1>", lambda event, role=role, label=label: self.edit_role_name(event, role, label))

    def send_message(self, role):
        message = self.role_entries[role].get("1.0", tk.END).strip()
        if message:
            timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            log = f"{role} {timestamp}\n{message}\n\n"  # 不加引号
            self.chat_log.insert(tk.END, log)
            self.role_entries[role].delete("1.0", tk.END)

    def edit_role_name(self, event, role, label):
        entry = tk.Entry(label, width=10)
        entry.insert(0, role)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        entry.bind("<FocusOut>", lambda event, role=role, entry=entry, label=label: self.update_role_name(event, role, entry, label))

    def update_role_name(self, event, role, entry, label):
        new_name = entry.get().strip()
        if new_name and new_name != role:
            # 更新角色名
            index = self.roles.index(role)
            self.roles[index] = new_name

            # 更新当前角色名
            if self.current_role.get() == role:
                self.current_role.set(new_name)

            entry.grid_forget()
            label.configure(text=new_name)

            # 重新创建角色框架
            for widget in self.root.grid_slaves(column=2):
                widget.grid_forget()

            self.create_role_frames()

    def add_role(self):
        new_role = f"PL{len([role for role in self.roles if role.startswith('PL')]) + 1}"
        self.roles.append(new_role)
        self.create_role_frame(new_role, len(self.roles) - 1)

        # 更新当前角色名
        if new_role == self.current_role.get():
            self.current_role.set(self.roles[0])

        # 重新创建角色框架
        for widget in self.root.grid_slaves(column=2):
            widget.grid_forget()

        self.create_role_frames()

    def delete_role(self):
        if len(self.roles) > 2:
            role_to_delete = self.roles[-1]  # 从最新添加的角色开始删除
            self.roles.remove(role_to_delete)
            del self.role_entries[role_to_delete]

            # 更新当前角色名
            if role_to_delete == self.current_role.get():
                self.current_role.set(self.roles[0])

            # 重新创建角色框架
            for widget in self.root.grid_slaves(column=2):
                widget.grid_forget()

            self.create_role_frames()

    def output_chat_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_log_{timestamp}.txt"
        chat_log_content = self.chat_log.get("1.0", tk.END)
        with open(filename, "w") as file:
            file.write(chat_log_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
