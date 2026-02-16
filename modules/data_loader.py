import pandas as pd
import streamlit as st
from modules import REQUIRED_COLUMNS, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, DEFAULT_DATA_PATH

def _validate_file(file):
    ext = file.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    size_mb = file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError("File too large")

    return ext


@st.cache_data(ttl=3600)
def load_data(file=None):
    if file is None:
        df = pd.read_csv(DEFAULT_DATA_PATH)
        source = DEFAULT_DATA_PATH
    else:
        ext = _validate_file(file)
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        source = file.name

    _validate_columns(df)
    _sanitize_dataframe(df)

    return df, source


def _validate_columns(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def _sanitize_dataframe(df):
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["times cited"] = pd.to_numeric(df["times cited"], errors="coerce").fillna(0)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()