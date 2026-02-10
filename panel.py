import streamlit as st

# 페이지 설정
st.set_page_config(page_title="WOORI COST SOLVER", layout="centered")

# CSS 수정: 배경 검정, 글자 흰색/금색, 선택 박스 내부 가독성 확보
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 기본 설정 */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* 모든 텍스트 강제 흰색 (단, 제목은 금색) */
    span, p, label, div { color: #FFFFFF !important; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }

    /* 숫자 입력창 스타일 */
    input { 
        background-color: #262626 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #D4AF37 !important; 
    }

    /* 드롭다운(Selectbox) 전체 스타일 수정 */
    div[data-baseweb="select"] > div {
        background-color: #262626 !important;
        color: #FFFFFF !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* 드롭다운 메뉴 리스트(클릭 시 나오는 부분) 가독성 확보 */
    ul[role="listbox"] {
        background-color: #262626 !important;
    }
    li[role="option"] {
        color: #FFFFFF !important;
        background-color: #262626 !important;
    }
    li[role="option"]:hover {
        background-color: #D4AF37 !important;
        color: #000000 !important;
    }

    /* 버튼 스타일: 금색 배경에 검정 글자 */
    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        border-radius: 10px; 
        height: 3.5em;
        border: none;
        margin-top: 10px;
    }

    /* 결과값 강조 */
    div[data-testid="stMetricValue"] { 
        color: #D4AF37 !important; 
        font-size: 3rem !important; 
        font-weight: bold; 
        text-align: center;
    }
    div[data-testid="stMetricLabel"] { text-align: center; width: 100%; }

    /* 라디오 버튼 텍스트 정렬 */
    div[data-testid="stMarkdownContainer"] p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("WOORI COST SOLVER")
st.write("---")

# --- 1. 매입 단가 설정 ---
st.subheader("1. 기본 매입 단가")
col1, col2 = st.columns(2)
with col1:
    coil_price = st.number_input("코일 매입가 (kg)", value=1100, format="%d")
with col2:
    process_fee = st.number_input("가공비 (인건비+소모품)", value=2700, format="%d")

st.write("")

# --- 2. 제품 사양 선택 ---
st.subheader("2. 제품 사양 및 심재")
core_type = st.radio("심재 종류 선택", ["EPS", "그라스울(48k)", "그라스울(64k)", "우레탄"], horizontal=True)

col3, col4 = st.columns(2)
with col3:
    if core_type == "EPS":
        label, default = "EPS 50T 보드값", 3650
    elif "그라스울" in core_type:
        label, default = "GW kg당 매입가", (1770 if "48k" in core_type else 1600)
    else: # 우레탄
        label, default = "우레탄 m당 원액비", 18000
    core_price = st.number_input(label, value=default, format="%d")
    
with col4:
    thickness = st.number_input("제품 두께 (T)", value=150, format="%d")

# 드롭다운 - 이제 글자가 잘 보일 겁니다
coil_option = st.selectbox("코일 조합 선택 (내외 / 내내)", ["내부/외부 (1040/1219)", "내부/내부 (1040/1040)"])

# --- 계산 로직 ---
coil_w = 8.867 if "외부" in coil_option else 8.164
cost_coil = coil_price * coil_w

if core_type == "EPS":
    cost_core = (thickness / 50) * core_price
elif "그라스울" in core_type:
    density = 48 if "48k" in core_type else 64
    cost_core = (thickness / 1000) * density * 1.219 * core_price
else: # 우레탄
    cost_core = (thickness / 50) * core_price

total_cost = int(coil_total := cost_coil + cost_core + process_fee)

# --- 결과 출력 ---
st.write("---")
st.metric(label="예상 제조 원가 (1m 기준)", value=f"{total_cost:,} 원")

# 공유 기능
st.write("")
if st.button("결과 텍스트 복사 (카톡용)"):
    res_txt = f"[우리 스틸] {core_type} {thickness}T ({coil_option.split(' ')[0]}) 원가: {total_cost:,}원"
    st.code(res_txt)
    st.success("위 코드를 복사해서 사용하세요!")
