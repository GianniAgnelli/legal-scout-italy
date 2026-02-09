import requests
import os
import json

# Recupera le chiavi che hai appena inserito nei Secrets
SERPER_KEY = os.getenv('SERPER_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def invia_telegram(messaggio):
    """Invia il risultato direttamente sul tuo cellulare"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def search_legal_jobs():
    url = "https://google.serper.dev/search"
    # Ricerca estesa agli ultimi 20 giorni per non perdere nulla
    queries = [
        'site:4clegal.com "civile" OR "lavoro" when:20d',
        'site:traspare.com "incarico legale" "civile" when:20d',
        'site:.it "amministrazione trasparente" "incarico legale" civile when:20d'
    ]
    
    nuovi_link = []
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}

    for q in queries:
        payload = json.dumps({"q": q, "gl": "it", "hl": "it"})
        response = requests.post(url, headers=headers, data=payload)
        items = response.json().get('organic', [])
        for item in items:
            nuovi_link.append(f"📌 *{item['title']}*\n{item['link']}")
    
    return list(set(nuovi_link)) # Elimina i doppioni

if __name__ == "__main__":
    risultati = search_legal_jobs()
    if risultati:
        testo_finale = "⚖️ *LEGAL SCOUT: BANDI TROVATI (Ultimi 20gg)*\n\n" + "\n\n".join(risultati)
        invia_telegram(testo_finale)
    else:
        invia_telegram("🔎 Ricerca completata: nessun nuovo bando trovato negli ultimi 20 giorni.")
