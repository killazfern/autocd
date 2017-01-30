import sqlite3
import os
import sys
import logging

dblog = logging.getLogger("database.py")
class Aulas_db(object):
    def __init__(self,dbg):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        if(dbg):
            logging.basicConfig(level=logging.DEBUG)
        dblog.debug("Database")
        if(not os.path.exists(self.dir_path+"/aulas.db")):
            dblog.debug("Connect+Create")
            self.connect()
            self.create()
        else:
            dblog.debug("Connect")
            self.connect()

    def create(self):
        dblog.debug("Create Tables")
        self.dbase.execute("""  
                                CREATE TABLE aulas 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nome TEXT,
                                        shortname TEXT UNIQUE, 
                                        caminho TEXT)
                           """)
        self.dbase.execute("""
                                CREATE TABLE data_aulas 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        idaula INTEGER,
                                        dia_semana NUMERIC,
                                        hora_inicio NUMERIC,
                                        hora_fim NUMERIC,
                                        FOREIGN KEY (idaula) REFERENCES aulas(id))
                           """)
        self.dbase.commit()

    def connect(self):
        dblog.debug("Connecting DBase")
        self.dbase = sqlite3.connect(self.dir_path+"/aulas.db")

    def add_aulas(self,aula_struct):
        self.dbase.execute("INSERT INTO aulas VALUES (NULL,?,?,?)", aula_struct)
        self.dbase.commit()
    
    def update_aulas(self,aula_struct):
        self.dbase.execute("UPDATE aulas SET nome=? , shortname=?,caminho=? WHERE id == ?",(aula_struct))
        self.dbase.commit()
        
    def delete_aulas(self,aulaid):
        self.dbase.execute("DELETE FROM aulas WHERE id == ?",(aulaid))
        self.dbase.commit()

    def add_data_aulas(self,data_aulas_struct):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT time(?),time(?)",(data_aulas_struct[2],data_aulas_struct[3]))
        aux = cursor.fetchone()
        dblog.debug("Dates:%s",aux)
        self.dbase.execute("INSERT INTO data_aulas VALUES (NULL,?,?,?,?)", (data_aulas_struct[0],data_aulas_struct[1],aux[0],aux[1]))
        self.dbase.commit()
        cursor.close()
        
    def update_data_aulas(self,data_aulas_struct):
        self.dbase.execute("UPDATE data_aulas SET dia_semana=?, hora_inicio =?, hora_fim=? WHERE id==?",data_aulas_struct)
        self.dbase.commit()
        
    def delete_data_aulas(self,aulaid):
        self.dbase.execute("DELETE FROM data_aulas WHERE id == ?",(aulaid))
        self.dbase.commit()

    def get_data_aulas_edit(self):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT d.id,a.nome,d.dia_semana,d.hora_inicio,d.hora_fim FROM data_aulas AS d INNER JOIN aulas AS a on a.id == d.idaula")
        aux = cursor.fetchall()
        cursor.close()
        return aux

    def get_atalhos(self):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT shortname FROM aulas")
        aux=cursor.fetchall()
        for x in aux:
            dblog.debug("Get_Atalhos:%s",x[0])
        cursor.close()
        return aux

    def get_aulas(self):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT * FROM aulas")
        aux=cursor.fetchall()
        cursor.close()
        return aux

    def get_path_from_time(self):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT a.caminho FROM aulas AS a INNER JOIN data_aulas as d ON a.id == d.idaula WHERE time('now') BETWEEN d.hora_inicio AND d.hora_fim AND STRFTIME('%w','now') == d.dia_semana;")
        aux=cursor.fetchone()
        cursor.close()
        if(aux == None):
            return ("None",)
        dblog.debug("Caminho:%s",aux[0])
        return aux

    def get_path_from_atalho(self,atalho):
        cursor = self.dbase.cursor()
        cursor.execute("SELECT caminho FROM aulas WHERE shortname == ?",(atalho))
        aux=cursor.fetchone()
        cursor.close()
        if(aux == None):
            return ("None",)
        dblog.debug("Caminho:%s",aux[0])
        return aux

    def close(self):
        self.dbase.close()


