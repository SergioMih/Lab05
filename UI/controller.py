import flet as ft
from UI.view import View
from model.model import Model
from model.corso import Corso

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._id_map_corsi = {}
        self.corso_selezionato = None


    def populate_dd_corso(self):
        for corso in self._model.get_corsi():
            self._id_map_corsi[corso.codins] = corso
            self._view.dd_corso.options.append(ft.dropdown.Option(key=corso.codins, text=corso))
        self._view.update_page()

    def leggi_corso(self, e):
        self.corso_selezionato = self._view.dd_corso.value

    def cerca_iscritti(self, e):
        if self.corso_selezionato is None:
            self._view.create_alert("Selezionare un corso!")
            return
        iscritti = self._model.get_iscritti_corso(self.corso_selezionato)
        if iscritti is None:
            self._view.create_alert("Problema nella connessione!")
            return
        self._view.txt_result.controls.clear()
        if len(iscritti) == 0:
            self._view.txt_result.controls.append(ft.Text("Non ci sono iscritti al corso"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Ci sono {len(iscritti)} iscritti al corso:"))
            for studente in iscritti:
                self._view.txt_result.controls.append(ft.Text(f"{studente}"))
            self._view.update_page()

    def cerca_studente(self,e):
        matricola = self._view.txt_matricola.value
        if matricola == "":
            self._view.create_alert("inserire una matricola")
            return
        if matricola.isdigit() == False:
            self._view.create_alert("inserire un int")
            return
        studente = self._model.cerca_studente(matricola)
        if studente is None:
            self._view.create_alert("Matricola non presente nel database")
            return
        else:
            self._view.txt_nome.value = studente.nome
            self._view.txt_cognome.value = studente.cognome
        self._view.update_page()

    def cerca_corsi(self,e):
        matricola = self._view.txt_matricola.value
        corsi = self._model.get_corsi_studente(matricola)
        if matricola == "":
            self._view.create_alert("inserire una matricola")
            return
        if len(corsi)==0:
            self._view.create_alert("nessun corso per la matricola")
            return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append (ft.Text(f"Ci sono {len(corsi)}"))
            for corso in corsi:
                self._view.txt_result.controls.append(ft.Text(f"{corso}"))
            self._view.update_page()
    def iscrivi(self,e):
        matricola = self._view.txt_matricola.value
        if matricola == "":
            self._view.create_alert("inserire una matricola")
            return
        studente = self._model.cerca_studente(matricola)
        if studente is None:
            self._view.create_alert("studente non esiste")
            return
        result = self._model.iscrivi_corso(studente.matricola,self.corso_selezionato)
        self._view.txt_result.controls.clear()
        if result:
            self._view.txt_result.controls.append(ft.Text("Iscrizione avvenuta con successo"))
        else:
            self._view.txt_result.controls.append(ft.Text("Iscrizione fallita"))
        self._view.update_page()


