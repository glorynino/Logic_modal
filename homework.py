import tkinter as tk
from tkinter import ttk
import sys
sys.stdout.reconfigure(encoding='utf-8')


states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'sink'}
alphabet = {'A', '□', '◇', '∧', '∨', '¬', '→'}
initial_state = 'q0'
accepting_state = 'q2'

transition = {
    # Lecture d'une proposition atomique
    ('q0', 'A'): 'q2',
    
    # Lecture d'un modal (□ ou ◇) : on attend une proposition ensuite
    ('q0', '□'): 'q1',
    ('q0', '◇'): 'q1',
    ('q1', 'A'): 'q2',
    ('q1', '¬'): 'q3',
    
    # Gestion de la négation
    ('q0', '¬'): 'q3',  # Après un ¬, on attend une proposition ou un modal
    ('q3', 'A'): 'q2',
    ('q3', '□'): 'q1',
    ('q3', '◇'): 'q1',
    
    # Gestion de l'implication (A → B)
    ('q2', '→'): 'q4',  # Après A → on attend une autre proposition
    ('q4', 'A'): 'q2',
    ('q4', '¬'): 'q3',  # A → ¬B doit être accepté
    ('q4', '□'): 'q1',
    ('q4', '◇'): 'q1',
    
    # Conjonction et disjonction
    ('q2', '∧'): 'q5',  # Après une formule valide, ∧ ou ∨ peut être suivi d'une autre
    ('q2', '∨'): 'q5',
    ('q5', 'A'): 'q2',
    ('q5', '¬'): 'q3',
    ('q5', '□'): 'q1',
    ('q5', '◇'): 'q1',
    
    # États non valides
    ('q1', '□'): 'sink',
    ('q1', '◇'): 'sink',
    ('q2', '□'): 'sink',
    ('q2', '◇'): 'sink',
    ('q2', '→'): 'sink',
    ('q4', '→'): 'sink',
    ('q5', '→'): 'sink',
}

# Fonction pour simuler l'automate
def run_dfa(input_string):
    current_state = initial_state
    for symbol in input_string:
        if symbol not in alphabet:
            return False, f"{symbol} n'est pas dans l'alphabet"
        current_state = transition.get((current_state, symbol), 'sink')
        print(f"Après lecture de '{symbol}', état actuel : {current_state}")
    return (True, "✅ Chaîne acceptée") if current_state == accepting_state else (False, "❌ Chaîne rejetée")

# Fonction pour tester la chaîne entrée
def test_string():
    input_string = entry.get()
    accepted, message = run_dfa(input_string)
    result_label.config(text=message, foreground="green" if accepted else "red")

# Fonction pour insérer un symbole dans l'entrée
def insert_symbol(symbol):
    entry.insert(tk.END, symbol)

# Fonction pour quitter l'application
def quit_app():
    root.destroy()

# Création de l'interface graphique
root = tk.Tk()
root.title("Testeur d'automate")
root.geometry("400x400")
root.configure(bg="#2C3E50")  # Fond sombre

# Style pour un look moderne
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 12))

# Conteneur principal
main_frame = tk.Frame(root, bg="#2C3E50")
main_frame.pack(pady=20)

# Label + Entrée utilisateur
ttk.Label(main_frame, text="Entrez une chaîne :").grid(row=0, column=0, columnspan=3, pady=5)
entry = ttk.Entry(main_frame, width=30, font=("Arial", 12))
entry.grid(row=1, column=0, columnspan=3, pady=5)

# Boutons de sélection des symboles
symbols = ['A', '□', '◇', '→', '∧', '∨', '¬']
symbol_frame = tk.Frame(main_frame, bg="#2C3E50")
symbol_frame.grid(row=2, column=0, columnspan=3, pady=10)

for i, sym in enumerate(symbols):
    ttk.Button(symbol_frame, text=sym, width=4, command=lambda s=sym: insert_symbol(s)).grid(row=i // 4, column=i % 4, padx=5, pady=5)

# Bouton "Tester"
test_button = ttk.Button(main_frame, text="Tester", command=test_string)
test_button.grid(row=3, column=0, columnspan=3, pady=10)

# Label pour afficher le résultat
result_label = ttk.Label(main_frame, text="", font=("Arial", 14, "bold"))
result_label.grid(row=4, column=0, columnspan=3, pady=10)

# Bouton "Quitter"
quit_button = tk.Button(main_frame, text="Quitter", command=quit_app, bg="red", fg="white", font=("Arial", 12))
quit_button.grid(row=5, column=0, columnspan=3, pady=10)


# Lancer l'application
root.mainloop()
