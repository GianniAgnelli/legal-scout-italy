import requests
import os
import json

SERPER_KEY = os.getenv('SERPER_API_KEY')

def search_legal_jobs():
    url = "https://google.serper.dev/search"
    
    # Usiamo le TUE parole esatte, divise in query che Google possa digerire meglio
    # Proprio come se le scrivessi tu nella barra di ricerca
    queries = [
        'avviso bando "short list" avvocati 2026',
        'costituzione elenco avvocati difesa ente',
        'selezione professionisti legali amministrazione trasparente',
        'site:traspare.com avvocato',
        'site:4clegal.com bando'
    ]
    
    tutti_i_risultati = []
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}

    print("--- INIZIO RICERCA AGGRESSIVA ---")

    for q in queries:
        # 'tbs': 'qdr:m' è il comando segreto per "Ultimo Mese"
        payload = json.dumps({"q": q, "gl": "it", "hl": "it", "tbs": "qdr:m"})
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            items = response.json().get('organic', [])
            print(f"Query: {q} | Trovati: {len(items)} risultati")
            for item in items:
                tutti_i_risultati.append(f"TITOLO: {item['title']}\nLINK: {item['link']}\n")
        else:
            print(f"Errore nella query {q}: {response.text}")

    return list(set(tutti_i_risultati))

if __name__ == "__main__":
    risultati = search_legal_jobs()
    
    if risultati:
        print(f"\n✅ TOTALE RISULTATI UNICI: {len(risultati)}")
        for r in risultati[:20]: # Ne stampiamo 20 nei log per vedere se esistono
            print(r)
    else:
        print("\n❌ INCREDIBILE: Ancora 0 risultati. Verificare Serper Key.")
