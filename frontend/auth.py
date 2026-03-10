import streamlit as st


def is_logged_in():
    return st.session_state.get("logged_in",False)


def require_login():
    if not is_logged_in():
        st.warning("Please log in first.")
        st.stop()


def get_user_id():
    return st.session_state.get("user_id")


def get_user_name():
    return "User"


def logout():
        st.session_state.clear()
