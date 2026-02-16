import streamlit as st

def show_kpis(df):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Papers", len(df))
    c2.metric("Unique Journals", df["journal or conference"].nunique())
    c3.metric("Unique Approaches", df["approche simplifié"].nunique())
    c4.metric("Max Citations", int(df["times cited"].max()))