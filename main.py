 
import PyPDF2 
import tkinter as tk
from tkinter import filedialog, ttk
import csv

optiuni_categorie = ["Venit", "Creditare", "Cheltuială deductibilă", "Cheltuială nedeductibilă"]

def citeste_csv(cale_fisier):
    """Citește datele dintr-un fișier CSV și returnează lista de dicționare."""
    with open(cale_fisier, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def selecteaza_fisier():
    fisier = filedialog.askopenfilename(
        title="Selectează fișierul CSV",
        filetypes=[("Fișiere CSV", "*.csv"), ("Toate fișierele", "*.*")]
    )
    if fisier and fisier.lower().endswith(".csv"):
        date = citeste_csv(fisier)
        afiseaza_tabel(date)

def afiseaza_tabel(date):
    for widget in frame_tabel.winfo_children():
        widget.destroy()

    if not date:
        return

    coloane = list(date[0].keys()) + ["Categorie"]

    global tree
    tree = ttk.Treeview(frame_tabel, columns=coloane, show="headings")

    for col in coloane:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for rand in date:
        valori = list(rand.values()) + [""]
        tree.insert("", tk.END, values=valori)

    tree.pack(fill=tk.BOTH, expand=True)

    tree.bind("<Double-1>", editeaza_categorie)

def editeaza_categorie(event):
    item_id = tree.identify_row(event.y)
    col_id = tree.identify_column(event.x)

    if col_id != f"#{len(tree['columns'])}":  # ultima coloană
        return

    x, y, width, height = tree.bbox(item_id, col_id)
    valoare_curenta = tree.item(item_id, "values")[-1]

    combo = ttk.Combobox(frame_tabel, values=optiuni_categorie, state="readonly")
    combo.place(x=x, y=y, width=width, height=height)
    combo.set(valoare_curenta)

    def selecteaza_valoare(event=None):
        valori = list(tree.item(item_id, "values"))
        valori[-1] = combo.get()
        tree.item(item_id, values=valori)
        combo.destroy()

    combo.bind("<<ComboboxSelected>>", selecteaza_valoare)
    combo.focus_set()

# Fereastra principală
root = tk.Tk()
root.title("Vizualizare Tranzacții cu Categorie")
root.geometry("900x500")

buton_selectie = ttk.Button(root, text="Alege fișier CSV", command=selecteaza_fisier)
buton_selectie.pack(pady=10)

frame_tabel = ttk.Frame(root)
frame_tabel.pack(fill=tk.BOTH, expand=True)

root.mainloop()
