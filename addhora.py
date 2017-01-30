import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from aux_funcs import error_dialog
import logging
import re
import time
import database as db
from aux_funcs import NumberEntry
guidbg = logging.getLogger("addhora.py")

class AddHora(Gtk.Window):
    def __init__(self,T_debug):
        Gtk.Window.__init__(self,title="Adicionar Hora")
        self.set_border_width(15)
        self.caminho = None
        self.T_debug = T_debug
        if(T_debug):
            logging.basicConfig(level=logging.DEBUG)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(5)
        self.add(self.grid)

        self.label_aula = Gtk.Label("Aula:")
        connect = db.Aulas_db(self.T_debug)
        aux = connect.get_aulas()
        cbox_info = Gtk.ListStore(int,str)
        for x in aux:
            cbox_info.append([x[0],x[1]])
        
        self.cbox_aula = Gtk.ComboBox.new_with_model_and_entry(cbox_info)
        self.cbox_aula.set_entry_text_column(1)

        self.grid.attach(self.label_aula,0,0,1,1)
        self.grid.attach(self.cbox_aula,1,0,1,1)

        cbox_semana = Gtk.ListStore(int,str)
        cbox_semana.append([0,"Domingo"])
        cbox_semana.append([1,"Segunda-Feira"])
        cbox_semana.append([2,"Terça-Feira"])
        cbox_semana.append([3,"Quarta-Feira"])
        cbox_semana.append([4,"Quinta-Feira"])
        cbox_semana.append([5,"Sexta-Feira"])
        cbox_semana.append([6,"Sabado"])
        self.cbox_semana = Gtk.ComboBox.new_with_model_and_entry(cbox_semana)
        self.cbox_semana.set_entry_text_column(1)
        self.label_semana = Gtk.Label("Dia da semana")
        self.grid.attach(self.label_semana,0,1,1,1)
        self.grid.attach(self.cbox_semana,1,1,1,1)

        self.horainicio = NumberEntry()
        self.horafim = NumberEntry()

        self.grid.attach(self.horainicio,0,2,1,1)
        self.grid.attach(self.horafim,1,2,1,1)

        self.btn_addicionar = Gtk.Button("Adicionar")
        self.grid.attach(self.btn_addicionar,1,3,1,1)
        self.btn_addicionar.connect("clicked",self.on_btn_addicionar)

    def on_btn_addicionar(self,widget):

        horainicio = self.horainicio.get_text()
        horafim = self.horafim.get_text()
        guidbg.debug("HoraInicio:%s",horainicio)
        guidbg.debug("HoraFim:%s",horafim)

        aux1 = self.cbox_aula.get_active_iter()
        aux2 = self.cbox_semana.get_active_iter()

        if aux1 == None: 
            error_dialog(self,"A aula não foi definda!")
            return
        if aux2 == None:
            error_dialog(self,"O dia de semana não foi definido!")
            return
        """
        if(horainicio == ""):
            error_dialog(self,"A hora inicial não foi definida!")
            return
        if(horafim == ""):
            error_dialog(self,"A hora final não foi definida!")
            return
        """

        model1 = self.cbox_aula.get_model()
        model2 = self.cbox_semana.get_model()
        idAula = model1[aux1][0]
        idSemana = model2[aux2][0]

        regex = r"([0 1][0-9]|2[0-3]):([0-5][0-9])"# (:([0-5][0-9]))?"
        resinit = re.match(regex,horainicio)
        resfim = re.match(regex,horafim)
        if(resinit == None):
            error_dialog(self,"A hora inicial não segue o formato esperado!\nExemplo: 15:20")
            return
        if(resfim == None):
            error_dialog(self,"A hora final não segue o formato esperado!\nExemplo: 15:20")
            return
        varinit =time.mktime(time.strptime(horainicio,"%H:%M"))
        varfim =time.mktime(time.strptime(horafim,"%H:%M"))
        if((varfim - varinit) <0):
            error_dialog(self,"A hora inicial não pode ser depois da hora final!")
            return
        horastruct = (idAula,idSemana,horainicio,horafim)
        guidbg.debug(horastruct)
        connect = db.Aulas_db(self.T_debug)
        connect.add_data_aulas(horastruct)
        connect.close()
        self.hide()
