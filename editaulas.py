import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
guidbg = logging.getLogger("aux_funcs.py")
import database as db

       
class EditAula(Gtk.Window):
    def __init__(self,T_debug):
        Gtk.Window.__init__(self,title="Editar Aulas")
        self.set_border_width(15)
        self.T_debug = T_debug
        if(T_debug):
            logging.basicConfig(level=logging.DEBUG)
            
        self.grid = Gtk.Grid()
        connect = db.Aulas_db(self.T_debug)
        aulas = connect.get_aulas()
        connect.close()
        self.rows = []
        i = 0
        self.add(self.grid)
        if not (len(aulas) == 0):
            for x in aulas:
                entry_nome = Gtk.Entry()
                entry_nome.set_text(x[1])
                entry_ata = Gtk.Entry()
                entry_ata.set_text(x[2])
                labelid = Gtk.Label(x[0])
                
                caminho = x[3]
                btn_caminho = Gtk.Button(label="Escolher:"+caminho)
                btn_caminho.connect("clicked",self.on_btn_folder)
                
                
                btn_del = Gtk.Button(label="Apagar")
                btn_del.connect("clicked",self.on_btn_del)
                btn_atual = Gtk.Button(label="Atualizar")
                btn_atual.connect("clicked",self.on_btn_atual)
                
                
                self.grid.attach(labelid    ,0,i,1,1)
                self.grid.attach(entry_nome ,1,i,1,1)
                self.grid.attach(entry_ata  ,2,i,1,1)
                self.grid.attach(btn_caminho,3,i,1,1)
                self.grid.attach(btn_del    ,4,i,1,1)
                self.grid.attach(btn_atual  ,5,i,1,1)
                
                btn_caminho.caminho = caminho
                btn_del.linha = i
                btn_atual.linha = i
                
                self.rows.append((labelid,entry_nome,entry_ata,btn_caminho))
                
                i = i+1
        else:
            self.grid.attach(Gtk.Label("Sem aulas para editar"),0,0,2,2)
            
    
    def on_btn_atual(self,widget):
        actualrow = self.rows[widget.linha]
        guidbg.debug(actualrow[0].get_text())
        guidbg.debug(actualrow[1].get_text())
        guidbg.debug(actualrow[2].get_text())
        guidbg.debug(actualrow[3].caminho   )
        
        aulastruct =(actualrow[1].get_text(),actualrow[2].get_text(),actualrow[3].caminho,actualrow[0].get_text())
        
        connect = db.Aulas_db(self.T_debug)
        connect.update_aulas(aulastruct)
        connect.close()
        
        
    def on_btn_del(self,widget):
        actualrow = self.rows[widget.linha]
        actualid = actualrow[0].get_text()
        connect = db.Aulas_db(self.T_debug)
        connect.delete_aulas(str(actualid),)
        connect.close()
        self.grid.remove_row(widget.linha)

        
    def on_btn_folder(self,widget):
        dialog = Gtk.FileChooserDialog("Escolha o destino do atalho", self,Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Escolher", Gtk.ResponseType.OK))
        dialog.set_default_size(100, 100)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            widget.caminho = dialog.get_filename()
            widget.set_label("Escolher:"+dialog.get_filename())
        dialog.destroy()
