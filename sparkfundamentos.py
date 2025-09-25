import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

class ModernIMCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💪 Calculadora IMC Inteligente")
        self.root.geometry("600x750")
        self.root.configure(bg="#0f172a")  # Fondo oscuro moderno
        self.root.resizable(False, False)
        
        # Variables para animaciones
        self.current_step = 1
        self.total_steps = 3
        
        # Fuentes personalizadas
        self.title_font = tkFont.Font(family="Segoe UI", size=24, weight="bold")
        self.subtitle_font = tkFont.Font(family="Segoe UI", size=14, weight="normal")
        self.label_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")
        self.button_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        self.result_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        
        # Colores del tema
        self.colors = {
            'primary': '#6366f1',      # Índigo
            'secondary': '#8b5cf6',    # Violeta
            'success': '#10b981',      # Verde
            'warning': '#f59e0b',      # Amarillo
            'danger': '#ef4444',       # Rojo
            'info': '#3b82f6',         # Azul
            'dark': '#1e293b',         # Gris oscuro
            'light': '#f1f5f9',       # Gris claro
            'white': '#ffffff',
            'background': '#0f172a'    # Fondo
        }
        
        self.create_header()
        self.create_main_container()
        self.create_progress_bar()
        self.create_input_section()
        self.create_action_buttons()
        self.create_result_section()
        self.create_info_cards()
        self.create_footer()
        
        # Centrar ventana
        self.center_window()
        
        # Animación de entrada
        self.animate_entrance()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f'600x750+{x}+{y}')
    
    def create_header(self):
        """Crea el encabezado con gradiente"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="💪 IMC Calculator Pro",
            font=self.title_font,
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=(20, 5))
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="Calcula tu Índice de Masa Corporal de forma inteligente",
            font=self.subtitle_font,
            bg=self.colors['primary'],
            fg="#e2e8f0"
        )
        subtitle_label.pack(pady=(0, 20))
    
    def create_main_container(self):
        """Crea el contenedor principal con efecto de tarjeta"""
        self.main_container = tk.Frame(self.root, bg=self.colors['white'])
        self.main_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Efecto sombra simulado
        shadow_frame = tk.Frame(self.main_container, bg="#cbd5e1", height=2)
        shadow_frame.pack(fill='x')
    
    def create_progress_bar(self):
        """Crea una barra de progreso visual"""
        progress_frame = tk.Frame(self.main_container, bg=self.colors['white'], pady=20)
        progress_frame.pack(fill='x', padx=30)
        
        tk.Label(
            progress_frame,
            text="📊 Progreso de tu análisis",
            font=self.label_font,
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 10))
        
        # Barra de progreso personalizada
        self.progress_canvas = tk.Canvas(
            progress_frame, 
            height=8, 
            bg="#e2e8f0", 
            highlightthickness=0
        )
        self.progress_canvas.pack(fill='x', pady=(0, 5))
        
        # Etiquetas de pasos
        steps_frame = tk.Frame(progress_frame, bg=self.colors['white'])
        steps_frame.pack(fill='x')
        
        steps = ["📝 Datos", "⚖️ Cálculo", "📈 Resultado"]
        for i, step in enumerate(steps):
            tk.Label(
                steps_frame,
                text=step,
                font=("Segoe UI", 9),
                bg=self.colors['white'],
                fg=self.colors['dark']
            ).pack(side='left', expand=True)
    
    def create_input_section(self):
        """Crea la sección de entrada de datos con diseño moderno"""
        input_frame = tk.Frame(self.main_container, bg=self.colors['white'], pady=20)
        input_frame.pack(fill='x', padx=30)
        
        # Título de la sección
        tk.Label(
            input_frame,
            text="📋 Ingresa tus datos corporales",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 20))
        
        # Contenedor de inputs en grid
        inputs_container = tk.Frame(input_frame, bg=self.colors['white'])
        inputs_container.pack(fill='x')
        
        # Input de peso con icono y unidades
        self.create_modern_input(
            inputs_container, 
            "⚖️ Peso", 
            "kg", 
            "Ej: 70.5",
            0, 0
        )
        
        # Input de altura con icono y unidades  
        self.create_modern_input(
            inputs_container, 
            "📏 Altura", 
            "m", 
            "Ej: 1.75",
            0, 1
        )
        
        # Información adicional
        info_frame = tk.Frame(input_frame, bg="#f8fafc", relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(
            info_frame,
            text="💡 Consejo: Para mayor precisión, pésate en ayunas y sin ropa pesada",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.colors['info'],
            pady=10
        ).pack()
    
    def create_modern_input(self, parent, label, unit, placeholder, row, col):
        """Crea un input moderno con etiqueta, icono y unidades"""
        input_frame = tk.Frame(parent, bg=self.colors['white'])
        input_frame.grid(row=row, column=col, padx=15, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Etiqueta con icono
        tk.Label(
            input_frame,
            text=label,
            font=self.label_font,
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 5))
        
        # Contenedor del input con unidades
        entry_container = tk.Frame(input_frame, bg=self.colors['white'])
        entry_container.pack(fill='x')
        
        # Campo de entrada
        entry = tk.Entry(
            entry_container,
            font=("Segoe UI", 12),
            bg="#f8fafc",
            fg="#94a3b8",
            relief='solid',
            bd=2,
            width=15
        )
        entry.pack(side='left', fill='x', expand=True, ipady=8)
        entry.insert(0, placeholder)
        
        # Label de unidades
        tk.Label(
            entry_container,
            text=unit,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            width=3
        ).pack(side='right', padx=(5, 0))
        
        # Label de error
        error_label = tk.Label(
            input_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.colors['white'],
            fg=self.colors['danger']
        )
        error_label.pack(anchor='w', pady=(2, 0))
        
        # Eventos para placeholder
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.colors['dark'], bd=2, highlightcolor=self.colors['primary'])
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg="#94a3b8")
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Almacenar referencias
        if 'Peso' in label:
            self.entry_peso = entry
            self.peso_error = error_label
        else:
            self.entry_altura = entry
            self.altura_error = error_label
    
    def create_action_buttons(self):
        """Crea los botones de acción con efectos hover"""
        buttons_frame = tk.Frame(self.main_container, bg=self.colors['white'], pady=20)
        buttons_frame.pack(fill='x', padx=30)
        
        # Botón principal de cálculo
        self.calc_button = tk.Button(
            buttons_frame,
            text="🚀 Calcular Mi IMC",
            font=self.button_font,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            activebackground=self.colors['secondary'],
            relief='flat',
            cursor='hand2',
            pady=15,
            command=self.calcular_imc
        )
        self.calc_button.pack(fill='x', pady=(0, 10))
        
        # Efectos hover
        def on_enter(e):
            self.calc_button.config(bg=self.colors['secondary'])
        def on_leave(e):
            self.calc_button.config(bg=self.colors['primary'])
        
        self.calc_button.bind('<Enter>', on_enter)
        self.calc_button.bind('<Leave>', on_leave)
        
        # Botones secundarios
        secondary_frame = tk.Frame(buttons_frame, bg=self.colors['white'])
        secondary_frame.pack(fill='x')
        
        # Botón limpiar
        clear_btn = tk.Button(
            secondary_frame,
            text="🧹 Limpiar",
            font=("Segoe UI", 10),
            bg=self.colors['light'],
            fg=self.colors['dark'],
            relief='flat',
            cursor='hand2',
            pady=8,
            command=self.limpiar_campos
        )
        clear_btn.pack(side='left', padx=(0, 10))
        
        # Botón info
        info_btn = tk.Button(
            secondary_frame,
            text="ℹ️ Más Info",
            font=("Segoe UI", 10),
            bg=self.colors['info'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            pady=8,
            command=self.mostrar_info_detallada
        )
        info_btn.pack(side='left')
    
    def create_result_section(self):
        """Crea la sección de resultados con diseño atractivo"""
        self.result_frame = tk.Frame(self.main_container, bg="#f8fafc", relief='solid', bd=1)
        self.result_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        # Título de resultados
        tk.Label(
            self.result_frame,
            text="📊 Tu Resultado",
            font=("Segoe UI", 14, "bold"),
            bg="#f8fafc",
            fg=self.colors['dark']
        ).pack(pady=(15, 10))
        
        # Resultado principal
        self.result_label = tk.Label(
            self.result_frame,
            text="Ingresa tus datos para ver tu IMC",
            font=self.result_font,
            bg="#f8fafc",
            fg="#64748b",
            pady=15
        )
        self.result_label.pack()
        
        # Medidor visual del IMC
        self.create_imc_gauge()
        
        # Interpretación del resultado
        self.interpretation_label = tk.Label(
            self.result_frame,
            text="",
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg="#64748b",
            wraplength=400,
            justify='center',
            pady=0
        )
        self.interpretation_label.pack(pady=(0, 15))
    
    def create_imc_gauge(self):
        """Crea un medidor visual del IMC"""
        gauge_frame = tk.Frame(self.result_frame, bg="#f8fafc")
        gauge_frame.pack(pady=10)
        
        # Canvas para el medidor
        self.gauge_canvas = tk.Canvas(
            gauge_frame,
            width=300,
            height=60,
            bg="#f8fafc",
            highlightthickness=0
        )
        self.gauge_canvas.pack()
        
        # Dibujar escala base
        self.draw_gauge_base()
    
    def draw_gauge_base(self):
        """Dibuja la base del medidor IMC"""
        canvas = self.gauge_canvas
        canvas.delete("all")
        
        # Rangos de IMC con colores
        ranges = [
            (0, 60, self.colors['info']),      # Bajo peso
            (60, 120, self.colors['success']), # Normal  
            (120, 180, self.colors['warning']), # Sobrepeso
            (180, 240, self.colors['danger'])   # Obesidad
        ]
        
        for start, end, color in ranges:
            canvas.create_rectangle(start + 30, 35, end + 30, 45, fill=color, outline="")
        
        # Etiquetas
        labels = ["Bajo", "Normal", "Sobrepeso", "Obesidad"]
        positions = [60, 120, 180, 240]
        
        for label, pos in zip(labels, positions):
            canvas.create_text(pos + 30, 55, text=label, font=("Segoe UI", 8), fill=self.colors['dark'])
    
    def update_gauge(self, imc):
        """Actualiza el medidor con el valor del IMC"""
        self.draw_gauge_base()
        
        # Calcular posición del indicador
        if imc < 18.5:
            position = (imc / 18.5) * 60 + 30
        elif imc < 25:
            position = ((imc - 18.5) / 6.5) * 60 + 90
        elif imc < 30:
            position = ((imc - 25) / 5) * 60 + 150
        else:
            position = min(((imc - 30) / 10) * 60 + 210, 270)
        
        # Dibujar indicador
        self.gauge_canvas.create_polygon(
            position, 30, position - 5, 20, position + 5, 20,
            fill=self.colors['dark'], outline=""
        )
        self.gauge_canvas.create_text(
            position, 15, text=f"{imc:.1f}", 
            font=("Segoe UI", 10, "bold"), fill=self.colors['dark']
        )
    
    def create_info_cards(self):
        """Crea tarjetas informativas sobre el IMC"""
        info_frame = tk.Frame(self.main_container, bg=self.colors['white'])
        info_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        tk.Label(
            info_frame,
            text="📚 Guía Rápida del IMC",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor='w', pady=(0, 15))
        
        # Grid de tarjetas
        cards_frame = tk.Frame(info_frame, bg=self.colors['white'])
        cards_frame.pack(fill='x')
        
        categories = [
            ("Bajo peso", "< 18.5", self.colors['info'], "🔵"),
            ("Normal", "18.5 - 24.9", self.colors['success'], "🟢"),
            ("Sobrepeso", "25.0 - 29.9", self.colors['warning'], "🟡"),
            ("Obesidad", "≥ 30.0", self.colors['danger'], "🔴")
        ]
        
        for i, (categoria, rango, color, emoji) in enumerate(categories):
            card = tk.Frame(cards_frame, bg=color, relief='flat', bd=0)
            card.grid(row=0, column=i, padx=3, pady=5, sticky='ew')
            cards_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(
                card,
                text=f"{emoji} {categoria}",
                font=("Segoe UI", 9, "bold"),
                bg=color,
                fg=self.colors['white'],
                pady=5
            ).pack()
            
            tk.Label(
                card,
                text=rango,
                font=("Segoe UI", 8),
                bg=color,
                fg=self.colors['white'],
                pady=0
            ).pack(pady=(0, 5))
    
    def create_footer(self):
        """Crea el pie de página"""
        footer = tk.Frame(self.root, bg=self.colors['background'], height=40)
        footer.pack(fill='x', side='bottom')
        
        tk.Label(
            footer,
            text="💡 Recuerda: El IMC es una guía. Consulta a un profesional de la salud para evaluación completa.",
            font=("Segoe UI", 9),
            bg=self.colors['background'],
            fg="#64748b"
        ).pack(pady=10)
    
    def animate_entrance(self):
        """Animación de entrada de la aplicación"""
        self.main_container.pack_forget()
        self.root.after(100, lambda: self.main_container.pack(fill='both', expand=True, padx=30, pady=(0, 30)))
    
    def update_progress(self, step):
        """Actualiza la barra de progreso"""
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        if width > 1:
            progress_width = (step / self.total_steps) * width
            self.progress_canvas.create_rectangle(
                0, 0, progress_width, 8, 
                fill=self.colors['primary'], outline=""
            )
    
    def limpiar_campos(self):
        """Limpia todos los campos"""
        self.entry_peso.delete(0, tk.END)
        self.entry_peso.insert(0, "Ej: 70.5")
        self.entry_peso.config(fg="#94a3b8")
        
        self.entry_altura.delete(0, tk.END)
        self.entry_altura.insert(0, "Ej: 1.75")
        self.entry_altura.config(fg="#94a3b8")
        
        self.peso_error.config(text="")
        self.altura_error.config(text="")
        
        self.result_label.config(
            text="Ingresa tus datos para ver tu IMC",
            fg="#64748b"
        )
        self.interpretation_label.config(text="")
        self.draw_gauge_base()
        
        self.root.after(100, lambda: self.update_progress(1))
    
    def mostrar_info_detallada(self):
        """Muestra información detallada sobre el IMC"""
        info_window = tk.Toplevel(self.root)
        info_window.title("ℹ️ Información Detallada del IMC")
        info_window.geometry("500x600")
        info_window.configure(bg=self.colors['white'])
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Centrar ventana de info
        info_window.update_idletasks()
        x = (info_window.winfo_screenwidth() // 2) - (info_window.winfo_width() // 2)
        y = (info_window.winfo_screenheight() // 2) - (info_window.winfo_height() // 2)
        info_window.geometry(f'+{x}+{y}')
        
        # Contenido de información
        scroll_frame = tk.Frame(info_window, bg=self.colors['white'])
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        content = """
📊 ¿Qué es el Índice de Masa Corporal (IMC)?

El IMC es una medida que relaciona el peso y la altura de una persona para evaluar si tiene un peso saludable.

🔢 Fórmula: IMC = Peso (kg) / Altura² (m)

📈 Interpretación de Resultados:

🔵 Bajo peso (< 18.5):
• Puede indicar desnutrición
• Consulte a un profesional de la salud

🟢 Normal (18.5 - 24.9):
• Rango de peso saludable
• Mantenga hábitos saludables

🟡 Sobrepeso (25.0 - 29.9):
• Riesgo aumentado de problemas de salud
• Considere cambios en dieta y ejercicio

🔴 Obesidad (≥ 30.0):
• Alto riesgo de complicaciones
• Busque ayuda profesional inmediatamente

⚠️ Limitaciones del IMC:
• No distingue entre músculo y grasa
• No considera la distribución de grasa
• Puede no ser preciso para atletas o ancianos

💡 Recomendaciones:
• Use el IMC como guía inicial
• Combine con otras medidas de salud
• Consulte siempre a profesionales médicos
• Mantenga un estilo de vida activo
"""
        
        tk.Label(
            scroll_frame,
            text=content,
            font=("Segoe UI", 10),
            bg=self.colors['white'],
            fg=self.colors['dark'],
            justify='left',
            wraplength=450
        ).pack(anchor='w')
        
        tk.Button(
            scroll_frame,
            text="✓ Entendido",
            font=self.button_font,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            relief='flat',
            cursor='hand2',
            command=info_window.destroy
        ).pack(pady=20)
    
    def calcular_imc(self):
        """Calcula el IMC con validación mejorada y animaciones"""
        # Limpiar errores previos
        self.peso_error.config(text="")
        self.altura_error.config(text="")
        
        # Actualizar progreso
        self.update_progress(2)
        
        try:
            # Obtener valores
            peso_text = self.entry_peso.get().strip()
            altura_text = self.entry_altura.get().strip()
            
            # Validar campos vacíos o con placeholder
            has_error = False
            
            if not peso_text or peso_text.startswith("Ej:"):
                self.peso_error.config(text="⚠️ Campo requerido")
                has_error = True
            
            if not altura_text or altura_text.startswith("Ej:"):
                self.altura_error.config(text="⚠️ Campo requerido")
                has_error = True
            
            if has_error:
                self.update_progress(1)
                return
            
            # Convertir a números
            peso = float(peso_text)
            altura = float(altura_text)
            
            # Validar rangos razonables
            if peso <= 0 or peso > 500:
                self.peso_error.config(text="⚠️ Peso debe estar entre 1-500 kg")
                self.update_progress(1)
                return
                
            if altura <= 0 or altura > 3:
                self.altura_error.config(text="⚠️ Altura debe estar entre 0.1-3.0 m")
                self.update_progress(1)
                return
            
            # Calcular IMC
            imc = peso / (altura ** 2)
            
            # Determinar categoría y color
            if imc < 18.5:
                categoria = "Bajo peso"
                color = self.colors['info']
                emoji = "🔵"
                interpretacion = "Tu IMC indica bajo peso. Considera consultar a un nutricionista para alcanzar un peso saludable."
            elif 18.5 <= imc < 25:
                categoria = "Normal"
                color = self.colors['success']
                emoji = "🟢"
                interpretacion = "¡Excelente! Tu IMC está en el rango saludable. Mantén tus hábitos actuales."
            elif 25 <= imc < 30:
                categoria = "Sobrepeso"
                color = self.colors['warning']
                emoji = "🟡"
                interpretacion = "Tu IMC indica sobrepeso. Una dieta equilibrada y ejercicio regular pueden ayudarte."
            else:
                categoria = "Obesidad"
                color = self.colors['danger']
                emoji = "🔴"
                interpretacion = "Tu IMC indica obesidad. Te recomendamos consultar a un profesional de la salud."
            
            # Mostrar resultado
            # Forzar que el resultado siempre se muestre
            try:
                self.result_label.config(
                    text=f"IMC: {imc:.2f}   |   Estado: {categoria} {emoji}",
                    fg=color
                )
            except Exception:
                self.result_label = tk.Label(
                    self.result_frame,
                    text=f"IMC: {imc:.2f}   |   Estado: {categoria} {emoji}",
                    font=self.result_font,
                    bg="#f8fafc",
                    fg=color,
                    pady=15
                )
                self.result_label.pack()
            
            self.interpretation_label.config(
                text=interpretacion,
                fg=self.colors['dark']
            )
            
            # Actualizar medidor
            self.root.after(100, lambda: self.update_gauge(imc))
            
            # Progreso completo
            self.update_progress(3)
            
        except ValueError:
            messagebox.showerror(
                "❌ Error de Entrada", 
                "Por favor, ingrese valores numéricos válidos.\n\n" +
                "Ejemplos correctos:\n" +
                "• Peso: 70.5\n" +
                "• Altura: 1.75"
            )
            self.update_progress(1)
        
        except Exception as e:
            messagebox.showerror("❌ Error Inesperado", f"Ha ocurrido un error: {str(e)}")
            self.update_progress(1)


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    
    # Configuraciones adicionales de la ventana
    try:
        # Intentar establecer el ícono (opcional)
        # root.iconbitmap('imc_icon.ico')
        pass
    except:
        pass
    
    # Crear la aplicación
    app = ModernIMCApp(root)
    
    print("💪 Calculadora IMC Moderna iniciada correctamente")
    print("🎯 Características:")
    print("   • Interfaz moderna y amigable")
    print("   • Validación completa de datos")
    print("   • Medidor visual del IMC")
    print("   • Información detallada")
    print("   • Animaciones suaves")
    print("   • Diseño responsivo")
    
    # Ejecutar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()