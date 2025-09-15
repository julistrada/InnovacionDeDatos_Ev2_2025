import tkinter as tk
from db import ConexionDB
from gui import InterfazAgenda

def inicializar_base():
    cursor = ConexionDB.obtener_cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    ConexionDB.obtener_conexion().commit()
    
if __name__ == "__main__":
    inicializar_base()

    root = tk.Tk()
    app = InterfazAgenda(root)
    root.mainloop()