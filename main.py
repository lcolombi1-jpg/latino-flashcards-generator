import streamlit as st
import re
import random

# Funzione di analisi (rimane quasi uguale)
def crea_flashcards(testo):
    flashcards = []
    schema = re.compile(r"([^(]+)\s+\[.*?\]:\s+(.*)")
    linee = testo.strip().split('\n')
    for linea in linee:
        linea_pulita = re.sub(r"\(\d+\)", "", linea).strip()
        match = schema.search(linea_pulita)
        if match:
            info_latina = match.group(1).strip()
            traduzione = match.group(2).strip()
            parti_latine = info_latina.split()
            if parti_latine:
                flashcards.append({"fronte": parti_latine[0], "retro": f"{info_latina} \n\n Traduzione: {traduzione}"})
    return flashcards

# --- INTERFACCIA STREAMLIT ---
st.title("📇 Generatore Flashcards di Latino")

try:
    with open("lessico.txt", "r", encoding="utf-8") as file:
        contenuto = file.read()
    
    cards = crea_flashcards(contenuto)
    
    if "indice" not in st.session_state:
        st.session_state.indice = 0
        random.shuffle(cards)
        st.session_state.cards = cards

    attuale = st.session_state.cards[st.session_state.indice]

    # Visualizzazione Flashcard
    with st.container():
        st.subheader("Parola:")
        st.info(f"### {attuale['fronte']}")
        
        if st.button("Mostra Retro"):
            st.success(attuale['retro'])

    if st.button("Prossima Parola ➡️"):
        if st.session_state.indice < len(st.session_state.cards) - 1:
            st.session_state.indice += 1
            st.rerun()
        else:
            st.write("Hai finito il lessico! Ricarica per ricominciare.")

except FileNotFoundError:
    st.error("Errore: Assicurati che 'lessico.txt' sia caricato su GitHub insieme a main.py")
