import streamlit as st
import plotly.graph_objects as go
import numpy as np
from modules.math_engine import analyze_function
from modules.challenges import generate_challenge, calculate_score
from modules.resources import generate_worksheet_pdf

st.set_page_config(page_title="Graph Explorer", page_icon="📈", layout="wide")

st.title("📈 Graph Explorer")
st.caption("Interactive algebra, real-time calculus visualizer & match challenges.")

tabs = st.tabs(["📊 Interactive Explorer", "🎮 Challenge Mode", "🎓 Teacher & Premium Portal"])

# TAB 1: INTERACTIVE EXPLORER
with tabs[0]:
    col_sidebar, col_main = st.columns([1, 2.5])
    
    with col_sidebar:
        st.header("Function Controls")
        fn_type = st.selectbox("Function Family", ["Linear", "Quadratic", "Exponential", "Trigonometric"])
        
        params = {}
        if fn_type == "Linear":
            params['m'] = st.slider("Slope (m)", -5.0, 5.0, 1.0, 0.1)
            params['c'] = st.slider("Y-Intercept (c)", -5.0, 5.0, 0.0, 0.5)
        elif fn_type == "Quadratic":
            params['a'] = st.slider("a", -3.0, 3.0, 1.0, 0.1)
            params['b'] = st.slider("b", -5.0, 5.0, 0.0, 0.5)
            params['c'] = st.slider("c", -5.0, 5.0, 0.0, 0.5)
        elif fn_type == "Exponential":
            params['a'] = st.slider("Scale (a)", -3.0, 3.0, 1.0, 0.1)
            params['b'] = st.slider("Base (b)", 0.1, 5.0, 2.0, 0.1)
            params['c'] = st.slider("Shift (c)", -5.0, 5.0, 0.0, 0.5)
        elif fn_type == "Trigonometric":
            params['a'] = st.slider("Amplitude (a)", -3.0, 3.0, 1.0, 0.1)
            params['b'] = st.slider("Frequency (b)", 0.1, 3.0, 1.0, 0.1)
            params['c'] = st.slider("Phase Shift (c)", -3.14, 3.14, 0.0, 0.1)
            params['d'] = st.slider("Vertical Shift (d)", -5.0, 5.0, 0.0, 0.5)

        x_eval = st.slider("Evaluate Gradient at x =", -8.0, 8.0, 2.0, 0.5)

    res = analyze_function(fn_type, params, x_eval)

    with col_main:
        st.latex(f"f(x) = {res['latex']}")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=res['x_vals'], y=res['y_vals'], mode='lines', name='f(x)', line=dict(color='#0066FF', width=3)))
        
        # Plot y-intercept
        fig.add_trace(go.Scatter(x=[0], y=[res['y_intercept']], mode='markers', name='Y-Intercept', marker=dict(color='orange', size=10)))
        
        # Plot roots
        if res['roots']:
            fig.add_trace(go.Scatter(x=res['roots'], y=[0]*len(res['roots']), mode='markers', name='Roots', marker=dict(color='red', size=10, symbol='x')))

        # Plot turning points
        for tp in res['turning_points']:
            fig.add_trace(go.Scatter(x=[tp[0]], y=[tp[1]], mode='markers+text', name=f'{tp[2]} Point',
                                     text=[f"{tp[2]} ({tp[0]:.2f}, {tp[1]:.2f})"], textposition="top center",
                                     marker=dict(color='purple', size=11, symbol='diamond')))

        fig.update_layout(title="Function Graph", xaxis_title="x", yaxis_title="y",
                          xaxis=dict(range=[-10, 10]), yaxis=dict(range=[-10, 10]), height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Key Analytical Properties")
        m1, m2, m3 = st.columns(3)
        m1.metric("Y-Intercept", f"(0, {res['y_intercept']:.2f})")
        m2.metric("Roots / X-Intercepts", f"{[round(r, 2) for r in res['roots']]}")
        m3.metric(f"Gradient at x = {x_eval}", f"{res['gradient']:.2f}")

# TAB 2: CHALLENGE MODE
with tabs[1]:
    st.header("🎮 Match the Graph Challenge")
    st.write("Adjust your sliders to match the hidden target curve!")
    
    if 'target_type' not in st.session_state:
        st.session_state.target_type, st.session_state.target_params = generate_challenge()

    if st.button("Generate New Challenge"):
        st.session_state.target_type, st.session_state.target_params = generate_challenge()
        st.rerun()

    target_res = analyze_function(st.session_state.target_type, st.session_state.target_params)
    
    fig_chal = go.Figure()
    fig_chal.add_trace(go.Scatter(x=target_res['x_vals'], y=target_res['y_vals'], mode='lines', 
                                  name='Target Curve (Hidden)', line=dict(color='grey', width=3, dash='dash')))
    fig_chal.add_trace(go.Scatter(x=res['x_vals'], y=res['y_vals'], mode='lines', 
                                  name='Your Curve', line=dict(color='#00CC66', width=3)))
    
    fig_chal.update_layout(xaxis=dict(range=[-10, 10]), yaxis=dict(range=[-10, 10]), height=450)
    st.plotly_chart(fig_chal, use_container_width=True)

    mse, accuracy = calculate_score(res['y_vals'], target_res['y_vals'])
    st.metric("Match Accuracy", f"{accuracy}%", delta=f"MSE: {mse}")
    if accuracy > 95:
        st.balloons()
        st.success("🎉 Excellent! You matched the target curve!")

# TAB 3: TEACHER & PREMIUM PORTAL
with tabs[2]:
    st.header("🎓 Premium Teaching Resources")
    st.write("Access downloadable classroom materials and printable student worksheets.")
    
    pdf_bytes = generate_worksheet_pdf()
    st.download_button(label="📄 Download Student Worksheet (PDF)", data=pdf_bytes, file_name="graph_explorer_worksheet.pdf", mime="application/pdf")
