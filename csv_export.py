import csv
from datetime import datetime
import db

def exportiere_lagerbestand(dateipfad=None, nur_vorhandene=True):
    """
    Exportiert den Lagerbestand als CSV-Datei
    :param dateipfad: Optionaler Pfad für die CSV-Datei
    :param nur_vorhandene: Wenn True, nur Produkte mit Menge > 0
    :return: Pfad der erstellten Datei
    """
    if dateipfad is None:
        datum = datetime.now().strftime("%Y-%m-%d_%H-%M")
        dateipfad = f"lagerbestand_{datum}.csv"
    
    try:
        with open(dateipfad, mode='w', newline='', encoding='utf-8') as datei:
            writer = csv.writer(datei, delimiter=';')
            writer.writerow(['Name', 'Menge', 'Preis', 'Kategorie'])
            
            # Daten aus der Datenbank holen
            if nur_vorhandene:
                daten = db.get_produkte(mit_null=False)
            else:
                daten = db.get_produkte(mit_null=True)
            
            for produkt in daten:
                writer.writerow([
                    produkt['name'],
                    produkt['menge'],
                    f"{produkt['preis']:.2f}",
                    produkt['kategorie']
                ])
        
        return dateipfad
    except Exception as e:
        raise Exception(f"Fehler beim CSV-Export: {str(e)}")