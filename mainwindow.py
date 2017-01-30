import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
from addaula import AddAula
from addhora import AddHora
from editaulas import EditAula
from edithoras import EditHoras


guidbg = logging.getLogger("gui.py")

def error_dialog(parent,texto):
    dialog =Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR,Gtk.ButtonsType.CANCEL, "Erro")
    dialog.format_secondary_text(texto)
    dialog.run()
    dialog.destroy()

class MainWindow(Gtk.Window):
    def __init__(self,T_debug):
        Gtk.Window.__init__(self,title="autoCD")
        self.set_border_width(15)
        self.T_debug = T_debug
        if(T_debug):
            logging.basicConfig(level=logging.DEBUG)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.add(self.grid)

        self.btn_aula = Gtk.Button(label="Adicionar aula")
        self.btn_aula.connect("clicked",self.on_aula_clicked)

        self.btn_hora = Gtk.Button(label="Adicionar Horario")
        self.btn_hora.connect("clicked",self.on_hora_clicked)

        self.btn_editar_aula = Gtk.Button(label="Editar aulas")
        self.btn_editar_aula.connect("clicked",self.on_editar_aula_clicked)

        self.btn_editar_hora = Gtk.Button(label="Editar Horario")
        self.btn_editar_hora.connect("clicked",self.on_editar_hora_clicked)


        self.grid.attach(self.btn_aula,0,0,1,1)
        self.grid.attach(self.btn_hora,1,0,1,1)
        self.grid.attach(self.btn_editar_aula,0,1,1,1)
        self.grid.attach(self.btn_editar_hora,1,1,1,1)

    def reshow(self, widget):
        guidbg.debug("Reshow")
        self.show_all()

    def on_aula_clicked(self, widget):
        guidbg.debug("Adicionar Aula!")
        self.hide()
        window = AddAula(self.T_debug)
        window.connect("hide",self.reshow)
        window.show_all()

    def on_hora_clicked(self,widget):
        guidbg.debug("Adicionar Hora")
        self.hide()
        window = AddHora(self.T_debug)
        window.connect("hide",self.reshow)
        window.show_all()

    def on_editar_aula_clicked(self, widget):
        guidbg.debug("Editar Aula!")
        self.hide()
        windows = EditAula(self.T_debug)
        windows.connect("hide",self.reshow)
        windows.show_all()

    def on_editar_hora_clicked(self,widget):
        guidbg.debug("Editar Hora")
        self.hide()
        windows = EditHoras(self.T_debug)
        windows.connect("hide",self.reshow)
        windows.show_all()

