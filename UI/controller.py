import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnni(self):          # punto 1a: riempie "Anno da" e "Anno a"
        for a in self._model.getAnni():
            self._view._ddAnno1.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnno2.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
            # 1. pulisco l'output
            self._view._txt_result.controls.clear()

            # 2. leggo i due anni (il dropdown restituisce una stringa, oppure None)
            if self._view._ddAnno1.value is None or self._view._ddAnno2.value is None:
                self._errore("Selezionare entrambi gli anni!")
                return
            anno1 = int(self._view._ddAnno1.value)
            anno2 = int(self._view._ddAnno2.value)

            # 3. controllo l'ordine
            if anno1 > anno2:
                self._errore("L'anno di inizio non può essere successivo all'anno di fine!")
                return

            # 4. creo il grafo
            self._model.buildGraph(anno1, anno2)

            # 5. stampo nodi e archi
            self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
            self._view._ddPilota.options.clear()
            self._view._ddPilota.value = None
            for d in self._model.getNodiOrdinati():  # piloti in ordine alfabetico
                self._view._ddPilota.options.append(
                    ft.dropdown.Option(key=str(d.driverId), text=str(d)))

            self._view.update_page()


    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()

        # controllo che il grafo esista (max su grafo vuoto darebbe errore)
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. i 3 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text("Top 3 archi di peso maggiore:"))
        for i, (n1, n2, peso) in enumerate(self._model.getTop3(), start=1):
            self._view._txt_result.controls.append(ft.Text(f"{i}. {n1} -- {n2} (peso: {peso})"))

        # b. pilota con più podi
        pilota, podi = self._model.maxPodi()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Pilota con più podi: {pilota} ({podi} podi)"))

        # c. pilota con più rivali (grado maggiore)
        pilota, grado = self._model.getGradoMax()
        self._view._txt_result.controls.append(
            ft.Text(f"Pilota con più rivali: {pilota} (grado: {grado})"))

        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleCammino(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. pilota di partenza
        if self._view._ddPilota.value is None:
            self._errore("Selezionare un pilota di partenza!")
            return
        partenza = self._model.idMap[int(self._view._ddPilota.value)]

        # 3. lunghezza L
        try:
            lun = int(self._view._txtInL.value)
        except (ValueError, TypeError):
            self._errore("L deve essere un numero intero!")
            return
        if lun < 1:
            self._errore("L deve essere almeno 1!")
            return

        # 4. ricorsione
        cammino, peso = self._model.getCammino(partenza, lun)

        # 5. stampa
        if len(cammino) == 0:
            self._errore(f"Nessun cammino di lunghezza {lun} partendo da {partenza}")
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Cammino di lunghezza {lun} partendo da {partenza}:"))
        self._view._txt_result.controls.append(
            ft.Text(f"1. {cammino[0]} ({cammino[0].nationality})"))
        for i in range(1, len(cammino)):
            p = self._model.getPeso(cammino[i - 1], cammino[i])
            self._view._txt_result.controls.append(
                ft.Text(f"{i + 1}. {cammino[i]} ({cammino[i].nationality}) - peso arco: {p}"))
        self._view._txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.update_page()

