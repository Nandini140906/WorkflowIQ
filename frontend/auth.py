import streamlit as st


def is_logged_in():
    return (
        st.session_state.get("user_id") is not None
        and st.session_state.get("access_token") is not None
    )


def require_login():
    if not is_logged_in():
        st.warning("Please log in first.")
        st.stop()


def get_user_id():
    return st.session_state.get("user_id")


def get_user_name():
    return st.session_state.get("user_name", "User")


def logout():
    for key in ["user_id", "access_token", "user_name"]:
        st.session_state.pop(key, None)
