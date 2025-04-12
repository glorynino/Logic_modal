import tkinter as tk
from tkinter import ttk

# Définition de l'automate
states = {'q0', 'q1', 'q2', 'sink'}
alphabet = {'A', '□', '◇', '∧', '∨', '¬', '→','B','(',')'}
initial_state = 'q0'
accepting_states = {'q0', 'q2'}


transition = {
    # q0 : début ou après opérateur logique
    ('q0', 'A'): 'q2',
    ('q0', 'B'): 'q2',
    ('q0', '□'): 'q1',
    ('q0', '◇'): 'q1',
    ('q0', '('): 'q3',

    # q1 : après un opérateur modal, on attend une proposition
    ('q1', 'A'): 'q2',
    ('q1', 'B'): 'q2',
    ('q1', '□'): 'sink',
    ('q1', '◇'): 'sink',
    ('q1', '('): 'sink',

    # q2 : après une proposition, on attend un opérateur logique ou fermeture
    ('q2', '∧'): 'q0',
    ('q2', '∨'): 'q0',
    ('q2', ')'): 'q0',
    ('q2', 'A'): 'sink',
    ('q2', 'B'): 'sink',
    ('q2', '□'): 'sink',
    ('q2', '◇'): 'sink',
    ('q2', '('): 'sink',

    # q3 : après une parenthèse ouvrante '('
    ('q3', 'A'): 'q4',
    ('q3', 'B'): 'q4',
    ('q3', '□'): 'q1',
    ('q3', '◇'): 'q1',
    ('q3', '('): 'q3',  # parenthèses imbriquées autorisées

    # q4 : à l’intérieur d’une parenthèse après une proposition
    ('q4', '∧'): 'q3',
    ('q4', '∨'): 'q3',
    ('q4', ')'): 'q0',
    ('q4', 'A'): 'sink',
    ('q4', 'B'): 'sink',
    ('q4', '□'): 'sink',
    ('q4', '◇'): 'sink',
    ('q4', '('): 'sink',

    # sink : état poubelle
    ('sink', 'A'): 'sink',
    ('sink', 'B'): 'sink',
    ('sink', '□'): 'sink',
    ('sink', '◇'): 'sink',
    ('sink', '('): 'sink',
    ('sink', ')'): 'sink',
    ('sink', '∧'): 'sink',
    ('sink', '∨'): 'sink',
}



def run_dfa(input_string):
    current_state = initial_state
    for symbol in input_string:
        if symbol not in alphabet:
            return False, f"'{symbol}' n'est pas dans l'alphabet"
        current_state = transition.get((current_state, symbol), 'sink')
        print(f"Après lecture de '{symbol}', état actuel : {current_state}")
    return (True, "✅ Chaîne acceptée") if current_state in accepting_states else (False, "❌ Chaîne rejetée")


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
root.geometry("600x600")
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
symbols = ['A', '□', '◇', '→', '∧', '∨', '¬','B','(',')']
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
quit_button = ttk.Button(main_frame, text="Quitter", command=quit_app)
quit_button.grid(row=5, column=0, columnspan=3, pady=10)

# Lancer l'application
root.mainloop()
