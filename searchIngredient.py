import tkinter as tk
from tkinter import font, messagebox
import json
import os
from datetime import datetime
import os
import tkinter as tk
from tkinter import font, messagebox
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 위치
MASTER_FILE = os.path.join(BASE_DIR, "ingredients_master.json")
DATA_FILE = os.path.join(BASE_DIR, "ingredients.json")


def get_recent_ingredients(max_count=9):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception:
            return []

    seen = set()
    result = []
    for item in reversed(data):
        name = item.get("name")
        if name and name not in seen:
            result.append(name)
            seen.add(name)
        if len(result) == max_count:
            break
    return list(reversed(result))

def get_all_ingredients():
    if not os.path.exists(MASTER_FILE):
        return []
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception as e:
            print("ingredients_master.json 로딩 오류:", e)
            return []

def open_search_window(add_callback):
    search_win = tk.Toplevel()
    search_win.title("재료 검색")
    search_win.geometry("370x440")
    search_win.configure(bg="white")

    entry_font = font.Font(family="Malgun Gothic", size=12)
    tag_font = font.Font(family="Malgun Gothic", size=13, weight="bold")

    top_frame = tk.Frame(search_win, bg="white")
    top_frame.pack(fill="x", pady=12, padx=12)

    def go_back():
        search_win.destroy()

    back_btn = tk.Button(top_frame, text="←", command=go_back, font=("Arial", 13), bd=0, bg="white",
                         activebackground="#f0f0f0", cursor="hand2")
    back_btn.pack(side="left", padx=(0, 6))

    search_var = tk.StringVar()
    entry = tk.Entry(top_frame, textvariable=search_var, font=entry_font, relief="solid", fg="#bbb", width=23, bd=1)
    entry.insert(0, "재료를 검색하세요")
    entry.pack(side="left", ipady=5, padx=(0, 2))

    def clear_placeholder(event):
        if entry.get() == "재료를 검색하세요":
            entry.delete(0, tk.END)
            entry.config(fg="#222")

    def add_placeholder(event):
        if not entry.get():
            entry.insert(0, "재료를 검색하세요")
            entry.config(fg="#bbb")

    entry.bind("<FocusIn>", clear_placeholder)
    entry.bind("<FocusOut>", add_placeholder)

    search_icon = tk.Label(top_frame, text="🔍", font=("Arial", 14), bg="white")
    search_icon.pack(side="left", padx=(2, 0))

    all_ingredients = get_all_ingredients()
    grid_frame = tk.Frame(search_win, bg="white")
    grid_frame.pack(expand=True, fill="both", pady=(15, 0))

    btn_bg = "#f9fafb"
    btn_fg = "#222"
    btn_active_bg = "#e6f0fc"

    def on_click_ingr(name):
        popup = tk.Toplevel(search_win)
        popup.title("유통기한 입력")
        popup.geometry("250x120")
        popup.configure(bg="white")

        label = tk.Label(popup, text=f"[{name}] 유통기한(YYYY-MM-DD):", bg="white")
        label.pack(pady=(15, 5))
        expiry_entry = tk.Entry(popup)
        expiry_entry.pack()

        def submit():
            expiry = expiry_entry.get().strip()
            if not expiry:
                messagebox.showwarning("입력오류", "유통기한을 입력하세요.")
                return
            try:
                datetime.strptime(expiry, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("입력오류", "YYYY-MM-DD 형식으로 입력하세요.")
                return
            add_callback(name, expiry)
            popup.destroy()
            search_win.destroy()

        submit_btn = tk.Button(popup, text="추가", command=submit)
        submit_btn.pack(pady=10)

    def show_ingredients(ingredients):
        for widget in grid_frame.winfo_children():
            widget.destroy()

        if not ingredients:
            tk.Label(grid_frame, text="검색 결과가 없습니다.", bg="white", fg="#999", font=tag_font).pack(pady=30)
            return

        max_col = 3
        row = col = 0
        for ingr in ingredients:
            tag = tk.Label(grid_frame, text=ingr, font=tag_font, bg=btn_bg, fg=btn_fg,
                           width=9, height=2, bd=0, relief="solid", cursor="hand2")
            tag.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            tag.bind("<Button-1>", lambda e, ingr=ingr: on_click_ingr(ingr))
            tag.bind("<Enter>", lambda e, t=tag: t.config(bg=btn_active_bg))
            tag.bind("<Leave>", lambda e, t=tag: t.config(bg=btn_bg))

            col += 1
            if col == max_col:
                col = 0
                row += 1
        for c in range(max_col):
            grid_frame.grid_columnconfigure(c, weight=1)

    def update_search_results(*args):
        keyword = search_var.get().strip()
        if not keyword or keyword == "재료를 검색하세요":
            show_ingredients(get_recent_ingredients())
        else:
            filtered = [i for i in all_ingredients if keyword in i]
            show_ingredients(filtered)

    search_var.trace_add("write", update_search_results)
    show_ingredients(get_recent_ingredients())

    search_win.mainloop()

if __name__ == "__main__":
    def dummy(name, expiry):
        print(f"선택됨: {name}, {expiry}")
    open_search_window(dummy)
