

import os

def rename_decks(base_dir):
    """
    Parcourt les sous-dossiers de 'DECK' et renomme chaque fichier selon la logique :
    - Le dernier segment avant l'extension est le numéro.
    - Le segment juste avant le numéro est le code de la série.
    - Tout ce qui précède ces deux éléments constitue le reste (type + éventuel sous-type).
    Nouveau format : {serie}_{num}_{reste}.ext
    Exemple : 'DECK_EX_PCG_CDCH_011.jpeg' -> 'CDCH_011_DECK_EX_PCG.jpeg'
    """
    deck_dir = os.path.join(base_dir, "DECK")
    if not os.path.isdir(deck_dir):
        print(f"Le dossier {deck_dir} n'existe pas.")
        return

    for subfolder in os.listdir(deck_dir):
        subfolder_path = os.path.join(deck_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        for filename in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, filename)
            if not os.path.isfile(file_path):
                continue

            name, ext = os.path.splitext(filename)
            parts = name.split("_")
            # On doit avoir au moins 3 segments : reste, série, numéro
            if len(parts) < 3:
                print(f"Ignoré (format inattendu) : {filename}")
                continue

            num = parts[-1]       # dernier segment
            serie = parts[-2]     # avant-dernier segment
            reste = "_".join(parts[:-2])  # tout ce qui précède

            new_name = f"{serie}_{num}_{reste}{ext.lower()}"
            new_path = os.path.join(subfolder_path, new_name)

            if os.path.exists(new_path):
                print(f"Le fichier {new_name} existe déjà, on le saute.")
                continue

            os.rename(file_path, new_path)
            print(f"Deck: {filename} -> {new_name}")

if __name__ == "__main__":
    base_directory = os.path.join(os.getcwd(), "static", "cards", "S&S")
    print(f"Debug: base_directory = {base_directory}")
    rename_decks(base_directory)