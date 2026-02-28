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
                token = result.get("access_token")
                # Login only returns access_token + token_type (Token schema)
                # We don't have user_id yet — decode it from token payload
                try:
                    from jose import jwt
                    SECRET_KEY = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    uid = payload.get("user_id")
                except Exception:
                    uid = None

                if uid:
                    st.session_state.access_token = token
                    st.session_state.user_id = uid
                    # Fetch name from /api/user/{user_id}
                    user_data = get_user(uid)
                    st.session_state.user_name = user_data.get("name", email.split("@")[0]) if user_data else email.split("@")[0]
                    st.rerun()
                else:
                    st.error("Login succeeded but could not read user info. Check your SECRET_KEY in app.py matches auth.py.")
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
