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
                    token = result.get("access_token")

                    # save token
                    st.session_state.access_token = token

                    # decode token to get user info
                    payload = jwt.get_unverified_claims(token)
                    uid = payload.get("user_id")

                    st.session_state.user_id = uid

                    user_data = get_user(uid)
                    if user_data:
                        st.session_state.user_name = user_data.get("name", email.split("@")[0])
                    else:
                        st.session_state.user_name=email.split("@")[0]

                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")