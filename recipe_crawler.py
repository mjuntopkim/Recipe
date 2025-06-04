#만개의레시피 사이트 크롤링
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import messagebox

#주어진 keyword로 10000recipe 사이트에서 레시피 크롤링
def get_recipes_from_10000recipe(keyword, max_results=6):
    url = f"https://www.10000recipe.com/recipe/list.html?q={keyword}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print("검색 실패:", e)
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for card in soup.select(".common_sp_list_ul li")[:max_results]:
        try:
            link = "https://www.10000recipe.com" + card.select_one("a")["href"]
            title = card.select_one(".common_sp_caption_tit").get_text(strip=True)
            img_url = card.select_one("img")["src"]
            results.append({"title": title, "link": link, "img": img_url})
        except:
            continue
    return results

# 레시피 리스트를 팝업창에 이미지와 함께 출력
def show_recipe_results(recipes):
    popup = tk.Toplevel()
    popup.title("레시피 추천 결과")
    popup.geometry("460x630")
    popup.configure(bg="white")
    canvas = tk.Canvas(popup, bg="white", highlightthickness=0)
    canvas.pack(expand=True, fill="both")

    y = 20
    imgs = []
    for rec in recipes:
        # 이미지 표시
        try:
            img_res = requests.get(rec["img"], timeout=5)
            pil_img = Image.open(io.BytesIO(img_res.content)).resize((76, 76))
            tk_img = ImageTk.PhotoImage(pil_img)
            imgs.append(tk_img)
            img_label = tk.Label(canvas, image=tk_img, bg="white")
            img_label.image = tk_img  # Prevent GC
            img_label.place(x=30, y=y)
        except:
            img_label = tk.Label(canvas, width=76, height=5, text="[이미지 없음]", bg="#eee")
            img_label.place(x=30, y=y)
        # 레시피 제목 및 링크
        tk.Label(canvas, text=rec["title"], bg="white", anchor="w", font=("Malgun Gothic", 13, "bold"),
                 wraplength=250, justify="left").place(x=120, y=y+13)
        
        # '자세히' 버튼 클릭 시 웹사이트로 연결
        def open_url(url=rec["link"]):
            import webbrowser
            webbrowser.open(url)
        tk.Button(canvas, text="자세히", command=open_url, bg="#f5f5ff", width=7).place(x=350, y=y+22)
        y += 96
