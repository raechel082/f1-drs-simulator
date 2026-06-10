import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="DRS Simulator",
    layout="wide",
    page_icon="🏎️"
)

# ========================
# SIDEBAR
# ========================
st.sidebar.markdown("## ⚙️ Control Panel")

# ========================
# TEAM THEME SELECTOR
# ========================
st.sidebar.markdown("### 🎨 F1 Team Theme")

team_theme = st.sidebar.selectbox(
    "Select Team Theme",
    [
        "Mercedes", "Ferrari", "Red Bull Racing", "McLaren",
        "Aston Martin", "Alpine", "Williams", "Haas",
        "Racing Bulls", "Sauber"
    ]
)

themes = {
    "Mercedes":          {"primary": "#00E6CC", "secondary": "#00F5FF", "bg": "#040D14"},
    "Ferrari":           {"primary": "#FF1E00", "secondary": "#FF6600", "bg": "#120002"},
    "Red Bull Racing":   {"primary": "#004BFF", "secondary": "#FFCC00", "bg": "#02050D"},
    "McLaren":           {"primary": "#FF7B00", "secondary": "#FFB700", "bg": "#0F0600"},
    "Aston Martin":      {"primary": "#008765", "secondary": "#CCFF00", "bg": "#020B08"},
    "Alpine":            {"primary": "#FF33B5", "secondary": "#0099FF", "bg": "#05020B"},
    "Williams":          {"primary": "#00A2FF", "secondary": "#00E1FF", "bg": "#010612"},
    "Haas":              {"primary": "#E60000", "secondary": "#FFFFFF", "bg": "#0A0A0A"},
    "Racing Bulls":      {"primary": "#1A52FF", "secondary": "#FFEC40", "bg": "#020614"},
    "Sauber":            {"primary": "#00FF44", "secondary": "#AAFF00", "bg": "#010602"},
}
theme   = themes[team_theme]
PRIMARY   = theme["primary"]
SECONDARY = theme["secondary"]
BG        = theme["bg"]

# ========================
# STYLESHEET
# ========================
st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        radial-gradient(circle at top left, {PRIMARY}33, transparent 30%),
        radial-gradient(circle at bottom right, {SECONDARY}20, transparent 35%),
        linear-gradient(to bottom, #020202, {BG});
    background-size: cover, 40px 40px, 40px 40px, cover, cover, cover;
    color: white;
    animation: ambientGlow 8s ease infinite alternate;
    overflow-x: hidden;
}}
.stApp::before {{
    content: "";
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        rgba(255,255,255,0.015), rgba(255,255,255,0.015) 1px,
        transparent 1px, transparent 3px
    );
    pointer-events: none; z-index: 999;
    animation: scanMove 8s linear infinite;
}}
@keyframes scanMove {{ from {{ transform: translateY(0px); }} to {{ transform: translateY(10px); }} }}
.stApp::after {{
    content: "";
    position: fixed; inset: 0;
    background-image:
        radial-gradient({PRIMARY}99 1px, transparent 1px),
        radial-gradient({SECONDARY}66 1px, transparent 1px);
    background-size: 120px 120px;
    animation: particles 18s linear infinite;
    opacity: 0.12; pointer-events: none;
}}
@keyframes particles {{ from {{ transform: translateY(0px); }} to {{ transform: translateY(-120px); }} }}
@keyframes ambientGlow {{ 0% {{ filter: brightness(0.95); }} 100% {{ filter: brightness(1.08); }} }}
section[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.92);
    border-right: 1px solid {PRIMARY}aa;
    box-shadow: 0 0 25px {PRIMARY}33;
}}
.title {{
    font-size: 72px; font-weight: 900; text-align: center;
    background: linear-gradient(90deg, {PRIMARY}, white, {SECONDARY}, {PRIMARY});
    background-size: 300% auto;
    color: transparent; -webkit-background-clip: text;
    animation: shine 5s linear infinite, titleGlow 2s ease-in-out infinite alternate;
    margin-bottom: 0px;
}}
@keyframes shine {{ to {{ background-position: 300% center; }} }}
@keyframes titleGlow {{
    from {{ text-shadow: 0 0 10px {PRIMARY}88; }}
    to   {{ text-shadow: 0 0 20px {SECONDARY}88; }}
}}
.subtitle {{
    text-align: center; color: rgba(255,255,255,0.75);
    font-size: 20px; margin-top: -10px; margin-bottom: 30px;
}}
.card {{
    position: relative;
    background: rgba(12,19,33,0.85);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 10px 14px;
    border-radius: 12px;
    border: 2px solid {PRIMARY}aa;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
    margin: 6px 0px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.6), 0 0 15px {PRIMARY}44, 0 0 30px {SECONDARY}15;
}}
.card:hover {{
    transform: translateY(-4px);
    background: rgba(18,28,48,0.95);
    border-color: {PRIMARY};
    box-shadow: 0 10px 25px rgba(0,0,0,0.7), 0 0 30px {PRIMARY}, 0 0 15px {SECONDARY};
}}
.card h4 {{
    color: rgba(255,255,255,0.9); margin: 0;
    font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; font-size: 14.5px;
}}
.card h2 {{
    color: white; font-size: 33px;
    margin: 6px 0 0 0; font-weight: 800;
    text-shadow: 0 0 12px {PRIMARY}aa;
}}
h3 {{ color: {PRIMARY} !important; text-shadow: 0 0 12px {PRIMARY}; margin-top: 25px; }}
.stSlider {{ padding: 10px 4px 20px 4px !important; }}
.stSlider > div > div > div > div {{
    background: linear-gradient(90deg, {PRIMARY}, {SECONDARY}) !important;
    box-shadow: 0 0 6px {PRIMARY}44 !important;
}}
.stSlider [role="slider"] {{
    background-color: white !important;
    border: 2px solid {PRIMARY} !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5) !important;
    width: 20px !important; height: 20px !important;
    transition: transform 0.1s ease;
}}
.stSlider [role="slider"]:hover {{ transform: scale(1.15); }}
[data-testid="stSelectbox"] {{ padding: 8px 6px !important; }}
.stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(0,0,0,0.5); border-radius: 14px;
    border: 2px solid {PRIMARY}bb;
    box-shadow: 0 0 18px {PRIMARY}55;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}}
.stSelectbox div[data-baseweb="select"]:focus-within {{
    border-color: {PRIMARY} !important;
    box-shadow: 0 0 25px {PRIMARY}ff, 0 0 10px {SECONDARY}aa !important;
}}
.stProgress {{ padding: 10px 0px !important; }}
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
    box-shadow: 0 0 20px {PRIMARY};
    height: 12px !important;
}}
.js-plotly-plot {{
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 35px {PRIMARY}33;
}}
.stButton button {{
    border-radius: 12px; border: 2px solid {PRIMARY}aa;
    background: rgba(255,255,255,0.05); color: white;
    box-shadow: 0 0 15px {PRIMARY}33; transition: 0.2s;
}}
.stButton button:hover {{
    transform: translateY(-2px); border-color: {PRIMARY};
    box-shadow: 0 0 20px {PRIMARY}bb, 0 0 30px {SECONDARY}44;
}}
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-thumb {{
    background: {PRIMARY}bb; border-radius: 10px;
    box-shadow: 0 0 10px {PRIMARY};
}}
</style>
""", unsafe_allow_html=True)

# ========================
# OPTIONAL BACKGROUND IMAGE
# ========================
def set_bg(file):
    try:
        with open(file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.94)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

set_bg("f1.jpg")

# ========================
# MARQUEE TICKER
# ========================
st.markdown(f"""
<div style="overflow:hidden;white-space:nowrap;padding:10px;border:1px solid {PRIMARY}aa;
box-shadow:0 0 15px {PRIMARY}44;border-radius:12px;margin-bottom:25px;">
    <div style="display:inline-block;animation:scroll 18s linear infinite;font-weight:bold;">
    🏁 ACTIVE AERO SYSTEM • REAR WING CONTROL • DRS READY • REAL TIME VISUALIZATION
    </div>
</div>
<style>
@keyframes scroll {{ 0% {{transform:translateX(100%);}} 100% {{transform:translateX(-100%);}} }}
</style>
""", unsafe_allow_html=True)

# ========================
# TITLE
# ========================
st.markdown(f"""
<h1 class="title">🏎️ DRS Aero Simulator</h1>
<p class="subtitle">Active Aerodynamic Rear Wing System</p>
""", unsafe_allow_html=True)

st.info(
    "This model simulates aerodynamic trade-offs between drag reduction and downforce "
    "using a parametric DRS rear wing system."
)

# ========================
# SIDEBAR INPUTS
# ========================
speed   = st.sidebar.slider("Speed (m/s)",            0,   100,  60)
angle   = st.sidebar.slider("Flap Angle (°)",          0,    40,  20)
A       = st.sidebar.slider("Wing Area (m²)",         0.3,  0.7, 0.45)
Cd_base = st.sidebar.slider("Base Drag Coefficient",  0.1,  1.0,  0.5)
rho     = st.sidebar.slider("Air Density (kg/m³)",    0.8,  1.5, 1.23)

# ========================
# REAR WING GEOMETRY
# ========================
st.sidebar.markdown("### 🛠️ Rear Wing Geometry (Derived)")
wing_span  = st.sidebar.slider("Wing Span (m)",  0.8, 1.2, 1.0)
wing_chord = st.sidebar.slider("Wing Chord (m)", 0.2, 0.4, 0.3)
A_geom = wing_span * wing_chord
st.sidebar.caption(f"Derived Wing Area: {A_geom:.2f} m²")
use_geom = st.sidebar.checkbox("Use Geometry-Based Wing Area", value=False)
A_used = A_geom if use_geom else A

# ========================
# CAR DIMENSIONS
# ========================
st.sidebar.markdown("### 🏎️ Car Dimensions")
car_length = st.sidebar.selectbox("Car Length",
    ["5.2 m (Compact)", "5.5 m (Standard F1)", "5.8 m (Extended)"])
car_width = st.sidebar.selectbox("Car Width",
    ["1.9 m (Narrow)", "2.0 m (Standard F1)", "2.1 m (Wide)"])

length_map = {"5.2 m (Compact)": 5.2, "5.5 m (Standard F1)": 5.5, "5.8 m (Extended)": 5.8}
width_map  = {"1.9 m (Narrow)": 1.9, "2.0 m (Standard F1)": 2.0, "2.1 m (Wide)": 2.1}
L = length_map[car_length]
W = width_map[car_width]

# ========================
# DRS TOGGLE  (captured early so we can branch physics cleanly)
# ========================
DRS_ON = st.sidebar.toggle("Activate DRS", value=False)

# ========================
# AERODYNAMIC PHYSICS
#
# We keep the USER's selected angle as the "DRS OFF" baseline.
# When DRS is ON the flap opens by ~12° (angle drops by 12, floored at 0°).
# All forces are computed separately for both states so DRS impact is real.
# ========================

angle_off = float(angle)                        # DRS OFF  → user-selected angle
angle_on  = max(float(angle) - 12.0, 0.0)      # DRS ON   → flap partially open

def wing_Cl(a):
    """Non-linear lift coefficient with stall beyond 32°."""
    cl = 0.9 + 0.05 * a - 0.0008 * a**2
    if a > 32:
        cl -= 0.03 * (a - 32)
    return max(cl, 0.0)

def wing_Cd(a):
    """Non-linear drag coefficient."""
    return Cd_base + 0.012 * a + 0.0004 * a**2

# --- Active angle (what the car is running right now) ---
angle_active = angle_on if DRS_ON else angle_off

Cl_active = wing_Cl(angle_active)
Cd_active = wing_Cd(angle_active)

drag_wing   = 0.5 * rho * A_used * Cd_active * speed**2
downforce_rear = 0.5 * rho * A_used * Cl_active * speed**2
efficiency  = Cl_active / Cd_active if Cd_active > 0 else 0.0

# --- Body drag (independent of DRS) ---
A_body  = 1.5
Cd_body = 0.32
drag_body  = 0.5 * rho * A_body * Cd_body * speed**2
drag_total = drag_wing + drag_body

# --- Ground-effect floor (independent of DRS) ---
Cl_floor = 3.2 + 0.004 * speed
A_floor  = 1.6
downforce_floor = 0.5 * rho * A_floor * Cl_floor * speed**2
downforce = downforce_floor + downforce_rear

# --- DRS impact: compare DRS OFF vs DRS ON at the current speed ---
Cl_drs_off = wing_Cl(angle_off)
Cd_drs_off = wing_Cd(angle_off)
Cl_drs_on  = wing_Cl(angle_on)
Cd_drs_on  = wing_Cd(angle_on)

drag_drs_off      = 0.5 * rho * A_used * Cd_drs_off * speed**2
drag_drs_on       = 0.5 * rho * A_used * Cd_drs_on  * speed**2
downforce_drs_off = 0.5 * rho * A_used * Cl_drs_off * speed**2
downforce_drs_on  = 0.5 * rho * A_used * Cl_drs_on  * speed**2

drag_saving     = drag_drs_off - drag_drs_on
drag_saving_pct = (drag_saving / drag_drs_off * 100) if drag_drs_off > 0 else 0.0
df_loss         = downforce_drs_off - downforce_drs_on

# --- Drag contribution percentages ---
wing_pct = (drag_wing  / drag_total * 100) if drag_total > 0 else 0.0
body_pct = (drag_body  / drag_total * 100) if drag_total > 0 else 0.0

# --- Performance Index ---
eff_norm  = efficiency / 3
drag_norm = drag_total / 5000
PerformanceIndex = (eff_norm * 70) - (drag_norm * 30)

pi_color = (
    "#00ff9f" if PerformanceIndex > 60
    else "#ffd700" if PerformanceIndex > 40
    else "#ff4b4b"
)

# ========================
# PERFORMANCE OVERVIEW
# ========================
st.markdown("### ⚡ Performance Overview")
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div class='card'><h4>Wing Drag</h4><h2>{drag_wing:.0f} N</h2></div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class='card'><h4>Total Downforce</h4><h2>{downforce:.0f} N</h2></div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class='card'><h4>Efficiency (L/D)</h4><h2>{efficiency:.2f}</h2></div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class='card'>
<h4 style="color:{pi_color}">Performance Index</h4>
<h2>{PerformanceIndex:.1f}</h2>
</div>
""", unsafe_allow_html=True)

# ========================
# LIVE SPEEDOMETER
# ========================
st.markdown("")
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=speed * 3.6,
    title={"text": "Vehicle Speed (km/h)"},
    gauge={
        "axis": {"range": [0, 360]},
        "bar": {"color": PRIMARY},
        "steps": [
            {"range": [0, 150],   "color": "#161b26"},
            {"range": [150, 220], "color": "#222b3d"},
            {"range": [220, 300], "color": "#3d141a"},
        ],
    }
))
gauge.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    height=350,
    font=dict(color="white")
)
st.plotly_chart(gauge, use_container_width=True)

# ========================
# DRAG BREAKDOWN
# ========================
st.markdown("### 🏎️ Drag Breakdown")
b1, b2, b3 = st.columns(3)

b1.markdown(f"""
<div class='card'><h4>Wing Drag</h4><h2>{drag_wing:.0f} N</h2></div>
""", unsafe_allow_html=True)

b2.markdown(f"""
<div class='card'><h4>Body Drag</h4><h2>{drag_body:.0f} N</h2></div>
""", unsafe_allow_html=True)

b3.markdown(f"""
<div class='card'><h4>Total Drag</h4><h2>{drag_total:.0f} N</h2></div>
""", unsafe_allow_html=True)

# ========================
# DRAG CONTRIBUTION %
# ========================
st.markdown("### 📊 Drag Contribution")
p1, p2 = st.columns(2)

p1.markdown(f"""
<div class='card'><h4>Wing %</h4><h2>{wing_pct:.1f}%</h2></div>
""", unsafe_allow_html=True)

p2.markdown(f"""
<div class='card'><h4>Body %</h4><h2>{body_pct:.1f}%</h2></div>
""", unsafe_allow_html=True)

# ========================
# SYSTEM STATUS
# ========================
st.markdown("### ⚙️ System Status")

mode_label = "LOW DRAG CONFIGURATION" if DRS_ON else "HIGH DOWNFORCE CONFIGURATION"
if DRS_ON:
    st.success(f"🟢 🟢 🟢 DRS ACTIVE — {mode_label}  |  Effective flap angle: {angle_on:.0f}°")
else:
    st.info(f"🔵 🔵 🔵 DRS INACTIVE — {mode_label}  |  Flap angle: {angle_off:.0f}°")

if speed == 0:
    st.warning("⚠️ Vehicle stationary — aerodynamic forces are zero")

if angle_active > 32:
    st.warning("⚠️ Rear wing approaching stall region")

if efficiency < 1.5:
    st.warning("⚠️ Aerodynamic efficiency is low")

# ========================
# DRS IMPACT
# ========================
st.markdown("### 🚀 DRS Impact")
d1, d2, d3 = st.columns(3)

d1.markdown(f"""
<div class='card'><h4>Drag Saving</h4><h2>{drag_saving:.0f} N</h2></div>
""", unsafe_allow_html=True)

d2.markdown(f"""
<div class='card'><h4>Drag Reduction</h4><h2>{drag_saving_pct:.1f}%</h2></div>
""", unsafe_allow_html=True)

d3.markdown(f"""
<div class='card'><h4>Downforce Loss</h4><h2>{df_loss:.0f} N</h2></div>
""", unsafe_allow_html=True)

# ========================
# GRAPH 1: Drag vs Speed — DRS OFF vs ON
# ========================
speed_range    = np.linspace(0, 350, 300)
speed_ms_range = speed_range / 3.6

drag_off_curve = 0.5 * rho * A_used * Cd_drs_off * speed_ms_range**2
drag_on_curve  = 0.5 * rho * A_used * Cd_drs_on  * speed_ms_range**2

# Current operating point (wing drag at active angle)
current_drag_point = 0.5 * rho * A_used * Cd_active * speed**2

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=speed_range, y=drag_off_curve,
    name=f"DRS OFF ({angle_off:.0f}°)",
    line=dict(color="#00d4ff", width=3)
))
fig1.add_trace(go.Scatter(
    x=speed_range, y=drag_on_curve,
    name=f"DRS ON  ({angle_on:.0f}°)",
    line=dict(color="#00ff9f", width=3)
))
fig1.add_trace(go.Scatter(
    x=[speed * 3.6],
    y=[current_drag_point],
    mode="markers",
    name="Current Point",
    marker=dict(size=12, color="#ff4b4b")
))

fig1.update_layout(
    template="plotly_dark",
    title="Drag vs Speed — DRS OFF vs ON",
    xaxis_title="Speed (km/h)",
    yaxis_title="Drag Force (N)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

# ========================
# GRAPH 2: Efficiency vs Flap Angle
# ========================
angles_arr = np.linspace(0, 40, 200)

Cl_arr = 0.9 + 0.05 * angles_arr - 0.0008 * angles_arr**2
stall_mask = angles_arr > 32
Cl_arr[stall_mask] -= 0.03 * (angles_arr[stall_mask] - 32)
Cd_arr  = Cd_base + 0.012 * angles_arr + 0.0004 * angles_arr**2
eff_arr = np.where(Cd_arr > 0, Cl_arr / Cd_arr, 0.0)

valid_region  = (angles_arr >= 8) & (angles_arr <= 32)
optimal_angle = angles_arr[valid_region][np.argmax(eff_arr[valid_region])]

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=angles_arr, y=eff_arr,
    name="L/D Efficiency",
    line=dict(color="#9aa8ff", width=3)
))
fig2.add_trace(go.Scatter(
    x=[angle_active],
    y=[efficiency],
    mode="markers",
    name=f"Active angle ({angle_active:.0f}°)",
    marker=dict(size=12, color=PRIMARY)
))
fig2.add_vline(
    x=optimal_angle,
    line_dash="dash",
    line_color=PRIMARY,
    annotation_text=f"Optimal ({optimal_angle:.1f}°)"
)

fig2.update_layout(
    template="plotly_dark",
    title="Efficiency vs Flap Angle",
    xaxis_title="Flap Angle (°)",
    yaxis_title="L/D Efficiency",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# ========================
# REAR WING FLAP VISUALIZATION
# ========================
st.markdown("### 🛠️ Rear Wing Flap Visualization")
st.progress(angle_active / 40)

if angle_active < 12:
    aero_mode = "Low Downforce Setup"
elif angle_active < 22:
    aero_mode = "Balanced Setup"
elif angle_active < 32:
    aero_mode = "High Downforce Setup"
else:
    aero_mode = "Near Stall Region"

drs_tag = " (DRS Active)" if DRS_ON else ""
st.caption(f"Flap Angle: {angle_active:.0f}°  |  {aero_mode}{drs_tag}")

# ========================
# WING AREA INSIGHT
# ========================
st.markdown("### 📐 Wing Area Insight")
c1, c2, c3 = st.columns(3)

c1.markdown(f"""
<div class='card'><h4>Manual Area</h4><h2>{A:.2f} m²</h2></div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class='card'><h4>Geometry Area</h4><h2>{A_geom:.2f} m²</h2></div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class='card'><h4>Active Area</h4><h2>{A_used:.2f} m²</h2></div>
""", unsafe_allow_html=True)

# ========================
# SMART RECOMMENDATION
# ========================
st.markdown("### 🧠 Smart Recommendation")

if DRS_ON:
    st.success("💡 DRS active — low drag configuration for maximum straight-line speed")
else:
    st.info("💡 High-downforce configuration — improved cornering performance")

if angle_active < 12:
    st.info("🔄 Low downforce setup: suited for high-speed circuits such as Monza")
elif angle_active < 22:
    st.info("🔄 Balanced setup: speed + cornering compromise — suited for Silverstone and Spa")
elif angle_active < 32:
    st.success("✅ High downforce setup: maximum cornering grip — suited for Monaco and Singapore")
else:
    st.warning("⚠️ Near stall region: consider reducing flap angle")

if efficiency > 2.5:
    st.success("🚀 Excellent aerodynamic efficiency")
elif efficiency < 1.5:
    st.warning("⚠️ Low L/D efficiency — adjust flap angle")

# ========================
# SYSTEM INSIGHT
# ========================
st.markdown("### 🧠 System Insight")

if angle_active > 32:
    st.warning(
        "⚠️ Rear wing approaching stall region — excessive drag may reduce efficiency"
    )
elif efficiency < 1.5:
    st.warning(
        "⚠️ Aerodynamic efficiency is low — consider reducing flap angle"
    )
elif angle_active < 12:
    st.info("💡 Low-downforce setup — ideal for circuits such as Monza")
elif angle_active < 22:
    st.success("✅ Balanced setup — suited for Silverstone and Spa")
else:
    st.success("✅ High-downforce setup — suited for Monaco and Singapore")

# ========================
# FOOTER
# ========================
st.markdown(f"""
<br><br>
<hr style="border:1px solid rgba(255,255,255,0.1)">
<p style='text-align:center;color:gray;'>
🏁 Formula 1 Inspired Active Aerodynamics Dashboard
</p>
""", unsafe_allow_html=True)
