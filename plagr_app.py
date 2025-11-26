import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

# ==================== 1. Page Configuration ====================
st.set_page_config(
    page_title="Plagiarism Detector Pro",
    page_icon="🟥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 2. Theme State Management ====================
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

# Toggle Logic
col_head, col_toggle = st.columns([9, 1])
with col_toggle:
    mode = st.toggle("Dark Mode", value=(st.session_state.theme == "dark"))
    if mode and st.session_state.theme != "dark":
        st.session_state.theme = "dark"
        st.rerun()
    elif not mode and st.session_state.theme != "light":
        st.session_state.theme = "light"
        st.rerun()

# ==================== 3. Swiss Design System ====================
THEMES = {
    "light": {
        "bg": "#ffffff",
        "text": "#000000",
        "accent": "#FF3B30",
        "box_bg": "#ffffff",
        "border": "#000000",
        "input_bg": "#f9f9f9",
        "header_bg": "#000000", 
        "header_text": "#ffffff",
        "sub_text": "#666666",
        "bar_bg": "#e0e0e0" # Empty part of the bar
    },
    "dark": {
        "bg": "#000000", 
        "text": "#ffffff",
        "accent": "#FF453A", 
        "box_bg": "#000000", 
        "border": "#333333", 
        "input_bg": "#111111", 
        "header_bg": "#000000",
        "header_text": "#ffffff",
        "sub_text": "#888888",
        "bar_bg": "#222222" # Empty part of the bar
    }
}

C = THEMES[st.session_state.theme]

st.markdown(f"""
<style>
    /* 1. FORCE APP BACKGROUND */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {C['bg']} !important;
    }}
    
    /* 2. Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, p, div, label, span {{
        font-family: 'Inter', Helvetica, Arial, sans-serif !important;
        color: {C['text']} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        color: {C['text']} !important;
    }}
    
    /* 3. Buttons */
    .stButton>button {{
        background-color: {C['accent']} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        font-weight: 700 !important;
        padding: 16px 24px !important;
    }}
    
    /* 4. Inputs */
    .stTextArea textarea, .stTextInput input {{
        background-color: {C['input_bg']} !important;
        color: {C['text']} !important;
        border: 1px solid {C['border']} !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
    }}
    .stTextArea textarea::placeholder {{ color: {C['sub_text']} !important; }}

    /* 5. Custom Header Block */
    .swiss-header {{
        background-color: {C['header_bg']};
        padding: 4rem 0;
        border-bottom: 4px solid {C['accent']};
        margin-bottom: 3rem;
    }}
    .swiss-header h1 {{ color: {C['header_text']} !important; }}
    .swiss-header p {{ color: #999999 !important; font-family: 'Courier New', monospace !important; }}

    /* 6. Containers */
    .metric-box {{
        border: 1px solid {C['border']};
        background: {C['box_bg']};
        padding: 20px;
    }}
    
    .compare-box {{
        background-color: {C['box_bg']};
        border: 1px solid {C['border']};
        border-left: 4px solid {C['text']};
        padding: 20px;
        font-family: 'Georgia', serif;
        height: 400px;
        overflow-y: auto;
        color: {C['text']};
    }}
    
    .highlight {{
        background-color: #FFE600;
        color: #000;
        padding: 2px 5px;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== 4. Logic ====================
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

def vectorize(texts):
    return TfidfVectorizer().fit_transform(texts).toarray()

def similarity(doc1, doc2):
    return cosine_similarity([doc1], [doc2])[0][0]

def get_common_sentences(text1, text2, threshold=0.65):
    s1 = [s.strip() for s in re.split(r'[.!?]+', text1) if len(s.strip()) > 20]
    s2 = [s.strip() for s in re.split(r'[.!?]+', text2) if len(s.strip()) > 20]
    if not s1 or not s2: return []
    try:
        vectorizer = TfidfVectorizer()
        all_s = s1 + s2
        vectors = vectorizer.fit_transform(all_s)
        v1, v2 = vectors[:len(s1)], vectors[len(s1):]
        matches = []
        for i, sent1 in enumerate(s1):
            for j, sent2 in enumerate(s2):
                sim = cosine_similarity(v1[i:i+1], v2[j:j+1])[0][0]
                if sim >= threshold:
                    matches.append((sent1, sent2, round(sim, 3)))
        return sorted(matches, key=lambda x: x[2], reverse=True)[:50]
    except:
        return []

def highlight_text(text, sentences, is_first=True):
    result = text
    idx = 0 if is_first else 1
    for pair in sentences:
        sent = pair[idx]
        if sent in result:
            result = result.replace(sent, f'<span class="highlight">{sent}</span>')
    return result

# ==================== 5. UI Structure ====================

st.markdown("""
<div class="swiss-header">
    <div style="max-width: 100%; margin: 0 auto;">
        <h1>PLAGIARISM DETECTOR PRO</h1>
        <p>/// SENTENCE LEVEL ANALYSIS SYSTEM ///</p>
    </div>
</div>
""", unsafe_allow_html=True)

main = st.container()

with main:
    if not st.session_state.analyzed:
        st.markdown("### 01. INPUT DATA")
        method = st.radio("SELECT SOURCE", ["PASTE TEXT", "UPLOAD FILES"], label_visibility="collapsed")
        st.markdown("---")
        
        texts, names = [], []

        if method == "PASTE TEXT":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**DOCUMENT A**")
                t1 = st.text_area("A", height=300, label_visibility="collapsed", placeholder="Paste text...")
            with c2:
                st.markdown("**DOCUMENT B**")
                t2 = st.text_area("B", height=300, label_visibility="collapsed", placeholder="Paste text...")
            if t1 and t2:
                texts = [t1, t2]
                names = ["Doc A", "Doc B"]
        else:
            st.markdown("**FILE UPLOAD**")
            files = st.file_uploader("Upload", type=["txt"], accept_multiple_files=True, label_visibility="collapsed")
            if files:
                for f in files:
                    texts.append(f.read().decode("utf-8", errors="ignore"))
                    names.append(f.name)
                st.success(f"LOADED {len(texts)} FILES")

        if len(texts) >= 2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("INITIATE ANALYSIS", use_container_width=True):
                with st.spinner("PROCESSING..."):
                    vecs = vectorize(texts)
                    res = []
                    for i in range(len(texts)):
                        for j in range(i+1, len(texts)):
                            sc = similarity(vecs[i], vecs[j])
                            risk = "HIGH" if sc > 0.5 else "MODERATE" if sc > 0.2 else "LOW"
                            res.append({"a": names[i], "b": names[j], "score": sc, "risk": risk, "text_a": texts[i], "text_b": texts[j]})
                    st.session_state.results = res
                    st.session_state.analyzed = True
                    st.rerun()

    else:
        c1, c2 = st.columns([6, 1])
        with c1: st.markdown(f"### 02. REPORT / {len(st.session_state.results)} PAIRS")
        with c2: 
            if st.button("RESET"):
                st.session_state.analyzed = False
                st.rerun()
        st.markdown("---")
        
        results = st.session_state.results
        opts = [f"{r['a']} vs {r['b']}" for r in results]
        sel_name = st.selectbox("SELECT PAIR", opts)
        sel = results[opts.index(sel_name)]
        
        r_col = "#27ae60" if sel['risk'] == "LOW" else "#f39c12" if sel['risk'] == "MODERATE" else "#c0392b"
        
        # === SCORE + INDICATOR BAR ===
        st.markdown(f"""
        <div class="metric-box">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <span style="font-size:12px; font-weight:700; color:{C['sub_text']}; letter-spacing:1px;">SIMILARITY</span>
                    <div style="font-size:48px; font-weight:800; line-height:1;">{sel['score']*100:.1f}%</div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:12px; font-weight:700; color:{C['sub_text']}; letter-spacing:1px;">RISK</span>
                    <div style="font-size:32px; font-weight:800; color:{r_col};">{sel['risk']}</div>
                </div>
            </div>
            
            <div style="width:100%; height:20px; background-color:{C['bar_bg']}; margin-top:20px; border:1px solid {C['border']};">
                <div style="width:{sel['score']*100}%; height:100%; background-color:{r_col};"></div>
            </div>
            
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        common = get_common_sentences(sel["text_a"], sel["text_b"])
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**SOURCE: {sel['a']}**")
            st.markdown(f'<div class="compare-box">{highlight_text(sel["text_a"], common, True)}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"**SOURCE: {sel['b']}**")
            st.markdown(f'<div class="compare-box">{highlight_text(sel["text_b"], common, False)}</div>', unsafe_allow_html=True)

        st.markdown("### 03. EXPORT")
        st.download_button("DOWNLOAD CSV", pd.DataFrame(results).to_csv().encode(), "report.csv", "text/csv")