import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

st.set_page_config(
    page_title="Aqua Sentinel",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #0f172a;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .stButton>button {
        background-color: #0ea5e9;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #0284c7;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .disclaimer {
        background: #fef9c3;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #78350f;
    }

    .stSlider>div>div>div>div {
        background: #0ea5e9;
    }

    .stCheckbox>label>div:first-child {
        background-color: #0ea5e9;
    }

    .loading-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        margin: 2rem auto;
    }
    .loading-wave span {
        display: inline-block;
        width: 10px;
        height: 50px;
        margin: 0 6px;
        background: #0ea5e9;
        border-radius: 6px;
        animation: wave 1.2s ease-in-out infinite;
    }
    .loading-wave span:nth-child(2) { animation-delay: 0.1s; }
    .loading-wave span:nth-child(3) { animation-delay: 0.2s; }
    .loading-wave span:nth-child(4) { animation-delay: 0.3s; }
    .loading-wave span:nth-child(5) { animation-delay: 0.4s; }
    @keyframes wave {
        0%, 100% { transform: scaleY(0.5); }
        50% { transform: scaleY(1); }
    }

    .leak-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        background: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(239,68,68,0.7);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(239,68,68,0.7); }
        70% { box-shadow: 0 0 0 15px rgba(239,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model_bundle():
    try:
        bundle = joblib.load("aqua_sentinel_model.pkl")
        return bundle
    except FileNotFoundError:
        st.error("Model file 'aqua_sentinel_model.pkl' not found. Please ensure it is in the same directory.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

bundle = load_model_bundle()

if "page" not in st.session_state:
    st.session_state.page = "loading"
if "loaded" not in st.session_state:
    st.session_state.loaded = False

def show_loading_screen():
    st.markdown(
        """
        <div style="text-align:center; padding-top:10vh;">
            <h1 style="font-size:3rem; font-weight:700; color:#0f172a;">Aqua Sentinel</h1>
            <p style="font-size:1.2rem; color:#475569;">Smart source‑to‑tap water monitoring & conservation</p>
            <div class="loading-wave">
                <span></span><span></span><span></span><span></span><span></span>
            </div>
            <p style="color:#64748b;">Initializing water intelligence…</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(2)
    st.session_state.loaded = True
    st.session_state.page = "main"
    st.rerun()

def show_main_menu():
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:3rem;">
            <h1 style="font-size:2.5rem;">Aqua Sentinel</h1>
            <p style="font-size:1.1rem; color:#475569;">What would you like to explore?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("💧 SOURCE TANK", use_container_width=True):
            st.session_state.page = "source_tank"
            st.rerun()
        st.markdown(
            """
            <div style="text-align:center; color:#64748b;">
                <p>Analyze water quality parameters using the embedded AI model.</p>
                <p style="font-size:0.85rem;">Interactive reservoir · sedimentation · quality score</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("🚰 WATER FLOW", use_container_width=True):
            st.session_state.page = "water_flow"
            st.rerun()
        st.markdown(
            """
            <div style="text-align:center; color:#64748b;">
                <p>Explore scaling from household to city with anomaly detection.</p>
                <p style="font-size:0.85rem;">Conceptual simulation · flow control · AI alerts</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_tank(water_level, turbidity, ph, do, conductivity, bod, nitrate, temperature):
    num_sediment = int(np.clip(turbidity / 5, 0, 20))
    sediment_particles = []
    for i in range(num_sediment):
        left = np.random.randint(5, 95)
        bottom = np.random.randint(0, 80)
        duration = np.random.uniform(3, 8)
        delay = np.random.uniform(0, 3)
        size = np.random.randint(3, 8)
        sediment_particles.append({
            "left": left,
            "bottom": bottom,
            "duration": duration,
            "delay": delay,
            "size": size,
            "type": "sediment"
        })

    num_algae = int(np.clip((bod + nitrate) / 2, 0, 15))
    algae_particles = []
    for i in range(num_algae):
        left = np.random.randint(5, 95)
        bottom = np.random.randint(20, 90)
        duration = np.random.uniform(4, 10)
        delay = np.random.uniform(0, 5)
        size = np.random.randint(4, 10)
        algae_particles.append({
            "left": left,
            "bottom": bottom,
            "duration": duration,
            "delay": delay,
            "size": size,
            "type": "algae"
        })

    bubble_rate = int(np.clip(do, 0, 20)) * 2
    bubble_html = ""
    if bubble_rate > 0:
        for i in range(bubble_rate):
            left = np.random.randint(5, 95)
            bottom = np.random.randint(0, 60)
            duration = np.random.uniform(2, 5)
            delay = np.random.uniform(0, 3)
            size = np.random.randint(3, 8)
            bubble_html += f'<div class="bubble" style="left:{left}%; bottom:{bottom}%; width:{size}px; height:{size}px; animation-duration:{duration}s; animation-delay:{delay}s;"></div>'

    hue = 200
    if ph < 7:
        hue = 200 + (7 - ph) * 15
    elif ph > 7:
        hue = 200 - (ph - 7) * 15
    sat = min(100, 70 + conductivity / 50)
    light = max(40, 60 - turbidity / 2)
    water_color = f"hsl({hue}, {sat}%, {light}%)"

    shimmer = ""
    if temperature > 25:
        shimmer = '<div class="shimmer"></div>'

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }}
            .tank-container {{
                position: relative;
                width: 200px;
                height: 320px;
                border: 3px solid #0f172a;
                border-radius: 12px;
                overflow: hidden;
                background: #f1f5f9;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            }}
            .water {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: {water_color};
                transition: height 0.8s ease, background 0.5s ease;
                border-radius: 0 0 8px 8px;
                z-index: 1;
            }}
            .sediment-layer {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: #92400e;
                opacity: {min(0.8, turbidity/100)};
                z-index: 2;
                transition: height 0.8s ease, opacity 0.5s;
            }}
            .particle {{
                position: absolute;
                border-radius: 50%;
                animation: settle linear infinite;
                z-index: 3;
            }}
            .particle.sediment {{
                background: #b45309;
            }}
            .particle.algae {{
                background: #4ade80;
                opacity: 0.7;
                animation: float linear infinite;
            }}
            @keyframes settle {{
                0% {{ transform: translateY(0); opacity: 0.8; }}
                100% {{ transform: translateY(60px); opacity: 0; }}
            }}
            @keyframes float {{
                0% {{ transform: translateY(0); opacity: 0.7; }}
                50% {{ transform: translateY(-20px); opacity: 0.4; }}
                100% {{ transform: translateY(0); opacity: 0.7; }}
            }}
            .bubble {{
                position: absolute;
                background: rgba(255,255,255,0.6);
                border-radius: 50%;
                animation: rise linear infinite;
                z-index: 4;
            }}
            @keyframes rise {{
                0% {{ transform: translateY(0); opacity: 0.8; }}
                100% {{ transform: translateY(-100px); opacity: 0; }}
            }}
            .water-surface {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 10px;
                background: rgba(255,255,255,0.4);
                animation: ripple 2s ease-in-out infinite;
                z-index: 5;
            }}
            @keyframes ripple {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-4px); }}
            }}
            .shimmer {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
                background-size: 200% 200%;
                animation: shimmer 3s ease-in-out infinite;
                z-index: 6;
            }}
            @keyframes shimmer {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
        </style>
    </head>
    <body>
        <div class="tank-container" id="tank">
            <div class="water" id="water" style="height: {water_level}%;"></div>
            <div class="sediment-layer" style="height: {min(15, turbidity*0.3)}px;"></div>
            {''.join([f'<div class="particle sediment" style="left:{p["left"]}%; bottom:{p["bottom"]}%; width:{p["size"]}px; height:{p["size"]}px; animation-duration:{p["duration"]}s; animation-delay:{p["delay"]}s;"></div>' for p in sediment_particles])}
            {''.join([f'<div class="particle algae" style="left:{p["left"]}%; bottom:{p["bottom"]}%; width:{p["size"]}px; height:{p["size"]}px; animation-duration:{p["duration"]}s; animation-delay:{p["delay"]}s;"></div>' for p in algae_particles])}
            {bubble_html}
            <div class="water-surface" style="bottom: calc({water_level}% - 5px);"></div>
            {shimmer}
        </div>
    </body>
    </html>
    """
    st.html(html_code, height=340, width=220)

def render_flow_diagram(scale, flow_rate, pressure, abnormal_event, n_items=None):
    if scale == "Household":
        n_items = 1
    elif scale == "Colony":
        n_items = n_items if n_items else 5
    else:
        n_items = n_items if n_items else 5

    nodes = []
    edges = []

    # Determine which nodes will leak (1-2 for Colony/City when abnormal)
    leak_indices = []
    if abnormal_event and scale in ["Colony", "City"]:
        num_leaks = min(2, n_items)
        leak_indices = list(range(num_leaks))  # first 1-2 nodes

    if scale == "Household":
        nodes = [
            {"id": "source", "label": "Source Tank", "type": "tank", "x": 10, "y": 50},
            {"id": "house", "label": "Household", "type": "box", "x": 50, "y": 50},
            {"id": "outlet", "label": "Outlet", "type": "circle", "x": 90, "y": 50}
        ]
        edges = [
            {"from": "source", "to": "house", "flow": flow_rate, "leak": abnormal_event},
            {"from": "house", "to": "outlet", "flow": flow_rate * 0.3 if abnormal_event else flow_rate, "leak": abnormal_event, "pressure": pressure}
        ]
    elif scale == "Colony":
        nodes.append({"id": "source", "label": "Central Source", "type": "tank", "x": 5, "y": 50})
        for i in range(n_items):
            x = 40 + (i % 3) * 20
            y = 20 + (i // 3) * 40
            nodes.append({"id": f"house{i}", "label": f"House {i+1}", "type": "box", "x": x, "y": y})
            is_leak = i in leak_indices
            input_flow = flow_rate / n_items
            output_flow = input_flow * 0.3 if is_leak else input_flow
            edges.append({"from": "source", "to": f"house{i}", "flow": input_flow, "leak": is_leak})
            nodes.append({"id": f"monitor{i}", "label": f"Node {i+1}", "type": "circle", "x": x+15, "y": y})
            edges.append({"from": f"house{i}", "to": f"monitor{i}", "flow": output_flow, "leak": is_leak})
    else:  # City
        nodes.append({"id": "plant", "label": "Treatment Plant", "type": "tank", "x": 50, "y": 5})
        for i in range(n_items):
            angle = (i / n_items) * 2 * np.pi
            x = 50 + 40 * np.cos(angle)
            y = 50 + 40 * np.sin(angle)
            nodes.append({"id": f"zone{i}", "label": f"Zone {i+1}", "type": "box", "x": x, "y": y})
            is_leak = i in leak_indices
            input_flow = flow_rate / n_items
            output_flow = input_flow * 0.3 if is_leak else input_flow
            edges.append({"from": "plant", "to": f"zone{i}", "flow": input_flow, "leak": is_leak})
            nodes.append({"id": f"monitor{i}", "label": f"Monitor {i+1}", "type": "circle", "x": x*0.8+10, "y": y*0.8+10})
            edges.append({"from": f"zone{i}", "to": f"monitor{i}", "flow": output_flow, "leak": is_leak})

    svg_width = 800
    svg_height = 500
    svg_elements = []
    svg_elements.append('<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker></defs>')
    for edge in edges:
        from_node = next(n for n in nodes if n["id"] == edge["from"])
        to_node = next(n for n in nodes if n["id"] == edge["to"])
        x1, y1 = from_node["x"], from_node["y"]
        x2, y2 = to_node["x"], to_node["y"]
        x1_px = x1 * svg_width / 100
        y1_px = y1 * svg_height / 100
        x2_px = x2 * svg_width / 100
        y2_px = y2 * svg_height / 100

        stroke_color = "#ef4444" if edge.get("leak", False) else "#475569"
        stroke_width = 4
        if edge.get("leak", False):
            leak_x = (x1_px + x2_px) / 2
            leak_y = (y1_px + y2_px) / 2
            svg_elements.append(f'<circle cx="{leak_x}" cy="{leak_y}" r="6" fill="#ef4444" opacity="0.8"><animate attributeName="r" from="3" to="12" dur="1s" repeatCount="indefinite"/><animate attributeName="opacity" from="0.8" to="0" dur="1s" repeatCount="indefinite"/></circle>')
            svg_elements.append(f'<circle cx="{leak_x}" cy="{leak_y + 20}" r="3" fill="#ef4444" opacity="0.6"><animate attributeName="cy" from="{leak_y+20}" to="{leak_y+40}" dur="0.8s" repeatCount="indefinite"/><animate attributeName="opacity" from="0.6" to="0" dur="0.8s" repeatCount="indefinite"/></circle>')

        svg_elements.append(f'<line x1="{x1_px}" y1="{y1_px}" x2="{x2_px}" y2="{y2_px}" stroke="{stroke_color}" stroke-width="{stroke_width}" marker-end="url(#arrow)"/>')
        label_x = (x1_px + x2_px) / 2 + 10
        label_y = (y1_px + y2_px) / 2 - 10
        svg_elements.append(f'<text x="{label_x}" y="{label_y}" font-family="Inter" font-size="12" fill="{stroke_color}">{edge["flow"]:.1f} L/min</text>')

    for node in nodes:
        x_px = node["x"] * svg_width / 100
        y_px = node["y"] * svg_height / 100
        if node["type"] == "tank":
            fill = "#bae6fd"
            shape = f'<rect x="{x_px-30}" y="{y_px-30}" width="60" height="60" rx="10" fill="{fill}" stroke="#0284c7" stroke-width="2"/>'
        elif node["type"] == "box":
            fill = "#e2e8f0"
            shape = f'<rect x="{x_px-30}" y="{y_px-15}" width="60" height="30" rx="5" fill="{fill}" stroke="#475569" stroke-width="2"/>'
        else:
            fill = "#cbd5e1"
            shape = f'<circle cx="{x_px}" cy="{y_px}" r="15" fill="{fill}" stroke="#475569" stroke-width="2"/>'
        svg_elements.append(shape)
        svg_elements.append(f'<text x="{x_px}" y="{y_px+5}" font-family="Inter" font-size="12" text-anchor="middle" fill="#0f172a">{node["label"]}</text>')

    svg = f'<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; background:white; border:1px solid #e2e8f0; border-radius:8px;">{"".join(svg_elements)}</svg>'
    st.html(svg, height=500, width=800)

def show_source_tank():
    st.markdown("## 💧 Source Tank Water Quality Analysis")
    st.markdown("Adjust the parameters below to simulate a source‑tank condition. The model will predict an **Aqua Sentinel Water Quality Score** based on 2,547 Indian lake observations (CPCB/NWMP‑derived).")

    with st.container():
        st.markdown("#### Water Parameters")
        col1, col2, col3 = st.columns(3)

        with col1:
            water_level = st.slider("Water Level (%)", 0, 100, 70, 5)
            turbidity = st.slider("Turbidity (NTU)", 0.0, 100.0, 5.0, 0.5)
            ph = st.slider("pH", 0.0, 14.0, 7.5, 0.1)
            do = st.slider("DO (mg/L)", 0.0, 20.0, 7.0, 0.1)

        with col2:
            conductivity = st.slider("Conductivity (µS/cm)", 0, 2000, 400, 10)
            bod = st.slider("BOD (mg/L)", 0.0, 50.0, 3.0, 0.1)
            nitrate = st.slider("Nitrate (mg/L)", 0.0, 50.0, 5.0, 0.1)

        with col3:
            fecal_coliform = st.slider("Fecal Coliform (MPN/100mL)", 0, 10000, 100, 10)
            total_coliform = st.slider("Total Coliform (MPN/100mL)", 0, 10000, 200, 10)
            temperature = st.slider("Temperature (°C)", 0.0, 40.0, 25.0, 0.5)

    st.markdown("#### Reservoir Visualization")
    tank_col, vis_col = st.columns([1, 2])
    with tank_col:
        render_tank(water_level, turbidity, ph, do, conductivity, bod, nitrate, temperature)
        st.caption(f"Level: {water_level}% | Turbidity: {turbidity:.1f} NTU")

    with vis_col:
        if st.button("🔍 ANALYZE WITH AQUA SENTINEL", use_container_width=True):
            if bundle is None:
                st.error("Model bundle not loaded. Cannot perform analysis.")
            else:
                input_dict = {
                    "Water Level": water_level,
                    "Turbidity": turbidity,
                    "pH": ph,
                    "DO": do,
                    "Conductivity": conductivity,
                    "BOD": bod,
                    "Nitrate": nitrate,
                    "Fecal Coliform": fecal_coliform,
                    "Total Coliform": total_coliform,
                    "Temperature": temperature,
                }
                input_df = pd.DataFrame([input_dict])

                features = bundle["features"]
                imputer = bundle["imputer"]
                missing = [f for f in features if f not in input_df.columns]
                if missing:
                    st.error(f"Input data is missing required features: {missing}.")
                    return
                input_df = input_df[features]

                input_imputed = imputer.transform(input_df)
                input_imputed_df = pd.DataFrame(input_imputed, columns=features)
                model = bundle["model"]
                y_pred_norm = model.predict(input_imputed_df)[0]

                quality_min = bundle["quality_min"]
                quality_max = bundle["quality_max"]
                if 0 <= y_pred_norm <= 1:
                    score = y_pred_norm * (quality_max - quality_min) + quality_min
                else:
                    score = y_pred_norm
                score = float(np.clip(score, quality_min, quality_max))

                if score >= 80:
                    category = "Excellent"
                    color = "#16a34a"
                elif score >= 60:
                    category = "Good"
                    color = "#65a30d"
                elif score >= 40:
                    category = "Fair"
                    color = "#f59e0b"
                elif score >= 20:
                    category = "Poor"
                    color = "#ea580c"
                else:
                    category = "Very Poor"
                    color = "#dc2626"

                st.markdown("#### Aqua Sentinel Prediction")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <p style="font-size:0.9rem; color:#64748b;">Water Quality Score</p>
                            <p style="font-size:2.5rem; font-weight:700; color:{color};">{score:.1f}</p>
                            <p style="font-size:1rem; font-weight:500; color:{color};">{category}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_b:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <p style="font-size:0.9rem; color:#64748b;">Model Information</p>
                            <p style="font-size:1rem; font-weight:500;">{bundle['model_name']}</p>
                            <p style="font-size:0.9rem; color:#64748b;">R² = {bundle['r2']:.4f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                if "importance" in bundle and bundle["importance"] is not None:
                    st.markdown("#### Most Important Parameters")
                    imp_df = pd.DataFrame({
                        "Feature": list(features),
                        "Importance": list(bundle["importance"])
                    }).sort_values("Importance", ascending=False).head(5)
                    st.bar_chart(imp_df.set_index("Feature"), use_container_width=True)

                st.markdown(
                    """
                    <div class="disclaimer">
                        ⚠️ <strong>Prototype / Educational Model Only</strong><br>
                        This prediction is based on a machine learning model trained on Indian lake water quality data.
                        It is <strong>not</strong> a certified drinking‑water test and must not be used for regulatory or health decisions.
                        Always consult official laboratory analysis for real‑world water quality assessment.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

def show_water_flow():
    st.markdown("## 🚰 Water Flow & Network Monitoring")
    st.markdown("Explore scaling from a single household to a city‑wide distributed water network. These are **conceptual simulations** to illustrate the vision of Aqua Sentinel; the current Gradient Boosting model is **not** trained for leak detection.")

    scale = st.radio("Select Scale", ["Household", "Colony", "City"], horizontal=True)

    st.markdown("#### Flow Conditions")
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        flow_rate = st.slider("Flow Rate (L/min)", 0.0, 50.0, 25.0, 0.5)
    with col_ctrl2:
        pressure = st.slider("Pressure (bar)", 0.0, 10.0, 4.0, 0.1)
    with col_ctrl3:
        abnormal_event = st.checkbox("Simulate Water‑Loss / Abnormal Flow")

    if scale == "Colony":
        n_items = st.slider("Number of Households", 3, 10, 5)
    elif scale == "City":
        n_items = st.slider("Number of Zones", 3, 8, 5)
    else:
        n_items = 1

    st.markdown(f"#### {scale} Simulation")
    render_flow_diagram(scale, flow_rate, pressure, abnormal_event, n_items)

    if abnormal_event:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:10px; margin-top:1rem;">
                <span class="leak-indicator"></span>
                <span style="color:#dc2626; font-weight:600;">AI anomaly detected – abnormal flow pattern or water‑loss event flagged.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning("**Conceptual simulation only** – the current Gradient Boosting model does not perform leak detection.")

    st.markdown(
        """
        <div style="background:#f8fafc; padding:1rem; border-radius:8px; border:1px solid #e2e8f0; margin-top:2rem;">
            <p style="color:#64748b; font-size:0.9rem; margin:0;">
                🔹 This is a <strong>conceptual interface</strong> to visualize the future of Aqua Sentinel. 
                The current Gradient Boosting model is exclusively for water quality scoring; it does not perform leak detection or flow anomaly detection.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not st.session_state.loaded:
    show_loading_screen()
elif st.session_state.page == "main":
    show_main_menu()
elif st.session_state.page == "source_tank":
    if st.button("← Back to Main Menu"):
        st.session_state.page = "main"
        st.rerun()
    show_source_tank()
elif st.session_state.page == "water_flow":
    if st.button("← Back to Main Menu"):
        st.session_state.page = "main"
        st.rerun()
    show_water_flow()
else:
    st.session_state.page = "main"
    st.rerun()