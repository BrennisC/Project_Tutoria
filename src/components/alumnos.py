import os
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from .face_recognition_system import FaceRecognitionSystem


class AlumnoApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.face_recognition_system = FaceRecognitionSystem()

        self.app = Tk()
        self.app.title("Gestión de Alumnos")
        self.app.geometry("900x700")
        self.app.configure(bg="#E8F0F2")

        self.Codigo = StringVar()
        self.Nombre = StringVar()
        self.Apellido = StringVar()
        self.Email = StringVar()
        self.Telefono = StringVar()
        self.Ciclo = StringVar()

        self.create_widgets()
        self.app.mainloop()

    def create_widgets(self):
        main_frame = Frame(self.app, bg="#E8F0F2")
        main_frame.pack(fill=BOTH, expand=True)

        self.create_title(main_frame)
        self.create_input_frame(main_frame)
        self.create_table(main_frame)

    def create_title(self, parent):
        title_label = Label(
            parent,
            text="Registro de Alumnos",
            bg="#E8F0F2",
            fg="#333333",
            font=("Helvetica", 24, "bold"),
            pady=20,
        )
        title_label.pack()

    def create_input_frame(self, parent):
        input_frame = Frame(
            parent, bg="#FFFFFF", bd=2, relief="groove", padx=20, pady=20
        )
        input_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.create_input_fields(input_frame)
        self.create_buttons(input_frame)

    def create_input_fields(self, frame):
        Label(frame, text="Código", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=0, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Codigo, font=("Helvetica", 12)).grid(
            column=1, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Nombre", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=1, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Nombre, font=("Helvetica", 12)).grid(
            column=1, row=1, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Apellido", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=0, row=2, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Apellido, font=("Helvetica", 12)).grid(
            column=1, row=2, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Email", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=0, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Email, font=("Helvetica", 12)).grid(
            column=3, row=0, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Teléfono", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=1, padx=10, pady=10, sticky=E
        )
        Entry(frame, textvariable=self.Telefono, font=("Helvetica", 12)).grid(
            column=3, row=1, padx=10, pady=10, sticky=W
        )

        Label(frame, text="Ciclo", font=("Helvetica", 12), bg="#FFFFFF").grid(
            column=2, row=2, padx=10, pady=10, sticky=E
        )
        self.combox_ciclo = ttk.Combobox(
            frame, textvariable=self.Ciclo, state="readonly", font=("Helvetica", 12)
        )
        self.combox_ciclo["values"] = [str(i) for i in range(1, 11)]
        self.combox_ciclo.grid(column=3, row=2, padx=10, pady=10, sticky=W)

    def create_buttons(self, frame):
        button_frame = Frame(frame, bg="#FFFFFF")
        button_frame.grid(column=0, row=3, columnspan=4, pady=20)

        Button(
            button_frame,
            text="Registrar",
            command=self.registrar,
            font=("Helvetica", 12),
            bg="#2ECC71",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=0, row=0, padx=10)
        Button(
            button_frame,
            text="Actualizar",
            command=self.actualizar,
            font=("Helvetica", 12),
            bg="#F39C12",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=1, row=0, padx=10)
        Button(
            button_frame,
            text="Eliminar",
            command=self.eliminar,
            font=("Helvetica", 12),
            bg="#E74C3C",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=2, row=0, padx=10)
        Button(
            button_frame,
            text="Cargar Foto",
            command=self.cargar_foto,
            font=("Helvetica", 12),
            bg="#3498DB",
            fg="#FFFFFF",
            width=10,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=3, row=0, padx=10)
        Button(
            button_frame,
            text="Capturar Imágenes",
            command=self.capture_images,
            font=("Helvetica", 12),
            bg="#3498DB",
            fg="#FFFFFF",
            width=15,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=4, row=0, padx=10)
        Button(
            button_frame,
            text="Reconocer Estudiante",
            command=self.recognize_student,
            font=("Helvetica", 12),
            bg="#3498DB",
            fg="#FFFFFF",
            width=20,
            padx=5,
            pady=5,
            cursor="hand2",
        ).grid(column=5, row=0, padx=10)

        self.photo_label = Label(frame, bg="#FFFFFF")
        self.photo_label.grid(row=4, column=1, columnspan=2, pady=10)

    def create_table(self, frame):
        table_frame = Frame(frame, bg="#E8F0F2")
        table_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        columns = ("id", "Código", "Nombre", "Apellido", "Email", "Teléfono", "Ciclo")
        self.tvAlumnos = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tvAlumnos.pack(fill=BOTH, expand=True)

        for col in columns:
            self.tvAlumnos.column(col, anchor=CENTER, width=100)
            self.tvAlumnos.heading(col, text=col)

        self.tvAlumnos.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.load_data()

    def capture_images(self):
        try:
            student_id = simpledialog.askstring("Ingrese", "Ingrese estudiante ID:")
            if student_id:
                self.face_recognition_system.capture_images(student_id)
                messagebox.showinfo("Información", "Imágenes capturadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture images: {e}")

    def recognize_student(self):
        try:
            self.face_recognition_system.recognize_student()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to recognize student: {e}")

    def cargar_foto(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.mostrar_imagen(file_path)

    def mostrar_imagen(self, file_path):
        img = Image.open(file_path)
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(img)
        self.photo_label.configure(image=self.photo_image)
        self.photo_label.image = self.photo_image  # Mantener una referencia

    def registrar(self):
        alumno_data = (
            self.Codigo.get(),
            self.Nombre.get(),
            self.Apellido.get(),
            self.Email.get(),
            self.Telefono.get(),
            self.Ciclo.get(),
        )
        try:
            self.db_manager.insert(alumno_data)
            messagebox.showinfo("Información", "Alumno registrado con éxito")
            self.clear_entries()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el alumno: {e}")

    def clear_entries(self):
        self.Codigo.set("")
        self.Nombre.set("")
        self.Apellido.set("")
        self.Email.set("")
        self.Telefono.set("")
        self.Ciclo.set("")

    def actualizar(self):
        selected_items = self.tvAlumnos.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_data = (
            self.Codigo.get(),
            self.Nombre.get(),
            self.Apellido.get(),
            self.Email.get(),
            self.Telefono.get(),
            self.Ciclo.get(),
            self.tvAlumnos.item(selected_item, "values")[0],  # ID del alumno
        )
        try:
            self.db_manager.update(alumno_data)
            messagebox.showinfo("Información", "Alumno actualizado con éxito")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el alumno: {e}")

    def eliminar(self):
        selected_items = self.tvAlumnos.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_id = self.tvAlumnos.item(selected_item, "values")[0]
        try:
            self.db_manager.delete(alumno_id)
            messagebox.showinfo("Información", "Alumno eliminado con éxito")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el alumno: {e}")

    def load_data(self):
        for i in self.tvAlumnos.get_children():
            self.tvAlumnos.delete(i)
        for row in self.db_manager.fetch_all():
            self.tvAlumnos.insert("", "end", values=row)

    def on_treeview_click(self, event):
        selected_items = self.tvAlumnos.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        item_values = self.tvAlumnos.item(selected_item, "values")
        fields = ["Codigo", "Nombre", "Apellido", "Email", "Telefono", "Ciclo"]
        for idx, field in enumerate(fields):
            getattr(self, field).set(item_values[idx + 1])
