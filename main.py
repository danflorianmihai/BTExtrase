import tkinter as tk
from tkinter import filedialog
# Funcție pentru a deschide un dialog de fișiere
def select_file_dialog():
    file = filedialog.askopenfilename(
         titlu="Selectează un fișier",
        filetypes=[("Fișiere CSV", "*.csv"), ("Fișiere PDF", "*.pdf"), ("Toate fișierele", "*.*")]
    )
    if file:
        print(f"Fișier selectat: {file}")
# Creează fereastra principală
root = tk.Tk()
root.title("Selectare fișier")

# Creează un buton pentru selectarea fișierului
buton_selectie = tk.Button(root, text="Alege fișier", command=select_file_dialog)
buton_selectie.pack(pady=20)

# Rulează bucla principală
root.mainloop()