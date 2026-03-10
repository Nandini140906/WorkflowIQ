import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from api import login, signup, get_user
from auth import is_logged_in, logout, get_user_name
from jose import jwt

st.set_page_config(page_title="WorkflowIQ", page_icon="⚡", layout="centered")

if is_logged_in():
    st.title(f"👋 Hey, {get_user_name()}!")
    st.caption("Use the sidebar to navigate.")
    if st.button("Logout"):
        logout()
        st.rerun()
    st.stop()

st.title("⚡ WorkflowIQ")
st.caption("AI-powered productivity tracker")
st.divider()

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    email    = st.text_input("Email", key="l_email")
    password = st.text_input("Password", type="password", key="l_pass")
    if st.button("Login", type="primary", use_container_width=True):
        if not email or not password:
            st.error("Please fill in both fields.")
        else:
            with st.spinner("Logging in..."):
                result = login(email, password)
            

                if result:
                    if result:
                        st.session_state["access_token"] = result["access_token"]
                        st.session_state["logged_in"] = True

                        st.success("Login successful!")
                        st.rerun()