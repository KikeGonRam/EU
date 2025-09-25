import tkinter as tk
from tkinter import ttk
import time

class SparkPersonasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación PySpark - DataFrame Personas")
        self.root.geometry("900x600")

        # Configuración de colores
        self.colors = {
            "bg": "#1e1e2e",
            "fg": "#cdd6f4",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8",
            "info": "#89b4fa",
            "data": "#94e2d5"
        }

        # Configuración de la interfaz
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Título
        title = tk.Label(
            main_frame, 
            text="💻 Procesamiento de DataFrame con PySpark (Simulación)",
            font=("Consolas", 16, "bold"),
            fg=self.colors["info"],
            bg=self.colors["bg"]
        )
        title.pack(pady=10, fill="x")

        # Botón para iniciar
        self.start_button = tk.Button(
            main_frame,
            text="▶ Iniciar Simulación",
            font=("Consolas", 12, "bold"),
            command=self.start_simulation,
            bg=self.colors["info"],
            fg="black",
            relief="raised",
            padx=10,
            pady=5
        )
        self.start_button.pack(pady=10)

        # Textbox para mostrar resultados
        self.text_area = tk.Text(
            main_frame,
            wrap="word",
            font=("Consolas", 12),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            insertbackground=self.colors["fg"]
        )
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.text_area.yview
        )
        self.text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    
    def add_result(self, text, tag=None):
        """Agrega texto al área de resultados con estilo opcional"""
        if tag:
            self.text_area.insert("end", text + "\n", tag)
        else:
            self.text_area.insert("end", text + "\n")
        self.text_area.see("end")
        self.root.update()
    
    def start_simulation(self):
        self.text_area.delete(1.0, "end")
        self.add_result("🚀 Iniciando simulación de procesamiento de DataFrame con PySpark...\n", "info")
        self.root.after(100, self.run_steps)
    
    def run_steps(self):
        # Definición de datos
        self.add_result("📦 Paso 1: Definiendo los datos iniciales...", "info")
        data = [
            ("Juan", 25, "Madrid"),
            ("María", 30, "Barcelona"),
            ("Pedro", 35, "Valencia"),
            ("Lucía", 28, "Sevilla"),
            ("Ana", 40, "Bilbao")
        ]
        time.sleep(1)
        
        # Mostrar DataFrame original
        self.show_original_dataframe(data)
        
        # Simular operaciones PySpark
        self.simulate_operations()
    
    def show_original_dataframe(self, data):
        """Muestra el DataFrame original"""
        self.add_result("=== DATAFRAME ORIGINAL ===", 'success')
        self.add_result("+----------+----+-----------+", 'data')
        self.add_result("|    nombre|edad|     ciudad|", 'data')
        self.add_result("+----------+----+-----------+", 'data')
        
        for nombre, edad, ciudad in data:
            line = f"|{nombre:>10}|{edad:>4}|{ciudad:>11}|"
            self.add_result(line, 'data')
            time.sleep(0.1)
        
        self.add_result("+----------+----+-----------+", 'data')
        self.add_result("", 'info')
    
    def simulate_operations(self):
        """Simula las operaciones con el DataFrame"""
        steps = [
            ("📊 Mostrando solo nombres y edades...", 'info'),
            ("+----------+----+", 'data'),
            ("|    nombre|edad|", 'data'),
            ("+----------+----+", 'data'),
            ("|      Juan|  25|", 'data'),
            ("|     María|  30|", 'data'),
            ("|     Pedro|  35|", 'data'),
            ("|     Lucía|  28|", 'data'),
            ("|       Ana|  40|", 'data'),
            ("+----------+----+", 'data'),
            ("", None),
            
            ("🔍 Filtrando personas mayores de 30 años...", 'info'),
            ("+----------+----+-----------+", 'data'),
            ("|    nombre|edad|     ciudad|", 'data'),
            ("+----------+----+-----------+", 'data'),
            ("|     Pedro|  35|   Valencia|", 'data'),
            ("|       Ana|  40|     Bilbao|", 'data'),
            ("+----------+----+-----------+", 'data'),
            ("", None),
            
            ("📈 Calculando la edad promedio...", 'info'),
            ("Edad promedio: 31.6 años", 'success'),
            ("", None)
        ]
        
        for text, tag in steps:
            self.add_result(text, tag)
            time.sleep(0.3)


if __name__ == "__main__":
    root = tk.Tk()
    app = SparkPersonasGUI(root)
    
    # Estilos para tags
    app.text_area.tag_configure('success', foreground=app.colors["success"])
    app.text_area.tag_configure('warning', foreground=app.colors["warning"])
    app.text_area.tag_configure('error', foreground=app.colors["error"])
    app.text_area.tag_configure('info', foreground=app.colors["info"])
    app.text_area.tag_configure('data', foreground=app.colors["data"])
    
    root.mainloop()


"""
GUÍA COMPLETA DE USO:

1. Ejecuta este script con Python 3:
   python spark_gui.py

2. Aparecerá una ventana con un botón "▶ Iniciar Simulación".

3. Haz clic en el botón para comenzar la simulación paso a paso:
   - Se definen los datos iniciales
   - Se muestra el DataFrame original
   - Se seleccionan columnas específicas
   - Se filtran registros por condición
   - Se calcula una agregación (promedio de edad)

4. Los resultados aparecen en un área de texto con colores
   para diferenciar información, resultados y datos.

5. Este programa es una SIMULACIÓN: 
   No requiere tener instalado Apache Spark ni PySpark.
"""
