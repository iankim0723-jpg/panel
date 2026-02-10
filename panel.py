import streamlit as st

# 페이지 설정 (홀덤 솔버 스타일 다크 모드)
st.set_page_config(page_title="WOORI COST SOLVER", layout="centered")

# 다크 테마 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stNumberInput, .stSelectbox { background-color: #1A1A1A !important; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Courier New'; font-size: 2.5rem !important; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 10px; height: 3em; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("WOORI COST SOLVER")
st.subheader("샌드위치 판넬 원가 계산기")

# --- 입력 영역 ---
with st.container():
    st.write("### 1. 매입 단가 설정")
    col1, col2 = st.columns(2)
    with col1:
        coil_price = st.number_input("코일 매입가 (kg당)", value=1100, step=10)
    with col2:
        process_fee = st.number_input("가공비 (인건비+소모품)", value=2700, step=100)

    st.write("---")
    st.write("### 2. 제품 사양 선택")
    
    core_type = st.radio("심재 종류", ["EPS", "그라스울(48k)", "그라스울(64k)", "우레탄"], horizontal=True)
    
    col3, col4 = st.columns(2)
    with col3:
        # 심재 단가 레이블 자동 변경
        label = "EPS 50T 보드값" if core_type == "EPS" else "심재 매입 단가"
        if "그라스울" in core_type: label = "GW kg당 단가"
        if core_type == "우레탄": label = "우레탄 m당 원액비"
        
        default_price = 3650 if core_type == "EPS" else (1770 if "48k" in core_type else 1600)
        core_price = st.number_input(label, value=default_price, step=10)
        
    with col4:
        thickness = st.number_input("제품 두께 (T)", value=150, step=5)

    coil_option = st.selectbox("코일 조합 선택", ["내부/외부 (1040/1219)", "내부/내부 (1040/1040)"])

# --- 계산 로직 ---
coil_w = 8.867 if "외부" in coil_option else 8.164
cost_coil = coil_price * coil_w

cost_core = 0
if core_type == "EPS":
    cost_core = (thickness / 50) * core_price
elif "그라스울" in core_type:
    density = 48 if "48k" in core_type else 64
    cost_core = (thickness / 1000) * density * 1.219 * core_price
else: # 우레탄
    cost_core = (thickness / 50) * core_price

total_cost = int(cost_coil + cost_core + process_fee)

# --- 결과 출력 ---
st.write("---")
st.metric(label="예상 제조 원가 (1m 기준)", value=f"{total_cost:,} 원")

if st.button("카톡 공유용 텍스트 복사"):
    share_text = f"[우리 스틸] {core_type} {thickness}T 원가: {total_cost:,}원"
    st.code(share_text)
    st.success("위 코드를 복사해서 카톡에 붙여넣으세요!")
