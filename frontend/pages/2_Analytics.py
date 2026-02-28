import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import require_login, get_user_id
from api import get_tasks, get_logs_for_task

st.set_page_config(page_title="Analytics", page_icon="📈", layout="centered")
require_login()

user_id = get_user_id()
st.title("📈 Analytics")

with st.spinner("Loading..."):
    tasks = get_tasks(user_id)
    all_logs = []
    for t in tasks:
        tid  = t.get("id")
        logs = get_logs_for_task(tid, user_id)
        for l in logs:
            l["task_title"] = t.get("title", "Untitled")
        all_logs.extend(logs)

total = len(tasks)
done  = sum(1 for t in tasks if t.get("status","").lower() == "completed")
# field is time_spent in ProductivityLogResponse
hours = sum(l.get("time_spent", 0) for l in all_logs)

c1, c2, c3 = st.columns(3)
c1.metric("Total Tasks", total)
c2.metric("Completed", done)
c3.metric("Hours Logged", f"{hours:.1f}h")

if total:
    st.progress(done / total, text=f"{done}/{total} completed")

st.info(f"You've completed **{done}** tasks and logged **{hours:.1f}** total hours.")
st.divider()

if all_logs:
    # Hours per task
    by_task = {}
    for l in all_logs:
        k = l["task_title"]
        by_task[k] = by_task.get(k, 0) + l.get("time_spent", 0)
    df = pd.DataFrame(by_task.items(), columns=["Task", "Hours"]).sort_values("Hours", ascending=False)
    st.plotly_chart(
        px.bar(df, x="Task", y="Hours", title="Hours per Task",
               color_discrete_sequence=["#6366f1"]),
        use_container_width=True
    )
else:
    st.info("Log time on tasks to see analytics here.")
