"""
Oncology / RWD Analytics Dashboard (from oncology-ai-insights).
Streamlit dashboard for synthetic oncology patient data and AI insights.
"""

import sys
from pathlib import Path

# Project root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Biomedical Data Platform — Analytics", layout="wide")
st.title("Biomedical Data Platform — Analytics Dashboard")

st.markdown("""
This dashboard visualizes OMOP/oncology data from the platform.
Uses synthetic or ingested OMOP data. *Demo only. No real patient data.*
""")

DATA_PATH = Path(__file__).resolve().parents[2] / "data"
SYNTHETIC_CSV = DATA_PATH / "synthetic_oncology_patients.csv"
OMOP_PERSON = DATA_PATH / "omop" / "person.parquet"
OMOP_CONDITION = DATA_PATH / "omop" / "condition_occurrence.parquet"


@st.cache_data
def load_synthetic_or_omop():
    """Load synthetic oncology data or OMOP person/condition."""
    if SYNTHETIC_CSV.exists():
        return pd.read_csv(SYNTHETIC_CSV), "synthetic"
    if (DATA_PATH / "omop" / "person.parquet").exists():
        import pyarrow.parquet as pq
        person = pq.read_table(OMOP_PERSON).to_pandas()
        person["cancer_type"] = "N/A"
        person["stage"] = "N/A"
        person["biomarker_status"] = "N/A"
        person["treatment"] = "N/A"
        person["survival_months"] = 0
        return person.rename(columns={"person_id": "patient_id"}), "omop"
    # Generate minimal synthetic data
    import random
    n = 50
    return pd.DataFrame({
        "patient_id": [f"P{i:04d}" for i in range(n)],
        "age": [random.randint(35, 85) for _ in range(n)],
        "gender": random.choices(["M", "F"], k=n),
        "cancer_type": random.choices(["Breast", "Lung", "Colorectal", "Prostate"], k=n),
        "stage": random.choices(["I", "II", "III", "IV"], k=n),
        "biomarker_status": random.choices(["Positive", "Negative", "Unknown"], k=n),
        "treatment": random.choices(["Chemo", "Immunotherapy", "Targeted", "Surgery"], k=n),
        "survival_months": [random.randint(6, 60) for _ in range(n)],
    }), "synthetic"


df, source = load_synthetic_or_omop()

cancer_types = df["cancer_type"].unique().tolist()
st.sidebar.header("Filter Data")
selected_cancer = st.sidebar.multiselect("Cancer Type", cancer_types, default=cancer_types)
filtered_df = df[df["cancer_type"].isin(selected_cancer)]

st.subheader("Patient Demographics")
cols = [c for c in ["patient_id", "age", "gender", "cancer_type", "stage"] if c in filtered_df.columns]
st.dataframe(filtered_df[cols] if cols else filtered_df.head())

try:
    import plotly.express as px
    st.subheader("Cancer Type Distribution")
    fig1 = px.histogram(filtered_df, x="cancer_type", color="gender", barmode="group", title="Cancer Type by Gender")
    st.plotly_chart(fig1, use_container_width=True)
    if "biomarker_status" in filtered_df.columns and "treatment" in filtered_df.columns:
        st.subheader("Biomarker Status vs. Treatment")
        fig2 = px.histogram(filtered_df, x="biomarker_status", color="treatment", barmode="group")
        st.plotly_chart(fig2, use_container_width=True)
    if "survival_months" in filtered_df.columns:
        st.subheader("Survival Time Distribution")
        fig3 = px.histogram(filtered_df, x="survival_months", nbins=8)
        st.plotly_chart(fig3, use_container_width=True)
except ImportError:
    st.info("Install plotly for charts: pip install plotly")

st.markdown("---")
st.caption(f"Data source: {source} | Biomedical Data Platform")
