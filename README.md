# Autocd
#Description
Python program that allows to create folder bookmarks to be used in terminal enviroment.
The idea came from university class organization, where there was a need to transverse various folders to reach the current class folder.
Said bookmarks ar time dependent, meaning if the provided bash function is called during a weekday and time that matches a class, the script goes directly to the class folder. If no class is ocurring, the program lists the various bookmarks and asks the destination.

#Dependencies
GTK+3
Python 2 (2.6 or later) or Python 3 (3.1 or later)
gobject-introspection
sqlite3
