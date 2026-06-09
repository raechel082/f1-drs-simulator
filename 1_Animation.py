import streamlit as st
import base64

# ========================
# PAGE CONFIG — MUST BE FIRST STREAMLIT CALL
# ========================
st.set_page_config(
    page_title="DRS Rear Wing Animation",
    layout="wide",
    page_icon="🏎️"
)

# ========================
# PITCH BLACK EMISSION PALETTE
# ========================
PRIMARY = "#00F5FF"      # Vivid Cyan Glow Accent
SECONDARY = "#FF007F"    # Vivid Magenta Glow Accent
BG = "#000000"           # Absolute Pitch Black

# ========================
# FIA TELEMETRY MARQUEE TICKER
# ========================
st.markdown(f"""
<div style="
overflow:hidden;
white-space:nowrap;
padding:10px;
border:1px solid {PRIMARY}aa;
box-shadow: 0 0 15px {PRIMARY}44;
border-radius:12px;
margin-bottom:25px;
">
    <div style="
    display:inline-block;
    animation: scroll 18s linear infinite;
    font-weight:bold;
    ">
    🏁 ACTIVE AERO SYSTEM • REAR WING CONTROL • DRS READY • REAL TIME VISUALIZATION 
    </div>
</div>

<style>
@keyframes scroll {{
    0% {{transform:translateX(100%);}}
    100% {{transform:translateX(-100%);}}
}}
</style>
""", unsafe_allow_html=True)

# ========================
# GLOBAL SIMULATOR AESTHETICS (CSS)
# ========================
st.markdown(f"""
<style>

/* ABSOLUTE PITCH BLACK BACKGROUND */
.stApp {{
    background: #000000 !important;
    color: #FFFFFF;
    overflow-x: hidden;
    background-image: none !important;
}}

/* SCANLINE OVERLAY */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.008),
        rgba(255, 255, 255, 0.008) 1px,
        transparent 1px,
        transparent 4px
    );
    pointer-events: none;
    z-index: 999;
}}

/* SIDEBAR ABSOLUTE BLACK (BLANK) */
section[data-testid="stSidebar"] {{
    background-color: #000000 !important;
    background: #000000 !important;
    border-right: 1px solid #111111 !important;
    box-shadow: none !important;
}}

/* NEON TITLE AND SUBTITLE */
.title-glow {{
    font-size: 56px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, {PRIMARY}, #FFFFFF, {SECONDARY}, {PRIMARY});
    background-size: 300% auto;
    color: transparent;
    -webkit-background-clip: text;
    animation: shine 5s linear infinite;
    margin-bottom: 0px;
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
}}

@keyframes shine {{
    to {{ background-position: 300% center; }}
}}

.subtitle-glow {{
    text-align: center;
    color: #888888;
    font-size: 20px;
    margin-top: -10px;
    margin-bottom: 30px;
}}

/* SUBHEADINGS */
h2 {{
    color: #FFFFFF !important;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}}

/* PROGRESS BAR */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
    box-shadow: 0 0 15px {PRIMARY};
}}

/* STEALTH BLACK SLIDER STYLING */
.stSlider [data-baseweb="slider"] > div {{
    background-color: #111111 !important;
    border: 1px solid #222222;
    height: 8px !important;
    border-radius: 4px;
}}

.stSlider [data-baseweb="slider"] > div > div {{
    background: linear-gradient(90deg, #000000, {PRIMARY}) !important;
    box-shadow: 0 0 12px {PRIMARY}aa;
}}

.stSlider [role="slider"] {{
    background-color: #000000 !important;
    border: 2px solid {PRIMARY} !important;
    box-shadow: 0 0 8px {PRIMARY}88;
    width: 20px !important;
    height: 20px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.stSlider [role="slider"]:hover, 
.stSlider [role="slider"]:focus {{
    transform: scale(1.2);
    border-color: {SECONDARY} !important;
    box-shadow: 0 0 15px {SECONDARY} !important;
}}

.stSlider [data-testid="stWidgetLabel"],
.stSlider [data-baseweb="slider"] div {{
    color: #888888 !important;
    font-family: monospace;
}}

/* STREAMLIT INFO BOX CUSTOMIZATION */
div[data-testid="stInfo"] {{
    background-color: #0a0a0a !important;
    color: #FFFFFF !important;
    border: 1px solid #1c1c1c !important;
}}

</style>
""", unsafe_allow_html=True)

# ========================
# MAIN APP TITLE
# ========================
st.markdown(f"""
<h1 class="title-glow">🎬 DRS Rear Wing Animation</h1>
<p class="subtitle-glow">
Aerodynamic flap opening and closing visualization
</p>
""", unsafe_allow_html=True)

# ========================
# READ VIDEO
# ========================
try:
    with open("40s.mp4", "rb") as video_file:
        video_bytes = video_file.read()
    video_base64 = base64.b64encode(video_bytes).decode()
except FileNotFoundError:
    video_base64 = ""

# ========================
# VIDEO HTML WITH INTENSIFIED GLOW
# ========================
if video_base64:
    video_html = f"""
    <div style="display:flex; justify-content:center; padding: 20px 0;">
        <video
            id="drsVideo"
            width="620"
            muted
            style="
            border-radius:20px;
            border:2px solid {PRIMARY};
            /* HIGH-INTENSIFIED MULTI-LAYERING NEON GLOW FRAME */
            box-shadow: 
                0 0 20px {PRIMARY}99, 
                0 0 50px {PRIMARY}44, 
                0 0 80px {SECONDARY}22;
            display: block;
            ">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
    </div>

    <script>
    const video = document.getElementById('drsVideo');
    function playLoop() {{
        video.play();
        video.onended = () => {{
            setTimeout(() => {{
                video.currentTime = 0;
                video.play();
            }}, 2000);
        }};
    }}
    playLoop();
    </script>
    """
    st.components.v1.html(video_html, height=480)
else:
    st.warning("⚠️ 40s.mp4 video file not found. Place it in the working directory to view animation.")

# ========================
# DESCRIPTION
# ========================
st.markdown("## 🧠 Animation Insight")
st.info("""
This animation visualizes the active aerodynamic rear wing system of a Formula 1 car.

• Closed flap → higher downforce for cornering grip

• Open flap (DRS active) → lower drag for maximum straight-line speed

The rear flap rotates about its hinge axis to dynamically modify airflow behavior and aerodynamic efficiency.
""")

# ========================
# FOOTER
# ========================
st.markdown(f"""
<hr style="border:1px solid #111111">
<div style="text-align:center; padding:20px; color: #444444;">
🏎️ Formula 1 Active Aerodynamics Animation Matrix
<br><br>

</div>
""", unsafe_allow_html=True)