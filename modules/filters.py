import streamlit as st

def sidebar_filters(df):

    year_range = st.sidebar.slider(
        "Year range",
        int(df["year"].min()),
        int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max()))
    )

    def multiselect(label, col):
        values = df[col].dropna().unique()
        return st.sidebar.multiselect(label, values, default=values)

    filters = {
        "year_range": year_range,
        "approche": multiselect("Approaches", "approche simplifié"),
        "method": multiselect("Main Method", "main method"),
        "etat": multiselect("State", "etat"),
        "application": multiselect("Application", "Application"),
    }

    return filters


def apply_filters(df, f):
    return df[
        (df["year"].between(*f["year_range"])) &
        (df["approche simplifié"].isin(f["approche"])) &
        (df["main method"].isin(f["method"])) &
        (df["etat"].isin(f["etat"])) &
        (df["Application"].isin(f["application"]))
    ]