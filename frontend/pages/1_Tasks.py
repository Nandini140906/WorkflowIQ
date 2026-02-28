import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import sys, os
from datetime import date, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import require_login, get_user_id
from api import get_tasks, create_task, update_task, delete_task, create_log, get_logs_for_task, delete_log

st.set_page_config(page_title="Tasks", page_icon="✅", layout="centered")
require_login()

user_id = get_user_id()

# Valid categories and statuses
CATEGORIES = ["Work", "Personal", "Health", "Finance", "Learning", "Other"]
STATUSES   = ["pending", "in_progress", "completed"]

st.title("✅ Tasks")

tab_tasks, tab_logs = st.tabs(["Tasks", "Logs"])

# ─────────────────────────────────────────────────────────────────────────────
# TASKS TAB
# ─────────────────────────────────────────────────────────────────────────────
with tab_tasks:

    # Add task
    with st.expander("＋ New Task"):
        new_title    = st.text_input("Title (max 25 chars)", max_chars=25)
        col1, col2   = st.columns(2)
        new_category = col1.selectbox("Category", CATEGORIES)
        new_deadline = col2.date_input("Deadline", value=date.today())

        if st.button("Create Task", type="primary"):
            if not new_title:
                st.error("Title is required.")
            else:
                with st.spinner("Creating..."):
                    result = create_task(user_id, new_title, new_category, str(new_deadline))
                if result:
                    p     = (result.get("priority") or "medium").lower()
                    badge = "🔴" if p == "high" or "urgent" else "🟡" if p == "medium" else "🟢"
                    st.success(f"Created! AI priority: {badge} {p.upper()}")
                    st.rerun()
                else:
                    st.error("Failed to create task. Check backend is running.")

    # Filters
    col1, col2 = st.columns(2)
    f_status   = col1.selectbox("Filter status",   ["All"] + STATUSES,             label_visibility="collapsed")
    f_priority = col2.selectbox("Filter priority", ["All", "high", "medium", "low"], label_visibility="collapsed")

    with st.spinner("Loading tasks..."):
        tasks = get_tasks(user_id)

    if f_status   != "All": tasks = [t for t in tasks if t.get("status","").lower()   == f_status]
    if f_priority != "All": tasks = [t for t in tasks if t.get("priority","").lower() == f_priority]

    st.caption(f"{len(tasks)} task(s)")

    for task in reversed(tasks):
        tid      = task.get("id")
        p        = (task.get("priority") or "medium").lower()
        badge    = "🔴" if p == "high" else "🟡" if p == "medium" else "🟢"
        status   = task.get("status", "pending")
        title    = task.get("title", "Untitled")
        deadline = task.get("deadline", "")
        # deadline comes back as full datetime string — trim to date part
        if deadline and "T" in str(deadline):
            deadline = str(deadline)[:10]

        with st.expander(f"{badge} {title}  ·  {status}  ·  {deadline}"):
            st.caption(f"Category: {task.get('category','—')}   |   Priority: {p.upper()}")

            col1, col2, col3 = st.columns([3, 2, 1])
            new_status = col1.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(status) if status in STATUSES else 0,
                key=f"st_{tid}"
            )
            if col2.button("Save", key=f"sv_{tid}"):
                with st.spinner("Saving..."):
                    res = update_task(tid, user_id, status=new_status)
                if res:
                    st.success("Saved!")
                    st.rerun()
                else:
                    st.error("Failed to save.")

            if col3.button("🗑️", key=f"del_{tid}"):
                with st.spinner("Deleting..."):
                    ok = delete_task(tid, user_id)
                if ok:
                    st.rerun()
                else:
                    st.error("Failed to delete.")

# ─────────────────────────────────────────────────────────────────────────────
# LOGS TAB
# ─────────────────────────────────────────────────────────────────────────────
with tab_logs:
    st.subheader("Log Time")

    all_tasks = get_tasks(user_id)
    if not all_tasks:
        st.info("Create tasks first to log time against them.")
    else:
        task_map  = {t.get("id"): t.get("title", "Untitled") for t in all_tasks}
        task_ids  = list(task_map.keys())
        task_lbls = list(task_map.values())

        col1, col2 = st.columns(2)
        sel_idx    = col1.selectbox("Task", range(len(task_lbls)), format_func=lambda i: task_lbls[i])
        # field name is time_spent — matches ProductivityLogCreate in schemas.py
        time_spent = col2.number_input("Hours spent", min_value=0.25, step=0.25, value=1.0)

        if st.button("Log Time", type="primary"):
            with st.spinner("Logging..."):
                res = create_log(
                    user_id,
                    task_id=task_ids[sel_idx],
                    time_spent=time_spent,
                    date=str(date.today())
                )
            if res:
                st.success(f"Logged {time_spent}h!")
                st.rerun()
            else:
                st.error("Failed to log time.")

        st.divider()

        # View logs for selected task
        logs    = get_logs_for_task(task_ids[sel_idx], user_id)
        total_h = sum(l.get("time_spent", 0) for l in logs)  # field is time_spent
        st.caption(f"{len(logs)} log(s) · {total_h:.1f}h total for '{task_lbls[sel_idx]}'")

        for log in logs:
            lid = log.get("id")
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"**{log.get('time_spent', 0)}h** · {log.get('date', '?')}")
            if col2.button("🗑️", key=f"ldel_{lid}"):
                with st.spinner("Deleting..."):
                    ok = delete_log(lid, user_id)
                if ok:
                    st.rerun()
                else:
                    st.error("Failed to delete.")
