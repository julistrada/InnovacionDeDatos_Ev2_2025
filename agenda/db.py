import sqlite3

class ConexionDB:
    _conexion = None
    _db_name = "agenda.db"

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None:
            cls._conexion = sqlite3.connect(cls._db_name)
        return cls._conexion

    @classmethod
    def obtener_cursor(cls):
        return cls.obtener_conexion().cursor()

    @classmethod
    def cerrar_conexion(cls):
        if cls._conexion:
            cls._conexion.close()
            cls._conexion = None