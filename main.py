# ------------------------------
# Import packages and libraries
# ------------------------------
import streamlit as st



# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(page_title="FlowTrader", page_icon="assets/images/flowtrader_icon1.png", layout="wide", initial_sidebar_state="collapsed")


# ------------------------------
# Set Title
# ------------------------------
#varTitle = "FlowTrader"
#varSubtitle = "AI"
varTitle = "SignalGenius"
varSubtitle = "AI"
st.markdown(f"""<span style="font-weight: bold; font-size: 2em; color:#0096D7;">{varTitle} </span> <span style="font-weight: bold; color:#31333F; font-size:1.8em;">{varSubtitle}</span>""", unsafe_allow_html=True)
st.divider()