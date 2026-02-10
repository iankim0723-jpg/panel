import streamlit as st

# 페이지 설정
st.set_page_config(page_title="WOORI COST SOLVER", layout="centered")

# 디자인 수정: 배경은 검정, 글자는 흰색/금색으로 확실하게 구분
st.markdown("""
    <style>
    /* 전체 배경 검정 */
    .stApp { background-color: #000000; }
    
    /* 모든 텍스트 기본색을 흰색으로 강제 설정 */
    * { color: #FFFFFF !important; }
    
    /* 제목 및 강조 텍스트는 금색 */
    h1, h2, h3, .stMetric label { color: #D4AF37 !important; }
    
    /* 입력창 내부 배경과 글자색 설정 */
    input { background-color: #262626 !important; color: #FFFFFF !important; border: 1px solid #D4AF37 !important; }
    
    /* 선택 박스(Selectbox) 디자인 */
    div[data-baseweb="select"] > div { background-color: #262626 !important; }
    
    /* 버튼: 금색 배경에 검정 글자 (가장 잘 보임) */
    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        border-radius: 10px; 
        height: 3.5em;
        border: none;
    }
    
    /* 결과창(Metric) 숫자 강조 */
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-size: 3rem !important; font-weight: bold; }
    
    /* 라디오 버튼(심재 선택) 글자색 */
    div[data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("WOORI COST SOLVER")
st.write("---")

# --- 1. 매입 단가 설정 ---
st.subheader("1. 기본 매입 단가")
col1, col2 = st.columns(2)
with col1:
    coil_price = st.number_input("코일 매입가 (kg)", value=1100)
with col2:
    process_fee = st.number_input("가공비 (인건비+소모품)", value=2700)

st.write("")

# --- 2. 제품 사양 선택 ---
st.subheader("2. 제품 사양 및 심재")
core_type = st.radio("심재 종류 선택", ["EPS", "그라스울(48k)", "그라스울(64k)", "우레탄"], horizontal=True)

col3, col4 = st.columns(2)
with col3:
    # 심재별 라벨 및 기본값 세팅
    if core_type == "EPS":
        label, default = "EPS 50T 보드값", 3650
    elif "그라스울" in core_type:
        label, default = "GW kg당 매입가", (1770 if "48k" in core_type else 1600)
    else: # 우레탄
        label, default = "우레탄 m당 원액비", 18000
        
    core_price = st.number_input(label, value=default)
    
with col4:
    thickness = st.number_input("제품 두께 (T)", value=150)

coil_option = st.selectbox("코일 조합", ["내부/외부 (1040/1219)", "내부/내부 (1040/1040)"])

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

total_cost = int(cost_coil + cost_core + process_fee)

# --- 결과 출력 ---
st.write("---")
st.write("### 예상 제조 원가 (1m)")
st.metric(label="", value=f"{total_cost:,} 원")

# 공유 기능
if st.button("결과 텍스트 복사하기"):
    res_txt = f"[우리 스틸] {core_type} {thickness}T 원가: {total_cost:,}원"
    st.code(res_txt)
    st.success("위 코드를 길게 눌러 복사하세요!")
