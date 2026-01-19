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
st.set_page_config(page_title="Unit 33: O Fana' ato Tengil", page_icon="🧠", layout="centered")

# --- CSS 美化 (知性深紫色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #E1BEE7; color: #4A148C; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #F3E5F5 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #8E24AA;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #6A1B9A; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F3E5F5;
        border-left: 5px solid #AB47BC;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #E1BEE7; color: #4A148C; border: 2px solid #8E24AA; padding: 12px;
    }
    .stButton>button:hover { background-color: #CE93D8; border-color: #7B1FA2; }
    .stProgress > div > div > div > div { background-color: #8E24AA; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 33: 18個單字 - 認知與感官) ---
vocab_data = [
    {"amis": "Tengil", "chi": "聽 (詞根)", "icon": "👂", "source": "Root", "morph": "Root"},
    {"amis": "Matengil", "chi": "聽到 / 被聽見", "icon": "🔊", "source": "Row 238", "morph": "Ma-Tengil"},
    {"amis": "Tengilen", "chi": "聽起來 / 去聽 (命令/受事)", "icon": "🎧", "source": "Row 352", "morph": "Tengil-en"},
    {"amis": "Nengneng", "chi": "看 (詞根)", "icon": "👀", "source": "Root", "morph": "Root"},
    {"amis": "Minengneng", "chi": "看 / 注視 (主動)", "icon": "🧐", "source": "Row 350", "morph": "Mi-Nengneng"},
    {"amis": "Nengnengen", "chi": "看起來 / 被看 (受事)", "icon": "🖼️", "source": "Row 350", "morph": "Nengneng-en"},
    {"amis": "Manengneng", "chi": "看見 / 被看見", "icon": "🫣", "source": "Row 489", "morph": "Ma-Nengneng"},
    {"amis": "Harateng", "chi": "想法 / 心思 (詞根)", "icon": "🧠", "source": "Root", "morph": "Root"},
    {"amis": "Miharateng", "chi": "想 / 思考 (主動)", "icon": "🤔", "source": "Row 319", "morph": "Mi-Harateng"},
    {"amis": "Fana'", "chi": "知 / 會 (詞根)", "icon": "💡", "source": "Root", "morph": "Root"},
    {"amis": "Mafana'", "chi": "知道 / 懂", "icon": "✅", "source": "Row 6", "morph": "Ma-Fana'"},
    {"amis": "Kafana'en", "chi": "要知道 / 應當知道", "icon": "ℹ️", "source": "Grammar Ext.", "morph": "Ka-Fana'-en"},
    {"amis": "Sowal", "chi": "話語 / 語言 (詞根)", "icon": "💬", "source": "Root", "morph": "Root"},
    {"amis": "Misowal", "chi": "說 (主動)", "icon": "🗣️", "source": "Row 319", "morph": "Mi-Sowal"},
    {"amis": "Pasowal", "chi": "告訴 / 轉告", "icon": "📢", "source": "Row 377", "morph": "Pa-Sowal"},
    {"amis": "Araw", "chi": "看見 (詞根)", "icon": "👁️", "source": "Root", "morph": "Root"},
    {"amis": "Ma'araw", "chi": "看見了 (結果)", "icon": "🔭", "source": "Row 121", "morph": "Ma-'Araw"},
    {"amis": "Soni", "chi": "聲音", "icon": "🔔", "source": "Row 238", "morph": "Noun"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Matengil no mako ko soni no tangic.", "chi": "我聽見了哭聲。(哭聲被我聽見)", "icon": "🔊", "source": "Row 238"},
    {"amis": "Fa'elohay koni a radiw a tengilen.", "chi": "這首歌聽起來是新的。", "icon": "🎧", "source": "Row 352"},
    {"amis": "Takaraw kiso a nengnengen.", "chi": "你看起來很高。", "icon": "📏", "source": "Row 350"},
    {"amis": "Caay ka manengneng no mako.", "chi": "我沒看見。(非被我看見)", "icon": "🫣", "source": "Row 489"},
    {"amis": "Ma'araw ako ko 'adingo iso.", "chi": "我看見你的影子。", "icon": "👻", "source": "Row 121"},
    {"amis": "Mafana' ci Kacaw tisowanan.", "chi": "Kacaw認識你。", "icon": "💡", "source": "Row 6"},
    {"amis": "Miharatengay kako to misowalan no miso.", "chi": "我正在想你所說的話。", "icon": "🤔", "source": "Row 319"},
    {"amis": "O nia demak 'i, caay kafana' kako.", "chi": "這件事呢，我不知道。", "icon": "🤷", "source": "Row 238"},
    {"amis": "Pasowalen ci ina.", "chi": "去告訴媽媽。", "icon": "📢", "source": "Row 377 (Adapted)"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Fa'elohay koni a radiw a tengilen.",
        "audio": "Fa'elohay koni a radiw a tengilen",
        "options": ["這首歌聽起來是新的", "這首歌很好聽", "這首歌很舊"],
        "ans": "這首歌聽起來是新的",
        "hint": "Tengilen (聽起來) (Row 352)"
    },
    {
        "q": "單字測驗：Matengil",
        "audio": "Matengil",
        "options": ["聽到/被聽見", "去聽", "聽話"],
        "ans": "聽到/被聽見",
        "hint": "Ma- (被動/狀態) + Tengil"
    },
    {
        "q": "單字測驗：Nengnengen",
        "audio": "Nengnengen",
        "options": ["看起來/被看", "看見", "瞪"],
        "ans": "看起來/被看",
        "hint": "Row 350: Takaraw a nengnengen (看起來高)"
    },
    {
        "q": "Miharatengay kako to misowalan no miso.",
        "audio": "Miharatengay kako to misowalan no miso",
        "options": ["我正在想你說的話", "我聽不懂你說的話", "我忘記你說的話"],
        "ans": "我正在想你說的話",
        "hint": "Miharateng (思考) (Row 319)"
    },
    {
        "q": "單字測驗：Pasowal",
        "audio": "Pasowal",
        "options": ["告訴/轉告", "說話", "吵架"],
        "ans": "告訴/轉告",
        "hint": "Pa- (給/使) + Sowal (話)"
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
st.markdown("<h1 style='text-align: center; color: #6A1B9A;'>Unit 33: O Fana' ato Tengil</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>認知與感官 (Cognition & Senses)</p>", unsafe_allow_html=True)

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
            <div style="font-size: 20px; font-weight: bold; color: #6A1B9A;">{s['icon']} {s['amis']}</div>
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
        <div style='text-align: center; padding: 30px; background-color: #E1BEE7; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #6A1B9A;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會認知與感官詞彙了！</p>
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
