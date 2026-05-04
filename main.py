import re
import random

def crea_flashcards(testo):
    flashcards = []
    # Schema per trovare Lemma [Etimologia]: Traduzione
    schema = re.compile(r"([^(]+)\s+\[.*?\]:\s+(.*)")

    linee = testo.strip().split('\n')
    
    for linea in linee:
        # Rimuove numeri tra parentesi come (20)
        linea_pulita = re.sub(r"\(\d+\)", "", linea).strip()
        
        match = schema.search(linea_pulita)
        if match:
            info_latina = match.group(1).strip() 
            traduzione = match.group(2).strip() 
            
            parti_latine = info_latina.split()
            if parti_latine:
                fronte = parti_latine[0]
                retro = f"{info_latina} | Traduzione: {traduzione}"
                flashcards.append({"fronte": fronte, "retro": retro})

    random.shuffle(flashcards)
    return flashcards

# --- NUOVA PARTE: LETTURA DAL FILE ---

nome_file = "lessico.txt"

try:
    # Apriamo il file in modalità lettura ('r') con codifica 'utf-8'
    with open(nome_file, "r", encoding="utf-8") as file:
        contenuto_file = file.read()
        
    # Usiamo la funzione con il testo letto dal file
    lista_flashcards = crea_flashcards(contenuto_file)

    print(f"--- GENERATORE DI FLASHCARDS DA FILE ---")
    print(f"Caricate {len(lista_flashcards)} parole da '{nome_file}'.\n")

    # Mostriamo le prime 5 per prova
    for i, card in enumerate(lista_flashcards[:5], 1):
        print(f"FLASHCARD {i}")
        print(f"FRONTE: {card['fronte']}")
        print(f"RETRO: {card['retro']}")
        print("-" * 30)

except FileNotFoundError:
    print(f"Errore: Il file '{nome_file}' non è stato trovato. Assicurati che sia nella stessa cartella dello script.")
except Exception as e:
    print(f"Si è verificato un errore imprevisto: {e}")
