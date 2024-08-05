import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from src.components.profesores import ProfesoresApp
from PIL import Image, ImageTk
from src.components.alumnos import AlumnoApp
from src.model.database_profesores import DatabaseManagerProfesores
from src.model.database_alumnos import DatabaseManagerAlumnos


class LoginApp:
    def __init__(self):
        self.app = Tk()
        self.app.title("Login")
        self.app.geometry("800x600")
        self.app.configure(bg="#2C3E50")  # Fondo de la ventana principal
        self.role = StringVar(value=" ")
        self.create_widgets()
        self.icon_img = PhotoImage(
            file="src/example/UNAS.png"
        )  # Reemplaza con la ruta de tu ícono
        self.app.iconphoto(False, self.icon_img)
        self.db_manager_profesores = DatabaseManagerProfesores(
            host="localhost", user="root", password="123456789", database="tutoria"
        )
        self.db_manager_alumnos = DatabaseManagerAlumnos(
            host="localhost", user="root", password="123456789", database="tutoria"
        )
        self.app.mainloop()

    def resource_path(self, relative_path):
        """Get the absolute path to the resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Creando los widgets de programa
    def create_widgets(self):
        # Main Frame
        main_frame = Frame(self.app, bg="#22577A", bd=2, relief="raised")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        # Title
        title_label = Label(
            main_frame,
            text="Bienvenido",
            fg="#FFFFFF",
            font=("Helvetica", 24, "bold"),
            bg="#22577A",
        )
        title_label.pack(pady=(40, 20))

        # Rol Selection Frame
        rol_frame = Frame(main_frame, bg="#22577A")
        rol_frame.pack(pady=10)
        rol_frame.columnconfigure(0, weight=1)
        rol_frame.columnconfigure(1, weight=1)
        rol_frame.columnconfigure(2, weight=1)

        # Radio Buttons
        professor_radio = Radiobutton(
            rol_frame,
            text="Profesor",
            variable=self.role,
            value="Profesor",
            bg="#22577A",
            activebackground="#34495E",
            fg="#ECF0F1",
            font=("Helvetica", 18),
            selectcolor="#22577A",
        )
        professor_radio.grid(row=0, column=0, sticky="ew")

        student_radio = Radiobutton(
            rol_frame,
            text="Estudiante",
            variable=self.role,
            value="Estudiante",
            bg="#22577A",
            activebackground="#34495E",
            fg="#ECF0F1",
            font=("Helvetica", 18),
            selectcolor="#22577A",
        )
        student_radio.grid(row=0, column=2, sticky="ew")

        path_to_image = "src/example/UNAS.png"  # Asegúrate de que la ruta es correcta
        original_image = Image.open(path_to_image)
        resized_image = original_image.resize(
            (130, 130), Image.Resampling.LANCZOS
        )  # Redimensiona la imagen
        self.image = ImageTk.PhotoImage(resized_image)

        # Image Label
        self.image_label = Label(rol_frame, image=self.image, bg="#22577A")
        self.image_label.grid(row=4, column=1, sticky="nsew")

        # Login Button
        login_btn = Button(
            main_frame,
            text="Login",
            command=self.login,
            bg="#57A773",
            fg="white",
            font=("Helvetica", 16, "bold"),
            padx=20,
            pady=10,
            bd=0,
            activebackground="#22577A",
            highlightthickness=0,
        )
        login_btn.pack(pady=(20, 10))

        # Back Button
        back_btn = Button(
            main_frame,
            text="Volver",
            command=self.app.quit,
            bg="#22577A",
            fg="#A7BBC7",
            font=("Helvetica", 10, "bold"),
            bd=0,
            activebackground="#22577A",
            highlightthickness=0,
        )
        back_btn.pack(side=BOTTOM, pady=(10, 20))

    # Función para iniciar sesión
    def login(self):
        role = self.role.get()
        if role == "Profesor":
            self.app.destroy()
            ProfesoresApp(self.db_manager_profesores)
        elif role == "Estudiante":
            self.app.destroy()
            AlumnoApp(self.db_manager_alumnos)
        else:
            messagebox.showerror("Error", "Por favor seleccione un rol.")


if __name__ == "__main__":
    app = LoginApp()
