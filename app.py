import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Importamos Spark (comentado para evitar errores si no está instalado)
# from pyspark.sql import SparkSession

class SparkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark Data Processing - Interfaz Gráfica")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.spark_session = None
        self.is_running = False
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Centrar ventana
        self.center_window()
    
    def setup_styles(self):
        """Configura los estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', 
                       font=('Helvetica', 16, 'bold'),
                       foreground='white',
                       background='#2c3e50')
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 10),
                       foreground='#bdc3c7',
                       background='#2c3e50')
        
        style.configure('Card.TFrame',
                       background='#34495e',
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Action.TButton',
                       font=('Helvetica', 10, 'bold'),
                       foreground='white')
        
        style.map('Action.TButton',
                 background=[('active', '#3498db'),
                           ('!active', '#2980b9')])
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', pady=20)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, 
                               text="🚀 Apache Spark Data Processing",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Interfaz gráfica para procesamiento de datos con PySpark",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        left_panel.pack(side='left', fill='both', padx=(0, 10), expand=True)
        
        # Controls title
        controls_title = ttk.Label(left_panel, 
                                  text="⚙ Configuración",
                                  font=('Helvetica', 12, 'bold'))
        controls_title.pack(anchor='w', pady=(0, 15))
        
        # App name
        ttk.Label(left_panel, text="Nombre de la aplicación:").pack(anchor='w', pady=(0, 5))
        self.app_name_var = tk.StringVar(value="Test Spark 3.2.2")
        app_name_entry = ttk.Entry(left_panel, textvariable=self.app_name_var, width=30)
        app_name_entry.pack(fill='x', pady=(0, 10))
        
        # Master URL
        ttk.Label(left_panel, text="Master URL:").pack(anchor='w', pady=(0, 5))
        self.master_var = tk.StringVar(value="local[*]")
        master_combo = ttk.Combobox(left_panel, textvariable=self.master_var, width=27)
        master_combo['values'] = ('local[*]', 'local[1]', 'local[2]', 'local[4]')
        master_combo.pack(fill='x', pady=(0, 10))
        
        # Data range
        ttk.Label(left_panel, text="Rango de datos:").pack(anchor='w', pady=(0, 5))
        self.range_var = tk.StringVar(value="5")
        range_spinbox = ttk.Spinbox(left_panel, from_=1, to=1000, 
                                   textvariable=self.range_var, width=28)
        range_spinbox.pack(fill='x', pady=(0, 15))
        
        # Status frame
        status_frame = ttk.Frame(left_panel)
        status_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(status_frame, text="Estado:").pack(anchor='w')
        self.status_var = tk.StringVar(value="Sesión Spark: Inactiva")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                     foreground='#e74c3c')
        self.status_label.pack(anchor='w')
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(left_panel, variable=self.progress_var,
                                          maximum=100, length=200)
        self.progress_bar.pack(fill='x', pady=(0, 15))
        
        # Buttons frame
        buttons_frame = ttk.Frame(left_panel)
        buttons_frame.pack(fill='x', pady=(0, 10))
        
        self.run_button = ttk.Button(buttons_frame, 
                                    text="🚀 Ejecutar Procesamiento",
                                    command=self.run_spark_job,
                                    style='Action.TButton')
        self.run_button.pack(side='left', padx=(0, 5))
        
        self.stop_button = ttk.Button(buttons_frame,
                                     text="⏹ Detener",
                                     command=self.stop_spark_job,
                                     state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        self.clear_button = ttk.Button(buttons_frame,
                                      text="🗑 Limpiar Log",
                                      command=self.clear_log)
        self.clear_button.pack(side='left', padx=5)
        
        # Right panel - Results and metrics
        right_panel = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Metrics frame
        metrics_frame = ttk.LabelFrame(right_panel, text="📊 Métricas", padding="10")
        metrics_frame.pack(fill='x', pady=(0, 15))
        
        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.pack()
        
        # Métricas
        ttk.Label(metrics_grid, text="Registros procesados:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.records_var = tk.StringVar(value="0")
        ttk.Label(metrics_grid, textvariable=self.records_var, 
                 font=('Helvetica', 10, 'bold'), foreground='#27ae60').grid(row=0, column=1, sticky='w')
        
        ttk.Label(metrics_grid, text="Tiempo de ejecución:").grid(row=1, column=0, sticky='w', padx=(0, 10))
        self.time_var = tk.StringVar(value="0.0s")
        ttk.Label(metrics_grid, textvariable=self.time_var,
                 font=('Helvetica', 10, 'bold'), foreground='#27ae60').grid(row=1, column=1, sticky='w')
        
        ttk.Label(metrics_grid, text="Versión Spark:").grid(row=2, column=0, sticky='w', padx=(0, 10))
        self.version_var = tk.StringVar(value="3.2.2")
        ttk.Label(metrics_grid, textvariable=self.version_var,
                 font=('Helvetica', 10, 'bold'), foreground='#27ae60').grid(row=2, column=1, sticky='w')
        
        # Results frame
        results_frame = ttk.LabelFrame(right_panel, text="📋 Log de Ejecución", padding="10")
        results_frame.pack(fill='both', expand=True)
        
        # Text widget para el log
        self.log_text = scrolledtext.ScrolledText(results_frame,
                                                 height=20,
                                                 width=50,
                                                 font=('Consolas', 9),
                                                 bg='#1e1e1e',
                                                 fg='#ffffff',
                                                 insertbackground='white')
        self.log_text.pack(fill='both', expand=True)
        
        # Configurar tags para colores
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#27ae60')
        self.log_text.tag_config('error', foreground='#e74c3c')
        self.log_text.tag_config('warning', foreground='#f39c12')
        
        # Mensaje inicial
        self.add_log("Interfaz gráfica de Spark inicializada correctamente", 'info')
        self.add_log("Configuración lista para ejecutar trabajos de Spark", 'info')
    
    def add_log(self, message, msg_type='info'):
        """Añade un mensaje al log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, msg_type)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Limpia el área de log"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("Log limpiado", 'info')
    
    def update_status(self, status, color='#e74c3c'):
        """Actualiza el estado de la aplicación"""
        self.status_var.set(status)
        self.status_label.configure(foreground=color)
    
    def simulate_spark_job(self):
        """Simula la ejecución del trabajo Spark"""
        try:
            start_time = time.time()
            data_range = int(self.range_var.get())
            app_name = self.app_name_var.get()
            master_url = self.master_var.get()
            
            # Simulación de las etapas del script original
            stages = [
                ("Iniciando SparkSession...", 10),
                ("Configurando aplicación Spark...", 20),
                (f"Creando sesión con master: {master_url}", 30),
                ("SparkSession creada exitosamente", 50),
                (f"Generando DataFrame con rango de {data_range} registros...", 70),
                ("Ejecutando operación spark.range()...", 80),
                ("Mostrando datos del DataFrame...", 90),
                ("Cerrando sesión Spark...", 100)
            ]
            
            self.add_log("=" * 50, 'info')
            self.add_log("INICIANDO TRABAJO SPARK", 'info')
            self.add_log("=" * 50, 'info')
            
            for stage, progress in stages:
                if not self.is_running:
                    break
                    
                self.add_log(stage, 'info')
                self.progress_var.set(progress)
                time.sleep(0.5)  # Simular tiempo de procesamiento
            
            if self.is_running:
                # Simular la salida del DataFrame
                self.add_log("", 'info')
                self.add_log("DataFrame.show() - Resultado:", 'success')
                self.add_log("+---+", 'success')
                self.add_log("| id|", 'success')
                self.add_log("+---+", 'success')
                
                for i in range(data_range):
                    self.add_log(f"|  {i}|", 'success')
                    time.sleep(0.1)
                
                self.add_log("+---+", 'success')
                self.add_log("", 'info')
                
                end_time = time.time()
                execution_time = round(end_time - start_time, 2)
                
                # Actualizar métricas
                self.records_var.set(str(data_range))
                self.time_var.set(f"{execution_time}s")
                
                self.add_log("Sesión Spark cerrada correctamente", 'success')
                self.add_log(f"Trabajo completado en {execution_time} segundos", 'success')
                self.add_log("=" * 50, 'info')
                
                self.update_status("Trabajo completado exitosamente", '#27ae60')
            
        except Exception as e:
            self.add_log(f"Error durante la ejecución: {str(e)}", 'error')
            self.update_status("Error en la ejecución", '#e74c3c')
        
        finally:
            self.is_running = False
            self.run_button.configure(state='normal')
            self.stop_button.configure(state='disabled')
            self.progress_var.set(0)
    
    def run_spark_job(self):
        """Inicia el trabajo Spark en un hilo separado"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "Ya hay un trabajo ejecutándose")
            return
        
        self.is_running = True
        self.run_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.update_status("Ejecutando trabajo Spark...", '#f39c12')
        
        # Ejecutar en hilo separado para no bloquear la GUI
        thread = threading.Thread(target=self.simulate_spark_job)
        thread.daemon = True
        thread.start()
    
    def stop_spark_job(self):
        """Detiene el trabajo Spark"""
        self.is_running = False
        self.add_log("Deteniendo trabajo Spark...", 'warning')
        self.update_status("Trabajo detenido por el usuario", '#e74c3c')
        self.run_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.progress_var.set(0)

# Código para ejecutar la aplicación con Spark real (descomentarlo cuando tengas Spark instalado)
def run_real_spark_job(app_name, master_url, data_range):
    """
    Función que ejecuta el script Spark real
    Descomenta este código cuando tengas PySpark instalado
    """
    try:
        # from pyspark.sql import SparkSession
        
        # # Crear SparkSession
        # spark = SparkSession.builder \
        #     .appName(app_name) \
        #     .master(master_url) \
        #     .getOrCreate()
        
        # # Crear DataFrame
        # df = spark.range(int(data_range))
        
        # # Mostrar datos
        # df.show()
        
        # # Cerrar sesión
        # spark.stop()
        
        return True, "Trabajo Spark ejecutado correctamente"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Función principal"""
    root = tk.Tk()
    app = SparkGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()