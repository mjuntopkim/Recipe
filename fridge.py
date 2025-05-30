# 나만의 냉장고 기능 

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from searchIngredient import open_search_window

ingredient_list = [] # 냉장고에 들어있는 재료 리스트
DATA_FILE = "ingredients.json"  # 냉장고 재료 정보가 저장될 JSON 파일

# 재료 데이터를 파일에 저장
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredient_list, f, ensure_ascii=False, indent=2)

# 재료 파일에서 불러오기
def load_data():
    global ingredient_list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            ingredient_list = json.load(f)
    else:
        ingredient_list = []
    return ingredient_list

# 나만의 냉장고창
def open_fridge_window(main_root, update_warning_label_callback):
    main_root.withdraw()

    fridge_win = tk.Toplevel()
    fridge_win.title("나만의 냉장고")
    fridge_win.geometry("400x500")
    fridge_win.configure(bg="white")

    title_font = ("Malgun Gothic", 18, "bold")

    # 상단바
    top_bar = tk.Frame(fridge_win, bg="white")
    top_bar.pack(fill="x", pady=10, padx=15)

    def go_home():
        save_data()
        update_warning_label_callback(ingredient_list)
        fridge_win.destroy()
        main_root.deiconify()

    tk.Button(top_bar, text="🏠", font=("Arial", 14),
              command=go_home, bd=0, bg="white", cursor="hand2").pack(side="left")

    tk.Label(top_bar, text="나만의 냉장고", font=title_font, bg="white").pack(side="left", padx=10)
    # 재료 추가 버튼튼
    tk.Button(top_bar, text="+", font=("Arial", 14), width=3,
              command=lambda: open_search_window(add_ingredient_to_fridge),
              bg="#f0f0f0", relief="flat", cursor="hand2").pack(side="right")

    # 재료 리스트 영역 (스크롤 가능하게)
    container_frame = tk.Frame(fridge_win, bg="white")
    container_frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(container_frame, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas, bg="white")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 마우스 휠 스크롤 지원 
    def _on_mousewheel(event):
        if os.name == 'nt':
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            canvas.yview_scroll(int(-1*event.delta), "units")
    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units")) # Linux up
    scrollable_frame.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux down

    # 유통기한 색상 (남은 날짜에 따라 다르게)
    def color_by_expiry(expiry):
        try:
            today = datetime.today().date()
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
            diff = (expiry_date - today).days
            if diff <= 1:
                return "#ffd6d6"  # 연빨강
            elif diff <= 3:
                return "#fff0c6"  # 연주황
            elif diff <= 7:
                return "#fffbe0"  # 연노랑
            else:
                return "#f6f6f6"  # 기본
        except:
            return "#f6f6f6"
        
    #재료 리스트 UI 다시 그리기
    def rebuild_ingredient_ui():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for item in ingredient_list:
            cont_color = color_by_expiry(item["expiry"])
            container = tk.Frame(scrollable_frame, bg=cont_color, bd=2, relief="groove", padx=10, pady=5)
            container.pack(fill="x", pady=4)

            row = tk.Frame(container, bg=cont_color)
            row.pack(fill="x")

            #재료 이름
            tk.Label(row, text=item["name"], width=12, anchor="w", bg=cont_color, font=("Arial", 12, "bold")).pack(side="left")

            expiry_var = tk.StringVar(value=item["expiry"])
            expiry_entry = tk.Entry(row, textvariable=expiry_var, width=12)
            expiry_entry.pack(side="left", padx=5)

            def update_expiry(var=expiry_var, item=item):
                try:
                    datetime.strptime(var.get(), "%Y-%m-%d")
                    item["expiry"] = var.get()
                except ValueError:
                    expiry_var.set(item["expiry"])

            expiry_entry.bind("<FocusOut>", lambda e, var=expiry_var, item=item: update_expiry(var, item))

            # 수량 증가,감소 버튼
            count_var = tk.IntVar(value=item["count"])

            def increase(i=item, cv=count_var):
                cv.set(cv.get() + 1)
                i["count"] = cv.get()

            def decrease(i=item, cv=count_var):
                if cv.get() > 0:
                    cv.set(cv.get() - 1)
                    i["count"] = cv.get()

            tk.Button(row, text="-", command=decrease, width=2).pack(side="left")
            tk.Label(row, textvariable=count_var, width=3, bg=cont_color).pack(side="left")
            tk.Button(row, text="+", command=increase, width=2).pack(side="left")

            def delete_ingredient(idx=ingredient_list.index(item), name=item["name"]):
                if messagebox.askokcancel("삭제 확인", f"'{name}'을(를) 정말 삭제할까요?"):
                    ingredient_list.pop(idx)
                    rebuild_ingredient_ui()

            del_btn = tk.Button(row, text="삭제", width=5, bg="#fafafa", command=delete_ingredient)
            del_btn.pack(side="right", padx=4)
    #쟈료 추가 콜백 함수(searchIngredient에서 사용)
    def add_ingredient_to_fridge(name, expiry):
        try:
            datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError:
            return

        for item in ingredient_list:
            if item["name"] == name and item["expiry"] == expiry:
                item["count"] += 1
                rebuild_ingredient_ui()
                return

        ingredient_list.append({
            "name": name,
            "expiry": expiry,
            "count": 1
        })
        rebuild_ingredient_ui()

    load_data()
    rebuild_ingredient_ui()
