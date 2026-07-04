#!/usr/bin/env python3
"""
Lucky - 本地 API 密钥管理程序
黑白配色 / 简洁风格 / 半角图标
"""

import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


def resource_path(filename):
    """获取资源文件路径（兼容 PyInstaller 打包）"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

# ── 数据层 ──────────────────────────────────────────────────────────────────

DATA_DIR = Path.home() / ".luck"
DATA_FILE = DATA_DIR / "keys.json"


def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_keys() -> list[dict]:
    ensure_data_file()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return []


def save_keys(keys: list[dict]):
    ensure_data_file()
    DATA_FILE.write_text(
        json.dumps(keys, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ── 弹窗表单 ────────────────────────────────────────────────────────────────

class KeyFormDialog(tk.Toplevel):
    """添加 / 编辑密钥弹窗"""

    def __init__(self, parent, title="添加", data=None):
        super().__init__(parent)
        self.title(f"[ {title} ]")
        self.geometry("460x340")
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.data = data or {}
        self.show_key = False

        self.name_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.key_var = tk.StringVar()

        self._build_ui()
        self._center()

        if self.data:
            self.name_var.set(self.data.get("name", ""))
            self.url_var.set(self.data.get("api_url", ""))
            self.key_var.set(self.data.get("api_key", ""))

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.bind("<Escape>", lambda e: self._cancel())
        self.bind("<Return>", lambda e: self._confirm())

        try:
            self.iconbitmap(resource_path("lucky.ico"))
        except Exception:
            pass

        self.name_entry.focus_set()

    def _build_ui(self):
        font = ("Microsoft YaHei", 10)
        label_font = ("Microsoft YaHei", 9)

        # AI 名称
        tk.Label(
            self, text="AI  名称", font=label_font,
            fg="#000", bg="#ffffff", anchor="w"
        ).pack(fill="x", padx=24, pady=(24, 4))

        self.name_entry = tk.Entry(
            self, textvariable=self.name_var,
            font=font, fg="#000", bg="#ffffff",
            insertbackground="#000", relief="solid", bd=1
        )
        self.name_entry.pack(fill="x", padx=24, ipady=6)

        # 接口地址
        tk.Label(
            self, text="接口地址", font=label_font,
            fg="#000", bg="#ffffff", anchor="w"
        ).pack(fill="x", padx=24, pady=(16, 4))

        self.url_entry = tk.Entry(
            self, textvariable=self.url_var,
            font=font, fg="#000", bg="#ffffff",
            insertbackground="#000", relief="solid", bd=1
        )
        self.url_entry.pack(fill="x", padx=24, ipady=6)

        # 接口密钥
        tk.Label(
            self, text="接口密钥", font=label_font,
            fg="#000", bg="#ffffff", anchor="w"
        ).pack(fill="x", padx=24, pady=(16, 4))

        self.key_entry = tk.Entry(
            self, textvariable=self.key_var,
            font=font, fg="#000", bg="#ffffff",
            insertbackground="#000", relief="solid", bd=1,
            show="•"
        )
        self.key_entry.pack(fill="x", padx=24, ipady=6)

        # 显示 / 隐藏
        self.toggle_btn = tk.Label(
            self, text="[ 显示 ]", font=label_font,
            fg="#666", bg="#ffffff", cursor="hand2"
        )
        self.toggle_btn.pack(anchor="e", padx=24, pady=4)
        self.toggle_btn.bind("<Button-1>", self._toggle_key)

        # Buttons
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(fill="x", padx=24, pady=(16, 20))

        btn_font = ("Microsoft YaHei", 9, "bold")

        cancel_btn = tk.Button(
            btn_frame, text="取消", font=btn_font,
            fg="#000", bg="#ffffff",
            activebackground="#000", activeforeground="#fff",
            relief="solid", bd=1, cursor="hand2",
            command=self._cancel, width=10
        )
        cancel_btn.pack(side="right", padx=(8, 0))

        confirm_btn = tk.Button(
            btn_frame, text="确认", font=btn_font,
            fg="#ffffff", bg="#000000",
            activebackground="#333", activeforeground="#fff",
            relief="flat", cursor="hand2",
            command=self._confirm, width=10
        )
        confirm_btn.pack(side="right")

    def _toggle_key(self, event):
        self.show_key = not self.show_key
        self.key_entry.configure(show="" if self.show_key else "•")
        self.toggle_btn.configure(
            text="[ 隐藏 ]" if self.show_key else "[ 显示 ]"
        )

    def _confirm(self):
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()
        key = self.key_var.get().strip()

        if not name:
            self.name_entry.focus_set()
            return
        if not key:
            self.key_entry.focus_set()
            return

        self.result = {"name": name, "api_url": url, "api_key": key}
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")


# ── 主窗口 ──────────────────────────────────────────────────────────────────

class LuckApp:
    """Lucky 主应用"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lucky")
        self.root.geometry("820x520")
        self.root.minsize(600, 360)
        self.root.configure(bg="#ffffff")

        # 设置窗口图标
        try:
            self.root.iconbitmap(resource_path("lucky.ico"))
        except Exception:
            pass

        self.keys: list[dict] = []
        self.filtered: list[dict] = []
        self.visibility = "masked"

        self._build_ui()
        self._load_and_refresh()

        self.root.bind("<Control-n>", lambda e: self._add_key())
        self.root.bind("<Control-e>", lambda e: self._edit_key())
        self.root.bind("<Control-d>", lambda e: self._delete_key())
        self.root.bind("<Control-c>", lambda e: self._copy_key())
        self.root.bind("<Escape>", lambda e: self._clear_search())

    def _build_ui(self):
        font = ("Microsoft YaHei", 10)
        font_sm = ("Microsoft YaHei", 9)
        font_title = ("Microsoft YaHei", 16, "bold")
        font_btn = ("Microsoft YaHei", 9, "bold")

        # ── 顶栏 ──
        header = tk.Frame(self.root, bg="#ffffff")
        header.pack(fill="x", padx=16, pady=(16, 0))

        tk.Label(
            header, text="Lucky", font=font_title,
            fg="#000", bg="#ffffff"
        ).pack(side="left")

        tk.Label(
            header, text="密钥管理", font=font_sm,
            fg="#999", bg="#ffffff"
        ).pack(side="left", padx=(12, 0), anchor="s", pady=(0, 4))

        # ── 搜索栏 ──
        search_frame = tk.Frame(self.root, bg="#ffffff")
        search_frame.pack(fill="x", padx=16, pady=(12, 0))

        tk.Label(
            search_frame, text="/",
            font=("Consolas", 12, "bold"),
            fg="#999", bg="#ffffff"
        ).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=font, fg="#000", bg="#ffffff",
            insertbackground="#000", relief="solid", bd=1
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)

        tk.Label(
            search_frame, text="[Esc] 清除",
            font=("Microsoft YaHei", 8), fg="#ccc", bg="#ffffff"
        ).pack(side="right", padx=(8, 0))

        # ── 分隔线 ──
        tk.Frame(self.root, bg="#000", height=1).pack(fill="x", padx=16, pady=(12, 0))

        # ── 表格 ──
        table_frame = tk.Frame(self.root, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Lucky.Treeview",
            font=font,
            background="#ffffff",
            foreground="#000000",
            fieldbackground="#ffffff",
            borderwidth=0,
            rowheight=32,
        )
        style.configure(
            "Lucky.Treeview.Heading",
            font=font_btn,
            background="#f5f5f5",
            foreground="#000000",
            relief="flat",
        )
        style.map(
            "Lucky.Treeview",
            background=[("selected", "#000000")],
            foreground=[("selected", "#ffffff")],
        )
        style.map(
            "Lucky.Treeview.Heading",
            background=[("active", "#e0e0e0")],
        )

        columns = ("name", "api_url", "api_key")
        self.tree = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", style="Lucky.Treeview",
            selectmode="browse"
        )

        self.tree.heading("name", text="AI 名称", anchor="w")
        self.tree.heading("api_url", text="接口地址", anchor="w")
        self.tree.heading("api_key", text="接口密钥", anchor="w")

        self.tree.column("name", width=160, minwidth=100)
        self.tree.column("api_url", width=320, minwidth=150)
        self.tree.column("api_key", width=280, minwidth=120)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda e: self._edit_key())

        # 空状态
        self.empty_label = tk.Label(
            table_frame,
            text="暂无密钥  -  点击 [+] 添加",
            font=("Microsoft YaHei", 10), fg="#ccc", bg="#ffffff"
        )

        # ── 底栏 ──
        tk.Frame(self.root, bg="#000", height=1).pack(fill="x", padx=16, pady=(8, 0))

        bottom = tk.Frame(self.root, bg="#ffffff")
        bottom.pack(fill="x", padx=16, pady=(10, 14))

        btn_cfg = dict(
            font=font_btn, cursor="hand2",
            relief="solid", bd=1, width=8
        )

        tk.Button(
            bottom, text="+  添加",
            fg="#fff", bg="#000",
            activebackground="#333", activeforeground="#fff",
            command=self._add_key, **btn_cfg
        ).pack(side="left")

        tk.Button(
            bottom, text="*  编辑",
            fg="#000", bg="#fff",
            activebackground="#000", activeforeground="#fff",
            command=self._edit_key, **btn_cfg
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            bottom, text="-  删除",
            fg="#000", bg="#fff",
            activebackground="#000", activeforeground="#fff",
            command=self._delete_key, **btn_cfg
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            bottom, text=">  复制",
            fg="#000", bg="#fff",
            activebackground="#000", activeforeground="#fff",
            command=self._copy_key, **btn_cfg
        ).pack(side="left", padx=(8, 0))

        # 右侧
        self.vis_btn = tk.Button(
            bottom, text="[ 显示全部 ]",
            font=font_sm, fg="#666", bg="#fff",
            activebackground="#000", activeforeground="#fff",
            relief="flat", cursor="hand2",
            command=self._toggle_visibility
        )
        self.vis_btn.pack(side="right")

        self.count_label = tk.Label(
            bottom, text="0 条密钥",
            font=font_sm, fg="#999", bg="#ffffff"
        )
        self.count_label.pack(side="right", padx=(0, 16))

    # ── 数据 ──

    def _load_and_refresh(self):
        self.keys = load_keys()
        self._apply_filter()

    def _save(self):
        save_keys(self.keys)

    def _apply_filter(self):
        query = self.search_var.get().strip().lower()
        if query:
            self.filtered = [
                k for k in self.keys
                if query in k.get("name", "").lower()
                or query in k.get("api_url", "").lower()
            ]
        else:
            self.filtered = list(self.keys)
        self._refresh_tree()

    def _refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.filtered:
            key_display = self._mask_key(entry["api_key"])
            self.tree.insert(
                "", "end",
                values=(entry["name"], entry.get("api_url", ""), key_display)
            )

        if not self.filtered:
            self.tree.pack_forget()
            self.empty_label.pack(expand=True)
        else:
            self.empty_label.pack_forget()
            if not self.tree.winfo_ismapped():
                self.tree.pack(side="left", fill="both", expand=True)

        total = len(self.keys)
        shown = len(self.filtered)
        if shown < total:
            self.count_label.configure(text=f"{shown} / {total} 条密钥")
        else:
            self.count_label.configure(text=f"{total} 条密钥")

    def _mask_key(self, key: str) -> str:
        if self.visibility == "visible":
            return key
        if len(key) <= 6:
            return "•" * len(key)
        return key[:3] + "•" * (len(key) - 6) + key[-3:]

    # ── 操作 ──

    def _add_key(self):
        dialog = KeyFormDialog(self.root, title="添加")
        self.root.wait_window(dialog)
        if dialog.result:
            self.keys.append(dialog.result)
            self._save()
            self._apply_filter()

    def _edit_key(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        if idx >= len(self.filtered):
            return

        entry = self.filtered[idx]
        real_idx = self.keys.index(entry)

        dialog = KeyFormDialog(self.root, title="编辑", data=entry)
        self.root.wait_window(dialog)
        if dialog.result:
            self.keys[real_idx] = dialog.result
            self._save()
            self._apply_filter()

    def _delete_key(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        if idx >= len(self.filtered):
            return

        entry = self.filtered[idx]
        name = entry["name"]

        if messagebox.askyesno("删除", f"确认删除「{name}」？", parent=self.root):
            real_idx = self.keys.index(entry)
            self.keys.pop(real_idx)
            self._save()
            self._apply_filter()

    def _copy_key(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        if idx >= len(self.filtered):
            return

        entry = self.filtered[idx]
        self.root.clipboard_clear()
        self.root.clipboard_append(entry["api_key"])

        self.count_label.configure(text="> 已复制！")
        self.root.after(1500, lambda: self._apply_filter())

    def _toggle_visibility(self):
        if self.visibility == "masked":
            self.visibility = "visible"
            self.vis_btn.configure(text="[ 隐藏全部 ]")
        else:
            self.visibility = "masked"
            self.vis_btn.configure(text="[ 显示全部 ]")
        self._apply_filter()

    def _clear_search(self):
        self.search_var.set("")

    def run(self):
        self.root.mainloop()


# ── 入口 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = LuckApp()
    app.run()
