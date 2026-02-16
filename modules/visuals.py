import streamlit as st
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from modules import TEXT_COLUMNS
import matplotlib.pyplot as plt

def plot_publications(df_filtered):
    st.markdown("### 📊 Publications per Year")
    fig = px.histogram(
        df_filtered,
        x="year",
        color="approche simplifié",
        barmode="group",
        title="Publications per Year by Approach"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_top_journals(df_filtered, top_n=10):
    st.markdown("### 🏛 Top Journals/Conferences")
    top_journals = df_filtered["journal or conference"].value_counts().head(top_n).reset_index()
    top_journals.columns = ["Journal", "Count"]
    fig = px.bar(
        top_journals,
        x="Journal",
        y="Count",
        color="Count",
        text="Count",
        title=f"Top {top_n} Journals/Conferences"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_occurrences(df_filtered):
    st.markdown("### 📈 Occurrences by Category")
    col1, col2 = st.columns(2)

    with col1:
        for col_name, title in [("main method", "Main Method"),
                                ("approche simplifié", "Approach"),
                                ("Application", "Applications")]:
            counts = df_filtered[col_name].value_counts().reset_index()
            counts.columns = [title, "Count"]
            st.markdown(f"**{title}**")
            st.dataframe(counts, use_container_width=True)

    with col2:
        for col_name, title in [("main method", "Main Method"),
                                ("approche simplifié", "Approach"),
                                ("Application", "Applications")]:
            counts = df_filtered[col_name].value_counts().reset_index()
            counts.columns = [title, "Count"]
            fig = px.pie(counts, names=title, values="Count", title=f"Distribution of {title}s")
            st.plotly_chart(fig, use_container_width=True)

def plot_wordcloud(df_filtered):
    st.markdown("### 📝 Text Analysis – Word Cloud")
    available_text_cols = {
        label: col for label, col in TEXT_COLUMNS.items()
        if col in df_filtered.columns
    }
    
    if not available_text_cols:
        st.info("No text columns available (abstract / keywords / keywords_plus).")
        return

    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        wc_label = st.radio("Select text source", options=list(available_text_cols.keys()), horizontal=True)
    with col_ctrl2:
        max_words_wc = st.slider("Max words", min_value=20, max_value=300, value=80, step=10)

    wc_source = available_text_cols[wc_label]
    text_data = (
        df_filtered[wc_source]
        .dropna()
        .astype(str)
        .str.replace(";", " ")
        .str.replace(",", " ")
        .str.cat(sep=" ")
    )

    if not text_data.strip():
        st.warning("⚠️ No valid text available for the selected source.")
        return

    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stopwords,
        max_words=max_words_wc,
        collocations=False
    ).generate(text_data)

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)