import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import mysql.connector
from src.model.database_alumnos import DatabaseManagerAlumnos
from src.components.face_recognition_system import FaceRecognitionSystem


class AlumnoApp:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.face_recognition_system = FaceRecognitionSystem()
        self.root = Tk()
        self.root.title("Gestión de Alumnos")
        self.root.geometry("800x700")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = Label(
            self.root,
            text="Registro de Alumnos",
            font=("Roboto Medium", 24),
            bg="#3498DB",
            fg="white",
        )
        self.title_label.pack(fill=X, pady=10)

        self.form_frame = Frame(self.root, bg="#ECF0F1")
        self.form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        fields = ["Código", "Nombre", "Apellido", "Email", "Teléfono", "Ciclo"]
        self.entries = {}
        for index, field in enumerate(fields):
            label = Label(
                self.form_frame, text=f"{field}:", font=("Roboto", 14), bg="#ECF0F1"
            )
            label.grid(
                row=index // 3, column=(index % 3) * 2, pady=10, padx=10, sticky="w"
            )
            entry = Entry(self.form_frame, width=30, font=("Roboto", 14))
            entry.grid(
                row=index // 3, column=(index % 3) * 2 + 1, pady=10, padx=10, sticky="w"
            )
            self.entries[field] = entry

        self.add_button = Button(
            self.form_frame,
            text="Registrar",
            command=self.registrar,
            bg="#2ECC71",
            fg="white",
            font=("Roboto", 14),
        )
        self.update_button = Button(
            self.form_frame,
            text="Actualizar",
            command=self.actualizar,
            bg="#F39C12",
            fg="white",
            font=("Roboto", 14),
        )
        self.delete_button = Button(
            self.form_frame,
            text="Eliminar",
            command=self.eliminar,
            bg="#E74C3C",
            fg="white",
            font=("Roboto", 14),
        )
        self.load_photo_button = Button(
            self.form_frame,
            text="Cargar Foto",
            command=self.cargar_foto,
            bg="#3498DB",
            fg="white",
            font=("Roboto", 14),
        )
        self.capture_images_button = Button(
            self.form_frame,
            text="Capturar Imágenes",
            command=self.capture_images,
            bg="#3498DB",
            fg="white",
            font=("Roboto", 14),
        )
        self.recognize_student_button = Button(
            self.form_frame,
            text="Reconocer Estudiante",
            command=self.recognize_student,
            bg="#3498DB",
            fg="white",
            font=("Roboto", 14),
        )

        self.add_button.grid(row=3, column=0, pady=20)
        self.update_button.grid(row=3, column=1, pady=20)
        self.delete_button.grid(row=3, column=2, pady=20)
        self.load_photo_button.grid(row=4, column=0, pady=20)
        self.capture_images_button.grid(row=4, column=1, pady=20)
        self.recognize_student_button.grid(row=4, column=2, pady=20)

        self.photo_label = Label(self.form_frame, bg="#ECF0F1")
        self.photo_label.grid(row=5, column=1, columnspan=2)

        self.table_frame = Frame(self.root)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.treeview = ttk.Treeview(
            self.table_frame, columns=("id",) + tuple(fields), show="headings"
        )
        for field in ("id",) + tuple(fields):
            self.treeview.heading(field, text=field)
            self.treeview.column(field, anchor="center", width=100)
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)
        self.treeview.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.load_data()

    def capture_images(self):
        try:
            student_id = simpledialog.askstring("Input", "Enter Student ID:")
            if student_id:
                self.face_recognition_system.capture_images(student_id)
                messagebox.showinfo("Success", "Images captured successfully.")
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
            self.entries["Código"].get(),
            self.entries["Nombre"].get(),
            self.entries["Apellido"].get(),
            self.entries["Email"].get(),
            self.entries["Teléfono"].get(),
            self.entries["Ciclo"].get(),
        )
        try:
            self.db_manager.insert(alumno_data)
            messagebox.showinfo("Información", "Alumno registrado con éxito")
            self.clear_entries()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el alumno: {e}")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def actualizar(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_data = (
            self.entries["Código"].get(),
            self.entries["Nombre"].get(),
            self.entries["Apellido"].get(),
            self.entries["Email"].get(),
            self.entries["Teléfono"].get(),
            self.entries["Ciclo"].get(),
            self.treeview.item(selected_item, "values")[0],  # ID del alumno
        )
        try:
            self.db_manager.update(alumno_data)
            messagebox.showinfo("Información", "Alumno actualizado con éxito")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el alumno: {e}")

    def eliminar(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Selección", "No se ha seleccionado ningún elemento.")
            return

        selected_item = selected_items[0]
        alumno_id = self.treeview.item(selected_item, "values")[0]
        try:
            self.db_manager.delete(alumno_id)
            messagebox.showinfo("Información", "Alumno eliminado con éxito")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el alumno: {e}")

    def load_data(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        for row in self.db_manager.fetch_all():
            self.treeview.insert("", "end", values=row)

    def on_treeview_click(self, event):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        item_values = self.treeview.item(selected_item, "values")
        for index, key in enumerate(
            ["Código", "Nombre", "Apellido", "Email", "Teléfono", "Ciclo"]
        ):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, item_values[index + 1])


if __name__ == "__main__":
    try:
        db_manager = DatabaseManagerAlumnos(
            host="localhost", user="root", password="123456789", database="tutoria"
        )
        app = AlumnoApp(db_manager)
        app.root.mainloop()
    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error", f"Failed to connect to the database: {e}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
