import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def query_data_from_db(search_query, db_name='ebay_data.db'):
    """Fragt die Datenbank ab und gibt die Daten für eine bestimmte Suchanfrage in einem DataFrame zurück."""
    conn = sqlite3.connect(db_name)
    query = '''
        SELECT date, price 
        FROM ebay_products 
        WHERE search_query = ? 
        ORDER BY date ASC
    '''
    df = pd.read_sql_query(query, conn, params=(search_query,))
    conn.close()
    return df

def plot_combined_price_trends(search_queries, db_name='ebay_data.db'):
    """Visualisiert die Preis-Trends für mehrere Suchanfragen in einem Diagramm."""
    plt.figure(figsize=(12, 8))

    for query in search_queries:
        df = query_data_from_db(query, db_name)
        if df.empty:
            print(f"Keine Daten für den Preisverlauf von '{query}' gefunden.")
            continue

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        plt.plot(df.index, df['price'], marker='o', linestyle='-', label=query)

    plt.title('Preisverlauf für verschiedene Suchanfragen')
    plt.xlabel('Datum')
    plt.ylabel('Preis (€)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Beispiel-Suchanfragen
search_queries = ['elden ring', 'dragonball']

# Kombiniertes Diagramm für alle Suchanfragen
plot_combined_price_trends(search_queries)
