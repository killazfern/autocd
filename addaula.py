import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from aux_funcs import error_dialog
import database as db
import logging

guidbg = logging.getLogger("addaula.py")

class AddAula(Gtk.Window):
    def __init__(self,T_debug):
        Gtk.Window.__init__(self,title="Adicionar Aula")
        self.set_border_width(15)
        self.caminho = None
        self.T_debug = T_debug
        if(T_debug):
            logging.basicConfig(level=logging.DEBUG)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(5)
        self.add(self.grid)

        self.label_nome = Gtk.Label("Nome:")
        self.entry_nome = Gtk.Entry()

        self.label_ata = Gtk.Label("Atalho:")
        self.entry_ata = Gtk.Entry()

        self.label_caminho = Gtk.Label("Caminho:")
        self.btn_caminho = Gtk.Button(label="Escolher")
        self.btn_caminho.connect("clicked",self.on_btn_folder)

        self.btn_addicionar = Gtk.Button(label="Adicionar")
        self.btn_addicionar.connect("clicked",self.on_btn_addicionar)
        self.grid.attach(self.label_nome,0,0,1,1)
        self.grid.attach(self.entry_nome,1,0,1,1)

        self.grid.attach(self.label_ata,0,1,1,1)
        self.grid.attach(self.entry_ata,1,1,1,1)

        self.grid.attach(self.label_caminho,0,2,1,1)
        self.grid.attach(self.btn_caminho,1,2,1,1)

        self.grid.attach(self.btn_addicionar,1,3,1,1)

    def on_btn_folder(self,widget):
        dialog = Gtk.FileChooserDialog("Escolha o destino do atalho", self,Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Escolher", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.caminho = dialog.get_filename()
            self.btn_caminho.set_label("Escolher:"+dialog.get_filename())

        dialog.destroy()


    def on_btn_addicionar(self,widget):
        guidbg.debug("Nome:%s",self.entry_nome.get_text())
        guidbg.debug("Atalho:%s",self.entry_ata.get_text())
        if(self.caminho == None):
            error_dialog(self,"O Caminho ainda não foi definido!")
            guidbg.debug("No Path")
            return

        aulastruct = (self.entry_nome.get_text(),self.entry_ata.get_text(),self.caminho)
        connect = db.Aulas_db(self.T_debug)
        atalhos = connect.get_atalhos()
        aulas = connect.get_aulas()
        for x in aulas:
            guidbg.debug("Nome:%s",x[1])
            if(x[1] == aulastruct[0]):
                error_dialog(self,"Esta aula já existe")
                guidbg.debug("Exists!")
                return
        for x in atalhos:
            guidbg.debug("AtalhoDB:%s",x[0])
            if(x[0] == aulastruct[1]):
                error_dialog(self,"Este atalho já existe")
                guidbg.debug("Exists!")
                return

        connect.add_aulas(aulastruct)
        connect.close()
        self.hide()
