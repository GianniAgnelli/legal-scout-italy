import requests
import os
import json

API_KEY = os.getenv('SERPER_API_KEY')

def search_legal_jobs():
    url = "https://google.serper.dev/search"
    
    # Questa ricerca setaccia i portali specifici (4clegal, traspare, ecc.) 
    # e i siti della PA per Civile e Lavoro
    queries = [
        'site:4clegal.com "civile" OR "lavoro" "avviso"',
        'site:traspare.com "incarico legale" "civile"',
        'site:.it "amministrazione trasparente" "elenco avvocati" 2026',
        '"avviso pubblico" "patrocinio legale" civile lavoro when:1d'
    ]
    
    all_results = []
    headers = {'X-API-KEY': API_KEY, 'Content-Type': 'application/json'}

    for q in queries:
        payload = json.dumps({"q": q, "gl": "it", "hl": "it"})
        response = requests.post(url, headers=headers, data=payload)
        items = response.json().get('organic', [])
        for item in items:
            all_results.append(f"- {item['title']}\n  Link: {item['link']}")
    
    return "\n\n".join(all_results)

if __name__ == "__main__":
    report = search_legal_jobs()
    if report:
        print("INCARICHI TROVATI (CIVILE E LAVORO):\n")
        print(report)
    else:
        print("Nessun nuovo bando trovato nelle ultime 24 ore.")
