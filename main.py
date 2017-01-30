import database as db 
import mainwindow
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import sys 
import logging
import os

T_gui = False
T_debug = False
for x in sys.argv:
    if(x == "--gui"):
        T_gui = True 
    if(x == "--debug"):
        logging.basicConfig(level=logging.DEBUG)


mainlog = logging.getLogger("main.py")
mainlog.debug("Starting")
# connect.add_aulas(("Logica Computacional","logica","~/Univ/2016-2017/1semestre/logica"))
# connect.add_data_aulas((1,0,"20:00","23:00"))

def add_aulas(aula_struct):
    mainlog.debug("Add Aulas")
    connect.add_aulas(aula_struct)

def add_data_aulas(aulaid,diasemana,inicio,fim):
    connec.add_data_aulas(aulaid,diasemana,inicio,fim)

if __name__ == "__main__":
    if(T_gui):
        mainlog.debug("Gui")
        mainwindow = mainwindow.MainWindow(T_debug) 
        mainwindow.connect("delete-event",Gtk.main_quit)
        mainwindow.show_all()
        Gtk.main()
    else:
        connect = db.Aulas_db(T_debug)
        mainlog.debug("NoGui")
        #aux = sys.argv[1]
        #out =connect.get_path_from_atalho((aux,))[0]
        out= connect.get_path_from_time()[0]
        while (out == "None"):
            aulas = connect.get_atalhos()
            sys.stderr.write("Nenhuma aula a decorrer.\nEscolher aula:\n")
            for x in aulas:
                sys.stderr.write(x[0]+"|")
            sys.stderr.write("\n")
            aux = input()
            out = connect.get_path_from_atalho((aux,))[0]
        print (out)

    mainlog.debug("Ending")



