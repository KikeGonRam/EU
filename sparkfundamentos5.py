import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class IMCAppHorizontalMejorada:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de IMC Avanzada")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f8fafc")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores
        self.colors = {
            'primary': '#3b82f6',
            'secondary': '#60a5fa',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'light': '#f1f5f9',
            'dark': '#1e293b',
            'background': '#f8fafc',
            'accent': '#8b5cf6',
            'text_light': '#64748b',
            'text_dark': '#1e293b'
        }
        
        # Configurar fuentes
        self.title_font = ("Segoe UI", 20, "bold")
        self.subtitle_font = ("Segoe UI", 12)
        self.label_font = ("Segoe UI", 11, "bold")
        self.button_font = ("Segoe UI", 12, "bold")
        self.result_font = ("Segoe UI", 16, "bold")
        self.interpretation_font = ("Segoe UI", 11)
        
        # Crear paneles principales
        self.create_left_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        # Panel izquierdo para entrada de datos
        self.left_frame = tk.Frame(self.root, bg=self.colors['light'], 
                                  relief=tk.RAISED, bd=1, padx=30, pady=30)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        tk.Label(self.left_frame, text="Calculadora de IMC", 
                font=self.title_font, bg=self.colors['light'], 
                fg=self.colors['dark']).pack(pady=(0, 10))
        
        # Subtítulo
        tk.Label(self.left_frame, text="Ingresa tus datos para calcular tu Índice de Masa Corporal", 
                font=self.subtitle_font, bg=self.colors['light'], 
                fg=self.colors['text_light']).pack(pady=(0, 30))
        
        # Entrada de peso
        weight_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        weight_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(weight_frame, text="Peso (kg):", font=self.label_font, 
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        self.entry_peso = ttk.Entry(weight_frame, font=("Segoe UI", 12))
        self.entry_peso.pack(fill=tk.X, pady=(10, 0), ipady=8)
        
        # Entrada de altura
        height_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        height_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(height_frame, text="Altura (m):", font=self.label_font, 
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        self.entry_altura = ttk.Entry(height_frame, font=("Segoe UI", 12))
        self.entry_altura.pack(fill=tk.X, pady=(10, 0), ipady=8)
        
        # Botón calcular
        button_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        self.calc_button = tk.Button(button_frame, text="Calcular IMC", 
                                    font=self.button_font, bg=self.colors['primary'], 
                                    fg="white", relief=tk.FLAT, cursor="hand2",
                                    command=self.calcular_imc)
        self.calc_button.pack(fill=tk.X, ipady=12)
        
        # Efecto hover para el botón
        self.calc_button.bind("<Enter>", lambda e: self.calc_button.config(bg=self.colors['secondary']))
        self.calc_button.bind("<Leave>", lambda e: self.calc_button.config(bg=self.colors['primary']))
        
        # Resultado
        result_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        result_frame.pack(fill=tk.X, pady=(30, 0))
        
        self.label_resultado = tk.Label(result_frame, text="Ingresa tus datos para calcular tu IMC", 
                                      font=self.result_font, bg=self.colors['light'], 
                                      fg=self.colors['text_light'])
        self.label_resultado.pack()
        
        self.label_categoria = tk.Label(result_frame, text="", 
                                      font=("Segoe UI", 12), bg=self.colors['light'], 
                                      fg=self.colors['text_light'])
        self.label_categoria.pack(pady=(5, 0))
        
        # Interpretación
        interpretation_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        interpretation_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(interpretation_frame, text="Interpretación:", 
                font=self.label_font, bg=self.colors['light'], 
                fg=self.colors['dark']).pack(anchor=tk.W, pady=(0, 5))
        
        self.label_interpretacion = tk.Label(interpretation_frame, text="", 
                                           font=self.interpretation_font, bg=self.colors['light'], 
                                           fg=self.colors['text_light'], wraplength=400, justify=tk.LEFT)
        self.label_interpretacion.pack(anchor=tk.W)
        
        # Información adicional
        info_frame = tk.Frame(self.left_frame, bg=self.colors['light'])
        info_frame.pack(fill=tk.X, pady=(30, 0))
        
        info_text = """• IMC < 18.5: Bajo peso
• IMC 18.5-24.9: Peso normal
• IMC 25-29.9: Sobrepeso
• IMC ≥ 30: Obesidad"""
        
        tk.Label(info_frame, text=info_text, font=("Segoe UI", 10), 
                bg=self.colors['light'], fg=self.colors['text_light'], justify=tk.LEFT).pack(anchor=tk.W)
    
    def create_right_panel(self):
        # Panel derecho para la gráfica
        self.right_frame = tk.Frame(self.root, bg=self.colors['light'], 
                                   relief=tk.RAISED, bd=1)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del panel derecho
        tk.Label(self.right_frame, text="Clasificación del IMC", 
                font=self.title_font, bg=self.colors['light'], 
                fg=self.colors['dark']).pack(pady=20)
        
        # Frame para la gráfica
        graph_frame = tk.Frame(self.right_frame, bg=self.colors['light'])
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor=self.colors['light'])
        self.ax = self.fig.add_subplot(111)
        
        # Configurar la gráfica inicial
        self.setup_chart()
        
        # Canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_chart(self):
        """Configura la gráfica inicial"""
        self.ax.clear()
        
        # Definir categorías y colores
        categories = ["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]
        colors = [self.colors['warning'], self.colors['success'], self.colors['warning'], self.colors['danger']]
        ranges = [(0, 18.5), (18.5, 25), (25, 30), (30, 40)]
        
        # Crear gráfica de barras para las categorías
        for i, (cat, color, rng) in enumerate(zip(categories, colors, ranges)):
            self.ax.barh(cat, width=rng[1]-rng[0], left=rng[0], color=color, alpha=0.7, edgecolor='white')
            mid = (rng[0] + rng[1]) / 2
            self.ax.text(mid, i, cat, ha='center', va='center', fontweight='bold')
        
        self.ax.set_xlabel('Índice de Masa Corporal (IMC)', fontweight='bold')
        self.ax.set_title('Categorías de IMC según la OMS', fontweight='bold')
        self.ax.set_xlim(0, 40)
        self.ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        self.fig.tight_layout()
    
    def calcular_imc(self):
        try:
            peso = float(self.entry_peso.get().replace(',', '.'))
            altura = float(self.entry_altura.get().replace(',', '.'))
            
            if peso <= 0 or altura <= 0:
                raise ValueError("Valores inválidos")
            
            imc = peso / (altura ** 2)
            
            # Determinar categoría e interpretación
            if imc < 18.5:
                categoria = "Bajo peso"
                color = self.colors['warning']
                interpretacion = "Tu peso está por debajo de lo recomendado. Considera consultar a un especialista en nutrición para ganar masa de forma saludable."
            elif 18.5 <= imc < 25:
                categoria = "Normal"
                color = self.colors['success']
                interpretacion = "¡Felicidades! Estás en un rango saludable. Mantén un estilo de vida equilibrado para conservar tu peso ideal."
            elif 25 <= imc < 30:
                categoria = "Sobrepeso"
                color = self.colors['warning']
                interpretacion = "Tienes un ligero exceso de peso. Se recomienda mejorar la alimentación y aumentar la actividad física."
            else:
                categoria = "Obesidad"
                color = self.colors['danger']
                interpretacion = "Tu IMC indica obesidad. Es importante acudir a un médico o nutriólogo para diseñar un plan de salud adecuado."
            
            # Actualizar etiquetas de resultado
            self.label_resultado.config(text=f"Tu IMC: {imc:.2f}", fg=color)
            self.label_categoria.config(text=f"Categoría: {categoria}", fg=color)
            self.label_interpretacion.config(text=interpretacion, fg=self.colors['text_dark'])
            
            # Actualizar gráfica
            self.update_chart(imc, categoria, color)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos para peso y altura.")
    
    def update_chart(self, imc, categoria, color):
        """Actualiza la gráfica con el IMC del usuario"""
        self.ax.clear()
        
        # Definir categorías y colores
        categories = ["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]
        colors = [self.colors['warning'], self.colors['success'], self.colors['warning'], self.colors['danger']]
        ranges = [(0, 18.5), (18.5, 25), (25, 30), (30, 40)]
        
        # Crear gráfica de barras para las categorías
        for i, (cat, clr, rng) in enumerate(zip(categories, colors, ranges)):
            self.ax.barh(cat, width=rng[1]-rng[0], left=rng[0], color=clr, alpha=0.7, edgecolor='white')
            mid = (rng[0] + rng[1]) / 2
            self.ax.text(mid, i, cat, ha='center', va='center', fontweight='bold')
        
        # Añadir línea para el IMC del usuario
        self.ax.axvline(x=imc, color='black', linestyle='-', linewidth=3, label=f'Tu IMC: {imc:.1f}')
        
        # Añadir marcador circular en la línea
        y_pos = categories.index(categoria) if categoria in categories else 0
        self.ax.plot(imc, y_pos, 'o', markersize=10, color='black', markeredgecolor='white', markeredgewidth=2)
        
        # Añadir texto con el valor del IMC
        self.ax.text(imc + 1, y_pos, f'{imc:.1f}', fontsize=12, fontweight='bold', 
                    verticalalignment='center', color=color)
        
        self.ax.set_xlabel('Índice de Masa Corporal (IMC)', fontweight='bold')
        self.ax.set_title('Categorías de IMC según la OMS', fontweight='bold')
        self.ax.set_xlim(0, 40)
        self.ax.legend(loc='lower right')
        self.ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        self.fig.tight_layout()
        self.canvas.draw()

# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = IMCAppHorizontalMejorada(root)
    root.mainloop()