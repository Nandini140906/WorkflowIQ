import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from api import login, signup, get_user
from auth import is_logged_in, logout, get_user_name

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
                st.session_state.access_token = result.get("access_token")
                st.session_state.user_id = result.get("user_id")
                st.session_state.user_name = result.get("name")
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
with tab2:
    name        = st.text_input("Full Name", key="s_name")
    email_su    = st.text_input("Email", key="s_email")
    password_su = st.text_input("Password (min 8 chars)", type="password", key="s_pass")
    if st.button("Create Account", type="primary", use_container_width=True):
        if not name or not email_su or not password_su:
            st.error("All fields are required.")
        elif len(password_su) < 8:
            st.error("Password must be at least 8 characters.")
        else:
            with st.spinner("Creating account..."):
                result = signup(name, email_su, password_su)
            if result:
                st.success("Account created! Please log in.")
            else:
                st.error("Signup failed. Email may already be in use.")
