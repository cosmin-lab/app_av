# frontend.py
import tkinter as tk
from tkinter import messagebox
from backend import registrazione_dipendente, disponibilita_settimanale

def callback_registrazione():
    # Ottieni i dati dalla GUI
    nome = entry_nome.get()
    cognome = entry_cognome.get()
    luogo_nascita = entry_luogo_nascita.get()
    data_nascita = entry_data_nascita.get()
    codice_fiscale = entry_codice_fiscale.get()
    numero_telefono = entry_numero_telefono.get()
    indirizzo = entry_indirizzo.get()
    data_assunzione = entry_data_assunzione.get()

    # Chiama la funzione di registrazione nel backend
    risultato = registrazione_dipendente(
        lista_dipendenti, nome, cognome, luogo_nascita, data_nascita,
        codice_fiscale, numero_telefono, indirizzo, data_assunzione
    )

    # Visualizza il risultato, ad esempio, in una finestra di dialogo
    messagebox.showinfo("Risultato Registrazione", risultato)

# Creazione della finestra principale
root = tk.Tk()
root.title("Gestione Dipendenti")

# Aggiungi elementi GUI come etichette, caselle di testo, pulsanti, ecc.
# ...

# Pulsanti con funzioni di callback
btn_registrazione = tk.Button(root, text="Registrati", command=callback_registrazione)
btn_registrazione.pack()

# Aggiungi altri elementi GUI come necessario
# ...

# Loop principale dell'interfaccia grafica
root.mainloop()