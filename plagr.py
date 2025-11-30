import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re

# page configuration
st.set_page_config(
    page_title="Plagiarism Detector",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Swiss design color system
C = {
    "bg": "#ffffff",
    "text": "#000000",
    "accent": "#FF3B30",
    "box_bg": "#ffffff",
    "border": "#000000",
    "input_bg": "#f9f9f9",
    "header_bg": "#000000", 
    "header_text": "#ffffff",
    "sub_text": "#666666",
    "bar_bg": "#e0e0e0"
}

st.markdown(f"""
<style>
    /* === SWISS DESIGN SYSTEM === */
    /* 1. FORCE APP BACKGROUND WITH GRID & BLUR */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {C['bg']} !important;
        position: relative !important;
    }}
    
    /* Grid Background Pattern */
    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(to right, {C['border']} 1px, transparent 1px),
            linear-gradient(to bottom, {C['border']} 1px, transparent 1px);
        background-size: 40px 40px;
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
    }}
    
    /* Ensure content is above background effects */
    [data-testid="stVerticalBlock"] {{
        position: relative;
        z-index: 1;
    }}
    
    /* 2. TYPOGRAPHY - Clean & Minimal */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, p, div, label, span {{
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: {C['text']} !important;
        line-height: 1.5 !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: {C['text']} !important;
        line-height: 1.1 !important;
        text-transform: uppercase !important;
    }}
    
    h1 {{ font-size: 3.5rem !important; font-weight: 900 !important; }}
    h2 {{ font-size: 2rem !important; }}
    h3 {{ font-size: 1.25rem !important; letter-spacing: 0.1em !important; }}
    
    /* 3. GRID SYSTEM */
    .swiss-grid {{
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: 24px;
        margin: 24px 0;
    }}
    
    /* 4. BUTTONS - Geometric & Functional */
    .stButton>button {{
        background-color: {C['accent']} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        font-weight: 700 !important;
        padding: 20px 40px !important;
        letter-spacing: 0.15em !important;
        transition: all 0.2s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 8px 8px 0px {C['text']} !important;
    }}
    
    .stButton>button:active {{
        transform: translateY(0px) !important;
        box-shadow: 4px 4px 0px {C['text']} !important;
    }}
    
    /* Download Button - Transparent Swiss Style */
    .stDownloadButton>button {{
        background-color: transparent !important;
        color: {C['text']} !important;
        border: 2px solid {C['text']} !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        font-weight: 700 !important;
        padding: 20px 40px !important;
        letter-spacing: 0.15em !important;
        transition: all 0.3s ease !important;
    }}
    
    .stDownloadButton>button:hover {{
        background-color: {C['accent']} !important;
        color: #fff !important;
        border-color: {C['accent']} !important;
        transform: translateY(-2px) !important;
        box-shadow: 6px 6px 0px {C['text']} !important;
    }}
    
    .stDownloadButton>button:active {{
        transform: translateY(0px) !important;
        box-shadow: 3px 3px 0px {C['text']} !important;
    }}
    
    /* 5. INPUTS - Clean & Minimal */
    .stTextArea textarea, .stTextInput input {{
        background-color: {C['input_bg']} !important;
        color: {C['text']} !important;
        border: 2px solid {C['border']} !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
        padding: 16px !important;
        transition: border-color 0.2s ease !important;
    }}
    
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: {C['accent']} !important;
        outline: none !important;
    }}
    
    .stTextArea textarea::placeholder {{ 
        color: {C['sub_text']} !important; 
        font-style: italic !important;
    }}

    /* 6. HEADER - Asymmetric Layout */
    .swiss-header {{
        background-color: {C['header_bg']};
        padding: 6rem 2rem 4rem 2rem;
        position: relative;
        overflow: hidden;
    }}
    
    .swiss-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background-color: {C['accent']};
    }}
    
    .swiss-header::after {{
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background-color: {C['accent']};
        opacity: 0.1;
        clip-path: polygon(100% 0, 100% 100%, 0 100%);
    }}
    
    .swiss-header h1 {{ 
        color: {C['header_text']} !important; 
        margin: 0 !important;
        position: relative;
        z-index: 2;
    }}
    
    .swiss-header p {{ 
        color: {C['accent']} !important; 
        font-family: 'Courier New', monospace !important; 
        font-size: 0.875rem !important;
        letter-spacing: 0.2em !important;
        margin-top: 1rem !important;
        position: relative;
        z-index: 2;
    }}

    /* 7. METRIC BOX - Grid-based */
    .metric-box {{
        border: 3px solid {C['border']};
        background: {C['box_bg']};
        padding: 32px;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-box::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 60px;
        height: 60px;
        background-color: {C['accent']};
        opacity: 0.15;
    }}
    
    /* 8. COMPARISON BOXES - Asymmetric Design */
    .compare-box {{
        background-color: {C['box_bg']};
        border: 2px solid {C['border']};
        border-left: 6px solid {C['accent']};
        padding: 32px;
        font-family: 'JetBrains Mono', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.875rem !important;
        height: 450px;
        overflow-y: auto;
        color: {C['text']};
        position: relative;
        line-height: 1.9 !important;
        font-weight: 400 !important;
    }}
    
    .compare-box::-webkit-scrollbar {{
        width: 8px;
    }}
    
    .compare-box::-webkit-scrollbar-track {{
        background: {C['bg']};
    }}
    
    .compare-box::-webkit-scrollbar-thumb {{
        background: {C['accent']};
        border-radius: 0px;
    }}
    
    /* 9. HIGHLIGHT - Swiss Yellow */
    .highlight {{
        background-color: #FFE600;
        color: #000;
        padding: 3px 6px;
        font-weight: 600;
        border-left: 3px solid #000;
    }}
    
    /* 10. SECTION HEADERS */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 48px 0 24px 0;
    }}
    
    .section-number {{
        background-color: {C['accent']};
        color: #fff;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.25rem;
    }}
    
    /* 11. DIVIDERS - Geometric */
    hr {{
        border: none !important;
        height: 2px !important;
        background-color: {C['border']} !important;
        margin: 32px 0 !important;
    }}
    
    /* 12. RADIO & SELECT - Minimal */
    .stRadio > div {{
        gap: 24px !important;
    }}
    
    .stRadio label {{
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-size: 0.875rem !important;
    }}
    
    .stSelectbox label {{
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-size: 0.875rem !important;
    }}
    
    /* 13. GEOMETRIC ACCENTS */
    .geo-square {{
        width: 24px;
        height: 24px;
        background-color: {C['accent']};
        display: inline-block;
        margin-right: 12px;
    }}
    
    .geo-line {{
        width: 100%;
        height: 4px;
        background-color: {C['accent']};
        margin: 24px 0;
    }}
    
    /* 14. CARDS */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
        gap: 24px !important;
    }}
    
    /* 15. TOGGLE SWITCH */
    .stCheckbox {{
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }}

    .metric-label {{
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.1em;
        opacity: 0.6;
    }}

    .comparison-text {{
        font-family: 'Georgia', serif;
        line-height: 1.6;
        padding: 20px;
        background: {C['input_bg']};
        height: 400px;
        overflow-y: auto;
        border: 1px solid {C['border']};
    }}

    .highlight-red {{
        background-color: {C['accent']};
        color: #FFFFFF !important;
        padding: 2px 0;
    }}
    
    /* FILE UPLOADER - Swiss Style */
    [data-testid="stFileUploader"] {{
        background-color: {C['bg']} !important;
        border: 2px dashed {C['border']} !important;
        border-radius: 0px !important;
        padding: 32px !important;
    }}
    
    [data-testid="stFileUploader"] section {{
        background-color: {C['input_bg']} !important;
        border: 2px solid {C['border']} !important;
        border-radius: 0px !important;
        padding: 24px !important;
    }}
    
    [data-testid="stFileUploader"] section > div {{
        color: {C['text']} !important;
    }}
    
    [data-testid="stFileUploader"] button {{
        background-color: transparent !important;
        color: {C['text']} !important;
        border: 2px solid {C['text']} !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }}
    
    [data-testid="stFileUploader"] button:hover {{
        background-color: {C['accent']} !important;
        color: #fff !important;
        border-color: {C['accent']} !important;
    }}
    
    /* PROGRESS BAR OVERRIDE */
    div[data-testid="stProgressBar"] > div {{
        height: 1rem !important;
        background-color: {C['bar_bg']} !important;
    }}
    div[data-testid="stProgressBar"] > div > div {{
        background-color: {C['accent']} !important;
    }}
    
</style>
""", unsafe_allow_html=True)

# Cursor-following blur effect
st.components.v1.html("""
<script>
(function() {
    const parentDoc = window.parent.document;
    
    // Remove any existing blur
    const existing = parentDoc.getElementById('cursor-blur');
    if (existing) existing.remove();
    
    // Create blur element
    const blur = parentDoc.createElement('div');
    blur.id = 'cursor-blur';
    blur.style.cssText = `
        position: fixed;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(139, 0, 0, 0.5) 0%, rgba(178, 34, 34, 0.3) 30%, transparent 70%);
        filter: blur(120px);
        pointer-events: none;
        z-index: 0;
        transform: translate(-50%, -50%);
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    parentDoc.body.appendChild(blur);
    
    let mouseX = 0, mouseY = 0;
    let currentX = 0, currentY = 0;
    
    parentDoc.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        blur.style.opacity = '1';
    });
    
    parentDoc.addEventListener('mouseleave', () => {
        blur.style.opacity = '0';
    });
    
    function animate() {
        currentX += (mouseX - currentX) * 0.15;
        currentY += (mouseY - currentY) * 0.15;
        blur.style.left = currentX + 'px';
        blur.style.top = currentY + 'px';
        requestAnimationFrame(animate);
    }
    animate();
})();
</script>
""", height=0)

# --- 5. LOGIC CORE ---
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

def vectorize(texts):
    return TfidfVectorizer().fit_transform(texts).toarray()

def similarity(doc1, doc2):
    return cosine_similarity([doc1], [doc2])[0][0]

def get_common_sentences(text1, text2, threshold=0.65):
    # Split by simple punctuation
    s1 = [s.strip() for s in re.split(r'[.!?]+', text1) if len(s.strip()) > 20]
    s2 = [s.strip() for s in re.split(r'[.!?]+', text2) if len(s.strip()) > 20]
    
    if not s1 or not s2: return []
    
    try:
        vectorizer = TfidfVectorizer()
        all_s = s1 + s2
        vectors = vectorizer.fit_transform(all_s)
        
        v1 = vectors[:len(s1)]
        v2 = vectors[len(s1):]
        
        matches = []
        for i, sent1 in enumerate(s1):
            for j, sent2 in enumerate(s2):
                sim = cosine_similarity(v1[i:i+1], v2[j:j+1])[0][0]
                if sim >= threshold:
                    matches.append((sent1, sent2, round(sim, 3)))
        
        # Sort by similarity score descending
        return sorted(matches, key=lambda x: x[2], reverse=True)[:50]
    except:
        return []

def highlight_text(text, sentences, is_first=True):
    result = text
    idx = 0 if is_first else 1
    # Simple replacement strategy (Note: This is basic and might overlap in complex cases)
    for pair in sentences:
        sent = pair[idx]
        if sent in result:
            result = result.replace(sent, f'<span class="highlight-red">{sent}</span>')
    return result

# --- 6. UI LAYOUT ---

# Header
st.markdown("""
<div class="swiss-header">
    <div style="max-width: 100%; margin: 0 auto;">
        <h1>PLAGIARISM<br>DETECTOR</h1>
        <p>/// SENTENCE-LEVEL SIMILARITY ANALYSIS ///</p>
    </div>
</div>
""", unsafe_allow_html=True)


# Main Content
if not st.session_state.analyzed:
    # --- INPUT MODE ---
    
    # Section 01: Input Data
    st.markdown("""
    <div class="section-header">
        <div class="section-number">01</div>
        <h3 style="margin:0;">INPUT DATA</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="geo-line"></div>', unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.radio(
        "SELECT INPUT METHOD",
        ["PASTE TEXT", "UPLOAD FILES"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    texts = []
    names = []
    
    if input_method == "PASTE TEXT":
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("**DOCUMENT A**")
            text_a = st.text_area("Input A", height=400, placeholder="Paste text here...", label_visibility="collapsed")
        
        with col2:
            st.markdown("**DOCUMENT B**")
            text_b = st.text_area("Input B", height=400, placeholder="Paste text here...", label_visibility="collapsed")
        
        if text_a and text_b:
            texts = [text_a, text_b]
            names = ["Document A", "Document B"]
    
    else:  # UPLOAD FILES
        st.markdown("**UPLOAD TEXT FILES**")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                content = file.read().decode("utf-8", errors="ignore")
                texts.append(content)
                names.append(file.name)
            
            st.success(f"✓ Loaded {len(texts)} file(s)")

    # Action Bar
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(texts) >= 2:
        if st.button("⚡ RUN PLAGIARISM ANALYSIS", use_container_width=True):
            with st.spinner("ANALYZING DOCUMENTS..."):
                # Vectorize all texts
                vecs = vectorize(texts)
                results = []
                
                # Compare all pairs
                for i in range(len(texts)):
                    for j in range(i + 1, len(texts)):
                        sim_score = similarity(vecs[i], vecs[j])
                        
                        if sim_score > 0.7:
                            risk = "CRITICAL"
                        elif sim_score > 0.4:
                            risk = "MODERATE"
                        else:
                            risk = "LOW"
                        
                        results.append({
                            "a": names[i],
                            "b": names[j],
                            "score": sim_score,
                            "risk": risk,
                            "text_a": texts[i],
                            "text_b": texts[j]
                        })
                
                st.session_state.results = results
                st.session_state.analyzed = True
                st.rerun()
    elif len(texts) == 1:
        st.warning("⚠ Please provide at least 2 documents for comparison")
    else:
        st.info("ℹ Please input documents to begin analysis")

else:
    # --- REPORT MODE ---
    results = st.session_state.results
    
    # Pair selector if multiple results
    if len(results) > 1:
        st.markdown(f"""
        <div style="background: {C['input_bg']}; padding: 16px; border-left: 4px solid {C['accent']}; margin-bottom: 24px;">
            <span style="font-size: 12px; font-weight: 700; letter-spacing: 1px; color: {C['sub_text']};">
                MULTIPLE COMPARISONS DETECTED
            </span>
            <div style="font-size: 14px; margin-top: 8px;">
                Found {len(results)} pair(s) to analyze. Select a pair below to view detailed results.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create selector options
        pair_options = [f"{r['a']} ↔ {r['b']}" for r in results]
        selected_pair = st.selectbox(
            "SELECT COMPARISON PAIR",
            pair_options,
            label_visibility="collapsed"
        )
        
        # Get selected result
        selected_index = pair_options.index(selected_pair)
        res = results[selected_index]
    else:
        res = results[0]
    
    # Determine risk color based on score
    if res['score'] > 0.7:
        risk_color = "#c0392b"  # Dark red for critical
        risk_label = "CRITICAL"
    elif res['score'] > 0.4:
        risk_color = "#f39c12"  # Orange for moderate
        risk_label = "MODERATE"
    else:
        risk_color = "#27ae60"  # Green for low
        risk_label = "LOW"
    
    # Section 02: Analysis Report
    st.markdown("""
    <div class="section-header">
        <div class="section-number">02</div>
        <h3 style="margin:0;">ANALYSIS REPORT</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="geo-line"></div>', unsafe_allow_html=True)
    
    # Metrics Display with Colored Progress Bar
    st.markdown(f"""
    <div class="metric-box">
        <div style="display:flex; justify-content:space-between; margin-bottom: 24px;">
            <div>
                <span style="font-size:12px; font-weight:700; color:{C['sub_text']}; letter-spacing:1px;">SIMILARITY SCORE</span>
                <div style="font-size:48px; font-weight:900; line-height:1; margin-top: 8px;">{res['score']*100:.1f}%</div>
            </div>
            <div style="text-align:right;">
                <span style="font-size:12px; font-weight:700; color:{C['sub_text']}; letter-spacing:1px;">RISK LEVEL</span>
                <div style="font-size:32px; font-weight:900; color:{risk_color}; margin-top: 8px;">{risk_label}</div>
            </div>
        </div>
        <div style="width:100%; height:24px; background-color:{C['bar_bg']}; margin-top:20px; border:2px solid {C['border']}; position: relative; overflow: hidden;">
            <div style="width:{res['score']*100}%; height:100%; background-color:{risk_color}; transition: width 0.5s ease;"></div>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    # Reset Button
    col_reset1, col_reset2 = st.columns([4, 1])
    with col_reset2:
        if st.button("⟲ NEW SCAN", use_container_width=True):
            st.session_state.analyzed = False
            st.rerun()
    
    # Section 03: Text Comparison
    st.markdown("""
    <div class="section-header">
        <div class="section-number">03</div>
        <h3 style="margin:0;">TEXT COMPARISON</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="geo-line"></div>', unsafe_allow_html=True)
    
    common_sents = get_common_sentences(res['text_a'], res['text_b'])
    
    comp1, comp2 = st.columns(2, gap="large")
    
    with comp1:
        st.markdown("**DOCUMENT A**")
        safe_html_a = highlight_text(res['text_a'], common_sents, True)
        st.markdown(f'<div class="compare-box">{safe_html_a}</div>', unsafe_allow_html=True)
        
    with comp2:
        st.markdown("**DOCUMENT B**")
        safe_html_b = highlight_text(res['text_b'], common_sents, False)
        st.markdown(f'<div class="compare-box">{safe_html_b}</div>', unsafe_allow_html=True)

    # Section 04: Export
    st.markdown("""
    <div class="section-header">
        <div class="section-number">04</div>
        <h3 style="margin:0;">EXPORT DATA</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.download_button(
        "⬇ DOWNLOAD CSV REPORT", 
        pd.DataFrame(st.session_state.results).to_csv().encode(), 
        "plagiarism_report.csv", 
        "text/csv",
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Reset button at the end
    if st.button("⟲ RUN NEW ANALYSIS", use_container_width=True, type="secondary"):
        st.session_state.analyzed = False
        st.rerun()