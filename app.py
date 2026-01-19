import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 32: O Tayal", page_icon="✍️", layout="centered")

# --- CSS 美化 (知性靛藍色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #C5CAE9; color: #1A237E; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E8EAF6 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #3F51B5;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #303F9F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E8EAF6;
        border-left: 5px solid #7986CB;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #C5CAE9; color: #1A237E; border: 2px solid #3F51B5; padding: 12px;
    }
    .stButton>button:hover { background-color: #9FA8DA; border-color: #283593; }
    .stProgress > div > div > div > div { background-color: #3F51B5; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 32: 18個單字 - 構詞與活動) ---
vocab_data = [
    {"amis": "Mitilid", "chi": "讀書 / 寫字", "icon": "✍️", "source": "Row 1153", "morph": "Mi + Tilid"},
    {"amis": "Pitilidan", "chi": "學校 / 教室", "icon": "🏫", "source": "Row 485", "morph": "Pi + Tilid + an"},
    {"amis": "Miasip", "chi": "讀 / 數 (計算)", "icon": "🔢", "source": "Row 712", "morph": "Mi + Asip"},
    {"amis": "Minengneng", "chi": "看 / 注視", "icon": "👁️", "source": "Row 350", "morph": "Mi + Nengneng"},
    {"amis": "Mafokil", "chi": "不會 / 不知道", "icon": "🤷", "source": "Row 238", "morph": "Ma + Fokil"},
    {"amis": "Tangsol", "chi": "立刻 / 馬上", "icon": "⚡", "source": "Row 2261", "morph": "Adverb"},
    {"amis": "Mipadang", "chi": "幫忙", "icon": "🤝", "source": "Row 384", "morph": "Mi + Padang"},
    {"amis": "Keriden", "chi": "帶領 / 攜帶", "icon": "👫", "source": "CSV Extracted", "morph": "Kerid + en"},
    {"amis": "Miala", "chi": "拿 / 取", "icon": "🤲", "source": "Row 23", "morph": "Mi + Ala"},
    {"amis": "Mikalic", "chi": "爬 / 搭乘", "icon": "🧗", "source": "Row 4535", "morph": "Mi + Kalic"},
    {"amis": "Patireng", "chi": "站立 / 建設", "icon": "🏗️", "source": "Row 524", "morph": "Pa + Tireng"},
    {"amis": "Pa'aca", "chi": "賣 (讓...買)", "icon": "🏪", "source": "Row 468", "morph": "Pa + Aca"},
    {"amis": "Mikilim", "chi": "尋找", "icon": "🔍", "source": "Row 2883", "morph": "Mi + Kilim"},
    {"amis": "Paca'of", "chi": "回答", "icon": "🗣️", "source": "Row 2261", "morph": "Pa + Ca'of"},
    {"amis": "Tilid", "chi": "字 / 書 (詞根)", "icon": "📖", "source": "Root", "morph": "Root"},
    {"amis": "Asip", "chi": "數 / 讀 (詞根)", "icon": "1️⃣", "source": "Root", "morph": "Root"},
    {"amis": "Padang", "chi": "幫忙 (詞根)", "icon": "👐", "source": "Root", "morph": "Root"},
    {"amis": "Kerid", "chi": "帶領 (詞根)", "icon": "👉", "source": "Root", "morph": "Root"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Ciharateng kako to sapitilidaw.", "chi": "我想要讀書(上學)。", "icon": "🎒", "source": "Row 1153"},
    {"amis": "Miasip to payso ci mama.", "chi": "爸爸在數錢。", "icon": "💴", "source": "Row 712 (Adapted)"},
    {"amis": "Tangsol han nira a paca'of.", "chi": "他立刻回答。", "icon": "⚡", "source": "Row 2261"},
    {"amis": "Mipadang ci ina to tayal no loma'.", "chi": "媽媽幫忙家務。", "icon": "🧹", "source": "Row 384 (Adapted)"},
    {"amis": "Keriden no mako kiso a tayra.", "chi": "我帶你去那裡。", "icon": "👫", "source": "Standard Corpus"},
    {"amis": "Miala ko kaying to dateng.", "chi": "小姐拿菜。", "icon": "🥬", "source": "Row 23"},
    {"amis": "Mikalic to lanyan.", "chi": "爬梯子。", "icon": "🧗", "source": "Row 4535 (Adapted)"},
    {"amis": "Patireng to loma' i omah.", "chi": "在田裡蓋房子。", "icon": "🏠", "source": "Row 524 (Adapted)"},
    {"amis": "Mafokil kako a misowar.", "chi": "我不會說。", "icon": "🤐", "source": "Row 238 (Adapted)"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Tangsol han nira a paca'of.",
        "audio": "Tangsol han nira a paca'of",
        "options": ["他立刻回答", "他立刻生氣", "他立刻離開"],
        "ans": "他立刻回答",
        "hint": "Tangsol (立刻), Paca'of (回答) (Row 2261)"
    },
    {
        "q": "單字測驗：Pitilidan",
        "audio": "Pitilidan",
        "options": ["學校/教室", "書本", "筆"],
        "ans": "學校/教室",
        "hint": "Pi-..-an (地點) + Tilid (書)"
    },
    {
        "q": "Miala ko kaying to dateng.",
        "audio": "Miala ko kaying to dateng",
        "options": ["小姐拿菜", "小姐買菜", "小姐煮菜"],
        "ans": "小姐拿菜",
        "hint": "Miala (拿) (Row 23)"
    },
    {
        "q": "單字測驗：Pa'aca",
        "audio": "Pa'aca",
        "options": ["賣", "買", "借"],
        "ans": "賣",
        "hint": "Pa- (使動) + Aca (買) = 讓人買 = 賣"
    },
    {
        "q": "單字測驗：Mafokil",
        "audio": "Mafokil",
        "options": ["不會/不知", "不喜歡", "不想"],
        "ans": "不會/不知",
        "hint": "Fokil (不懂) (Row 238)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #303F9F;'>Unit 32: O Tayal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>動作與活動 (Action & Morphology)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #303F9F;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #C5CAE9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #1A237E;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經掌握這些動作詞彙了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
