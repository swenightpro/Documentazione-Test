import os
import shutil
from copy import deepcopy as dc

# Viene cancellato il contenuto della cartella docs se questa è presente
def clear_docs():
    if os.path.exists("docs"):
        shutil.rmtree('docs')
    os.mkdir("docs")

# Partendo dal percorso di un file latex, viene compilato il file pdf e lo sposta nella sottocartella corretta
def latex_to_pdf(src_file: list[str]):
    src = os.path.join("src", *src_file)
    
    # Viene compilato il file pdf
    os.system("latexmk -pdf " + src)
    # Vengono eliminati i file temporanei
    os.system("latexmk -c " + src)
    
    # Il pdf generato viene spostato nella sottocartella corretta
    output_file = src_file[-1].replace(".tex", ".pdf")
    output_file_path = os.path.join("docs", *src_file[:-1], output_file)
    shutil.move(output_file, output_file_path)

# Per ognuno dei file .tex trovati, vengono generate le sottocartelle necessarie in docs e viene generato il pdf
def generate_docs(paths):
    for src_file in paths:
        # Verifica la presenza del file .tex
        if not os.path.exists(os.path.join("src", *src_file)): continue
        # Creazione delle sottocartelle mancanti
        for i in range(len(src_file)):
            path = os.path.join("docs", *src_file[:i])
            if not os.path.exists(path):
                os.mkdir(path)
        # Viene richiamata la funzione per generare e spostare il pdf
        latex_to_pdf(src_file)


# Ricerca di tutti i file .tex presenti nella cartella src
# path cambia in base alla chiamata, paths è una lista condivisa tra tutte le chiamate della funzione, come se passassi il puntatore
def find_paths(path: list[str], paths: list):
    
    # Partendo dalla sottocartella src (che aggiungo manualmente per non avercela nei percorsi in seguito)
    # viene letto tutto ciò che è presente nel percorso attuale
    for d in os.listdir(os.path.join("src", *path)):
        # Vengono aggiunti i percorsi dei file .tex alla lista e viene chiamata ricorsivamente la funzione nelle sottocartelle
        if d.endswith('.tex'):
            # In paths viene inserita una copia profonda per evitare problemi
            paths.append(dc(path) + [d])
        elif os.path.isdir(os.path.join("src", *path, d)):
            find_paths(path + [d], paths)

def main():
    paths = []
    clear_docs()
    find_paths([], paths)
    generate_docs(paths)

main()