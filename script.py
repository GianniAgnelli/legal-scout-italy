import requests
import os
import json

SERPER_KEY = os.getenv('SERPER_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def invia_telegram(messaggio):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def search_legal_jobs():
    url = "https://google.serper.dev/search"
    
    # Query potenziate per coprire Comuni, Regioni, Province e Portali Regionali
    queries = [
        'site:.it "amministrazione trasparente" "avviso" "elenco avvocati" when:30d',
        'site:.it "short list" avvocati "difesa" when:30d',
        'site:start.toscana.it "incarico legale" OR "avvocato" when:30d',
        'site:sardegnacat.it "incarico legale" OR "avvocato" when:30d',
        'site:traspare.com "avviso" "legale" when:30d',
        'site:4clegal.com "bando" when:30d',
        'site:gazzettaufficiale.it "avviso" "avvocati" when:30d'
    ]
    
    nuovi_link = []
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}

    for q in queries:
        payload = json.dumps({"q": q, "gl": "it", "hl": "it", "num": 10})
        try:
            response = requests.post(url, headers=headers, data=payload)
            items = response.json().get('organic', [])
            for item in items:
                nuovi_link.append(f"⚖️ *{item['title']}*\n🔗 {item['link']}")
        except:
            continue
    
    # Rimuoviamo duplicati mantenendo l'ordine
    return list(dict.fromkeys(nuovi_link))

if __name__ == "__main__":
    risultati = search_legal_jobs()
    if risultati:
        # Dividiamo i messaggi se sono troppi (limite Telegram)
        testo_base = "🚀 *RADAR LEGALE PA (Ultimi 30gg)*\n\n"
        # Mandiamo i primi 15 risultati per non sovraccaricare
        invia_telegram(testo_base + "\n\n".join(risultati[:15]))
    else:
        invia_telegram("🔎 Nessun nuovo bando PA rilevato nelle ultime ricerche.")
