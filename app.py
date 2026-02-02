import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("word_list_es_2000.csv")

df = load_data()

st.title("Apprentissage de l'espagnol avec Flashcards")

# --- Barre latérale pour filtrer par rang ---
st.sidebar.header("Mots les plus fréquents - Filtrer par rang")
#st.sidebar.("Sélectionnez la plage de rangs")

min_rank = int(df['Rank'].min())
max_rank = int(df['Rank'].max())

min_range = st.sidebar.number_input("Rang minimum", min_value=min_rank, max_value=max_rank, value=min_rank, step=1)
max_range = st.sidebar.number_input("Rang maximum", min_value=min_rank, max_value=max_rank, value=max_rank, step=1)
#selected_range = st.sidebar.slider(
#    "Sélectionnez la plage de rangs",
#    min_value=min_range,
#    max_value=max_range,
#    value=(min_rank, max_rank)
#)

# Filtrer les mots en fonction de la plage sélectionnée
filtered_df = df[(df['Rank'] >= min_range) & (df['Rank'] <= max_range)]

# --- Choix de la direction de traduction ---
direction = st.sidebar.selectbox("Direction de traduction", ["FR -> ES", "ES -> FR"])
selection = st.sidebar.selectbox("Revision", ["mots", "phrases"])

# --- Gestion de la flashcard dans la session ---
if 'flashcard' not in st.session_state:
    st.session_state.flashcard = None

if st.button("Nouvelle flashcard"):
    if filtered_df.empty:
        st.warning("Aucun mot disponible dans la plage sélectionnée.")
    else:
        # Sélectionne aléatoirement une ligne du DataFrame filtré
        st.session_state.flashcard = filtered_df.sample(n=1).iloc[0]

# --- Affichage de la flashcard ---
if st.session_state.flashcard is not None:
    if selection == "mots":
        if direction == "FR -> ES":
            st.subheader("Traduisez ce mot en espagnol :")
            st.write(f"**{st.session_state.flashcard['French']}**")
        else:
            st.subheader("Traduisez ce mot en français :")
            st.write(f"**{st.session_state.flashcard['Spanish']}**")
        with st.expander("Afficher la réponse"):
            if direction == "FR -> ES":
                st.write("**Mot en espagnol :**", st.session_state.flashcard['Spanish'])
            else:
                st.write("**Mot en français :**", st.session_state.flashcard['French'])
            st.write("**Exemple de phrase :**", st.session_state.flashcard['Phrase_ES'])
            st.write("**Traduction de la phrase :**", st.session_state.flashcard['Phrase_FR'])
    else:
        if direction == "FR -> ES":
            st.subheader("Traduisez cette phrase en espagnol :")
            st.write(f"**{st.session_state.flashcard['Phrase_FR']}**")
        else:
            st.subheader("Traduisez cette phrase en français :")
            st.write(f"**{st.session_state.flashcard['Phrase_ES']}**")
    
        with st.expander("Afficher la réponse"):
            st.write("**Exemple de phrase :**", st.session_state.flashcard['Phrase_ES'])
            st.write("**Traduction de la phrase :**", st.session_state.flashcard['Phrase_FR'])
with st.expander("Afficher la table filtrée"):
    st.dataframe(filtered_df)
