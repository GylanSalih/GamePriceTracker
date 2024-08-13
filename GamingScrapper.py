import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import sqlite3
import matplotlib.pyplot as plt

def load_filter_keywords(filepath):
    """Lädt Filter-Keywords aus einer Textdatei."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            keywords = file.read().splitlines()
        return [kw.lower() for kw in keywords if kw.strip()]
    except FileNotFoundError:
        print(f"Die Datei '{filepath}' wurde nicht gefunden.")
        return []

def extract_price(price_str):
    """Extrahiert den numerischen Preis aus einer Preiszeichenfolge und konvertiert ihn in float."""
    price_str = price_str.replace('€', '').replace('.', '').replace(',', '.').strip()
    match = re.search(r'\d+(\.\d{2})?', price_str)
    return float(match.group(0)) if match else None

def shorten_url(url):
    """Kürzt die URL für die Ausgabe auf die Basis-Domain."""
    base_url = "https://www.ebay.de/itm/"
    # Wenn die URL mit der Basis-URL beginnt, kürze sie auf die Basis-Domain
    if url.startswith(base_url):
        item_id = url[len(base_url):].split('?')[0]
        return f"https://www.ebay.com/itm/{item_id}"
    return url

def create_db_and_table(db_name='ebay_data.db'):
    """Erstellt eine SQLite-Datenbank und Tabelle, falls diese nicht existiert."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ebay_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_query TEXT,
            title TEXT,
            price REAL,
            condition TEXT,
            link TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def save_to_db(conn, df, search_query):
    """Speichert die eBay-Daten in der SQLite-Datenbank."""
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO ebay_products (search_query, title, price, condition, link)
            VALUES (?, ?, ?, ?, ?)
        ''', (search_query, row['title'], row['price'], row['condition'], row['shortened_link']))
    
    conn.commit()
    print(f"Daten wurden erfolgreich in der Datenbank gespeichert.")

def scrape_ebay(search_query, conditions, filter_keywords, language_keywords, max_pages=3, search_mode="buy_now"):
    items = []
    base_url = "https://www.ebay.de/sch/i.html?_nkw="
    
    # Mapping der Zustandsoptionen
    condition_mapping = {
        '1': '1000',   # Neu
        '2': '1500',   # Neuwertig
        '3': '1750',   # Sehr gut
        '4': '2000',   # Gut
        '5': '2500'    # Akzeptabel
    }
    
    # Prüfen, ob "6" (Alle) ausgewählt wurde
    if '6' in conditions:
        condition_codes_str = ''  # Keine Einschränkung auf Zustand
    else:
        # Zustandscodes aus den Eingaben sammeln
        condition_codes = [condition_mapping.get(cond.strip()) for cond in conditions if cond.strip() in condition_mapping]
        condition_codes_str = ','.join(condition_codes)

    # URL für die Suchanfrage
    url_query = f"{base_url}{search_query}&rt=nc"
    
    if condition_codes_str:
        url_query += f"&LH_ItemCondition={condition_codes_str}"

    if search_mode == "buy_now":
        url_query += "&LH_BIN=1"  # Nur Sofort-Kaufen
    elif search_mode == "completed":
        url_query += "&LH_Complete=1"  # Nur beendete Inserate
    elif search_mode == "sold":
        url_query += "&LH_Complete=1&LH_Sold=1"  # Nur verkaufte beendete Inserate

    url_query += "&_sacat=139973&_pgn="

    for page in range(1, max_pages + 1):
        url = f"{url_query}{page}&_stpos=0&LH_PrefLoc=2"  # Artikelstandort Deutschland
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.select('.s-item'):
            title = item.select_one('.s-item__title').text if item.select_one('.s-item__title') else "N/A"
            price = item.select_one('.s-item__price').text if item.select_one('.s-item__price') else "N/A"
            link = item.select_one('.s-item__link')['href'] if item.select_one('.s-item__link') else "N/A"
            condition = item.select_one('.SECONDARY_INFO').text if item.select_one('.SECONDARY_INFO') else "N/A"
            
            # Filtern nach dem exakten Produktnamen und Ausschluss von Keywords und Sprachen
            if (search_query.lower() in title.lower() 
                and not any(kw in title.lower() for kw in filter_keywords)
                and not any(lang in title.lower() for lang in language_keywords)):
                
                extracted_price = extract_price(price)
                if extracted_price:
                    items.append({
                        'title': title,
                        'price': extracted_price,
                        'condition': condition,
                        'shortened_link': shorten_url(link)  # Gekürzte URL
                    })
        
        time.sleep(2)  # Pause to avoid being blocked
    
    return pd.DataFrame(items)

def format_and_save_csv(df, search_query, conditions):
    """Formatieren und Speichern der CSV-Datei mit ansprechenderen Optionen."""
    if df.empty:
        print("Keine Artikel gefunden.")
        return
    
    # Sortieren der Daten nach Titel (alphabetisch) und Preis (aufsteigend)
    df = df.sort_values(by=['title', 'price'], ascending=[True, True]).reset_index(drop=True)
    
    # Berechnungen vor der Formatierung durchführen
    median_price = df['price'].median()
    lowest_price = df['price'].min()
    highest_price = df['price'].max()
    
    # Preis formatieren für die CSV-Ausgabe
    df['price'] = df['price'].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + ' €')

    # CSV-Datei speichern
    filename = f"ebay_{search_query.replace(' ', '_')}_{'_'.join(conditions)}_products.csv"
    df.to_csv(filename, index=False, columns=['title', 'price', 'condition', 'shortened_link'], header=['Titel', 'Preis', 'Zustand', 'Inserat Link'])
    
    # Ausgabe der Ergebnisse
    print(f"Daten gespeichert in {filename}")
    print(f"Der Medianpreis für '{search_query}' im Zustand {', '.join(conditions)} beträgt ca. {median_price:,.2f} €.")
    print(f"Der niedrigste Preis beträgt: {lowest_price:,.2f} €.")
    print(f"Der höchste Preis beträgt: {highest_price:,.2f} €.")

def analyze_price_trends(search_query, db_name='ebay_data.db'):
    """Analysiert und visualisiert den Preisverlauf eines bestimmten Produkts."""
    conn = sqlite3.connect(db_name)
    query = '''
        SELECT date, price 
        FROM ebay_products 
        WHERE search_query = ? 
        ORDER BY date ASC
    '''
    df = pd.read_sql_query(query, conn, params=(search_query,))
    conn.close()

    if df.empty:
        print("Keine Daten für den Preisverlauf gefunden.")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['price'].plot(title=f"Preisverlauf für {search_query}", ylabel="Preis (€)", xlabel="Datum")
    plt.show()

# Terminal-Abfragen:
search_term = input("Gib das Produkt ein, das du auf eBay suchen möchtest: ")

# Zustand wählen
print("Wähle den Zustand des Produkts (du kannst mehrere Optionen durch Komma getrennt eingeben):")
print("1. Neu")
print("2. Neuwertig")
print("3. Sehr gut")
print("4. Gut")
print("5. Akzeptabel")
print("6. Alle")

condition_choices = input("Gib die Zahlen ein, die den gewünschten Zuständen entsprechen: ").split(',')

# Filter-Keywords laden
filter_keywords = load_filter_keywords('filter_keywords.txt')

# Sprach-Keywords laden
language_keywords = load_filter_keywords('language_keywords.txt')

# Suchmodus auswählen:
print("Wählen Sie den Suchmodus:")
print("1. Nur Sofort-Kaufen Angebote")
print("2. Beendete Inserate")
print("3. Verkaufte beendete Inserate")

mode_choice = input("Gib die Zahl ein, die dem gewünschten Modus entspricht: ")

if mode_choice == "1":
    search_mode = "buy_now"
elif mode_choice == "2":
    search_mode = "completed"
elif mode_choice == "3":
    search_mode = "sold"
else:
    print("Ungültige Auswahl, es wird nur 'Sofort-Kaufen' durchsucht.")
    search_mode = "buy_now"

# Daten abrufen
ebay_data = scrape_ebay(search_term, condition_choices, filter_keywords, language_keywords, search_mode=search_mode)

# SQLite-Datenbank erstellen oder öffnen
conn = create_db_and_table()

# Daten in die Datenbank speichern
if not ebay_data.empty:
    save_to_db(conn, ebay_data, search_term)
    format_and_save_csv(ebay_data, search_term, condition_choices)
else:
    print("Keine Artikel gefunden.")

# Preisverlauf analysieren
analyze_price_trends(search_term)
