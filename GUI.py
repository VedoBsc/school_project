import tkinter as tk
from tkinter import messagebox, filedialog
import db
import csv_export

# Hauptfenster der GUI erstellen
gui_root = tk.Tk()
gui_root.title("Lagerverwaltung")
gui_root.geometry("800x600")
gui_root.resizable(True, True)

modus = tk.StringVar()  # Variable für den aktuellen Modus

# Überschrift Label
tk.Label(gui_root, text="Lagerverwaltung", font=("Arial", 20)).pack(pady=10)

##################
# AUSGABEFELD
##################
output_box = tk.Text(gui_root, height=6, width=80, font=("Arial", 12))
output_box.config(state="disabled")
output_box.pack(pady=5)

def show_output(text):
    """Zeigt Text im Ausgabefeld an"""
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

##################
# HAUPTMENÜ BUTTONS
##################
button_frame = tk.Frame(gui_root)
button_frame.pack(pady=20)

# Hauptmenü-Buttons
tk.Button(button_frame, text="Produkt bestellen", font=("Arial", 14), width=25,
          command=lambda: zeige_formular("bestellen")).pack(pady=5)
tk.Button(button_frame, text="Produkt entfernen", font=("Arial", 14), width=25,
          command=lambda: zeige_formular("entfernen")).pack(pady=5)
tk.Button(button_frame, text="Produkt hinzufügen", font=("Arial", 14), width=25,
          command=lambda: zeige_formular("hinzufügen")).pack(pady=5)
tk.Button(button_frame, text="Produkte filtern", font=("Arial", 14), width=25,
          command=lambda: filter_kategorie_anzeigen()).pack(pady=5)
tk.Button(button_frame, text="Alle Produkte", font=("Arial", 14), width=25,
          command=lambda: alle_produkte_anzeigen()).pack(pady=5)
tk.Button(button_frame, text="CSV Export", font=("Arial", 14), width=25,
          command=lambda: export_dialog()).pack(pady=5)

##################
# FILTER-FRAME
##################
filter_frame = tk.Frame(gui_root)
tk.Label(filter_frame, text="Kategorie wählen:", font=("Arial", 12)).pack(side="left", padx=10)

filter_var = tk.StringVar()
kategorien = ["Widerstand", "Kondensator", "Spule", "IC", "Sonstiges", "%"]
filter_var.set(kategorien[0])
tk.OptionMenu(filter_frame, filter_var, *kategorien).pack(side="left")

menge_filter_var = tk.IntVar()
menge_filter_check = tk.Checkbutton(filter_frame, text="Nur mit Menge >", variable=menge_filter_var)
menge_filter_check.pack(side="left", padx=10)
menge_filter_entry = tk.Entry(filter_frame, width=5)
menge_filter_entry.pack(side="left")

tk.Button(filter_frame, text="Anzeigen", font=("Arial", 12),
          command=lambda: produkte_nach_kategorie()).pack(side="left", padx=10)

filter_frame.pack_forget()

filter_cancel_button = tk.Button(gui_root, text="Abbrechen", font=("Arial", 12), 
                               command=lambda: zurueck_zum_hauptmenue())
filter_cancel_button.pack_forget()

##################
# ALLE PRODUKTE FRAME
##################
alle_produkte_frame = tk.Frame(gui_root)
tk.Button(alle_produkte_frame, text="Alle Produkte anzeigen", font=("Arial", 12),
          command=lambda: show_output(db.alle_produkte(mit_null=True))).pack(side="left", padx=10)
tk.Button(alle_produkte_frame, text="Vorhandene Produkte anzeigen", font=("Arial", 12),
          command=lambda: show_output(db.alle_produkte(mit_null=False))).pack(side="left", padx=10)
tk.Button(alle_produkte_frame, text="Zurück", font=("Arial", 12),
          command=lambda: zurueck_zum_hauptmenue()).pack(side="left", padx=10)
alle_produkte_frame.pack_forget()

##################
# FORMULARE
##################
input_frame = tk.Frame(gui_root)

# Kategorie-Eingabe
input_kategorie = tk.Frame(input_frame)
tk.Label(input_kategorie, text="Kategorie:", font=("Arial", 12)).pack(side="left", padx=10)
kategorie_var = tk.StringVar()
kategorie_var.set(kategorien[0])
kategorie_optionmenu = tk.OptionMenu(input_kategorie, kategorie_var, *kategorien[:-1])
kategorie_optionmenu.pack(side="left")

# Produktname-Eingabe
input_produktname = tk.Frame(input_frame)
tk.Label(input_produktname, text="Produktname:", font=("Arial", 12)).pack(side="left", padx=10)

produktname_var = tk.StringVar()
produktname_optionmenu = tk.OptionMenu(input_produktname, produktname_var, "")
produktname_eingabe = tk.Entry(input_produktname, textvariable=produktname_var, font=("Arial", 12))

# Menge-Eingabe
input_menge = tk.Frame(input_frame)
tk.Label(input_menge, text="Menge:", font=("Arial", 12)).pack(side="left", padx=10)
title_menge_eingabe = tk.Entry(input_menge, font=("Arial", 12))
title_menge_eingabe.pack(side="left")

# Preis-Eingabe
input_preis = tk.Frame(input_frame)
tk.Label(input_preis, text="Preis (€):", font=("Arial", 12)).pack(side="left", padx=10)
title_preis_eingabe = tk.Entry(input_preis, font=("Arial", 12))
title_preis_eingabe.pack(side="left")

input_frame.pack_forget()
input_kategorie.pack_forget()
input_produktname.pack_forget()
input_menge.pack_forget()
input_preis.pack_forget()

# OK/Abbrechen Buttons
bottom_button_frame = tk.Frame(gui_root)
tk.Button(bottom_button_frame, text="OK", font=("Arial", 12), 
          command=lambda: ok_ausfuehren()).pack(side="left", padx=10)
tk.Button(bottom_button_frame, text="Abbrechen", font=("Arial", 12), 
          command=lambda: reset_gui()).pack(side="left", padx=10)
bottom_button_frame.pack_forget()

##################
# CSV EXPORT DIALOG
##################
def export_dialog():
    export_window = tk.Toplevel(gui_root)
    export_window.title("CSV Export")
    export_window.geometry("400x200")
    
    tk.Label(export_window, text="Exportoptionen", font=("Arial", 14)).pack(pady=10)
    
    nur_vorhandene_var = tk.BooleanVar(value=True)
    tk.Checkbutton(export_window, text="Nur vorhandene Produkte (Menge > 0)",
                  variable=nur_vorhandene_var).pack(pady=5)
    
    tk.Button(export_window, text="Export starten", font=("Arial", 12),
              command=lambda: start_export(nur_vorhandene_var.get(), export_window)).pack(pady=15)

def start_export(nur_vorhandene, window):
    try:
        dateipfad = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")],
            title="Lagerbestand speichern unter"
        )
        
        if dateipfad:
            export_pfad = csv_export.exportiere_lagerbestand(
                dateipfad=dateipfad,
                nur_vorhandene=nur_vorhandene
            )
            messagebox.showinfo("Erfolg", f"Lagerbestand wurde exportiert nach:\n{export_pfad}")
            window.destroy()
    except Exception as e:
        messagebox.showerror("Fehler", f"Export fehlgeschlagen:\n{str(e)}")

##################
# HILFSFUNKTIONEN
##################
def update_produktnamen(*args):
    kategorie = kategorie_var.get()
    produktnamen = db.produktnamen_fuer_kategorie(kategorie)
    produktname_var.set("")
    menu = produktname_optionmenu["menu"]
    menu.delete(0, "end")
    for name in produktnamen:
        menu.add_command(label=name, command=lambda value=name: produktname_var.set(value))
    if produktnamen:
        produktname_var.set(produktnamen[0])

kategorie_var.trace("w", update_produktnamen)

def zeige_formular(aktion):
    modus.set(aktion)
    button_frame.pack_forget()
    filter_frame.pack_forget()
    filter_cancel_button.pack_forget()
    alle_produkte_frame.pack_forget()

    input_kategorie.pack(pady=5)

    input_produktname.pack_forget()
    if aktion == "hinzufügen":
        produktname_optionmenu.pack_forget()
        produktname_eingabe.pack(side="left")
        input_produktname.pack(pady=5)
    else:
        produktname_eingabe.pack_forget()
        produktname_optionmenu.pack(side="left")
        input_produktname.pack(pady=5)
        update_produktnamen()

    input_menge.pack(pady=5)

    if aktion == "hinzufügen":
        input_preis.pack(pady=5)
    else:
        input_preis.pack_forget()

    input_frame.pack()
    bottom_button_frame.pack(pady=20)

def reset_gui():
    title_menge_eingabe.delete(0, tk.END)
    title_preis_eingabe.delete(0, tk.END)
    kategorie_var.set(kategorien[0])
    produktname_var.set("")

    input_frame.pack_forget()
    input_kategorie.pack_forget()
    input_produktname.pack_forget()
    input_menge.pack_forget()
    input_preis.pack_forget()
    bottom_button_frame.pack_forget()
    filter_frame.pack_forget()
    filter_cancel_button.pack_forget()
    alle_produkte_frame.pack_forget()
    button_frame.pack(pady=20)

def ok_ausfuehren():
    produkt = produktname_var.get().strip()
    menge = title_menge_eingabe.get().strip()
    kategorie = kategorie_var.get()
    preis = title_preis_eingabe.get().strip()

    if not produkt:
        show_output("❌ Bitte Produktname eingeben/auswählen.")
        return

    if not menge.isdigit() or int(menge) <= 0:
        show_output("❌ Bitte eine gültige Menge eingeben (> 0).")
        return

    if modus.get() == "hinzufügen":
        if not preis.replace(",", ".").replace(".", "", 1).isdigit():
            show_output("❌ Bitte einen gültigen Preis eingeben.")
            return
        preis = preis.replace(",", ".")
        try:
            kosten = db.produkt_pruefen_und_hinzufuegen(produkt, menge, preis, kategorie)
            show_output(f"✅ Produkt hinzugefügt:\n- Kategorie: {kategorie}\n- Name: {produkt}\n- Menge: {menge}\n- Einzelpreis: {float(preis):.2f} €\n- Gesamtwert: {kosten:.2f} €")
        except Exception as e:
            show_output(f"❌ {e}")
    elif modus.get() == "bestellen":
        try:
            kosten = db.produkt_bestellen(produkt, menge, kategorie)
            show_output(f"✅ Produkt bestellt:\n- Kategorie: {kategorie}\n- Name: {produkt}\n- Menge: {menge}\n- Kosten: {kosten:.2f} €")
        except Exception as e:
            show_output(f"❌ Fehler: {e}")
    elif modus.get() == "entfernen":
        try:
            db.produkt_entfernen(produkt, menge, kategorie)
            show_output(f"✅ Produkt entfernt:\n- Kategorie: {kategorie}\n- Name: {produkt}\n- Menge: {menge}")
        except Exception as e:
            show_output(f"❌ Fehler: {e}")
    else:
        show_output("❌ Unbekannte Aktion.")

    reset_gui()

def alle_produkte_anzeigen():
    button_frame.pack_forget()
    alle_produkte_frame.pack(pady=20)

def produkte_nach_kategorie():
    kategorie = filter_var.get()
    try:
        min_menge = None
        if menge_filter_var.get() == 1:
            try:
                min_menge = int(menge_filter_entry.get())
            except ValueError:
                show_output("❌ Bitte eine gültige Menge eingeben.")
                return
        
        result = db.produkte_fuer_kategorie(kategorie, min_menge)
        if kategorie == "%":
            show_output("📂 Alle Produkte:\n" + result)
        else:
            show_output(f"📂 Produkte in Kategorie '{kategorie}':\n" + result)
    except Exception as e:
        show_output(f"❌ Fehler beim Filtern: {e}")
    zurueck_zum_hauptmenue()

def zurueck_zum_hauptmenue():
    filter_frame.pack_forget()
    filter_cancel_button.pack_forget()
    input_frame.pack_forget()
    bottom_button_frame.pack_forget()
    alle_produkte_frame.pack_forget()
    button_frame.pack(pady=20)

# Programmstart
if __name__ == "__main__":
    db.create_table()
    gui_root.mainloop()