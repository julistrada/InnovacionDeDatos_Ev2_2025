from db import ConexionDB


class Contacto:
    def __init__(self, nombre, apellido, telefono, email, id=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    @staticmethod
    def obtener_todos():
        cursor = ConexionDB.obtener_cursor()
        cursor.execute("SELECT id, nombre, apellido, telefono, email FROM contactos")
        filas = cursor.fetchall()
        return [Contacto(id=fila[0], nombre=fila[1], apellido=fila[2], telefono=fila[3], email=fila[4]) for fila in filas]

    def guardar(self):
        cursor = ConexionDB.obtener_cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)",
            (self.nombre, self.apellido, self.telefono, self.email)
        )
        ConexionDB.obtener_conexion().commit()

    def actualizar(self):
        cursor = ConexionDB.obtener_cursor()
        cursor.execute(
            "UPDATE contactos SET nombre = ?, apellido = ?, telefono = ?, email = ? WHERE id = ?",
            (self.nombre, self.apellido, self.telefono, self.email, self.id)
        )
        ConexionDB.obtener_conexion().commit()

    def eliminar(self):
        cursor = ConexionDB.obtener_cursor()
        cursor.execute("DELETE FROM contactos WHERE id = ?", (self.id,))
        ConexionDB.obtener_conexion().commit()
