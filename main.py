#### C. Archivo `main.py`
```python
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class BarberBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BarberBook - Destiny Studio Barbería (Prototipo v1.0)")
        self.root.geometry("820x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.iniciar_bd()
        self.crear_interfaz()
        self.cargar_citas()

    def iniciar_bd(self):
        self.conn = sqlite3.connect("destiny_studio.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                telefono TEXT NOT NULL,
                servicio TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def crear_interfaz(self):
        lbl_titulo = tk.Label(
            self.root,
            text="Destiny Studio Barbería - Gestión de Citas",
            font=("Segoe UI", 18, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        lbl_titulo.pack(pady=15)

        contenedor = tk.Frame(self.root, bg="#1e1e2e")
        contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- PANEL IZQUIERDO: FORMULARIO ---
        panel_form = tk.LabelFrame(
            contenedor, text=" Agendar Nueva Cita ", font=("Segoe UI", 11, "bold"),
            bg="#2a2a3c", fg="#89b4fa", padx=15, pady=15
        )
        panel_form.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(panel_form, text="Nombre del Cliente:", bg="#2a2a3c", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_cliente = tk.Entry(panel_form, width=28, font=("Segoe UI", 10))
        self.entry_cliente.pack(pady=(2, 10))

        tk.Label(panel_form, text="Teléfono:", bg="#2a2a3c", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_telefono = tk.Entry(panel_form, width=28, font=("Segoe UI", 10))
        self.entry_telefono.pack(pady=(2, 10))

        tk.Label(panel_form, text="Servicio:", bg="#2a2a3c", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.combo_servicio = ttk.Combobox(
            panel_form,
            values=["Corte Clásico ($5)", "Fade / Degradado ($7)", "Corte + Barba ($10)", "Arreglo de Barba ($4)"],
            state="readonly",
            width=26,
            font=("Segoe UI", 10)
        )
        self.combo_servicio.current(0)
        self.combo_servicio.pack(pady=(2, 10))

        tk.Label(panel_form, text="Fecha (DD/MM/AAAA):", bg="#2a2a3c", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_fecha = tk.Entry(panel_form, width=28, font=("Segoe UI", 10))
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_fecha.pack(pady=(2, 10))

        tk.Label(panel_form, text="Hora (HH:MM):", bg="#2a2a3c", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_hora = tk.Entry(panel_form, width=28, font=("Segoe UI", 10))
        self.entry_hora.pack(pady=(2, 15))

        btn_guardar = tk.Button(
            panel_form, text="Guardar Cita", command=self.agendar_cita,
            bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", width=24, pady=6
        )
        btn_guardar.pack()

        # --- PANEL DERECHO: TABLA DE CITAS ---
        panel_tabla = tk.LabelFrame(
            contenedor, text=" Citas Programadas ", font=("Segoe UI", 11, "bold"),
            bg="#2a2a3c", fg="#89b4fa", padx=10, pady=10
        )
        panel_tabla.pack(side="right", fill="both", expand=True)

        columnas = ("ID", "Cliente", "Teléfono", "Servicio", "Fecha", "Hora")
        self.tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings", height=15)

        anchos = [35, 130, 85, 135, 85, 60]
        for col, ancho in zip(columnas, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True)

    def agendar_cita(self):
        cliente = self.entry_cliente.get().strip()
        telefono = self.entry_telefono.get().strip()
        servicio = self.combo_servicio.get()
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()

        if not cliente or not telefono or not fecha or not hora:
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los datos de la cita.")
            return

        self.cursor.execute("SELECT * FROM citas WHERE fecha = ? AND hora = ?", (fecha, hora))
        if self.cursor.fetchone():
            messagebox.showerror("Horario ocupado", f"Ya existe una cita agendada el {fecha} a las {hora}.")
            return

        self.cursor.execute(
            "INSERT INTO citas (cliente, telefono, servicio, fecha, hora) VALUES (?, ?, ?, ?, ?)",
            (cliente, telefono, servicio, fecha, hora)
        )
        self.conn.commit()

        messagebox.showinfo("Cita Guardada", "La cita ha sido agendada correctamente.")
        self.entry_cliente.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.cargar_citas()

    def cargar_citas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.cursor.execute("SELECT * FROM citas ORDER BY fecha, hora")
        for row in self.cursor.fetchall():
            self.tabla.insert("", tk.END, values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = BarberBookApp(root)
    root.mainloop()
