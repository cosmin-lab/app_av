from flask import Flask, render_template, request
import uuid
from tabulate import tabulate
from datetime import datetime, timedelta
from geopy.distance import geodesic

app = Flask(__name__)

# Lista per memorizzare le informazioni dei dipendenti
lista_dipendenti = []

# Lista per memorizzare le presenze dei dipendenti
lista_presenze = []

# Coordinata GPS di Via Santo Stefano a Bologna (sostituiscila con la tua)
via_santo_stefano_coords = (44.493935, 11.343686)

# Definisco le route
@app.route('/')
def home():
    return render_template('frontendhtml.html')

@app.route('/registrazione')
def registrazione():
    return render_template('registrazione.html')

@app.route('/accedi')
def accedi():
    return render_template('accedi.html')

@app.route('/tabella-dipendenti')
def tabella_dipendenti():
    return render_template('tabella_dipendenti.html')

@app.route('/registra-entrata')
def regista_entrata():
    return render_template('registra_entrata.html')

@app.route('/registra-uscita')
def registra_uscita():
    return render_template('registra_uscita.html')

@app.route('/genera-report-mensile')
def genera_report_mensile():
    return render_template('genera_report_mensile.html')

@app.route('/esci')
def esci():
    return "Grazie e arrivederci"

# Altre definizioni di funzioni

def ottieni_ora_attuale():
    return datetime.utcnow()

def ottieni_posizione_attuale():
    # Simuliamo la posizione del dipendente (sostituiscila con la tua logica)
    return via_santo_stefano_coords

def calcola_distanza(coord1, coord2):
    return geodesic(coord1, coord2).meters

def genera_id():
    return str(uuid.uuid4())

def registrati():
    global lista_dipendenti
    print("Registrazione di un nuovo dipendente:")
    nome = input("Nome: ")
    cognome = input("Cognome: ")
    luogo_nascita = input("Luogo di nascita: ")
    data_nascita = input("Data di nascita (YYYY-MM-DD): ")
    anno_corrente = 2024  # Anno corrente (può essere aggiornato)
    anno_nascita = int(data_nascita.split('-')[0])
    eta = anno_corrente - anno_nascita

    if eta < 18:
        print("Spiacenti, devi avere almeno 18 anni per registrarti come dipendente.")
        return

    codice_fiscale = input("Codice Fiscale: ")

    while len(codice_fiscale) != 16:
        print("Il codice fiscale deve essere lungo 16 caratteri.")
        codice_fiscale = input("Codice Fiscale: ")

    codice_fiscale = codice_fiscale.upper()

    numero_telefono = input("Numero di Telefono: ")
    indirizzo = input("Indirizzo: ")
    data_assunzione = input("Data di assunzione (YYYY-MM-DD): ")

    id_dipendente = genera_id()

    dipendente = {
        'ID': id_dipendente,
        'Nome': nome,
        'Cognome': cognome,
        'Luogo di Nascita': luogo_nascita,
        'Data di Nascita': data_nascita,
        'Età': eta,
        'Codice Fiscale': codice_fiscale,
        'Numero di Telefono': numero_telefono,
        'Indirizzo': indirizzo,
        'Data di Assunzione': data_assunzione,
        'Contratto': None,
        'Disponibilità Settimanale': {}
    }

    lista_dipendenti.append(dipendente)

    print(f"Registrazione completata con successo! ID del dipendente: {id_dipendente}")

    giorni_settimana = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

    for giorno in giorni_settimana:
        print(f"\nSeleziona la disponibilità per {giorno}:")
        print("1. Turno Mattina (10:30 - 18:30)")
        print("2. Turno Sera")
        print("3. Turno Extra")

        scelta_disponibilita = input("Scelta (1/2/3): ")

        if scelta_disponibilita == '1':
            dipendente['Disponibilità Settimanale'][giorno] = 'Turno Mattina (10:30 - 18:30)'
        elif scelta_disponibilita == '2':
            if giorno in ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì']:
                dipendente['Disponibilità Settimanale'][giorno] = 'Turno Sera (16:30 - 00:30)'
            elif giorno == 'Venerdì' or giorno == 'Sabato':
                dipendente['Disponibilità Settimanale'][giorno] = 'Turno Sera (17:30 - 01:30)'
            elif giorno == 'Domenica':
                dipendente['Disponibilità Settimanale'][giorno] = 'Turno Sera (15:30 - 23:30)'
            else:
                print("Scelta non valida. La disponibilità non è stata registrata per questo giorno.")
        elif scelta_disponibilita == '3':
            turno_extra = input("Inserisci l'orario del Turno Extra (formato HH:MM - HH:MM): ")
            dipendente['Disponibilità Settimanale'][giorno] = f'Turno Extra: {turno_extra}'
        else:
            print("Scelta non valida. La disponibilità non è stata registrata per questo giorno.")

def accedi_dipendente():
    global lista_dipendenti
    id_dipendente = input("Inserisci l'ID del dipendente: ")

    for dipendente in lista_dipendenti:
        if dipendente['ID'] == id_dipendente:
            print("\nDati del dipendente:")
            for chiave, valore in dipendente.items():
                print(f"{chiave}: {valore}")
            return

    print("Nessun dipendente trovato con l'ID fornito.")

def visualizza_tabella():
    global lista_dipendenti
    headers = ["ID", "Disponibilità Settimanale"]

    data = []
    for dipendente in lista_dipendenti:
        row = [dipendente['ID'], formatta_disponibilita(dipendente)]
        data.append(row)

    print(tabulate(data, headers, tablefmt="pretty"))

def formatta_disponibilita(dipendente):
    disponibilita_formattata = ""
    for giorno, disponibilita in dipendente['Disponibilità Settimanale'].items():
        disponibilita_formattata += f"{giorno}: {disponibilita}\n"
    return disponibilita_formattata.strip()

def crea_report_mensile():
    global lista_presenze, lista_dipendenti
    # Ottieni la data attuale
    oggi = datetime.utcnow()

    # Creazione di un dizionario per raccogliere le informazioni mensili
    report_mensile = {}

    for dipendente in lista_dipendenti:
        id_dipendente = dipendente['ID']
        nome_dipendente = f"{dipendente['Nome']} {dipendente['Cognome']}"
        ore_totali = timedelta()

        # Creazione di un dizionario per raccogliere le informazioni giornaliere
        report_giornaliero = {}

        for presenza in lista_presenze:
            if presenza['ID'] == id_dipendente and presenza['Entrata'].month == oggi.month:
                giorno = presenza['Entrata'].strftime('%A, %Y-%m-%d')
                ora_entrata = presenza['Entrata'].strftime('%H:%M')
                ora_uscita = presenza['Uscita'].strftime('%H:%M') if presenza['Uscita'] else "N/A"

                # Calcola la durata del turno
                durata_turno = presenza['Uscita'] - presenza['Entrata'] if presenza['Uscita'] else timedelta()

                # Aggiungi la durata del turno alle ore totali
                ore_totali += durata_turno

                report_giornaliero[giorno] = {
                    'Entrata': ora_entrata,
                    'Uscita': ora_uscita,
                    'Durata': str(durata_turno)
                }

        # Aggiungi le informazioni mensili al report totale
        report_mensile[nome_dipendente] = {
            'Report Giornaliero': report_giornaliero,
            'Ore Totali': str(ore_totali)
        }

    return report_mensile

# Esecuzione del server Flask
if __name__ == '__main__':
    app.run(debug=True)
