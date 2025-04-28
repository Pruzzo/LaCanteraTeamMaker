import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random


def crea_simulazioni(ruoli):
    simulazioni_possibili = []

    for _ in range(1000):  # Genera 1000 simulazioni
        try:
            # Clona i ruoli disponibili
            disponibili = {k: v.copy() for k, v in ruoli.items()}

            torneo = []  # Una simulazione è un torneo di 12 squadre

            for _ in range(12):
                squadra = []

                squadra.append(disponibili["P"].pop(random.randrange(len(disponibili["P"]))))
                squadra.append(disponibili["D"].pop(random.randrange(len(disponibili["D"]))))
                squadra.append(disponibili["DE"].pop(random.randrange(len(disponibili["DE"]))))
                squadra.append(disponibili["C"].pop(random.randrange(len(disponibili["C"]))))
                squadra.extend(random.sample(disponibili["CE"], 3))
                for player in squadra[4:7]:
                    disponibili["CE"].remove(player)
                squadra.append(disponibili["A"].pop(random.randrange(len(disponibili["A"]))))
                squadra.append(disponibili["AE"].pop(random.randrange(len(disponibili["AE"]))))

                torneo.append(squadra)

            # Calcola l'equilibrio generale del torneo
            squilibri = []
            for squadra in torneo:
                voto_pd = squadra[0]['voto'] + squadra[1]['voto']
                voto_ccce = squadra[3]['voto'] + sum(player['voto'] for player in squadra[4:7])
                voto_aae = squadra[7]['voto'] + squadra[8]['voto']

                totale = abs(voto_pd - voto_ccce) + abs(voto_ccce - voto_aae) + abs(voto_aae - voto_pd)
                squilibri.append(totale)

            totale_torneo = sum(squilibri)

            simulazioni_possibili.append((totale_torneo, torneo))

        except (IndexError, ValueError):
            continue  # Se mancano giocatori o succede un errore, scarta

    # Ordina le simulazioni in base al totale di squilibrio
    simulazioni_possibili.sort(key=lambda x: x[0])

    # Prendi le 3 migliori
    migliori = simulazioni_possibili[:3]

    # Crea un unico popup con pulsanti per selezionare le simulazioni
    popup = tk.Toplevel()
    popup.title("Simulazioni Migliori")
    popup.geometry("600x700")

    label = tk.Label(popup, text="Seleziona una simulazione:", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    def mostra_simulazione(torneo, idx):
        # Mostra i dettagli della simulazione selezionata
        dettaglio_popup = tk.Toplevel()
        dettaglio_popup.title(f"Torneo Simulazione {idx}")
        dettaglio_popup.geometry("600x700")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(dettaglio_popup)
        scrollbar = tk.Scrollbar(dettaglio_popup, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        label = tk.Label(scrollable_frame, text=f"Torneo Simulazione {idx}", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        for num_squadra, squadra in enumerate(torneo, 1):
            squadra_label = tk.Label(scrollable_frame, text=f"Squadra {num_squadra}:", font=("Arial", 12, "bold"))
            squadra_label.pack(pady=5)
            for player in squadra:
                player_text = f"{player['nome']} ({player['voto']})"
                player_label = tk.Label(scrollable_frame, text=player_text, font=("Arial", 11))
                player_label.pack()
            separator = tk.Label(scrollable_frame, text="-------------------------------", font=("Arial", 10))
            separator.pack(pady=5)

        dettaglio_popup.transient()
        dettaglio_popup.grab_set()

    for idx, (_, torneo) in enumerate(migliori, 1):
        button = tk.Button(popup, text=f"Simulazione {idx}", font=("Arial", 12),
                           command=lambda t=torneo, i=idx: mostra_simulazione(t, i))
        button.pack(pady=5)

    popup.transient()
    popup.grab_set()


def carica_file():
    global ruoli  # Serve per poterlo usare anche nel bottone "Genera nuove squadre"
    filepath = filedialog.askopenfilename(
        title="Seleziona il file Excel",
        filetypes=[("File Excel", "*.xlsx")]
    )

    if not filepath:
        return

    try:
        df = pd.read_excel(filepath, sheet_name="RUOLI E VOTI 2025")

        roles = ['P', 'D', 'DE', 'C', 'CE', 'A', 'AE']
        ruoli = {
            "P": [],
            "D": [],
            "DE": [],
            "C": [],
            "CE": [],
            "A": [],
            "AE": []
        }

        # for _, col in df.items():
        #     if col.name not in roles:
        #         messagebox.showerror(
        #             "Errore", f"Colonna '{col.name}' non riconosciuta.")

        
        for _, row in df.iterrows():
            if(_ >60):
                break
            if len(row) > 3:
                role = row.iloc[1]
                if role in roles:
                    ruoli[role].append({"nome": row.iloc[2], "voto": row.iloc[3]})
            if len(row) > 8:
                role = row.iloc[6]
                if role in roles:
                    ruoli[role].append({"nome": row.iloc[7], "voto": row.iloc[8]})
            if len(row) > 13:
                role = row.iloc[11]
                if role in roles:
                    ruoli[role].append(
                        {"nome": row.iloc[12], "voto": row.iloc[13]})
            if len(row) > 18:
                role = row.iloc[16]
                if role in roles:
                    ruoli[role].append(
                        {"nome": row.iloc[17], "voto": row.iloc[18]})
            if len(row) > 23:
                role = row.iloc[21]
                if role in roles:
                    ruoli[role].append(
                        {"nome": row.iloc[22], "voto": row.iloc[23]})

        messagebox.showinfo(
            "File Caricato", f"Trovati ruoli e voti per {len(ruoli['P'])} portieri, {len(ruoli['D'])} difensori, {len(ruoli['DE'])} difensori esterni, {len(ruoli['C'])} centrocampisti, {len(ruoli['CE'])} centrocampisti esterni, {len(ruoli['A'])} attaccanti e {len(ruoli['AE'])} attaccanti esterni.")
        # ruolo = row['Ruolo']
        # nome = row['Nome']
        # voto = row['Voto']
        # if ruolo in ruoli:
        #     ruoli[ruolo].append({"nome": nome, "voto": voto})

        # Abilita il bottone dopo il caricamento
        genera_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore:\n{e}")


def main():
    global genera_button

    root = tk.Tk()
    root.title("Simulatore Squadre Torneo 2025")
    root.geometry("400x300")

    label = tk.Label(
        root, text="Seleziona il file Excel per iniziare:", font=("Arial", 12))
    label.pack(pady=20)

    carica_button = tk.Button(root, text="Carica File",
                              command=carica_file, font=("Arial", 12))
    carica_button.pack(pady=10)

    genera_button = tk.Button(root, text="Genera Nuove Squadre",
                              command=lambda: crea_simulazioni(ruoli), font=("Arial", 12))
    genera_button.pack(pady=10)
    genera_button.config(state=tk.DISABLED)  # All'inizio disattivo!

    root.mainloop()


if __name__ == "__main__":
    main()
