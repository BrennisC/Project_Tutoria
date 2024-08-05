import mysql.connector
from tkinter import messagebox


class DatabaseManagerProfesores:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
        )

    def fetch_all(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM profesores")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al obtener datos: {error}")
            return []

    def insert(self, data):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            sql = (
                "INSERT INTO profesores (codigo_profesor, nombre, apellido, email, genero, horario) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al insertar datos: {error}")

    def delete(self, id_profesor):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM profesores WHERE id_profesor = %s", (id_profesor,)
            )
            connection.commit()

            # Restablecer el ID a 1
            cursor.execute("ALTER TABLE profesores AUTO_INCREMENT = 1")
            connection.commit()

            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error al eliminar datos: {error}")
