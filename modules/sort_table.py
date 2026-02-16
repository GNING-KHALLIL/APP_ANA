import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
def sortable_dataframe(
    df,
    candidate_columns,
    default_sort=None,
    title="🔀 Drag & Drop sort priority"
):
    """
    DataFrame sortable avec :
    - Drag & drop pour priorité de tri
    - Asc / Desc par colonne
    - Suppression individuelle de critères
    - Clear all
    - Tri insensible à la casse
    """

    if df is None or df.empty:
        st.info("No data to display.")
        return df

    # Colonnes disponibles
    sort_columns = [c for c in candidate_columns if c in df.columns]
    if not sort_columns:
        st.warning("No sortable columns available.")
        return df

    st.markdown(f"### {title}")

    # Init session_state
    if "sort_by" not in st.session_state:
        st.session_state.sort_by = default_sort or []

    # =====================
    # Drag & Drop pour priorité
    # =====================
    st.caption("Drag columns to define sorting priority")

    sort_by = sort_items(
        items=st.session_state.sort_by or sort_columns,
        direction="horizontal",
        key="sortable_columns"
    )

    # Garder uniquement colonnes valides
    st.session_state.sort_by = [c for c in sort_by if c in sort_columns]

    # =====================
    # Ordres + suppression
    # =====================
    sort_orders = []

    if st.session_state.sort_by:
        st.markdown("#### Sorting rules (all on the same row)")

        # Créer autant de colonnes que de critères, avec trois sous-colonnes chacun : nom / asc-desc / remove
        cols = st.columns(len(st.session_state.sort_by))

        for i, col_name in enumerate(st.session_state.sort_by):
            col = cols[i]

            with col:
                st.markdown(f"**{col_name}**")

                order = st.radio(
                    "",
                    ["Ascending", "Descending"],
                    horizontal=True,
                    key=f"order_{col_name}"
                )
                sort_orders.append(order == "Ascending")

                if st.button("❌", key=f"remove_{col_name}_{i}"):
                    st.session_state.sort_by.remove(col_name)
                    sort_orders.pop(-1)
                    st.rerun()
            # Bouton Clear all
        if st.button("🧹 Clear all sorting"):
            st.session_state.sort_by = []
            st.rerun()

    # =====================
    # Appliquer le tri (case-insensitive) tout en gardant toutes les colonnes
    # =====================
    df_sorted = df.copy()  # garder toutes les colonnes

    if st.session_state.sort_by:
        # Préparer un DataFrame temporaire pour le tri insensible à la casse
        df_sort_temp = pd.DataFrame()
        for col in st.session_state.sort_by:
            if df[col].dtype == object:
                df_sort_temp[col] = df[col].str.lower()
            else:
                df_sort_temp[col] = df[col]

        # Trier et récupérer les index triés
        sorted_index = df_sort_temp.sort_values(
            by=st.session_state.sort_by,
            ascending=sort_orders,
            kind="mergesort"
        ).index

        # Appliquer l'ordre au DataFrame original
        df_sorted = df_sorted.loc[sorted_index]

    # Réinitialiser l’index
    df_sorted = df_sorted.reset_index(drop=True)

    
    return df_sorted