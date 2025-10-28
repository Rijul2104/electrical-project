# CSV-to-Graphical Representation using Streamlit
# Author: Reetesh (Modified by Sarthak)
# Run with: streamlit run minor.py

import pandas as pd
import streamlit as st

# Try importing plotly
try:
    import plotly.express as px
except ModuleNotFoundError:
    st.error("⚠️ Plotly is not installed. Please run `pip install plotly` and restart the app.")
    st.stop()

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Energy Data Visualization", layout="wide")

st.title("📊 Energy Data Visualization")
st.markdown("Upload your **meter data CSV file** to generate interactive graphs.")

# File uploader
uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Load CSV file
    df = pd.read_csv(uploaded_file)

    # Check if Timestamp column exists
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    else:
        st.error("❌ CSV must contain a 'Timestamp' column!")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # Show preview
    st.subheader("🔎 Data Preview")
    st.dataframe(df.head())

    # Filter only numeric columns
    numeric_columns = [col for col in df.select_dtypes(include=["number"]).columns if col != "Timestamp"]

    if len(numeric_columns) == 0:
        st.warning("⚠️ No numeric columns found in the file for plotting.")
        st.stop()

    # Dropdown for parameter selection
    parameter = st.selectbox(
        "📌 Select parameter to visualize",
        numeric_columns
    )

    # Line chart for selected parameter
    fig = px.line(df, x="Timestamp", y=parameter,
                  title=f"{parameter} vs Time",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Show multiple parameters
    st.subheader("📈 All Parameters")
    for col in numeric_columns:
        fig = px.line(df, x="Timestamp", y=col,
                      title=f"{col} vs Time")
        st.plotly_chart(fig, use_container_width=True)

    # Show basic statistics
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

else:
    st.info("👆 Please upload a CSV file to continue.")
