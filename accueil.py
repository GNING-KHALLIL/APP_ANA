import streamlit as st
from modules import load_data, SORT_COLUMNS
from modules import sidebar_filters, apply_filters
from modules import show_kpis, plot_occurrences, plot_top_journals, plot_wordcloud, plot_publications, sortable_dataframe
st.set_page_config(
    page_title="Mangrove Bibliography Dashboard",
    layout="wide"
)

st.title("📚 Mangrove Bibliography Dashboard")

with st.sidebar:
    st.header("📂 Data source")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

try:
    df, source = load_data(uploaded_file)
    st.sidebar.success(f"Loaded: {source}")
except Exception as e:
    st.error(f"❌ {e}")
    st.stop()

filters = sidebar_filters(df)
df_filtered = apply_filters(df, filters)

show_kpis(df_filtered)

df_filtered_sorted = sortable_dataframe(
    df_filtered,
    candidate_columns=SORT_COLUMNS,
    default_sort=SORT_COLUMNS
)

st.dataframe(df_filtered_sorted, use_container_width=True)

plot_top_journals(df_filtered)
plot_wordcloud(df_filtered)
plot_publications(df_filtered)
plot_occurrences(df_filtered)