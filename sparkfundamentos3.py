import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np

class FuturisticIMCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Analizador IMC Futurista")
        self.root.geometry("900x750")
        self.root.configure(bg="#0a1622")
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Configurar estilo futurista
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configurar colores futuristas
        self.colors = {
            'primary': '#00d4ff',
            'secondary': '#0099ff',
            'accent': '#ff00cc',
            'dark_bg': '#0a0e17',
            'dark_panel': '#131a2a',
            'light_text': '#ffffff',
            'medium_text': '#8b9bb4',
            'success': '#00ff9d',
            'warning': '#ffcc00',
            'danger': '#ff3860',
            'grid': '#1e2a3f'
        }

        # Configurar fuentes futuristas
        self.title_font = ("Montserrat", 22, "bold")
        self.subtitle_font = ("Montserrat", 12)
        self.label_font = ("Montserrat", 11, "bold")
        self.button_font = ("Montserrat", 12, "bold")
        self.result_font = ("Montserrat", 16, "bold")
        self.digital_font = ("Courier New", 14, "bold")

        # Crear efecto de gradiente
        self.create_gradient_bg()
        self.create_widgets()
        
    def create_gradient_bg(self):
        # Crear un canvas para el fondo con gradiente
        self.bg_canvas = tk.Canvas(self.root, width=900, height=750, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Dibujar gradiente radial
        center_x, center_y = 450, 375
        max_radius = 600
        
        for r in range(max_radius, 0, -5):
            alpha = 1 - (r / max_radius)
            color = self.interpolate_color("#050a15", "#0f1a2f", alpha)
            self.bg_canvas.create_oval(center_x - r, center_y - r, 
                                      center_x + r, center_y + r, 
                                      fill=color, outline="")
        
        # Añadir partículas de fondo
        for _ in range(50):
            x = np.random.randint(0, 900)
            y = np.random.randint(0, 750)
            size = np.random.randint(1, 3)
            self.bg_canvas.create_oval(x, y, x + size, y + size, 
                                      fill=self.colors['primary'], outline="")
    
    def interpolate_color(self, color1, color2, alpha):
        # Convertir colores hex a RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolar
        r = int(r1 + (r2 - r1) * alpha)
        g = int(g1 + (g2 - g1) * alpha)
        b = int(b1 + (b2 - b1) * alpha)
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def create_widgets(self):
        # Frame principal con transparencia
        main_frame = tk.Frame(self.bg_canvas, bg='white', bd=0)
        self.bg_canvas.create_window(450, 375, window=main_frame, width=850, height=700)
        
        # Título con efecto neón
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill=tk.X, pady=(20, 10))
        tk.Label(title_frame, text="🚀 Analizador Cuántico de IMC", 
                 font=self.title_font, bg='white', 
                 fg=self.colors['primary']).pack()
        tk.Label(title_frame, text="Sistema avanzado para calcular tu Índice de Masa Corporal", 
                 font=self.subtitle_font, bg='white', 
                 fg=self.colors['medium_text']).pack(pady=(5, 0))
        
        # Separador futurista
        separator = tk.Frame(main_frame, height=2, bg=self.colors['grid'])
        separator.pack(fill=tk.X, padx=50, pady=10)
        
        # Frame de entrada de datos con efecto de vidrio
        input_frame = tk.Frame(main_frame, bg=self.colors['dark_panel'], 
                              relief=tk.FLAT, bd=0, padx=30, pady=25)
        input_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        # Añadir borde sutil
        self.create_glow_border(input_frame, self.colors['primary'])
        
        # Entrada de peso
        weight_frame = tk.Frame(input_frame, bg=self.colors['dark_panel'])
        weight_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(weight_frame, text="Peso (kg):", font=self.label_font, 
                 bg=self.colors['dark_panel'], fg=self.colors['medium_text']).pack(anchor=tk.W)
        
        self.entry_peso = self.create_futuristic_entry(weight_frame)
        self.entry_peso.pack(fill=tk.X, pady=(10, 0), ipady=12)
        
        # Entrada de altura
        height_frame = tk.Frame(input_frame, bg=self.colors['dark_panel'])
        height_frame.pack(fill=tk.X, pady=15)
        tk.Label(height_frame, text="Estatura (m):", font=self.label_font, 
                 bg=self.colors['dark_panel'], fg=self.colors['medium_text']).pack(anchor=tk.W)
        self.entry_altura = self.create_futuristic_entry(height_frame)
        self.entry_altura.pack(fill=tk.X, pady=(10, 0), ipady=12)
        
        # Botón calcular con efecto futurista
        button_frame = tk.Frame(input_frame, bg=self.colors['dark_panel'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.calc_button = tk.Button(button_frame, text="Calcular IMC", 
                                     font=self.button_font, bg=self.colors['primary'], 
                                     fg="#0a0e17", relief=tk.FLAT, cursor="hand2",
                                     command=self.calcular_imc, bd=0,
                                     activebackground=self.colors['secondary'],
                                     activeforeground="#0a0e17")
        self.calc_button.pack(fill=tk.X, ipady=15)
        
        # Efecto hover para el botón
        self.calc_button.bind("<Enter>", lambda e: self.calc_button.config(bg=self.colors['secondary']))
        self.calc_button.bind("<Leave>", lambda e: self.calc_button.config(bg=self.colors['primary']))
        
        # Frame de resultados
        result_frame = tk.Frame(main_frame, bg=self.colors['dark_panel'], 
                               relief=tk.FLAT, bd=0, padx=20, pady=20)
        result_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        self.create_glow_border(result_frame, self.colors['primary'])
        
        self.label_resultado = tk.Label(result_frame, text="Esperando datos...", 
                                        font=self.digital_font, bg=self.colors['dark_panel'], 
                                        fg=self.colors['medium_text'])
        self.label_resultado.pack()
        self.label_categoria = tk.Label(result_frame, text="Ingresa tu peso y estatura", 
                                        font=("Montserrat", 12), bg=self.colors['dark_panel'], 
                                        fg=self.colors['medium_text'])
        self.label_categoria.pack(pady=(5, 0))
        
        # Frame para la gráfica
        graph_frame = tk.Frame(main_frame, bg=self.colors['dark_panel'], 
                              relief=tk.FLAT, bd=0)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.create_glow_border(graph_frame, self.colors['primary'])
        
        # Crear figura de matplotlib con estilo futurista
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor=self.colors['dark_panel'])
        self.ax = self.fig.add_subplot(111)
        
        # Configurar la gráfica inicial
        self.setup_chart()
        
        # Canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    # Información adicional
    # graph_frame ya está usando pack, no usar grid aquí
    
    def create_glow_border(self, widget, color):
        # Crear un efecto de borde con brillo
        border_frame = tk.Frame(widget.master, bg=color)
        border_frame.place(in_=widget, x=-1, y=-1, relwidth=1, relheight=1, width=2, height=2)
        widget.lift()
    
    def create_futuristic_entry(self, parent):
        # Crear un Entry directamente en el frame padre, sin frame intermedio
        entry = tk.Entry(parent, font=("Montserrat", 12), 
                        bg='white', fg='black',
                        insertbackground=self.colors['primary'], relief=tk.FLAT, bd=1, highlightthickness=1, highlightbackground=self.colors['primary'])
        return entry
    
    def setup_chart(self):
        """Configura la gráfica inicial con estilo futurista"""
        self.ax.clear()
        # Definir categorías y colores
        categorias = ["Bajo peso", "Saludable", "Sobrepeso", "Obesidad"]
        colores = [self.colors['warning'], self.colors['success'], self.colors['warning'], self.colors['danger']]
        rangos = [(0, 18.5), (18.5, 25), (25, 30), (30, 40)]
        # Crear gráfica de barras para las categorías
        for i, (cat, color, rng) in enumerate(zip(categorias, colores, rangos)):
            self.ax.barh(cat, width=rng[1]-rng[0], left=rng[0], color=color, alpha=0.8, 
                        edgecolor='white', linewidth=0.5)
            mid = (rng[0] + rng[1]) / 2
            self.ax.text(mid, i, cat, ha='center', va='center', fontweight='bold', 
                        color=self.colors['light_text'], fontsize=8)  # texto más pequeño
        self.ax.set_xlabel('ÍNDICE DE MASA CORPORAL (IMC)', fontweight='bold', 
                          color=self.colors['light_text'], fontsize=9)  # texto más pequeño
        self.ax.set_title('ANÁLISIS CUÁNTICO DE IMC', fontweight='bold', 
                         color=self.colors['primary'], fontsize=11)  # texto más pequeño
        self.ax.set_xlim(0, 40)
        self.ax.grid(axis='x', linestyle='--', alpha=0.3, color=self.colors['grid'])
        # Estilo futurista para los ejes
        self.ax.spines['bottom'].set_color(self.colors['primary'])
        self.ax.spines['top'].set_color(self.colors['primary']) 
        self.ax.spines['right'].set_color(self.colors['primary'])
        self.ax.spines['left'].set_color(self.colors['primary'])
        self.ax.tick_params(axis='x', colors=self.colors['light_text'])
        self.ax.tick_params(axis='y', colors=self.colors['light_text'])
        self.ax.set_facecolor(self.colors['dark_panel'])
        # Ajustar márgenes manualmente para evitar advertencia
        self.fig.subplots_adjust(top=0.88, bottom=0.18, left=0.13, right=0.97)
    
    def calcular_imc(self):
        try:
            peso = float(self.entry_peso.get().replace(',', '.'))
            altura = float(self.entry_altura.get().replace(',', '.'))
            
            if peso <= 0 or altura <= 0:
                raise ValueError("Valores inválidos")
            
            imc = peso / (altura ** 2)
            
            if imc < 18.5:
                categoria = "Bajo peso"
                color = self.colors['warning']
            elif 18.5 <= imc < 25:
                categoria = "Saludable"
                color = self.colors['success']
            elif 25 <= imc < 30:
                categoria = "Sobrepeso"
                color = self.colors['warning']
            else:
                categoria = "Obesidad"
                color = self.colors['danger']
            # Actualizar etiquetas de resultado
            self.label_resultado.config(text=f"IMC: {imc:.2f}", fg=color)
            self.label_categoria.config(text=f"Categoría: {categoria}", fg=color)
            # Actualizar gráfica
            self.update_chart(imc, categoria, color)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
    
    def update_chart(self, imc, categoria, color):
        """Actualiza la gráfica con el IMC del usuario"""
        self.ax.clear()
        # Definir categorías y colores
        categorias = ["Bajo peso", "Saludable", "Sobrepeso", "Obesidad"]
        colores = [self.colors['warning'], self.colors['success'], self.colors['warning'], self.colors['danger']]
        rangos = [(0, 18.5), (18.5, 25), (25, 30), (30, 40)]
        # Crear gráfica de barras para las categorías
        for i, (cat, clr, rng) in enumerate(zip(categorias, colores, rangos)):
            self.ax.barh(cat, width=rng[1]-rng[0], left=rng[0], color=clr, alpha=0.8, 
                        edgecolor='white', linewidth=0.5)
            mid = (rng[0] + rng[1]) / 2
            self.ax.text(mid, i, cat, ha='center', va='center', fontweight='bold', 
                        color=self.colors['light_text'], fontsize=8)  # texto más pequeño
        # Añadir línea para el IMC del usuario con efecto brillante
        self.ax.axvline(x=imc, color=color, linestyle='-', linewidth=3, alpha=0.9, 
                       label=f'Tu IMC: {imc:.1f}')
        # Añadir marcador circular futurista
        y_pos = categorias.index(categoria) if categoria in categorias else 0
        self.ax.plot(imc, y_pos, 'o', markersize=12, color=color, 
                   markeredgecolor='white', markeredgewidth=2, alpha=0.9)
        # Añadir efecto de brillo al marcador
        self.ax.plot(imc, y_pos, 'o', markersize=16, color=color, alpha=0.2)
        self.ax.set_xlabel('ÍNDICE DE MASA CORPORAL (IMC)', fontweight='bold', 
                          color=self.colors['light_text'], fontsize=9)  # texto más pequeño
        self.ax.set_title('ANÁLISIS CUÁNTICO DE IMC', fontweight='bold', 
                         color=self.colors['primary'], fontsize=11)  # texto más pequeño
        self.ax.set_xlim(0, 40)
        self.ax.legend(loc='lower right', facecolor=self.colors['dark_panel'], 
                      edgecolor=self.colors['primary'], labelcolor=self.colors['light_text'])
        self.ax.grid(axis='x', linestyle='--', alpha=0.3, color=self.colors['grid'])
        # Estilo futurista para los ejes
        self.ax.spines['bottom'].set_color(self.colors['primary'])
        self.ax.spines['top'].set_color(self.colors['primary']) 
        self.ax.spines['right'].set_color(self.colors['primary'])
        self.ax.spines['left'].set_color(self.colors['primary'])
        self.ax.tick_params(axis='x', colors=self.colors['light_text'])
        self.ax.tick_params(axis='y', colors=self.colors['light_text'])
        self.ax.set_facecolor(self.colors['dark_panel'])
        # Ajustar márgenes manualmente para evitar advertencia
        self.fig.subplots_adjust(top=0.88, bottom=0.18, left=0.13, right=0.97)
        self.canvas.draw()

# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticIMCApp(root)
    root.mainloop()