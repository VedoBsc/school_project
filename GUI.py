import tkinter as tk

# GUI-Fenster erstellen
gui_root = tk.Tk()
gui_root.title("Lagerverwaltung")
gui_root.geometry("800x600")
gui_root.resizable(True, True)

# Überschrift
ueberschrift = tk.Label(gui_root, text="Lagerverwaltung", font=("Arial", 20))
ueberschrift.pack(pady=20)

##################
# INPUT FIELDS
##################

# Produktname
input_produktname = tk.Frame(gui_root)
input_produktname.pack(pady=5)

title_produkt = tk.Label(input_produktname, text="Produktname:", font=("Arial", 12))
title_produkt.pack(side="left", padx=(0, 10))

title_eingabe = tk.Entry(input_produktname, font=("Arial", 12))
title_eingabe.pack(side="left", padx=(0, 10))

# Menge
input_menge = tk.Frame(gui_root)
input_menge.pack(pady=5)

title_menge = tk.Label(input_menge, text="Menge:", font=("Arial", 12))
title_menge.pack(side="left", padx=(0, 10))

title_menge_eingabe = tk.Entry(input_menge, font=("Arial", 12))
title_menge_eingabe.pack(side="left", padx=(0, 10))

# Preis
input_preis = tk.Frame(gui_root)
input_preis.pack(pady=5)

title_preis = tk.Label(input_preis, text="Preis (€):", font=("Arial", 12))
title_preis.pack(side="left", padx=(0, 10))

title_preis_eingabe = tk.Entry(input_preis, font=("Arial", 12))
title_preis_eingabe.pack(side="left", padx=(0, 10))

# Kategorie (Dropdown)
input_kategorie = tk.Frame(gui_root)
input_kategorie.pack(pady=5)

title_kategorie = tk.Label(input_kategorie, text="Kategorie:", font=("Arial", 12))
title_kategorie.pack(side="left", padx=(0, 10))

kategorien = ["Widerstand", "Kondensator", "Spule", "IC", "Sonstiges"]
kategorie_var = tk.StringVar()
kategorie_var.set(kategorien[0])  # Standardwert

dropdown_kategorie = tk.OptionMenu(input_kategorie, kategorie_var, *kategorien)
dropdown_kategorie.config(font=("Arial", 12))
dropdown_kategorie.pack(side="left", padx=(0, 10))

##################
# BUTTONS
##################
button_frame = tk.Frame(gui_root)
button_frame.pack(pady=30)

button_add = tk.Button(button_frame, text="Produkt hinzufügen", font=("Arial", 12))
button_add.pack(side="left", padx=10)

button_remove = tk.Button(button_frame, text="Produkt entfernen", font=("Arial", 12))
button_remove.pack(side="left", padx=10)

button_order = tk.Button(button_frame, text="Produkt bestellen", font=("Arial", 12))
button_order.pack(side="left", padx=10)

##################
# AUSGABEFELD (nicht editierbar)
##################
output_box = tk.Text(gui_root, height=7, width=70, font=("Arial", 12))
output_box.pack(pady=10)
output_box.config(state="disabled")

def show_output(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

# Beispielhafte Button-Funktionen mit Ausgabe
def add_button_click():
    produkt = title_eingabe.get()
    menge = title_menge_eingabe.get()
    preis = title_preis_eingabe.get()
    kategorie = kategorie_var.get()
    show_output(f"Produkt hinzugefügt:\n- Name: {produkt}\n- Menge: {menge}\n- Preis: {preis} €\n- Kategorie: {kategorie}")

def remove_button_click():
    produkt = title_eingabe.get()
    show_output(f"Produkt entfernt:\n- Name: {produkt}")

def order_button_click():
    produkt = title_eingabe.get()
    show_output(f"Bestellung ausgelöst:\n- Produkt: {produkt}")

# Buttons mit Funktionen verbinden
button_add.config(command=add_button_click)
button_remove.config(command=remove_button_click)
button_order.config(command=order_button_click)

# GUI starten
gui_root.mainloop()
