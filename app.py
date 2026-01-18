import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 10: O loma'", page_icon="🏠", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 10px;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: scale(1.02);
    }
    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 5px;
    }
    .med-font {
        font-size: 22px !important;
        color: #555;
        text-align: center;
        margin-bottom: 10px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據資料庫 (Unit 10 修正版) ---

# 單字：家與家具 (全部小寫)
VOCABULARY = {
    "loma'":      {"zh": "家/房子", "emoji": "🏠", "file": "u10_loma"},
    "panan":      {"zh": "門", "emoji": "🚪", "file": "u10_panan"},
    "sasingaran": {"zh": "窗戶", "emoji": "🪟", "file": "u10_sasingaran"},
    "anengan":    {"zh": "椅子/座位", "emoji": "🪑", "file": "u10_anengan"},
    "takar":      {"zh": "床鋪/竹藤床", "emoji": "🛏️", "file": "u10_takar"},
    "tilifi":     {"zh": "電視", "emoji": "📺", "file": "u10_tilifi"}
}

# 句型：地點與動作
SENTENCES = [
    {"amis": "I cowa kiso?", "zh": "你在哪裡？", "file": "u10_q_where_are_you"},
    {"amis": "I loma' kako.", "zh": "我在家。", "file": "u10_s_im_at_home"},
    {"amis": "Pifohat to panan.", "zh": "把門打開。", "file": "u10_s_open_door"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    try:
        # 使用印尼語 (id) 模擬南島語系發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (無聲)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 學習模式 ---
def show_learning_mode():
    st.markdown("<h2 style='text-align: center;'>Sakamotep: O loma'</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>溫暖的家 🏠</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 60px;">{data['emoji']}</div>
                    <div class="big-font">{amis}</div>
                    <div class="med-font">{data['zh']}</div>
                </div>
                """, unsafe_allow_html=True)
                play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    # 問答
    st.markdown("#### 📍 詢問地點")
    q1 = SENTENCES[0]
    st.info(f"🔹 {q1['amis']} ({q1['zh']})")
    play_audio(q1['amis'], filename_base=q1.get('file'))
    
    a1 = SENTENCES[1]
    st.success(f"🔹 {a1['amis']} ({a1['zh']})")
    play_audio(a1['amis'], filename_base=a1.get('file'))

    # 動作
    st.markdown("#### 🚪 動作指令")
    s3 = SENTENCES[2]
    st.warning(f"🔹 {s3['amis']} ({s3['zh']})")
    play_audio(s3['amis'], filename_base=s3.get('file'))

# --- 4. 測驗模式 ---
def show_quiz_mode():
    st.markdown("<h2 style='text-align: center;'>🎮 Sakamotep 居家小幫手</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    # 第一關：聽音辨位
    if st.session_state.current_q == 0:
        st.markdown("### 第一關：這是什麼聲音？")
        st.write("請聽單字：")
        play_audio("sasingaran", filename_base="u10_sasingaran")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🪟 sasingaran"):
                st.balloons()
                st.success("答對了！ Sasingaran 是窗戶！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("🚪 panan"): st.error("不對喔，panan 是門！")

    # 第二關：句子理解
    elif st.session_state.current_q == 1:
        st.markdown("### 第二關：我在哪裡？")
        st.markdown("#### 請聽句子：")
        play_audio("I loma' kako.", filename_base="u10_s_im_at_home")
        
        st.write("請問這句話是什麼意思？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 我在家"):
                st.snow()
                st.success("沒錯！ I loma' kako.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("🏫 我在學校"): st.error("不對喔，loma' 是家！")

    # 第三關：看圖問答
    elif st.session_state.current_q == 2:
        st.markdown("### 第三關：看圖回答")
        st.markdown("#### Q: O maan koni? (這是什麼？)")
        play_audio("O maan koni?", filename_base="u10_q_what") 
        
        st.markdown("<div style='font-size:80px; text-align:center;'>🚪</div>", unsafe_allow_html=True)
        
        options = ["O panan (是門)", "O takar (是床鋪)", "O tilifi (是電視)"]
        choice = st.radio("請選擇：", options)
        
        if st.button("確定送出"):
            if "panan" in choice:
                st.balloons()
                st.success("太厲害了！全部答對！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再看一次圖片喔！")

    else:
        st.markdown(f"<div style='text-align: center;'><h1>🏆 挑戰完成！</h1><h2>得分：{st.session_state.score}</h2></div>", unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 5. 主程式入口 ---
st.sidebar.title("Unit 10: O loma' 🏠")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()
