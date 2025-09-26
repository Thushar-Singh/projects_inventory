import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px

# -------------------------------
# Functions to load/save data
# -------------------------------
def load_data():
    try:
        return pd.read_excel("cat_tracker.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Date", "Section", "Topic", "Time Spent (minutes)", "Set Size", "Correct Answers"
        ])

def save_data(df):
    df.to_excel("cat_tracker.xlsx", index=False)

# -------------------------------
# Initialize session state
# -------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False

# -------------------------------
# Load data
# -------------------------------
df = load_data()

# -------------------------------
# Streamlit Layout
# -------------------------------
st.title("⏱ CAT Study Tracker & Analytics")

# Input fields
section = st.selectbox("Select Section", ["QA", "DILR", "VARC"])
topic = st.text_input("Enter Topic")
set_size = st.number_input("Set Size (Number of Questions)", min_value=1, step=1)
correct_answers = st.number_input("Correct Answers", min_value=0, max_value=set_size, step=1)

# -------------------------------
# Timer Buttons
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Timer"):
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.success("Timer started!")

with col2:
    if st.button("Stop Timer"):
        if st.session_state.running and st.session_state.start_time:
            elapsed_time = round((time.time() - st.session_state.start_time) / 60, 2)
            
            # Calculate accuracy percentage
            accuracy = (correct_answers / set_size) * 100

            # New entry
            new_entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Section": section,
                "Topic": topic,
                "Time Spent (minutes)": elapsed_time,
                "Set Size": set_size,
                "Correct Answers": correct_answers,
                "Accuracy (%)": accuracy
            }

            # Append to df
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

            # Auto-save
            save_data(df)

            st.success(f"Saved: {elapsed_time} minutes on {section} - {topic} | Accuracy: {accuracy:.2f}%")

            # Reset timer
            st.session_state.running = False
            st.session_state.start_time = None
        else:
            st.warning("No active timer to stop.")

# -------------------------------
# Display data
# -------------------------------
st.subheader("Recent Entries")
st.dataframe(df.tail(10))

# -------------------------------
# Download CSV
# -------------------------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="cat_tracker.csv",
    mime="text/csv"
)

# -------------------------------
# Analytics Charts
# -------------------------------
if not df.empty:
    st.subheader("Analytics")

    # Accuracy trend
    fig1 = px.line(df, x="Date", y="Accuracy (%)", color="Section", title="Accuracy Trend Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    # Average duration per section
    avg_time = df.groupby("Section")["Time Spent (minutes)"].mean().reset_index()
    fig2 = px.bar(avg_time, x="Section", y="Time Spent (minutes)", title="Average Duration per Section")
    st.plotly_chart(fig2, use_container_width=True)
