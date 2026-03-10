import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from datetime import date
from auth import require_login, get_user_id
from api import get_tasks, create_task, update_task, delete_task

st.set_page_config(page_title="Tasks", page_icon="✅", layout="centered")
require_login()

user_id = get_user_id()

CATEGORIES = ["Work", "Personal", "Health", "Finance", "Learning", "Other"]
STATUSES   = ["pending", "in_progress", "completed"]

st.title("✅ Tasks")

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
                badge = "🔴" if p in ("high", "urgent") else "🟡" if p == "medium" else "🟢"
                st.success(f"Created! AI priority: {badge} {p.upper()}")
                st.rerun()
            else:
                st.error("Failed to create task.")

# Filters
col1, col2 = st.columns(2)
f_status   = col1.selectbox("Filter status",   ["All"] + STATUSES,              label_visibility="collapsed")
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
    if deadline and "T" in str(deadline):
        deadline = str(deadline)[:10]

    with st.expander(f"{badge} {title}  ·  {status}  ·  {deadline}"):
        st.caption(f"Category: {task.get('category','—')}   |   Priority: {p.upper()}")

        col1, col2, col3 = st.columns([3, 2, 1])
        new_status = col1.selectbox(
            "Status", STATUSES,
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