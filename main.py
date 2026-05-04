import streamlit as st
import re
import random

def pulisci_lemma(testo):
    # Rimuove i segni delle vocali lunghe/brevi per il fronte della card
    mappa = {"ā": "a", "ă": "a", "ē": "e", "ĕ": "e", "ī": "i", "ĭ": "i", "ō": "o", "ŏ": "o", "ū": "u", "ŭ": "u"}
    for chiave, valore in mappa.items():
        testo = testo.replace(chiave, valore)
    return testo

def crea_flashcards(testo):
    flashcards = []
    linee = testo.strip().split('\n')
    
    for linea in linee:
        linea = linea.strip()
        if ":" in linea:
            # Dividiamo tra latino (prima dei :) e traduzione (dopo i :)
            parti = linea.split(":", 1)
            latino_completo = parti[0].strip()
            traduzione = parti[1].strip()
            
            # Estraiamo il primo lemma (prima della virgola o dello spazio)
            # Es: "arcŭo, arquo" -> diventa "arcŭo"
            lemma_principale = latino_completo.split(",")[0].split()[0]
            
            # Puliamo il lemma per il fronte (opzionale, rimuove accenti grafici)
            fronte = pulisci_lemma(lemma_principale)
            
            flashcards.append({
                "fronte": fronte.upper(), # In maiuscolo per chiarezza
                "retro": f"**Paradigma:** {latino_completo}\n\n**Traduzione:** {traduzione}"
            })
            
    return flashcards

# --- INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Latino Flashcards", layout="centered")

try:
    contenuto = ""
    try:
        with open("lessico.txt", "r", encoding="utf-8") as f:
            contenuto = f.read()
    except UnicodeDecodeError:
        with open("lessico.txt", "r", encoding="latin-1") as f:
            contenuto = f.read()

    if contenuto:
        cards = crea_flashcards(contenuto)
        
        if not cards:
            st.warning("⚠️ Non ho trovato parole. Controlla che nel file ci siano i due punti (:) tra il latino e l'italiano.")
        else:
            if "indice" not in st.session_state:
                st.session_state.indice = 0
                st.session_state.cards = cards
                random.shuffle(st.session_state.cards)

            # Mostra progresso
            st.write(f"Parola {st.session_state.indice + 1} di {len(st.session_state.cards)}")
            
            # Box della Flashcard
            st.markdown(f"""
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; 
            background-color: #f0f2f6; border-radius: 15px; border: 3px solid #ff4b4b; margin-bottom: 20px;">
                <h1 style="color: #31333F; font-family: 'serif';">{st.session_state.cards[st.session_state.indice]['fronte']}</h1>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("👁️ MOSTRA RETRO", use_container_width=True):
                    st.info(st.session_state.cards[st.session_state.indice]['retro'])
            
            with col2:
                if st.button("PROSSIMA ➡️", use_container_width=True):
                    if st.session_state.indice < len(st.session_state.cards) - 1:
                        st.session_state.indice += 1
                        st.rerun()
                    else:
                        st.success("Mazzo completato!")
                        if st.button("Ricomincia"):
                            st.session_state.indice = 0
                            random.shuffle(st.session_state.cards)
                            st.rerun()
    else:
        st.error("Il file lessico.txt è vuoto.")
except FileNotFoundError:
    st.error("File 'lessico.txt' non trovato.")
