import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="Energy Meter Dashboard",
    page_icon="⚡",
    layout="wide",
)

# ---------------- CSS THEMING ----------------
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .upload-box {
        border: 2px dashed #3f51b5;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        color: #ffffff88;
    }
    .metric-card {
        background: #1b1f24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center; color:#58a6ff;'>⚡ Energy Consumption Dashboard</h1>", unsafe_allow_html=True)
st.write("")
st.markdown("<p style='text-align:center;'>Upload CSV files to visualize trends, detect peaks, and explore usage analytics.</p>", unsafe_allow_html=True)
st.write("")


# ---------------- FILE UPLOAD ----------------
st.markdown("<div class='upload-box'>📁 Drag & Drop your CSV file here</div>", unsafe_allow_html=True)
file = st.file_uploader("", type=["csv"], accept_multiple_files=False)


# ---------------- MAIN LOGIC ----------------
if file is None:
    st.warning("Please upload a CSV file to continue.")
else:
    df = pd.read_csv(file)
    st.success("✅ File uploaded successfully!")

    # Convert timestamp
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Graphs", "📈 Dashboard", "⚠ Peak Detection"])

    # ---------------- TAB 1: Graphs ----------------
    with tab1:
        col = st.selectbox("Select parameter to visualize:", df.columns)

        fig, ax = plt.subplots()
        ax.plot(df["Timestamp"], df[col])
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(col)
        st.pyplot(fig)

        if st.button("Download Graph as PNG"):
            fig.savefig("graph.png")
            st.success("✅ Graph saved as graph.png")

    # ---------------- TAB 2: Dashboard ----------------
    with tab2:
        st.subheader("📌 Key Metrics")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", len(df))
        col2.metric("Max Value", round(df.select_dtypes(include='number').max().max(), 2))
        col3.metric("Min Value", round(df.select_dtypes(include='number').min().min(), 2))
        col4.metric("Average", round(df.select_dtypes(include='number').mean().mean(), 2))

        st.bar_chart(df.select_dtypes(include='number'))

    # ---------------- TAB 3: Peak Detection ----------------
    with tab3:
        st.subheader("⚠ High Usage Peaks")

        if "Power (kW)" in df.columns:
            threshold = st.slider("Set Threshold (kW)", 0.0, float(df["Power (kW)"].max()), 0.7)
            peaks = df[df["Power (kW)"] > threshold]

            st.write(peaks[["Timestamp", "Power (kW)"]])

            st.info(f"Detected {len(peaks)} peaks above {threshold} kW")
        else:
            st.warning("Column `Power (kW)` not found in your file. Rename accordingly.")
