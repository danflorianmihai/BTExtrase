import tkinter as tk
from tkinter import filedialog, ttk
import csv
import io

# Opțiuni pentru Combobox
optiuni_categorie = ["Venit", "Creditare", "Cheltuială deductibilă", "Cheltuială nedeductibilă", "Invalid"]
date_csv = []
categorii_selectate = {}

def citeste_csv(cale_fisier):
    global date_csv, categorii_selectate
    
    date_csv = []
    categorii_selectate = {}
    
    with open(cale_fisier, newline='', encoding='utf-8') as f:
        linii = f.readlines()
        
        # Caută rândul cu antet
        start_line = -1
        for i, linie in enumerate(linii):
            if "Data tranzactie" in linie and "Debit" in linie:
                start_line = i
                break
        
        if start_line == -1:
            print("Eroare: Antetul nu a putut fi găsit în fișier.")
            return []

        # Crează un string din liniile rămase și-l folosește pentru a citi CSV-ul
        data_string = "".join(linii[start_line:])
        data_file = io.StringIO(data_string)

        reader = csv.DictReader(data_file)
        date_csv = list(reader)

    return date_csv

def selecteaza_fisier():
    fisier = filedialog.askopenfilename(
        title="Selectează fișierul CSV",
        filetypes=[("Fișiere CSV", "*.csv"), ("Toate fișierele", "*.*")]
    )
    if fisier and fisier.lower().endswith(".csv"):
        date = citeste_csv(fisier)
        if date:
            afiseaza_tabel(date)

def afiseaza_tabel(date):
    for widget in frame_tabel.winfo_children():
        widget.destroy()
    if not date:
        return

    coloane_date = [str(k).strip() for k in date[0].keys()]
    coloane = coloane_date + ["Categorie"]

    global tree
    tree = ttk.Treeview(frame_tabel, columns=coloane, show="headings", selectmode="browse")
    
    for col in coloane:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    for idx, rand in enumerate(date):
        valori = [rand.get(c, "") for c in coloane_date] + [""]
        tree.insert("", tk.END, values=valori, iid=idx)

    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<Double-1>", editeaza_categorie)

    global tree_raport
    for widget in frame_raport.winfo_children():
        widget.destroy()

    tree_raport = ttk.Treeview(frame_raport, columns=["Categorie", "Sumă"], show="headings")
    tree_raport.heading("Categorie", text="Categorie")
    tree_raport.heading("Sumă", text="Sumă")
    tree_raport.column("Categorie", width=200, anchor="center")
    tree_raport.column("Sumă", width=100, anchor="center")
    tree_raport.pack(fill=tk.BOTH, expand=True)

    buton_raport = ttk.Button(frame_raport, text="Generează raport", command=genereaza_raport)
    buton_raport.pack(pady=5)

def editeaza_categorie(event):
    item_id = tree.identify_row(event.y)
    col_id = tree.identify_column(event.x)
    
    if not item_id or col_id != f"#{len(tree['columns'])}":
        return

    x, y, width, height = tree.bbox(item_id, col_id)
    valoare_curenta = tree.item(item_id, "values")[-1]

    combo = ttk.Combobox(frame_tabel, values=optiuni_categorie, state="readonly")
    combo.place(x=x, y=y, width=width, height=height)
    combo.set(valoare_curenta)

    def selecteaza_valoare(event=None):
        valori = list(tree.item(item_id, "values"))
        noua_valoare = combo.get()
        valori[-1] = noua_valoare
        tree.item(item_id, values=valori)
        categorii_selectate[item_id] = noua_valoare
        combo.destroy()

    combo.bind("<<ComboboxSelected>>", selecteaza_valoare)
    combo.focus_set()

def genereaza_raport():
    if not hasattr(tree, "get_children"):
        return

    totaluri = {}
    for item_id in tree.get_children():
        categorie = categorii_selectate.get(item_id, "")
        if categorie == "Invalid" or categorie == "":
            continue

        try:
            rand_idx = int(item_id)
            rand_csv = date_csv[rand_idx]
            debit_str = rand_csv.get("Debit", "0").replace(",", ".")
            credit_str = rand_csv.get("Credit", "0").replace(",", ".")
            debit = float(debit_str) if debit_str else 0
            credit = float(credit_str) if credit_str else 0
        except (ValueError, IndexError):
            continue

        suma = abs(debit) + abs(credit)
        totaluri[categorie] = totaluri.get(categorie, 0) + suma

    for r in tree_raport.get_children():
        tree_raport.delete(r)

    for cat, suma in totaluri.items():
        tree_raport.insert("", tk.END, values=[cat, f"{suma:.2f}"])

# Fereastra principală
root = tk.Tk()
root.title("Vizualizare Tranzacții cu Categorie")
root.geometry("1000x600")

buton_selectie = ttk.Button(root, text="Alege fișier CSV", command=selecteaza_fisier)
buton_selectie.pack(pady=10)

frame_tabel = ttk.Frame(root)
frame_tabel.pack(fill=tk.BOTH, expand=True)

frame_raport = ttk.Frame(root)
frame_raport.pack(fill=tk.BOTH, expand=True, pady=10)

tree_raport = ttk.Treeview(frame_raport)

root.mainloop()