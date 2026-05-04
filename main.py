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
        # Verifichiamo che ci siano i due punti E che non sia una riga vuota
        if ":" in linea:
            parti = linea.split(":", 1)
            latino_completo = parti[0].strip()
            traduzione = parti[1].strip()
            
            # PROTEZIONE: verifichiamo se c'è del testo prima dei due punti
            parti_latine = latino_completo.split(",")
            if parti_latine and parti_latine[0].strip():
                # Prendiamo la prima parte e dividiamo per spazi
                parole_nel_lemma = parti_latine[0].split()
                
                if parole_nel_lemma: # Solo se la lista non è vuota
                    lemma_principale = parole_nel_lemma[0]
                    
                    # Puliamo il lemma per il fronte
                    fronte = pulisci_lemma(lemma_principale)
                    
                    flashcards.append({
                        "fronte": fronte.upper(),
                        "retro": f"**Paradigma:** {latino_completo}\n\n**Traduzione:** {traduzione}"
                    })
            
    return flashcards

# --- INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Latino Flashcards", layout="centered")

try:
    contenuto = ""
    # Proviamo a leggere il file ignorando eventuali errori di caratteri strani
    try:
        with open("lessico.txt", "r", encoding="utf-8", errors="ignore") as f:
            contenuto = f.read()
    except UnicodeDecodeError:
        with open("lessico.txt", "r", encoding="latin-1", errors="ignore") as f:
            contenuto = f.read()

    # Pulizia di emergenza: se il file contiene simboli binari, li rimuoviamo
    contenuto = "".join(char for char in contenuto if char.isprintable() or char in "\n\r\t ")

    if contenuto and ":" in contenuto:
        cards = crea_flashcards(contenuto)
        # ... resto del codice per mostrare le card ...
    else:
        st.error("Il file sembra contenere dati illeggibili. Assicurati di aver copiato il TESTO dal PDF in un file .txt vero e proprio.")
except FileNotFoundError:
    st.error("File 'lessico.txt' non trovato.")
