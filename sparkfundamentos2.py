import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class IMCAppConGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("💪 Calculadora de IMC Avanzada")
        self.root.geometry("800x700")
        self.root.configure(bg="#f8fafc")
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores
        self.colors = {
            'primary': '#6366f1',
            'secondary': '#818cf8',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'light': '#f1f5f9',
            'dark': '#1e293b',
            'background': '#f8fafc'
        }
        
        # Configurar fuentes
        self.title_font = ("Segoe UI", 20, "bold")
        self.subtitle_font = ("Segoe UI", 12)
        self.label_font = ("Segoe UI", 11, "bold")
        self.button_font = ("Segoe UI", 12, "bold")
        self.result_font = ("Segoe UI", 14, "bold")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="💪 Calculadora de IMC Avanzada", 
                font=self.title_font, bg=self.colors['background'], 
                fg=self.colors['dark']).pack()
        
        tk.Label(title_frame, text="Calcula tu Índice de Masa Corporal y visualiza tu categoría", 
                font=self.subtitle_font, bg=self.colors['background'], 
                fg="#64748b").pack(pady=(5, 0))
        
        # Frame de entrada de datos
        input_frame = tk.Frame(main_frame, bg=self.colors['light'], 
                              relief=tk.RAISED, bd=1, padx=20, pady=20)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Entrada de peso
        weight_frame = tk.Frame(input_frame, bg=self.colors['light'])
        weight_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(weight_frame, text="Peso (kg):", font=self.label_font, 
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        self.entry_peso = ttk.Entry(weight_frame, font=("Segoe UI", 12), width=15)
        self.entry_peso.pack(fill=tk.X, pady=(5, 0))
        
        # Entrada de altura
        height_frame = tk.Frame(input_frame, bg=self.colors['light'])
        height_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(height_frame, text="Altura (m):", font=self.label_font, 
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        self.entry_altura = ttk.Entry(height_frame, font=("Segoe UI", 12), width=15)
        self.entry_altura.pack(fill=tk.X, pady=(5, 0))
        
        # Botón calcular
        button_frame = tk.Frame(input_frame, bg=self.colors['light'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.calc_button = tk.Button(button_frame, text="📊 Calcular IMC", 
                                    font=self.button_font, bg=self.colors['primary'], 
                                    fg="white", relief=tk.FLAT, cursor="hand2",
                                    command=self.calcular_imc)
        self.calc_button.pack(fill=tk.X, ipady=10)
        
        # Efecto hover para el botón
        self.calc_button.bind("<Enter>", lambda e: self.calc_button.config(bg=self.colors['secondary']))
        self.calc_button.bind("<Leave>", lambda e: self.calc_button.config(bg=self.colors['primary']))
        
        # Frame de resultados
        result_frame = tk.Frame(main_frame, bg=self.colors['light'], 
                               relief=tk.RAISED, bd=1, padx=20, pady=20)
        result_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.label_resultado = tk.Label(result_frame, text="Ingresa tus datos para calcular tu IMC", 
                                      font=self.result_font, bg=self.colors['light'], 
                                      fg=self.colors['dark'])
        self.label_resultado.pack()
        
        self.label_categoria = tk.Label(result_frame, text="", 
                                      font=("Segoe UI", 12), bg=self.colors['light'], 
                                      fg="#64748b")
        self.label_categoria.pack(pady=(5, 0))
        
        # Frame para la gráfica
        graph_frame = tk.Frame(main_frame, bg=self.colors['light'], 
                              relief=tk.RAISED, bd=1)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 4), dpi=100, facecolor=self.colors['light'])
        self.ax = self.fig.add_subplot(111)
        
        # Configurar la gráfica inicial
        self.setup_chart()
        
        # Canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Información adicional
        info_text = "• IMC < 18.5: Bajo peso\n• IMC 18.5-24.9: Normal\n• IMC 25-29.9: Sobrepeso\n• IMC ≥ 30: Obesidad"
        info_label = tk.Label(main_frame, text=info_text, font=("Segoe UI", 10), 
                             bg=self.colors['background'], fg="#64748b", justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=(10, 0))
    
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
        
        # Añadir línea vertical inicial
        self.user_line = self.ax.axvline(x=0, color='black', linestyle='-', linewidth=2, alpha=0)
        
        self.fig.tight_layout()
    
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
                categoria = "Normal"
                color = self.colors['success']
            elif 25 <= imc < 30:
                categoria = "Sobrepeso"
                color = self.colors['warning']
            else:
                categoria = "Obesidad"
                color = self.colors['danger']
            
            # Actualizar etiquetas de resultado
            self.label_resultado.config(text=f"Tu IMC: {imc:.2f}", fg=color)
            self.label_categoria.config(text=f"Categoría: {categoria}", fg=color)
            
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
        for i, (cat, color, rng) in enumerate(zip(categories, colors, ranges)):
            self.ax.barh(cat, width=rng[1]-rng[0], left=rng[0], color=color, alpha=0.7, edgecolor='white')
            mid = (rng[0] + rng[1]) / 2
            self.ax.text(mid, i, cat, ha='center', va='center', fontweight='bold')
        
        # Añadir línea para el IMC del usuario
        self.ax.axvline(x=imc, color='black', linestyle='-', linewidth=3, label=f'Tu IMC: {imc:.1f}')
        
        # Añadir marcador circular en la línea
        y_pos = categories.index(categoria) if categoria in categories else 0
        self.ax.plot(imc, y_pos, 'o', markersize=10, color='black', markeredgecolor='white', markeredgewidth=2)
        
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
    app = IMCAppConGrafica(root)
    root.mainloop()