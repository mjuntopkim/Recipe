import tkinter as tk
from tkinter import font, messagebox
from datetime import datetime
from fridge import open_fridge_window, load_data
from recipe_crawler import get_recipes_from_10000recipe, show_recipe_results
from ingredientRecommend import IngredientRecommendPage

# 유통기한 임박 알림 재료 표시
def update_warning_label(label, ingredients):
    today = datetime.today().date()
    expiring_soon = []
    for item in ingredients:
        try:
            expiry = datetime.strptime(item['expiry'], "%Y-%m-%d").date()
            diff = (expiry - today).days
            if 0 <= diff <= 7:
                expiring_soon.append((diff, item['name']))
        except:
            continue
    expiring_soon.sort()
    if expiring_soon:
        warning_text = "\n".join([f"⚠️ D-{d} {n}" for d, n in expiring_soon[:3]])
        label.config(text=warning_text)
    else:
        label.config(text="⚠️ 유통기한이 임박한 재료가 없습니다")

# 매인 창 생성 
def create_main_window():
    root = tk.Tk()
    root.title("레시피 추천 및 냉장고 관리")
    root.geometry("400x550")
    root.minsize(350, 500)
    root.configure(bg="white")

    v_gap = 18

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=0)
    root.grid_columnconfigure(0, weight=1)

    # 타이틀(타원형)
    title_canvas = tk.Canvas(root, width=260, height=60, bg="white", highlightthickness=0)
    title_canvas.create_oval(5, 5, 255, 55, fill="#f9f9f9", outline="#dcdcdc")

    # 텍스트 중앙 위치 조정 
    title_canvas.create_text(130, 30, text="🍽 My Recipe Mate", font=("Helvetica", 17, "bold"), fill="#333")

    title_canvas.grid(row=0, column=0, pady=(20, 5), sticky="n")

    # 요리명 검색창 
    search_frame = tk.Frame(root, bg="white")
    search_frame.grid(row=1, column=0, pady=(0, v_gap), sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    #검색 실행 함수 
    def on_recommend():
        keyword = search_entry.get().strip()
        if not keyword or keyword == "요리명 입력하세요":
            messagebox.showwarning("검색어 입력", "요리명을 입력하세요!")
            return
        recipes = get_recipes_from_10000recipe(keyword)
        if not recipes:
            messagebox.showinfo("검색 결과", "관련 레시피를 찾지 못했습니다.")
            return
        show_recipe_results(recipes)

    search_icon = tk.Button(search_frame, text="🔍", font=("Arial", 17), bg="white", bd=0, cursor="hand2", command=on_recommend, activebackground="#e8e8e8")
    search_icon.grid(row=0, column=0, padx=(8, 3), pady=1, sticky="w")

    search_entry = tk.Entry(search_frame, font=("Malgun Gothic", 13), relief="flat", fg="#bbb")
    search_entry.insert(0, "요리명 입력하세요")
    search_entry.grid(row=0, column=1, sticky="ew", ipadx=4, ipady=3, padx=(3, 10))

    def clear_placeholder(event):
        if search_entry.get() == "요리명 입력하세요":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="#222")

    def add_placeholder(event):
        if not search_entry.get():
            search_entry.insert(0, "요리명 입력하세요")
            search_entry.config(fg="#bbb")

    search_entry.bind("<FocusIn>", clear_placeholder)
    search_entry.bind("<FocusOut>", add_placeholder)
    search_entry.bind("<Return>", lambda e: on_recommend())

    # 기능 카드(레시피 추천, 냉장고 보기)
    card_frame = tk.Frame(root, bg="white")
    card_frame.grid(row=3, column=0, pady=(0,0), padx=14, sticky="nsew")
    card_frame.grid_rowconfigure(0, weight=1)
    card_frame.grid_columnconfigure(0, weight=1, uniform="cards")
    card_frame.grid_columnconfigure(1, weight=1, uniform="cards")
    
    
    recipe_card = tk.Frame(card_frame, bg="#f0f8ff", bd=0, highlightthickness=1, highlightbackground="#b0c4de", relief="ridge")
    recipe_card.grid(row=0, column=0, padx=(0,8), sticky="nsew")
    recipe_card.grid_propagate(False)
    recipe_icon = tk.Label(recipe_card, text="📋", bg="#f0f8ff", font=("Arial", 45))
    recipe_icon.pack(pady=(25, 5))
    recipe_label = tk.Label(recipe_card, text="레시피 추천", bg="#f0f8ff", font=("Malgun Gothic", 17, "bold"))
    recipe_label.pack()

    fridge_card = tk.Frame(card_frame, bg="#f0f8ff", bd=0, highlightthickness=1, highlightbackground="#b0c4de", relief="ridge")
    fridge_card.grid(row=0, column=1, padx=(8,0), sticky="nsew")
    fridge_card.grid_propagate(False)
    fridge_icon = tk.Label(fridge_card, text="🧊", bg="#f0f8ff", font=("Arial", 45))
    fridge_icon.pack(pady=(25, 5))
    fridge_label = tk.Label(fridge_card, text="나만의 냉장고", bg="#f0f8ff", font=("Malgun Gothic", 17, "bold"))
    fridge_label.pack()

    def open_fridge_action(event=None):
        open_fridge_window(root, lambda data: update_warning_label(warning_label, data))

    def open_recommend_page(event=None):
        IngredientRecommendPage(root, on_back=root.deiconify)

    for widget in [recipe_card, recipe_icon, recipe_label]:
        widget.bind("<Button-1>", open_recommend_page)
    for widget in [fridge_card, fridge_icon, fridge_label]:
        widget.bind("<Button-1>", open_fridge_action)

    warning_label = tk.Label(
        root, text="", font=("Malgun Gothic", 15, "bold"),
        fg="#d2691e", bg="white", anchor="w", padx=10, pady=10,
        relief="ridge", bd=1, width=34, justify="left"
    )
    warning_label.grid(row=4, column=0, padx=20, pady=(10, 15), sticky="sew")

    ingredients = load_data()
    update_warning_label(warning_label, ingredients)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()