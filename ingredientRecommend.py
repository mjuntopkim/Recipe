#레시피 추천 기능 
import tkinter as tk
from tkinter import font, messagebox
import json

from searchIngredient import get_all_ingredients, get_recent_ingredients
from fridge import load_data
from recipe_crawler import get_recipes_from_10000recipe, show_recipe_results

# 레시피 추천 기능 클래스
class IngredientRecommendPage(tk.Toplevel):
    def __init__(self, parent, on_back):
        super().__init__(parent)
        self.title("재료 기반 레시피 추천")
        self.geometry("400x620")
        self.configure(bg="white")
        self.on_back = on_back  # 홈으로 돌아가는 콜백 함수

      
        self.selected_ingredients = []  # 사용자가 선택한 재료
        self.fridge_ingredients = load_data()  # 냉장고에 있는 재료 목록 불러오기
        self.all_ingredients = get_all_ingredients()  # 전체 재료 마스터 목록

        # UI 구성 
        # 상단 타이틀 바 (홈 버튼 + 페이지 이름)
        title_bar = tk.Frame(self, bg="white")
        title_bar.pack(fill="x", pady=10, padx=15)

        home_btn = tk.Button(title_bar, text="🏠", font=("Arial", 14), command=self.on_back,
                             bd=0, bg="white", cursor="hand2")
        home_btn.pack(side="left")

        title_label = tk.Label(title_bar, text="재료 기반 레시피 추천", font=("Malgun Gothic", 16, "bold"), bg="white")
        title_label.pack(side="left", padx=10)

        # 검색창
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Malgun Gothic", 12), width=23)
        search_entry.pack(side="left", padx=(5, 2))

        search_btn = tk.Button(search_frame, text="🔍", font=("Arial", 11), bg="white", command=self.update_search_result)
        search_btn.pack(side="left")

        
        self.result_frame = tk.Frame(self, bg="white")
        self.result_frame.pack(pady=5, fill="both")

        # 냉장고 재료 보기 버튼
        fridge_btn = tk.Button(self, text="🧊 내 냉장고 재료 선택", font=("Malgun Gothic", 11), bg="#f3f3f3",
                               command=self.open_fridge_popup)
        fridge_btn.pack(pady=10)

        # 선택한 재료 타이틀
        selected_title = tk.Label(self, text="선택한 재료", font=("Malgun Gothic", 13, "bold"), bg="white")
        selected_title.pack(pady=(10, 0))

        self.list_frame = tk.Frame(self, bg="white") 
        self.list_frame.pack(pady=5)

        # 추천 실행 버튼
        recommend_btn = tk.Button(self, text="추천 레시피 보기", command=self.recommend,
                                   font=("Malgun Gothic", 13, "bold"), bg="#e0f7fa", width=30)
        recommend_btn.pack(pady=20)

    # 검색 버튼 클릭 시 결과 업데이트
    def update_search_result(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        keyword = self.search_var.get().strip().lower().replace(" ", "")
        if not keyword:
            return

        # 마스터 재료 목록에서 검색어가 포함된 재료 필터링
        matched = [i for i in self.all_ingredients if keyword in i.lower().replace(" ", "")]

        if not matched:
            tk.Label(self.result_frame, text="검색 결과 없음", bg="white", fg="gray").pack()
        else:
            for name in matched[:6]:
                btn = tk.Button(self.result_frame, text=name, bg="#f0f0f0", relief="groove",
                                command=lambda n=name: self.add_to_selected(n))
                btn.pack(padx=10, pady=2, fill="x")

    # 냉장고 재료 목록 팝업 (선택 버튼 포함)
    def open_fridge_popup(self):
        popup = tk.Toplevel(self)
        popup.title("내 냉장고 재료")
        popup.geometry("360x300")
        popup.configure(bg="white")

        outer_frame = tk.Frame(popup, bg="white")
        outer_frame.pack(fill="both", expand=True)

        # 스크롤
        canvas = tk.Canvas(outer_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for item in self.fridge_ingredients:
            name = item.get("name")
            btn = tk.Button(scroll_frame, text=name, font=("Malgun Gothic", 11), bg="#fafafa",
                            relief="solid", width=28,
                            command=lambda n=name: self.add_to_selected(n))
            btn.pack(pady=4, padx=10)

    #선택된 재료 리스트 UI 추가
    def update_selected_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for i, ing in enumerate(self.selected_ingredients):
            frame = tk.Frame(self.list_frame, bg="#f5f5f5")
            frame.pack(fill="x", padx=20, pady=2)
            tk.Label(frame, text=ing, bg="#f5f5f5", font=("Malgun Gothic", 11)).pack(side="left")
            tk.Button(frame, text="❌", bg="#f5f5f5", command=lambda i=i: self.remove_selected(i)).pack(side="right")

    # 재료 추가
    def add_to_selected(self, name):
        if name not in self.selected_ingredients:
            self.selected_ingredients.append(name)
            self.update_selected_list()

    # 재료 삭제
    def remove_selected(self, index):
        if 0 <= index < len(self.selected_ingredients):
            del self.selected_ingredients[index]
            self.update_selected_list()

    # 레시피 추천 실행
    def recommend(self):
        if not self.selected_ingredients:
            messagebox.showinfo("알림", "재료를 1개 이상 선택해주세요")
            return

        # 선택한 재료 조합해 검색
        keywords = "+".join(self.selected_ingredients)
        recipes = get_recipes_from_10000recipe(keywords)

        if not recipes:
            messagebox.showinfo("검색 결과", "해당 재료들로 추천할 레시피를 찾지 못했습니다.")
            return

        # 일치하는 재료 수를 기준으로 정렬
        def count_matches(recipe):
            text = recipe.get("title", "") + recipe.get("ingredients", "")
            return sum(1 for ingr in self.selected_ingredients if ingr in text)

        sorted_recipes = sorted(recipes, key=count_matches, reverse=True)
        show_recipe_results(sorted_recipes)



if __name__ == "__main__":
    def go_back():
        print("뒤로 가기")

    root = tk.Tk()
    root.withdraw()
    page = IngredientRecommendPage(root, on_back=go_back)
    root.mainloop()
