import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        # 1. 입력값 읽어오기
        coil_p = float(entry_coil_price.get())
        core_p = float(entry_core_price.get())
        thick = float(entry_thickness.get())
        
        # 2. 가공비 (인건비 2000 + 소모품 700)
        labor_plus_extra = 2700
        
        # 3. 코일 조합에 따른 중량 설정
        coil_type = var_coil_type.get()
        # 내부/외부(1040+1219) = 8.867kg, 내부/내부(1040+1040) = 8.164kg
        coil_w = 8.867 if coil_type == "내외" else 8.164
        
        # 4. 심재 종류에 따른 계산
        core_type = var_core_type.get()
        cost_core = 0
        
        if core_type == "EPS":
            # EPS는 50T 보드값 기준 비례 계산
            cost_core = (thick / 50) * core_p
        elif core_type == "GW48":
            # 그라스울 48k: 두께(m) * 밀도(48) * 폭(1.219) * kg단가
            cost_core = (thick / 1000) * 48 * 1.219 * core_p
        elif core_type == "GW64":
            # 그라스울 64k: 두께(m) * 밀도(64) * 폭(1.219) * kg단가
            cost_core = (thick / 1000) * 64 * 1.219 * core_p
        else: # 우레탄
            cost_core = (thick / 50) * core_p

        # 5. 최종 합계
        total = (coil_p * coil_w) + cost_core + labor_plus_extra
        
        label_result.config(text=f"{int(total):,} 원")
        
    except ValueError:
        messagebox.showerror("입력 오류", "숫자만 입력해주세요 (소수점 가능)")

# --- GUI 설정 ---
root = tk.Tk()
root.title("WOORI COST SOLVER")
root.geometry("350x550")
root.configure(bg='#1e1e1e') # 다크모드 배경

# 폰트 설정
font_label = ("Arial", 10, "bold")
font_input = ("Arial", 12)

# 입력 필드들
def create_label(text):
    return tk.Label(root, text=text, bg='#1e1e1e', fg='#d4af37', font=font_label)

create_label("\n1. 코일 매입가 (kg당)").pack()
entry_coil_price = tk.Entry(root, font=font_input, justify='center')
entry_coil_price.insert(0, "1100")
entry_coil_price.pack(pady=5)

create_label("2. 심재 종류").pack()
var_core_type = tk.StringVar(value="EPS")
frame_core = tk.Frame(root, bg='#1e1e1e')
frame_core.pack()
tk.Radiobutton(frame_core, text="EPS", variable=var_core_type, value="EPS", bg='#1e1e1e', fg='white', selectcolor='black').pack(side='left')
tk.Radiobutton(frame_core, text="GW48k", variable=var_core_type, value="GW48", bg='#1e1e1e', fg='white', selectcolor='black').pack(side='left')
tk.Radiobutton(frame_core, text="GW64k", variable=var_core_type, value="GW64", bg='#1e1e1e', fg='white', selectcolor='black').pack(side='left')

create_label("3. 심재 단가 (보드값 또는 kg단가)").pack()
entry_core_price = tk.Entry(root, font=font_input, justify='center')
entry_core_price.insert(0, "3650")
entry_core_price.pack(pady=5)

create_label("4. 제품 두께 (T)").pack()
entry_thickness = tk.Entry(root, font=font_input, justify='center')
entry_thickness.insert(0, "150")
entry_thickness.pack(pady=5)

create_label("5. 코일 조합").pack()
var_coil_type = tk.StringVar(value="내외")
frame_coil = tk.Frame(root, bg='#1e1e1e')
frame_coil.pack()
tk.Radiobutton(frame_coil, text="내부/외부", variable=var_coil_type, value="내외", bg='#1e1e1e', fg='white', selectcolor='black').pack(side='left')
tk.Radiobutton(frame_coil, text="내부/내부", variable=var_coil_type, value="내내", bg='#1e1e1e', fg='white', selectcolor='black').pack(side='left')

tk.Label(root, text="", bg='#1e1e1e').pack() # 공백

btn_calc = tk.Button(root, text="계산하기", command=calculate, bg='#d4af37', fg='black', font=("Arial", 12, "bold"), width=20, height=2)
btn_calc.pack(pady=20)

label_result = tk.Label(root, text="0 원", bg='#1e1e1e', fg='#d4af37', font=("Arial", 20, "bold"))
label_result.pack()

root.mainloop()
