from mysql.connector import connect, Error
from tkinter import messagebox

def get_connection():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="",
            database="lagerverwaltung"
        )
        return connection
    except Error as e:
        print(f"[FEHLER] Verbindung zur Datenbank fehlgeschlagen: {e}")
        return None

def create_table():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produkte (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    menge INT NOT NULL,
                    preis FLOAT NOT NULL,
                    kategorie VARCHAR(50) NOT NULL
                )
            """)
            connection.commit()
            print("[INFO] Tabelle 'produkte' erstellt oder existiert bereits.")
        except Error as e:
            print(f"[FEHLER] Tabelle konnte nicht erstellt werden: {e}")
        finally:
            connection.close()

def produkt_pruefen_und_hinzufuegen(name, menge, preis, kategorie):
    connection = get_connection()
    gesamtkosten = 0
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT menge, preis FROM produkte WHERE name = %s AND kategorie = %s",
                (name, kategorie)
            )
            result = cursor.fetchone()

            if result:
                connection.close()
                raise Exception("Dieses Produkt existiert schon.")
                
            cursor.execute(
                "INSERT INTO produkte (name, menge, preis, kategorie) VALUES (%s, %s, %s, %s)",
                (name, int(menge), float(preis), kategorie))
            gesamtkosten = int(menge) * float(preis)
            connection.commit()
        except Error as e:
            print(f"[FEHLER] Fehler beim Einfügen: {e}")
        finally:
            connection.close()
    return gesamtkosten

def produkt_bestellen(name, menge, kategorie):
    connection = get_connection()
    kosten = 0
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT preis, menge FROM produkte WHERE name = %s AND kategorie = %s", (name, kategorie))
            result = cursor.fetchone()
            if result:
                preis, aktuelle_menge = result
                neue_menge = aktuelle_menge + int(menge)
                kosten = float(preis) * int(menge)
                cursor.execute("UPDATE produkte SET menge = %s WHERE name = %s AND kategorie = %s", (neue_menge, name, kategorie))
                connection.commit()
            else:
                raise Exception("Produkt nicht gefunden.")
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()
    return kosten

def produkt_entfernen(name, menge, kategorie):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT menge FROM produkte WHERE name = %s AND kategorie = %s", (name, kategorie))
            result = cursor.fetchone()
            if result:
                aktuelle_menge = result[0]
                neue_menge = aktuelle_menge - int(menge)
                if neue_menge <= 0:
                    neue_menge = 0
                    messagebox.showwarning("Achtung!", f"Produkt '{name}' ist aufgebraucht. Bitte nachbestellen!")
                cursor.execute("UPDATE produkte SET menge = %s WHERE name = %s AND kategorie = %s", (neue_menge, name, kategorie))
                connection.commit()
            else:
                raise Exception("Produkt nicht gefunden.")
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()

def produkte_fuer_kategorie(kategorie, min_menge=None):
    connection = get_connection()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            if kategorie == "%":
                if min_menge is not None:
                    cursor.execute("SELECT name, menge, kategorie FROM produkte WHERE menge >= %s ORDER BY kategorie", (min_menge,))
                else:
                    cursor.execute("SELECT name, menge, kategorie FROM produkte ORDER BY kategorie")
            else:
                if min_menge is not None:
                    cursor.execute("SELECT name, menge FROM produkte WHERE kategorie = %s AND menge >= %s", (kategorie, min_menge))
                else:
                    cursor.execute("SELECT name, menge FROM produkte WHERE kategorie = %s", (kategorie,))
            results = cursor.fetchall()
            for row in results:
                if kategorie == "%":
                    output += f"- {row[0]} ({row[2]}): {row[1]} Stück\n"
                else:
                    output += f"- {row[0]}: {row[1]} Stück\n"
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()
    return output

def produktnamen_fuer_kategorie(kategorie):
    connection = get_connection()
    produktnamen = []
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name FROM produkte WHERE kategorie = %s", (kategorie,))
            results = cursor.fetchall()
            produktnamen = [row[0] for row in results]
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()
    return produktnamen

def alle_produkte(mit_null=True):
    connection = get_connection()
    output = ""
    if connection:
        cursor = connection.cursor()
        try:
            if mit_null:
                cursor.execute("SELECT name, menge, kategorie FROM produkte ORDER BY kategorie")
            else:
                cursor.execute("SELECT name, menge, kategorie FROM produkte WHERE menge > 0 ORDER BY kategorie")
            results = cursor.fetchall()
            for row in results:
                output += f"- {row[0]} ({row[2]}): {row[1]} Stück\n"
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()
    return output

def get_produkte(mit_null=True):
    connection = get_connection()
    produkte = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            if mit_null:
                cursor.execute("SELECT name, menge, preis, kategorie FROM produkte ORDER BY kategorie, name")
            else:
                cursor.execute("SELECT name, menge, preis, kategorie FROM produkte WHERE menge > 0 ORDER BY kategorie, name")
            produkte = cursor.fetchall()
        except Error as e:
            raise Exception(f"Datenbankfehler: {e}")
        finally:
            connection.close()
    return produkte