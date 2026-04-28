import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
/* Force Dark Mode natively (Bypasses config.toml) */
[data-testid="stAppViewContainer"] {
    background-color: #0E1117 !important;
    color: #FAFAFA !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
p, div, span, h1, h2, h3, h4, h5, h6, label {
    color: #FAFAFA !important;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.game-title {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    color: #FFD700;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
    padding: 20px 0;
}
.correct-flash {
    background: linear-gradient(135deg, #1a4a1a, #0d2b0d);
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.wrong-flash {
    background: linear-gradient(135deg, #4a1a1a, #2b0d0d);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.nanami-bubble {
    background: #16213e;
    border-left: 4px solid #FFD700;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin: 10px 0;
    font-size: 0.95rem;
    line-height: 1.7;
}
.boss-header {
    text-align: center;
    font-size: 1.8rem;
    color: #ff4444;
    text-shadow: 0 0 15px rgba(255,68,68,0.8);
    font-weight: bold;
}
.stProgress > div > div > div > div {
    background-color: #FFD700;
}
.exam-result-pass {
    background: #0d2b0d;
    border: 2px solid #00ff00;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin: 10px 0;
}
.exam-result-fail {
    background: #2b0d0d;
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin: 10px 0;
}
.stRadio label {
    padding: 8px 0;
    font-size: 1.1rem;
}
.stButton button {
    min-height: 50px;
    font-size: 1.1rem;
    font-weight: bold;
    background-color: #1E2235 !important;
    color: #FAFAFA !important;
    border: 1px solid #FFD700 !important;
}
.stTextInput input, .stTextInput div[data-baseweb="input"] {
    background-color: #1E2235 !important;
    color: #FAFAFA !important;
}
@media (max-width: 600px) {
    .game-title { font-size: 1.8rem; }
    .boss-header { font-size: 1.4rem; }
    .nanami-bubble { font-size: 0.9rem; padding: 10px; }
}
</style>
""", unsafe_allow_html=True)

def render_status_bar():
    c1, c2, c3 = st.columns([1.5, 1.5, 1])
    hp = st.session_state.hp
    exp = st.session_state.exp
    lvl = st.session_state.level
    
    with c1:
        st.markdown(f"**❤️ HP: {hp}/100**")
        st.progress(max(0, min(100, hp))/100)
    with c2:
        st.markdown(f"**⭐ EXP: {exp}**")
        st.progress(min(1.0, (exp % 100) / 100.0) if lvl < 7 else 1.0)
    with c3:
        st.markdown(f"**Lv.{lvl}**")
        
    if st.session_state.combo > 1:
        st.markdown(f"<div style='text-align: center; color: #FF4500; font-weight: bold; font-size: 1.2rem;'>🔥 {st.session_state.combo}連続コンボ！</div>", unsafe_allow_html=True)
    st.divider()

import html

def show_nanami_message(message):
    safe_msg = html.escape(str(message)).replace("\n", "<br>")
    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 20px;">
        <div style="font-size: 2.5rem; margin-right: 15px;">🧙‍♀️</div>
        <div class="nanami-bubble">{safe_msg}</div>
    </div>
    """, unsafe_allow_html=True)

def show_akira_message(message):
    safe_msg = html.escape(str(message)).replace("\n", "<br>")
    st.markdown(f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 20px;">
        <div style="font-size: 2.5rem; margin-right: 15px;">💻</div>
        <div class="nanami-bubble" style="border-left: 4px solid #00BFFF;">{safe_msg}</div>
    </div>
    """, unsafe_allow_html=True)

import base64
import os

def play_bgm(track="battle"):
    bgm_path = f"assets/bgm_{track}.wav"
    if not os.path.exists(bgm_path): return
    with open(bgm_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    vol = 0.15 if track == "town" else (0.35 if track == "boss" else (0.4 if track == "clear" else 0.25))
    
    st.markdown(f'''
        <div style="background: #16213e; padding: 8px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333 text-align: center;">
            <p style="font-size: 0.75rem; color: #aaa; margin: 0 0 5px 0;">♪ BGM (スマホで鳴らない場合は👇をタップ)</p>
            <audio id="bgm-player" controls loop autoplay style="width: 100%; height: 35px;">
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            <script>
                var player = document.getElementById("bgm-player");
                if (player) {{
                    player.volume = {vol};
                }}
            </script>
        </div>
    ''', unsafe_allow_html=True)

def stop_bgm():
    pass

def play_hit_sfx():
    hit_path = "assets/hit.wav"
    if not os.path.exists(hit_path): return
    with open(hit_path, "rb") as f:
        data = f.read()
    st.audio(data, format="audio/wav", autoplay=True)
