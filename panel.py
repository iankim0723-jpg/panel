import tkinter as tk
from tkinter import ttk

class WooriCostSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("WOORI COST SOLVER v1.0")
        self.root.geometry("400x700")
        self.root.configure(bg='#121212')  # 다크 모드 배경

        # 기본값 설정
        self.labor_cost = 2000
        self.extra_cost = 700
        
        self.setup_ui()

    def setup_ui(self):
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#121212", foreground="#D4AF37", font=('Apple SD Gothic Neo', 10))
        
        # 타이틀
        tk.Label(self.root, text="WOORI COST SOLVER", bg='#121212', fg='#D4AF37', 
                 font=('Arial', 18, 'bold'), pady=20).pack()

        # 입력 영역 컨테이너
        container = tk.Frame(self.root, bg='#121212', padx=30)
        container.pack(fill='both', expand=True)

        # 1. 코일 매입가
        tk.Label(container, text="코일 매입가 (kg당)", bg='#121212', fg='#888').pack(anchor='w')
        self.ent_coil_price = tk.Entry(container, bg='#2A2A2A', fg='white', insertbackground='white', borderwidth=0)
        self.ent_coil_price.insert(0, "1100")
        self.ent_coil_price.pack(fill='x', pady=(0, 15), ipady=8)

        # 2. 심재 종류 선택
        tk.Label(container, text="심재 종류 선택", bg='#121212', fg='#888').pack(anchor='w')
        self.var_core = tk.StringVar(value="EPS")
        core_combo = ttk.Combobox(container, textvariable=self.var_core, values=["EPS", "그라스울(48k)", "그라스울(64k)", "우레탄"])
        core_combo.pack(fill='x', pady=(0, 15), ipady=5)

        # 3. 심재 매입 단가 (EPS 보드값 or GW kg가)
        self.lbl_core_price = tk.Label(container, text="심재 단가 (EPS 50T 보드값)", bg='#121212', fg='#888')
        self.lbl_core_price.pack(anchor='w')
        self.ent_core_price = tk.Entry(container, bg='#2A2A2A', fg='white', insertbackground='white', borderwidth=0)
        self.ent_core_price.insert(0, "3650")
        self.ent_core_price.pack(fill='x', pady=(0, 15), ipady=8)

        # 4. 두께 (T)
        tk.Label(container, text="제품 두께 (T 입력)", bg='#121212', fg='#888').pack(anchor='w')
        self.ent_thickness = tk.Entry(container, bg='#2A2A2A', fg='white', insertbackground='white', borderwidth=0)
        self.ent_thickness.insert(0, "150")
        self.ent_thickness.pack(fill='x', pady=(0, 15), ipady=8)

        # 5. 코일 조합
        tk.Label(container, text="코일 조합 선택", bg='#121212', fg='#888').pack(anchor='w')
        self.var_coil_type = tk.StringVar(value="내부/외부 (1040/1219)")
        coil_combo = ttk.Combobox(container, textvariable=self.var_coil_type, 
                                  values=["내부/외부 (1040/1219)", "내부/내부 (1040/1040)"])
        coil_combo.pack(fill='x', pady=(0, 20), ipady=5)

        # 계산 버튼
        calc_btn = tk.Button(container, text="RUN CALCULATION", bg='#D4AF37', fg='black', 
                             font=('Arial', 12, 'bold'), borderwidth=0, command=self.calculate)
        calc_btn.pack(fill='x', ipady=15)

        # 결과창
        self.res_frame = tk.Frame(container, bg='#000000', pady=20, mt=20)
        self.res_frame.pack(fill='x', pady=20)
        tk.Label(self.res_frame, text="ESTIMATED COST (1M)", bg='#000000', fg='#888', font=(10)).pack()
        self.lbl_result = tk.Label(self.res_frame, text="0원", bg='#000000', fg='#D4AF37', font=('Courier', 24, 'bold'))
        self.lbl_result.pack()

    def calculate(self):
        try:
            coil_p = float(self.ent_coil_price.get())
            core_p = float(self.ent_core_price.get())
            thick = float(self.ent_thickness.get())
            core_type = self.var_core.get()
            coil_type = self.var_coil_type.get()

            # 코일 중량 결정
            coil_w = 8.867 if "외부" in coil_type else 8.164
            
            # 1. 코일비
            cost_coil = coil_p * coil_w
            
            # 2. 심재비
            cost_core = 0
            if core_type == "EPS":
                cost_core = (thick / 50) * core_p
            elif "그라스울" in core_type:
                density = 48 if "48k" in core_type else 64
                cost_core = (thick / 1000) * density * 1.219 * core_p
            elif core_type == "우레탄":
                cost_core = (thick / 50) * core_p

            # 3. 가공비
            total = cost_coil + cost_core + self.labor_cost + self.extra_cost
            
            self.lbl_result.config(text=f"{int(total):,}원")
        except ValueError:
            self.lbl_result.config(text="입력 오류")

if __name__ == "__main__":
    root = tk.Tk()
    app = WooriCostSolver(root)
    root.mainloop()
