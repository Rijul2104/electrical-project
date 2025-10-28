# CSV-to-Graphical Representation using Streamlit
# Author: Reetesh
# Run with: streamlit run app.py

import pandas as pd
import plotly.express as px
import streamlit as st

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
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    else:
        st.error("❌ CSV must contain a 'Timestamp' column!")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # Show preview
    st.subheader("🔎 Data Preview")
    st.dataframe(df.head())

    # Dropdown for parameter selection
    parameter = st.selectbox(
        "📌 Select parameter to visualize",
        [col for col in df.columns if col != "Timestamp"]
    )

    # Line chart for selected parameter
    fig = px.line(df, x="Timestamp", y=parameter,
                  title=f"{parameter} vs Time",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Show multiple parameters
    st.subheader("📈 All Parameters")
    for col in df.columns:
        if col != "Timestamp":
            fig = px.line(df, x="Timestamp", y=col,
                          title=f"{col} vs Time")
            st.plotly_chart(fig, use_container_width=True)

    # Show basic statistics
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

else:
    st.info("👆 Please upload a CSV file to continue.")