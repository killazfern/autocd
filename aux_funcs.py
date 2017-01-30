import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
guidbg = logging.getLogger("aux_funcs.py")

def error_dialog(parent,texto):
    dialog =Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR,Gtk.ButtonsType.CANCEL, "Erro")
    dialog.format_secondary_text(texto)
    dialog.run()
    dialog.destroy()

class NumberEntry(Gtk.Entry):
        def __init__(self):
            Gtk.Entry.__init__(self)
            self.connect('changed', self.on_changed)

        def on_changed(self, *args):
            text = self.get_text().strip()
            self.set_text(''.join([i for i in text if i in '0123456789:']))
