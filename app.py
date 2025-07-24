
import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

st.set_page_config(page_title="S2M Coder Portal", layout="wide")

# Load logo
try:
    logo = Image.open("s2m-logo.png")
    st.image(logo, width=150)
except:
    st.warning("Logo not found")

# Load login data
login_df = pd.read_csv("login_coder.csv")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.login_time = None

# Login Page
def login_page():
    st.title("Login Portal")
    username = st.text_input("Employee ID", key="emp_id", help="Enter your Employee ID")
    password = st.text_input("Password", type="password", key="pwd", help="Enter your password")
    if st.button("Login"):
        match = login_df[(login_df["username"].astype(str) == username) & (login_df["Password"] == password)]
        if not match.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.now()
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# Form Page
def form_page():
    st.title("Chart Entry Form")
    if "chart_id" not in st.session_state:
        st.session_state.update({
            "chart_id": "", "page_no": "", "dos": "", "codes": "",
            "error_type": "", "error_comments": "", "no_of_errors": "",
            "chart_status": "", "auditor_emp_id": "", "auditor_emp_name": ""
        })

    with st.form("entry_form"):
        st.text_input("Chart ID", key="chart_id")
        st.text_input("Page No", key="page_no")
        st.text_input("No of DOS", key="dos")
        st.text_input("No of Codes", key="codes")
        st.text_input("Error Type", key="error_type")
        st.text_input("Error Comments", key="error_comments")
        st.text_input("No of Errors", key="no_of_errors")
        st.text_input("Chart Status", key="chart_status")
        st.text_input("Auditor Emp ID", key="auditor_emp_id")
        st.text_input("Auditor Emp Name", key="auditor_emp_name")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Submitted successfully!")
            for field in ["chart_id", "page_no", "dos", "codes", "error_type",
                          "error_comments", "no_of_errors", "chart_status", 
                          "auditor_emp_id", "auditor_emp_name"]:
                st.session_state[field] = ""

# Dashboard Page
def dashboard_page():
    st.title("Dashboard")
    log_file = "user_logs.csv"
    if os.path.exists(log_file):
        user_logs = pd.read_csv(log_file)
        user_logs = user_logs[user_logs["Emp ID"] == st.session_state.username]
        total_logins = user_logs["Login Time"].count()
        total_hours = round(user_logs["Hours"].sum(), 2)
        total_seconds = (user_logs["Hours"] * 3600).sum()
        total_duration = str(pd.to_timedelta(total_seconds, unit='s'))
        st.metric("Total Logins", total_logins)
        st.metric("Total Time Logged In", total_duration)
        if st.session_state.login_time:
            current_duration = datetime.now() - st.session_state.login_time
            live_duration = str(current_duration).split(".")[0]
            st.metric("Current Session Duration", live_duration)
    else:
        st.info("No login logs found.")

# Page Routing
if not st.session_state.logged_in:
    login_page()
else:
    page = st.sidebar.radio("Select Page", ["Form", "Dashboard"])
    if page == "Form":
        form_page()
    elif page == "Dashboard":
        dashboard_page()
