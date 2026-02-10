import streamlit as st

# 페이지 설정
st.set_page_config(page_title="WOORI COST SOLVER", layout="centered")

# CSS: 가독성 및 다크모드 완벽 최적화
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    span, p, label, div { color: #FFFFFF !important; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }

    /* 숫자 입력창 스타일 */
    input { 
        background-color: #262626 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #D4AF37 !important; 
    }

    /* 드롭다운 메뉴 가독성 확보 (흰색 배경 방지) */
    div[data-baseweb="select"] > div {
        background-color: #262626 !important;
        color: #FFFFFF !important;
        border: 1px solid #D4AF37 !important;
    }
    div[data-baseweb="popover"], ul[role="listbox"] {
        background-color: #262626 !important;
        color: #FFFFFF !important;
    }
    li[role="option"] {
        color: #FFFFFF !important;
        background-color: #262626 !important;
    }
    li[role="option"]:hover {
        background-color: #D4AF37 !important;
        color: #000000 !important;
    }

    /* 버튼 스타일 */
    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        border-radius: 10px; 
        height: 3.5em;
        border: none;
    }

    /* 결과값 강조 */
    div[data-testid="stMetricValue"] { 
        color: #D4AF37 !important; 
        font-size: 3rem !important; 
        font-weight: bold; 
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("WOORI COST SOLVER")
st.write("---")

# --- 1. 코일 매입 단가 설정 (외부/내부 분리) ---
st.subheader("1. 코일 매입 단가 설정")
col_c1, col_c2 = st.columns(2)
with col_c1:
    ext_coil_price = st.number_input("외부 코일 단가 (kg)", value=1100, format="%d")
with col_c2:
    int_coil_price = st.number_input("내부 코일 단가 (kg)", value=1100, format="%d")

# --- 2. 심재 및 가공비 설정 ---
st.subheader("2. 심재 및 가공비 설정")
core_type = st.radio("심재 종류 선택", ["EPS", "그라스울(48k)", "그라스울(64k)", "우레탄"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    if core_type == "EPS":
        label, default = "EPS 50T 보드값", 3650
    elif "그라스울" in core_type:
        label, default = "GW kg당 매입가", (1770 if "48k" in core_type else 1600)
    else: # 우레탄
        label, default = "우레탄 m당 원액비", 18000
    core_price = st.number_input(label, value=default, format="%d")
with col2:
    process_fee = st.number_input("가공비 (인건비+소모품)", value=2700, format="%d")

st.write("---")

# --- 3. 상세 사양 선택 ---
st.subheader("3. 상세 사양")
col3, col4 = st.columns(2)
with col3:
    thickness = st.number_input("제품 두께 (T)", value=150, format="%d")
with col4:
    coil_option = st.selectbox("코일 조합 선택", ["외부(1219) + 내부(1040)", "내부(1040) + 내부(1040)"])

# --- 계산 로직 ---
# 중량 상수 (0.5T 기준)
# 1219폭: 4.784kg/m, 1040폭: 4.082kg/m (합계 8.866 / 8.164)
if "외부" in coil_option:
    # 외부(1219) + 내부(1040)
    cost_coil = (4.784 * ext_coil_price) + (4.082 * int_coil_price)
else:
    # 내부(1040) + 내부(1040)
    cost_coil = (4.082 * int_coil_price) + (4.082 * int_coil_price)

# 심재비 계산
if core_type == "EPS":
    cost_core = (thickness / 50) * core_price
elif "그라스울" in core_type:
    density = 48 if "48k" in core_type else 64
    cost_core = (thickness / 1000) * density * 1.219 * core_price
else: # 우레탄
    cost_core = (thickness / 50) * core_price

total_cost = int(cost_coil + cost_core + process_fee)

# --- 결과 출력 ---
st.metric(label="예상 제조 원가 (1m 기준)", value=f"{total_cost:,} 원")

if st.button("결과 텍스트 복사 (카톡용)"):
    res_txt = f"[우리 스틸] {core_type} {thickness}T ({coil_option.split(' ')[0]}) 원가: {total_cost:,}원"
    st.code(res_txt)
    st.success("위 텍스트를 복사해서 사용하세요!")
