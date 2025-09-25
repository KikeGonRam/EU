import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum as spark_sum, count

class SparkPersonasGUI:
    def show_statistics_analysis(self, data):
        """Muestra estadísticas generales del DataFrame"""
        self.add_result("=== ESTADÍSTICAS GENERALES ===", 'success')
        if data:
            edades = [edad for _, edad, _ in data]
            ciudades = [ciudad for _, _, ciudad in data]
            edad_min = min(edades)
            edad_max = max(edades)
            edad_promedio = sum(edades) / len(edades)
            ciudad_counts = {}
            for ciudad in ciudades:
                ciudad_counts[ciudad] = ciudad_counts.get(ciudad, 0) + 1
            ciudad_mas_comun = max(ciudad_counts.items(), key=lambda x: x[1])
            self.add_result(f"📊 Total de registros: {len(data)}", 'info')
            self.add_result(f"📈 Edad mínima: {edad_min} años", 'info')
            self.add_result(f"📈 Edad máxima: {edad_max} años", 'info')
            self.add_result(f"📈 Edad promedio: {edad_promedio:.1f} años", 'info')
            self.add_result(f"🏙️ Ciudades únicas: {len(set(ciudades))}", 'info')
            self.add_result(f"🏆 Ciudad más común: {ciudad_mas_comun[0]} ({ciudad_mas_comun[1]} personas)", 'info')
        self.add_result("", 'info')
    def show_city_grouping_analysis(self, data):
        """Muestra análisis agrupado por ciudad: promedio de edad por ciudad"""
        self.add_result("|   ciudad|edad_promedio|", 'data')
        self.add_result("+---------+-------------+", 'data')
        # Agrupar por ciudad
        city_groups = {}
        for nombre, edad, ciudad in data:
            if ciudad not in city_groups:
                city_groups[ciudad] = []
            city_groups[ciudad].append(edad)
        # Calcular promedios
        for ciudad in sorted(city_groups):
            edades = city_groups[ciudad]
            promedio = sum(edades) / len(edades) if edades else 0
            line = f"|{ciudad:>9}|{promedio:>13.1f}|"
            self.add_result(line, 'data')
        self.add_result("+---------+-------------+", 'data')
        self.add_result("", 'info')
    def show_age_filter_analysis(self, data):
        """Muestra análisis de filtro por edad mínima"""
        try:
            min_age = int(self.min_age_var.get()) if hasattr(self, 'min_age_var') else 0
        except Exception:
            min_age = 0
        filtered_data = [(n, e, c) for n, e, c in data if e > min_age]

        self.add_result(f"=== PERSONAS MAYORES DE {min_age} AÑOS ===", 'success')

        if filtered_data:
            self.add_result("+----------+----+-----------+", 'data')
            self.add_result("|    nombre|edad|     ciudad|", 'data')
            self.add_result("+----------+----+-----------+", 'data')
            for nombre, edad, ciudad in filtered_data:
                line = f"|{nombre:>10}|{edad:>4}|{ciudad:>11}|"
                self.add_result(line, 'data')
            self.add_result("+----------+----+-----------+", 'data')
            self.add_result(f"Total de personas: {len(filtered_data)}", 'success')
        else:
            self.add_result(f"No hay personas mayores de {min_age} años", 'warning')
        self.add_result("", 'info')
    def __init__(self, root):
        self.root = root
        self.root.title("Spark Personas Analyzer - Análisis de Datos")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Variables
        self.spark_session = None
        self.is_running = False
        self.current_dataframe = None
        
        # Datos predefinidos
        self.sample_data = [
            ("Ana", 23, "Toluca"),
            ("Luis", 31, "CDMX"),
            ("Carlos", 45, "Toluca"),
            ("María", 29, "Monterrey"),
            ("Pedro", 35, "CDMX"),
            ("Laura", 28, "Guadalajara"),
            ("Roberto", 42, "Monterrey"),
            ("Sofia", 26, "CDMX"),
            ("Diego", 39, "Toluca"),
            ("Carmen", 33, "Guadalajara")
        ]
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Centrar ventana
        self.center_window()
        
        # Cargar datos iniciales
        self.load_initial_data()
    
    def setup_styles(self):
        """Configura los estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema dark
        bg_primary = '#1e1e2e'
        bg_secondary = '#313244'
        accent = '#cba6f7'
        text_primary = '#cdd6f4'
        success = '#a6e3a1'
        warning = '#fab387'
        error = '#f38ba8'
        
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'),
                       foreground=text_primary,
                       background=bg_primary)
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#9399b2',
                       background=bg_primary)
        
        style.configure('Card.TFrame',
                       background=bg_secondary,
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Action.TButton',
                       font=('Segoe UI', 9, 'bold'))
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e2e', pady=15)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, 
                               text="👥 Spark Personas Analyzer",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Análisis avanzado de datos de personas con Apache Spark",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()
        
        # Main container con notebook (pestañas)
        main_frame = tk.Frame(self.root, bg='#1e1e2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Datos y Control
        self.create_data_tab()
        
        # Pestaña 2: Análisis
        self.create_analysis_tab()
        
        # Pestaña 3: Resultados
        self.create_results_tab()
    
    def create_data_tab(self):
        """Crea la pestaña de datos y control"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text='📊 Datos y Control')
        
        # Panel izquierdo - Configuración
        left_panel = ttk.Frame(data_frame, style='Card.TFrame', padding="20")
        left_panel.pack(side='left', fill='both', padx=(0, 10), expand=True)
        
        # Configuración Spark
        config_label = ttk.Label(left_panel, 
                                text="⚙️ Configuración Spark",
                                font=('Segoe UI', 12, 'bold'))
        config_label.pack(anchor='w', pady=(0, 15))
        
        # App name
        ttk.Label(left_panel, text="Nombre de la aplicación:").pack(anchor='w', pady=(0, 5))
        self.app_name_var = tk.StringVar(value="Ejemplo Spark Personas")
        ttk.Entry(left_panel, textvariable=self.app_name_var, width=40).pack(fill='x', pady=(0, 10))
        
        # Master URL
        ttk.Label(left_panel, text="Master URL:").pack(anchor='w', pady=(0, 5))
        self.master_var = tk.StringVar(value="local[*]")
        master_combo = ttk.Combobox(left_panel, textvariable=self.master_var, width=37)
        master_combo['values'] = ('local[*]', 'local[1]', 'local[2]', 'local[4]')
        master_combo.pack(fill='x', pady=(0, 15))
        
        # Gestión de datos
        data_label = ttk.Label(left_panel, 
                              text="📝 Gestión de Datos",
                              font=('Segoe UI', 12, 'bold'))
        data_label.pack(anchor='w', pady=(0, 15))
        
        # Botones para gestionar datos
        data_buttons_frame = ttk.Frame(left_panel)
        data_buttons_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Button(data_buttons_frame, text="📥 Cargar Datos Muestra",
                  command=self.load_sample_data).pack(side='left', padx=(0, 5))
        
        ttk.Button(data_buttons_frame, text="➕ Añadir Persona",
                  command=self.add_person_dialog).pack(side='left', padx=5)
        
        ttk.Button(data_buttons_frame, text="🗑 Limpiar Datos",
                  command=self.clear_data).pack(side='left', padx=5)
        
        # Estado
        status_frame = ttk.LabelFrame(left_panel, text="📡 Estado del Sistema", padding="10")
        status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_var = tk.StringVar(value="Sistema listo")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor='w')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var,
                                          maximum=100, length=300)
        self.progress_bar.pack(fill='x', pady=(10, 0))
        
        # Botones principales
        main_buttons_frame = ttk.Frame(left_panel)
        main_buttons_frame.pack(fill='x', pady=(0, 10))
        
        self.run_button = ttk.Button(main_buttons_frame, 
                                    text="🚀 Ejecutar Análisis Completo",
                                    command=self.run_complete_analysis,
                                    style='Action.TButton')
        self.run_button.pack(fill='x', pady=(0, 5))
        
        self.stop_button = ttk.Button(main_buttons_frame,
                                     text="⏹ Detener Análisis",
                                     command=self.stop_analysis,
                                     state='disabled')
        self.stop_button.pack(fill='x')
        
        # Panel derecho - Vista de datos
        right_panel = ttk.Frame(data_frame, style='Card.TFrame', padding="20")
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Tabla de datos
        table_label = ttk.Label(right_panel, 
                               text="👤 Datos de Personas",
                               font=('Segoe UI', 12, 'bold'))
        table_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para mostrar datos
        columns = ('nombre', 'edad', 'ciudad')
        self.data_tree = ttk.Treeview(right_panel, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.data_tree.heading(col, text=col.capitalize())
            self.data_tree.column(col, width=120, anchor='center')
        
        scrollbar_tree = ttk.Scrollbar(right_panel, orient='vertical', command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar_tree.set)
        
        self.data_tree.pack(side='left', fill='both', expand=True)
        scrollbar_tree.pack(side='right', fill='y')
    
    def create_analysis_tab(self):
        """Crea la pestaña de análisis"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text='🔍 Análisis')
        
        # Panel de filtros
        filters_panel = ttk.LabelFrame(analysis_frame, text="🔧 Filtros y Operaciones", padding="15")
        filters_panel.pack(fill='x', padx=20, pady=10)
        
        filters_grid = ttk.Frame(filters_panel)
        filters_grid.pack(fill='x')
        
        # Filtro por edad
        ttk.Label(filters_grid, text="Filtrar por edad mínima:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.min_age_var = tk.StringVar(value="30")
        ttk.Spinbox(filters_grid, from_=0, to=100, textvariable=self.min_age_var, width=10).grid(row=0, column=1, sticky='w')
        
        # Filtro por ciudad
        ttk.Label(filters_grid, text="Filtrar por ciudad:").grid(row=0, column=2, sticky='w', padx=(20, 10))
        self.city_filter_var = tk.StringVar(value="Todas")
        city_combo = ttk.Combobox(filters_grid, textvariable=self.city_filter_var, width=15)
        city_combo['values'] = ('Todas', 'Toluca', 'CDMX', 'Monterrey', 'Guadalajara')
        city_combo.grid(row=0, column=3, sticky='w')
        
        # Botones de análisis individual
        analysis_buttons_frame = ttk.Frame(analysis_frame)
        analysis_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(analysis_buttons_frame, text="👁 Mostrar DataFrame Original",
                  command=lambda: self.run_single_analysis('original')).pack(side='left', padx=(0, 5))
        
        ttk.Button(analysis_buttons_frame, text="🔍 Filtrar por Edad",
                  command=lambda: self.run_single_analysis('filter_age')).pack(side='left', padx=5)
        
        ttk.Button(analysis_buttons_frame, text="🏙 Agrupar por Ciudad",
                  command=lambda: self.run_single_analysis('group_city')).pack(side='left', padx=5)
        
        ttk.Button(analysis_buttons_frame, text="📊 Estadísticas Generales",
                  command=lambda: self.run_single_analysis('statistics')).pack(side='left', padx=5)
    
    def create_results_tab(self):
        """Crea la pestaña de resultados"""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text='📈 Resultados')
        
        # Panel superior - Métricas
        metrics_panel = ttk.LabelFrame(results_frame, text="📊 Métricas del Análisis", padding="15")
        metrics_panel.pack(fill='x', padx=20, pady=(10, 5))
        
        metrics_grid = ttk.Frame(metrics_panel)
        metrics_grid.pack()
        
        # Métricas
        metrics = [
            ("Total de registros:", "total_records", "0"),
            ("Edad promedio:", "avg_age", "0.0"),
            ("Ciudades únicas:", "unique_cities", "0"),
            ("Tiempo de ejecución:", "execution_time", "0.0s")
        ]
        
        self.metrics_vars = {}
        for i, (label, key, default) in enumerate(metrics):
            row, col = i // 2, (i % 2) * 2
            ttk.Label(metrics_grid, text=label).grid(row=row, column=col, sticky='w', padx=(0, 10))
            var = tk.StringVar(value=default)
            self.metrics_vars[key] = var
            ttk.Label(metrics_grid, textvariable=var, 
                     font=('Segoe UI', 10, 'bold'), 
                     foreground='#a6e3a1').grid(row=row, column=col+1, sticky='w', padx=(0, 30))
        
        # Panel de resultados
        results_panel = ttk.LabelFrame(results_frame, text="📋 Log de Resultados", padding="10")
        results_panel.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Área de texto para resultados
        self.results_text = scrolledtext.ScrolledText(results_panel,
                                                     height=25,
                                                     font=('Consolas', 9),
                                                     bg='#11111b',
                                                     fg='#cdd6f4',
                                                     insertbackground='white')
        self.results_text.pack(fill='both', expand=True)
        
        # Configurar tags para colores
        self.results_text.tag_config('info', foreground='#89b4fa')
        self.results_text.tag_config('success', foreground='#a6e3a1')
        self.results_text.tag_config('error', foreground='#f38ba8')
        self.results_text.tag_config('warning', foreground='#fab387')
        self.results_text.tag_config('header', foreground='#cba6f7', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('data', foreground='#f9e2af')
        
        # Botón para limpiar resultados
        ttk.Button(results_panel, text="🗑 Limpiar Resultados",
                  command=self.clear_results).pack(pady=(10, 0))
        
        # Mensaje inicial
        self.add_result("Sistema de análisis Spark inicializado correctamente", 'info')
        self.add_result("Carga algunos datos y ejecuta el análisis para comenzar", 'info')
    
    def load_initial_data(self):
        """Carga datos iniciales en la tabla"""
        for person in self.sample_data[:5]:  # Solo los primeros 5 inicialmente
            self.data_tree.insert('', 'end', values=person)
    
    def load_sample_data(self):
        """Carga todos los datos de muestra"""
        # Limpiar tabla actual
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Cargar todos los datos de muestra
        for person in self.sample_data:
            self.data_tree.insert('', 'end', values=person)
        
        self.add_result("Datos de muestra cargados correctamente", 'success')
        self.update_metrics()
    
    def add_person_dialog(self):
        """Abre diálogo para añadir una persona"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Añadir Persona")
        dialog.geometry("300x250")
        dialog.configure(bg='#1e1e2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg='#1e1e2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos
        ttk.Label(main_frame, text="Nombre:").pack(pady=(0, 5))
        name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=name_var, width=30).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Edad:").pack(pady=(0, 5))
        age_var = tk.StringVar()
        ttk.Spinbox(main_frame, from_=0, to=100, textvariable=age_var, width=28).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Ciudad:").pack(pady=(0, 5))
        city_var = tk.StringVar()
        city_combo = ttk.Combobox(main_frame, textvariable=city_var, width=27)
        city_combo['values'] = ('Toluca', 'CDMX', 'Monterrey', 'Guadalajara', 'Puebla', 'Tijuana')
        city_combo.pack(pady=(0, 15))
        
        def save_person():
            if name_var.get() and age_var.get() and city_var.get():
                try:
                    person = (name_var.get(), int(age_var.get()), city_var.get())
                    self.data_tree.insert('', 'end', values=person)
                    self.add_result(f"Persona añadida: {person}", 'success')
                    self.update_metrics()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "La edad debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        
        buttons_frame = tk.Frame(main_frame, bg='#1e1e2e')
        buttons_frame.pack(fill='x')
        
        ttk.Button(buttons_frame, text="Guardar", command=save_person).pack(side='left', padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancelar", command=dialog.destroy).pack(side='left')
    
    def clear_data(self):
        """Limpia todos los datos de la tabla"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        self.add_result("Datos limpiados", 'warning')
        self.update_metrics()
    
    def clear_results(self):
        """Limpia el área de resultados"""
        self.results_text.delete(1.0, tk.END)
        self.add_result("Resultados limpiados", 'info')
    
    def add_result(self, message, msg_type='info'):
        """Añade un mensaje al área de resultados"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.results_text.insert(tk.END, formatted_message, msg_type)
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_metrics(self):
        """Actualiza las métricas basadas en los datos actuales"""
        data = []
        for child in self.data_tree.get_children():
            values = self.data_tree.item(child)['values']
            if values:
                data.append(values)
        
        if data:
            total = len(data)
            ages = [int(row[1]) for row in data if row[1]]
            cities = set(row[2] for row in data if row[2])
            
            avg_age = sum(ages) / len(ages) if ages else 0
            
            self.metrics_vars['total_records'].set(str(total))
            self.metrics_vars['avg_age'].set(f"{avg_age:.1f}")
            self.metrics_vars['unique_cities'].set(str(len(cities)))
        else:
            for key in ['total_records', 'avg_age', 'unique_cities']:
                self.metrics_vars[key].set("0")
    
    def get_current_data(self):
        """Obtiene los datos actuales de la tabla"""
        data = []
        for child in self.data_tree.get_children():
            values = self.data_tree.item(child)['values']
            if values:
                # Convertir a tupla con tipos correctos
                data.append((str(values[0]), int(values[1]), str(values[2])))
        return data
    
    def simulate_spark_analysis(self, analysis_type='complete'):
        """Simula el análisis de Spark, seguro para hilos (solo usa after para la GUI)"""
        def run_steps():
            try:
                start_time = time.time()
                data = self.get_current_data()

                if not data:
                    self.add_result("No hay datos para analizar", 'error')
                    self.is_running = False
                    self.run_button.configure(state='normal')
                    self.stop_button.configure(state='disabled')
                    self.status_var.set("Análisis completado")
                    self.progress_var.set(0)
                    return

                app_name = self.app_name_var.get()
                master_url = self.master_var.get()

                # Simulación de inicialización de Spark
                self.add_result("=" * 60, 'header')
                self.add_result("INICIANDO ANÁLISIS SPARK DE PERSONAS", 'header')
                self.add_result("=" * 60, 'header')

                steps = [
                    (f"Iniciando SparkSession: {app_name}", 15),
                    (f"Configurando master: {master_url}", 25),
                    ("Creando DataFrame con datos de personas", 35),
                    ("DataFrame creado exitosamente", 45)
                ]

                def do_step(idx):
                    if not self.is_running or idx >= len(steps):
                        finish()
                        return
                    step, progress = steps[idx]
                    self.add_result(step, 'info')
                    self.progress_var.set(progress)
                    self.root.after(300, lambda: do_step(idx + 1))

                def finish():
                    if analysis_type == 'original':
                        self.show_original_dataframe(data)
                        self.add_result("Cerrando sesión Spark...", 'info')
                        self.progress_var.set(100)
                        end_time = time.time()
                        execution_time = round(end_time - start_time, 2)
                        self.metrics_vars['execution_time'].set(f"{execution_time}s")
                        self.add_result(f"Análisis completado en {execution_time} segundos", 'success')
                        self.add_result("=" * 60, 'header')
                        self.is_running = False
                        self.run_button.configure(state='normal')
                        self.stop_button.configure(state='disabled')
                        self.status_var.set("Análisis completado")
                        self.root.after(1000, lambda: self.progress_var.set(0))
                        return
                    # Mostrar siempre en este orden para el análisis completo
                    if analysis_type == 'complete':
                        self.show_original_dataframe(data)
                        self.show_age_filter_analysis(data)
                        self.show_city_grouping_analysis(data)
                        self.show_statistics_analysis(data)
                        self.progress_var.set(100)
                        self.root.after(500, end_analysis)
                        return
                    if analysis_type == 'filter_age':
                        self.show_age_filter_analysis(data)
                        self.add_result("Cerrando sesión Spark...", 'info')
                        self.progress_var.set(100)
                        end_time = time.time()
                        execution_time = round(end_time - start_time, 2)
                        self.metrics_vars['execution_time'].set(f"{execution_time}s")
                        self.add_result(f"Análisis completado en {execution_time} segundos", 'success')
                        self.add_result("=" * 60, 'header')
                        self.is_running = False
                        self.run_button.configure(state='normal')
                        self.stop_button.configure(state='disabled')
                        self.status_var.set("Análisis completado")
                        self.root.after(1000, lambda: self.progress_var.set(0))
                        return
                    if analysis_type == 'group_city':
                        self.show_city_grouping_analysis(data)
                        self.add_result("Cerrando sesión Spark...", 'info')
                        self.progress_var.set(100)
                        end_time = time.time()
                        execution_time = round(end_time - start_time, 2)
                        self.metrics_vars['execution_time'].set(f"{execution_time}s")
                        self.add_result(f"Análisis completado en {execution_time} segundos", 'success')
                        self.add_result("=" * 60, 'header')
                        self.is_running = False
                        self.run_button.configure(state='normal')
                        self.stop_button.configure(state='disabled')
                        self.status_var.set("Análisis completado")
                        self.root.after(1000, lambda: self.progress_var.set(0))
                        return
                    if analysis_type == 'statistics':
                        self.show_statistics_analysis(data)
                        self.add_result("Cerrando sesión Spark...", 'info')
                        self.progress_var.set(100)
                        end_time = time.time()
                        execution_time = round(end_time - start_time, 2)
                        self.metrics_vars['execution_time'].set(f"{execution_time}s")
                        self.add_result(f"Análisis completado en {execution_time} segundos", 'success')
                        self.add_result("=" * 60, 'header')
                        self.is_running = False
                        self.run_button.configure(state='normal')
                        self.stop_button.configure(state='disabled')
                        self.status_var.set("Análisis completado")
                        self.root.after(1000, lambda: self.progress_var.set(0))
                        return

                def end_analysis():
                    self.add_result("Cerrando sesión Spark...", 'info')
                    self.progress_var.set(100)
                    end_time = time.time()
                    execution_time = round(end_time - start_time, 2)
                    self.metrics_vars['execution_time'].set(f"{execution_time}s")
                    self.add_result(f"Análisis completado en {execution_time} segundos", 'success')
                    self.add_result("=" * 60, 'header')
                    self.is_running = False
                    self.run_button.configure(state='normal')
                    self.stop_button.configure(state='disabled')
                    self.status_var.set("Análisis completado")
                    self.root.after(1000, lambda: self.progress_var.set(0))

                do_step(0)

            except Exception as e:
                self.add_result(f"Error durante el análisis: {str(e)}", 'error')
                self.is_running = False
                self.run_button.configure(state='normal')
                self.stop_button.configure(state='disabled')
                self.status_var.set("Análisis completado")
                self.root.after(1000, lambda: self.progress_var.set(0))

        self.root.after(0, run_steps)
    
    def show_original_dataframe(self, data):
        """Muestra el DataFrame original en formato tabla"""
        self.add_result("=== DataFrame Original ===", 'success')
        self.add_result("+------+----+---------+", 'data')
        self.add_result("|nombre|edad|   ciudad|", 'data')
        self.add_result("+------+----+---------+", 'data')
        for nombre, edad, ciudad in data:
            line = f"|{nombre:>6}|{edad:>4}|{ciudad:>9}|"
            self.add_result(line, 'data')
        self.add_result("+------+----+---------+", 'data')
        self.add_result("", 'info')
    
    def run_single_analysis(self, analysis_type):
        """Ejecuta un análisis específico"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "Ya hay un análisis ejecutándose")
            return
        
        data = self.get_current_data()
        if not data:
            messagebox.showerror("Error", "No hay datos para analizar. Carga algunos datos primero.")
            return
        
        self.is_running = True
        self.status_var.set(f"Ejecutando análisis: {analysis_type}")
        
        # Cambiar a la pestaña de resultados
        self.notebook.select(2)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.simulate_spark_analysis, args=(analysis_type,))
        thread.daemon = True
        thread.start()
    
    def run_complete_analysis(self):
        """Ejecuta el análisis completo de Spark"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "Ya hay un análisis ejecutándose")
            return
        
        data = self.get_current_data()
        if not data:
            messagebox.showerror("Error", "No hay datos para analizar. Carga algunos datos primero.")
            return
        
        self.is_running = True
        self.run_button.configure(state='disabled')
        self.stop_button.configure(state='disabled')  # Se habilitará después de un momento
        self.status_var.set("Ejecutando análisis completo...")
        
        # Habilitar botón de detener después de un momento
        self.root.after(1000, lambda: self.stop_button.configure(state='normal'))
        
        # Cambiar a la pestaña de resultados
        self.notebook.select(2)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.simulate_spark_analysis, args=('complete',))
        thread.daemon = True
        thread.start()
    
    def stop_analysis(self):
        """Detiene el análisis en ejecución"""
        self.is_running = False
        self.add_result("Análisis detenido por el usuario", 'warning')
        self.status_var.set("Análisis detenido")
        self.run_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.progress_var.set(0)


# Funciones para integración con Spark real
def run_real_spark_personas_analysis():
    """
    Función que ejecuta el análisis real con Spark
    Descomenta y modifica este código cuando tengas PySpark instalado
    """
    try:
        # Descomenta las siguientes líneas para usar Spark real:
        # from pyspark.sql import SparkSession
        # from pyspark.sql.functions import col, avg, sum as spark_sum, count
        # spark = SparkSession.builder \
        #     .appName("Ejemplo Spark Personas") \
        #     .master("local[*]") \
        #     .getOrCreate()
        # data = [
        #     ("Ana", 23, "Toluca"),
        #     ("Luis", 31, "CDMX"),
        #     ("Carlos", 45, "Toluca"),
        #     ("María", 29, "Monterrey"),
        #     ("Pedro", 35, "CDMX")
        # ]
        # columnas = ["nombre", "edad", "ciudad"]
        # df = spark.createDataFrame(data, columnas)
        # print("=== DataFrame Original ===")
        # df.show()
        # print("=== Personas mayores de 30 años ===")
        # df.filter(col("edad") > 30).show()
        # print("=== Edad promedio por ciudad ===")
        # df.groupBy("ciudad").agg(avg("edad").alias("edad_promedio")).show()
        # spark.stop()
        return True, "Análisis Spark ejecutado correctamente"
    except Exception as e:
        return False, f"Error en el análisis Spark: {str(e)}"


class RealSparkIntegration:
    """
    Clase para integrar Spark real con la GUI
    Descomenta y modifica según tus necesidades
    """
    
    def __init__(self):
        self.spark = None
    
    def initialize_spark(self, app_name, master_url):
        """Inicializa una sesión Spark real"""
        try:
            # from pyspark.sql import SparkSession
            # self.spark = SparkSession.builder \
            #     .appName(app_name) \
            #     .master(master_url) \
            #     .getOrCreate()
            return True, "Spark inicializado correctamente"
        except Exception as e:
            return False, f"Error al inicializar Spark: {str(e)}"
    
    def create_dataframe(self, data, columns):
        """Crea un DataFrame de Spark"""
        try:
            if self.spark is None:
                raise Exception("Spark no está inicializado")
            
            # df = self.spark.createDataFrame(data, columns)
            # return df
            pass
        except Exception as e:
            raise Exception(f"Error al crear DataFrame: {str(e)}")
    
    def close_spark(self):
        """Cierra la sesión Spark"""
        try:
            if self.spark:
                # self.spark.stop()
                self.spark = None
            return True, "Sesión Spark cerrada"
        except Exception as e:
            return False, f"Error al cerrar Spark: {str(e)}"


def main():
    """Función principal para ejecutar la aplicación"""
    # Configurar tkinter para mejor apariencia en Windows
    try:
        from tkinter import ttk
        import tkinter as tk
        tk.Tk().withdraw()  # Crear y ocultar ventana temporal para inicialización
    except Exception:
        pass
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Configurar el ícono de la ventana (opcional)
    try:
        # Si tienes un archivo .ico, descomenta la siguiente línea:
        # root.iconbitmap('spark_icon.ico')
        pass
    except Exception:
        pass
    
    # Crear y ejecutar la aplicación
    app = SparkPersonasGUI(root)
    
    # Mensaje de bienvenida en consola
    print("🚀 Spark Personas Analyzer - Interfaz Gráfica Completa")
    print("=" * 60)
    print("✅ Aplicación iniciada correctamente")
    print("📊 Datos de muestra precargados")
    print("🔧 Para usar Spark real, descomenta las líneas correspondientes")
    print("📚 Revisa las pestañas: Datos y Control | Análisis | Resultados")
    print("=" * 60)
    
    # Ejecutar el loop principal de tkinter
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error en la aplicación: {e}")
        messagebox.showerror("Error Fatal", f"Error inesperado: {e}")


# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    main()

