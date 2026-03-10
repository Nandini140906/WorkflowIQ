import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import pandas as pd
import plotly.express as px
from auth import require_login, get_user_id
from api import get_tasks

st.set_page_config(page_title="Analytics", page_icon="📈", layout="centered")
require_login()

user_id = get_user_id()
st.title("📈 Analytics")

with st.spinner("Loading..."):
    tasks = get_tasks(user_id)

total    = len(tasks)
done     = sum(1 for t in tasks if t.get("status","").lower() == "completed")
pending  = sum(1 for t in tasks if t.get("status","").lower() == "pending")
in_prog  = sum(1 for t in tasks if t.get("status","").lower() == "in_progress")

c1, c2, c3 = st.columns(3)
c1.metric("Total Tasks", total)
c2.metric("Completed", done)
c3.metric("In Progress", in_prog)

if total:
    st.progress(done / total, text=f"{done}/{total} completed")

st.divider()

if tasks:
    # Tasks by category
    by_cat = {}
    for t in tasks:
        k = t.get("category", "Other")
        by_cat[k] = by_cat.get(k, 0) + 1
    df_cat = pd.DataFrame(by_cat.items(), columns=["Category", "Count"])
    st.plotly_chart(
        px.pie(df_cat, names="Category", values="Count", title="Tasks by Category",
               color_discrete_sequence=px.colors.sequential.Viridis),
        use_container_width=True
    )

    # Tasks by priority
    by_pri = {}
    for t in tasks:
        k = (t.get("priority") or "unset").capitalize()
        by_pri[k] = by_pri.get(k, 0) + 1
    df_pri = pd.DataFrame(by_pri.items(), columns=["Priority", "Count"])
    st.plotly_chart(
        px.bar(df_pri, x="Priority", y="Count", title="Tasks by Priority",
               color_discrete_sequence=["#6366f1"]),
        use_container_width=True
    )

    # Tasks by status
    by_status = {"Pending": pending, "In Progress": in_prog, "Completed": done}
    df_status = pd.DataFrame(by_status.items(), columns=["Status", "Count"])
    st.plotly_chart(
        px.bar(df_status, x="Status", y="Count", title="Tasks by Status",
               color_discrete_sequence=["#f59e0b"]),
        use_container_width=True
    )
else:
    st.info("Create some tasks to see analytics here.")