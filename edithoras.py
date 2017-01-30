import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
guidbg = logging.getLogger("aux_funcs.py")
import database as db
from aux_funcs import NumberEntry
import re
import time
    
class EditHoras(Gtk.Window):
    def __init__(self,T_debug):
        Gtk.Window.__init__(self,title="Editar Horario")
        self.set_border_width(15)
        self.T_debug = T_debug
        if(T_debug):
            logging.basicConfig(level=logging.DEBUG)
            
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(5)
        connect = db.Aulas_db(self.T_debug)
        data_aulas = connect.get_data_aulas_edit()
        connect.close()
        self.rows = []
        i = 0
        self.add(self.grid)
        cbox_semanavars = Gtk.ListStore(int,str)
        cbox_semanavars.append([0,"Domingo"])
        cbox_semanavars.append([1,"Segunda-Feira"])
        cbox_semanavars.append([2,"Terça-Feira"])
        cbox_semanavars.append([3,"Quarta-Feira"])
        cbox_semanavars.append([4,"Quinta-Feira"])
        cbox_semanavars.append([5,"Sexta-Feira"])
        cbox_semanavars.append([6,"Sabado"])
        if not (len(data_aulas) == 0):
            for x in data_aulas:
                """ d.id,a.nome,d.dia_semana,d.hora_inico,d.hora_fim"""
                labelid = Gtk.Label(x[0])
                labelaula = Gtk.Label(x[1])
                entry_inicio = NumberEntry()
                entry_inicio.set_text(x[3][:5])
                entry_fim = NumberEntry()
                entry_fim.set_text(x[4][:5])
                
                
                cbox_semana = Gtk.ComboBox.new_with_model_and_entry(cbox_semanavars)
                cbox_semana.set_entry_text_column(1)
                cbox_semana.set_active(x[2])
                
                
                
                btn_del = Gtk.Button(label="Apagar")
                btn_del.connect("clicked",self.on_btn_del)
                btn_atual = Gtk.Button(label="Atualizar")
                btn_atual.connect("clicked",self.on_btn_atual)
                
                
                self.grid.attach(labelid     ,0,i,1,1)
                self.grid.attach(labelaula   ,1,i,1,1)
                self.grid.attach(cbox_semana ,2,i,1,1)
                self.grid.attach(entry_inicio,3,i,1,1)
                self.grid.attach(entry_fim   ,4,i,1,1)
                self.grid.attach(btn_del     ,5,i,1,1)
                self.grid.attach(btn_atual   ,6,i,1,1)
                
                
                btn_del.linha = i
                btn_atual.linha = i
                
                self.rows.append((labelid,labelaula,cbox_semana,entry_inicio,entry_fim))
                
                i = i+1
        else:
            self.grid.attach(Gtk.Label("Sem horarios para editar"),0,0,2,2)
            
    
    def on_btn_atual(self,widget):
        """self.dbase.execute("UPDATE data_aulas SET dia_semana=?, hora_inicio =? hora_fim=? WHERE id==?")"""
        actualrow = self.rows[widget.linha]
        
        regex = r"([0 1][0-9]|2[0-3]):([0-5][0-9])"# (:([0-5][0-9]))?"
        horainicio = actualrow[3].get_text()
        horafim    = actualrow[4].get_text()
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
        
        aux = actualrow[2].get_active_iter()      
        model = actualrow[2].get_model()
        idSemana = model[aux][0]
        
        aulastruct =(idSemana,horainicio,horafim,actualrow[0].get_text())
        guidbg.debug(aulastruct)
        
        connect = db.Aulas_db(self.T_debug)
        connect.update_data_aulas(aulastruct)
        connect.close()
        
        
    def on_btn_del(self,widget):
        actualrow = self.rows[widget.linha]
        actualid = actualrow[0].get_text()
        connect = db.Aulas_db(self.T_debug)
        connect.delete_data_aulas(str(actualid),)
        connect.close()
        self.grid.remove_row(widget.linha)
        
