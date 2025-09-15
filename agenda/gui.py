import tkinter as tk
from tkinter import ttk
from contacto import Contacto
import tkinter.messagebox as messagebox


class InterfazAgenda:
    def __init__(self, master):
        self.master = master
        self.master.title("Agenda de Contactos")
        self.master.geometry("450x600")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")
    
        self.main_frame = tk.Frame(self.master, bg="#f3f3f3")
        self.main_frame.pack(fill="both", expand=True)

        self.form_frame = tk.Frame(self.main_frame, bg="#f0f0f0", padx=10, pady=10)
        self.form_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.form_frame.pack_forget()

        self._crear_formulario()

        self._crear_area_contactos()

        self.obtener_contactos()
        self._mostrar_mensaje(texto="Lista cargada con exito")

    def _crear_formulario(self):
        self.titulo_formulario = tk.Label(
            self.form_frame,
            text="Nuevo contacto",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.titulo_formulario.pack(fill="x", pady=(0, 10))


        self._crear_campo("Nombre", "nombre_entry")
        self._crear_campo("Apellido", "apellido_entry")
        self._crear_campo("Teléfono", "telefono_entry")
        self._crear_campo("Email", "email_entry")

        boton_frame = tk.Frame(self.form_frame, bg="#f0f0f0")
        boton_frame.pack(fill="x", pady=(10, 5))

        self.cancelar_btn = tk.Button(
            boton_frame,
            text="Cancelar",
            width=10,
            bg="#737373",
            fg="#ffffff",
            font=("Arial", 11),
            relief="flat",
            cursor="hand2",
            command=self.restablecer_formulario
        )
        self.cancelar_btn.pack(side="right", padx=(5, 0), ipady=5)

        self.guardar_btn = tk.Button(
            boton_frame,
            text="Guardar",
            width=10,
            bg="#000000",
            fg="#ffffff",
            font=("Arial", 11),
            relief="flat",
            cursor="hand2",
            command=self.guardar_o_actualizar
        )
        self.guardar_btn.pack(side="right", padx=(0, 5), ipady=5)


        self.notificacion_label = tk.Label(
            self.master,
            text="",
            bg="#ffffff",
            fg="#000000",
            font=("Arial", 10),
            anchor="w",
            padx=10,
            pady=5 
        )
        self.notificacion_label.pack(fill="x")

    def _crear_campo(self, label_text, entry_attr):
        campo_frame = tk.Frame(self.form_frame, bg="#f0f0f0")
        campo_frame.pack(fill="x", pady=5)

        label = tk.Label(
            self.form_frame,
            text=label_text,
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 0))

        entry = tk.Entry(
            self.form_frame,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#000000",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#2563EB"
        )
        entry.pack(fill="x", pady=(0, 10), ipady=6)

        setattr(self, entry_attr, entry)

    def _crear_area_contactos(self):
        self.lista_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        encabezado_frame = tk.Frame(self.lista_frame, bg="#f0f0f0")
        encabezado_frame.pack(fill="x", pady=(10, 5))

        titulo = tk.Label(
            encabezado_frame,
            text="Mis Contactos",
            bg="#f0f0f0",
            fg="#000000",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        titulo.pack(side="left", padx=(0, 10))

        nuevo_btn = tk.Button(
            encabezado_frame,
            text="Nuevo",
            bg="#2563EB",
            fg="#ffffff",
            font=("Arial", 10),
            cursor="hand2",
            width=12, 
            relief="flat",
            command=self.abrir_formulario
        )
        nuevo_btn.pack(side="right")

        scroll_area = tk.Frame(self.lista_frame, bg="#f0f0f0")
        scroll_area.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(scroll_area, bg="#f0f0f0", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(scroll_area, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig("frame", width=e.width))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="frame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")))
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all("<MouseWheel>"))

    def _crear_bloque_contacto(self, contacto):
        fila = tk.Frame(self.scrollable_frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
        fila.pack(fill="x", expand=True, pady=5)

        datos = tk.Frame(fila, bg="#ffffff")
        datos.pack(side="left", fill="both", expand=True)

        tk.Label(datos, text=f"{contacto.nombre} {contacto.apellido}".upper(), font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w")
        tk.Label(datos, text=f"Teléfono: {contacto.telefono}", bg="#ffffff", font=("Arial", 10)).pack(anchor="w")
        tk.Label(datos, text=f"Email: {contacto.email}", bg="#ffffff", font=("Arial", 10)).pack(anchor="w")

        acciones = tk.Frame(fila, bg="#ffffff")
        acciones.pack(side="right", padx=10)

        tk.Button(acciones, text="Modificar", bg="#000000", fg="#ffffff", width=12, relief="flat", cursor="hand2",command=lambda c=contacto: self.actualizar_contacto(c)).pack(pady=2)
        tk.Button(acciones, text="Eliminar", bg="#d13438", fg="#ffffff", width=12, relief="flat", cursor="hand2",command=lambda c=contacto: self.eliminar_contacto(c)).pack(pady=2)

    def _mostrar_mensaje(self, texto):
        self.notificacion_label.config(text=texto, bg="#0078d4", fg="#ffffff")
        self.master.after(2500, lambda: self.notificacion_label.config(text="", bg="#ffffff"))

    def abrir_formulario(self):
        self.lista_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def restablecer_formulario(self):
        self.nombre_entry.delete(0, "end")
        self.apellido_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

        self.modo_edicion = False
        self.id_en_edicion = None

        self.guardar_btn.config(text="Guardar")
        self.titulo_formulario.config(text="Nuevo contacto")

        self.form_frame.pack_forget()
        self.lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))


    # Metodos CRUD

    def obtener_contactos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        contactos = Contacto.obtener_todos()

        if not contactos:
            mensaje = tk.Label(
                self.scrollable_frame,
                text="No tienes ningún contacto guardado.\nAñade uno para comenzar a usar el sistema.",
                bg="#f0f0f0",
                fg="#555555",
                font=("Arial", 11),
                justify="center"
            )
            mensaje.pack(pady=50)
            return

        for contacto in contactos:
            self._crear_bloque_contacto(contacto)
        
    def eliminar_contacto(self, contacto):
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el contacto {contacto.nombre.upper()} {contacto.apellido.upper()}?"
        )

        if not confirmacion:
            self._mostrar_mensaje(texto="Eliminación cancelada")
            return

        contacto.eliminar()

        self._mostrar_mensaje(texto="Contacto eliminado correctamente")
        self.obtener_contactos()

    def actualizar_contacto(self, contacto):
        self.restablecer_formulario()
        self.titulo_formulario.config(text="Modificar contacto")
        self.abrir_formulario()

        self.nombre_entry.insert(0, contacto.nombre)
        self.apellido_entry.insert(0, contacto.apellido)
        self.telefono_entry.insert(0, contacto.telefono)
        self.email_entry.insert(0, contacto.email)

        self.guardar_btn.config(text="Modificar")

        self.modo_edicion = True
        self.id_en_edicion = contacto.id

        self._mostrar_mensaje(texto=f"Contacto seleccionado: {contacto.nombre.upper()} {contacto.apellido.upper()}")

    def guardar_o_actualizar(self):

        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        email = self.email_entry.get().strip()

        if not (nombre and apellido and telefono and email):
            self._mostrar_mensaje(texto="Todos los campos son obligatorios")
            return

        if hasattr(self, "modo_edicion") and self.modo_edicion:
            contacto = Contacto(nombre, apellido, telefono, email, id=self.id_en_edicion)
            contacto.actualizar()
            self._mostrar_mensaje(texto="Contacto actualizado correctamente")
        else:
            contacto = Contacto(nombre, apellido, telefono, email)
            contacto.guardar()
            self._mostrar_mensaje(texto="Contacto guardado correctamente")

        self.obtener_contactos()
        self.restablecer_formulario()

