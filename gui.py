import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageTk
import numpy as np

# Importamos todos los algoritmos desde el paquete
from algoritmos import floyd_steinberg, threshold, bayer, halftone_lineas, halftone_puntos, solarizacion

# ─────────────────────────────────────────
# CONFIGURACIÓN VISUAL
# ─────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLOR_FONDO      = "#0a0a0a"
COLOR_PANEL      = "#111111"
COLOR_NEON       = "#e0f0ff"
COLOR_NEON_TENUE = "#444444"
COLOR_BOTON      = "#1a1a1a"

# ─────────────────────────────────────────
# GUI
# ─────────────────────────────────────────

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DARKROOM ARAKI")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)
        self.imagen_path = None
        self.imagen_resultado = None
        self.construir_interfaz()

    def construir_interfaz(self):

        # ── Panel izquierdo — controles ──
        # Contenedor externo del panel para el scroll
        panel_contenedor = ctk.CTkScrollableFrame(self.root, fg_color=COLOR_PANEL, corner_radius=0, width=260)
        panel_contenedor.grid(row=0, column=0, sticky="ns", padx=(0, 0), pady=0)
        panel = panel_contenedor

        # Título
        ctk.CTkLabel(panel, text="DARKROOM ARAKI", font=("Consolas", 16, "bold"),
                     text_color=COLOR_NEON).pack(pady=(20, 5))
        ctk.CTkLabel(panel, text="procesador de imágenes", font=("Consolas", 10),
                     text_color=COLOR_NEON_TENUE).pack(pady=(0, 20))

        # Separador
        ctk.CTkFrame(panel, height=1, fg_color=COLOR_NEON_TENUE).pack(fill="x", padx=15, pady=(0, 20))

        # Botón elegir imagen
        ctk.CTkButton(panel, text="[ ELEGIR IMAGEN ]", command=self.elegir_imagen,
                      fg_color=COLOR_BOTON, hover_color="#222", text_color=COLOR_NEON,
                      border_color=COLOR_NEON, border_width=1, corner_radius=0,
                      font=("Consolas", 12)).pack(padx=15, fill="x")

        self.label_imagen = ctk.CTkLabel(panel, text="ninguna imagen seleccionada",
                                          font=("Consolas", 10), text_color=COLOR_NEON_TENUE)
        self.label_imagen.pack(pady=(5, 15))

        # Separador
        ctk.CTkFrame(panel, height=1, fg_color=COLOR_NEON_TENUE).pack(fill="x", padx=15, pady=(0, 15))

        # Selector de efecto
        ctk.CTkLabel(panel, text="EFECTO", font=("Consolas", 11, "bold"),
                     text_color=COLOR_NEON).pack(anchor="w", padx=15)
        self.efecto_var = ctk.StringVar(value="threshold")
        self.menu_efecto = ctk.CTkOptionMenu(panel, variable=self.efecto_var,
                                              values=["threshold", "floyd_steinberg", "bayer",
                                                      "halftone_lineas", "halftone_puntos", "solarizacion"],
                                              command=self.actualizar_sliders,
                                              fg_color=COLOR_BOTON, button_color="#222",
                                              button_hover_color="#333", text_color=COLOR_NEON,
                                              font=("Consolas", 12), corner_radius=0)
        self.menu_efecto.pack(padx=15, fill="x", pady=(5, 15))

        # Separador
        ctk.CTkFrame(panel, height=1, fg_color=COLOR_NEON_TENUE).pack(fill="x", padx=15, pady=(0, 15))

        # Slider contraste — aplica a todos los efectos
        ctk.CTkLabel(panel, text="CONTRASTE (1.0 - 5.0)", font=("Consolas", 11, "bold"),
                     text_color=COLOR_NEON).pack(anchor="w", padx=15)
        self.contraste_var = ctk.DoubleVar(value=2.0)
        self.label_contraste_val = ctk.CTkLabel(panel, text="2.0", font=("Consolas", 10),
                                                 text_color=COLOR_NEON_TENUE)
        self.label_contraste_val.pack(anchor="w", padx=15)
        ctk.CTkSlider(panel, from_=1.0, to=5.0, variable=self.contraste_var,
                      button_color=COLOR_NEON, button_hover_color="#aaa",
                      progress_color=COLOR_NEON, fg_color="#222",
                      command=lambda v: self.label_contraste_val.configure(text=f"{v:.1f}")).pack(
                      padx=15, fill="x", pady=(0, 15))

        # Slider umbral — solo para threshold y floyd_steinberg
        self.label_umbral_titulo = ctk.CTkLabel(panel, text="UMBRAL (0 - 255)",
                                                 font=("Consolas", 11, "bold"), text_color=COLOR_NEON)
        self.label_umbral_titulo.pack(anchor="w", padx=15)
        self.umbral_var = ctk.IntVar(value=180)
        self.label_umbral_val = ctk.CTkLabel(panel, text="180", font=("Consolas", 10),
                                              text_color=COLOR_NEON_TENUE)
        self.label_umbral_val.pack(anchor="w", padx=15)
        self.slider_umbral = ctk.CTkSlider(panel, from_=0, to=255, variable=self.umbral_var,
                                            button_color=COLOR_NEON, button_hover_color="#aaa",
                                            progress_color=COLOR_NEON, fg_color="#222",
                                            command=lambda v: self.label_umbral_val.configure(text=str(int(v))))
        self.slider_umbral.pack(padx=15, fill="x", pady=(0, 15))

        # Slider bloque — solo para halftone
        self.label_bloque_titulo = ctk.CTkLabel(panel, text="BLOQUE (5 - 50)",
                                                 font=("Consolas", 11, "bold"), text_color=COLOR_NEON)
        self.label_bloque_titulo.pack(anchor="w", padx=15)
        self.bloque_var = ctk.IntVar(value=20)
        self.label_bloque_val = ctk.CTkLabel(panel, text="20", font=("Consolas", 10),
                                              text_color=COLOR_NEON_TENUE)
        self.label_bloque_val.pack(anchor="w", padx=15)
        self.slider_bloque = ctk.CTkSlider(panel, from_=5, to=50, variable=self.bloque_var,
                                            button_color=COLOR_NEON, button_hover_color="#aaa",
                                            progress_color=COLOR_NEON, fg_color="#222",
                                            command=lambda v: self.label_bloque_val.configure(text=str(int(v))))
        self.slider_bloque.pack(padx=15, fill="x", pady=(0, 20))

        # Separador
        ctk.CTkFrame(panel, height=1, fg_color=COLOR_NEON_TENUE).pack(fill="x", padx=15, pady=(0, 15))

        # Botones procesar, guardar y restablecer
        ctk.CTkButton(panel, text="[ PROCESAR ]", command=self.procesar,
                      fg_color=COLOR_NEON, hover_color="#ccc", text_color="#000",
                      corner_radius=0, font=("Consolas", 13, "bold")).pack(padx=15, fill="x", pady=(0, 8))

        ctk.CTkButton(panel, text="[ GUARDAR ]", command=self.guardar,
                      fg_color=COLOR_BOTON, hover_color="#222", text_color=COLOR_NEON,
                      border_color=COLOR_NEON, border_width=1, corner_radius=0,
                      font=("Consolas", 12)).pack(padx=15, fill="x")
        
        ctk.CTkButton(panel, text="[ RESTABLECER ]", command=self.resetear,
                      fg_color=COLOR_BOTON, hover_color="#222", text_color=COLOR_NEON,
                      border_color=COLOR_NEON, border_width=1, corner_radius=0,
                      font=("Consolas", 12)).pack(padx=15, fill="x", pady=(8, 0))

        # ── Panel derecho — preview con grilla ──
        self.canvas = ctk.CTkCanvas(self.root, width=620, height=620,
                                     bg=COLOR_FONDO, highlightthickness=1,
                                     highlightbackground=COLOR_NEON)
        self.canvas.grid(row=0, column=1, padx=15, pady=15)
        self.dibujar_grilla()

        # Actualizamos sliders según efecto inicial
        self.actualizar_sliders()

    def dibujar_grilla(self):
        # Dibujamos la grilla de fondo con tono azulado frío
        espaciado = 30
        for i in range(0, 621, espaciado):
            self.canvas.create_line(i, 0, i, 620, fill="#0d2030", width=1)  # líneas verticales
            self.canvas.create_line(0, i, 620, i, fill="#0d2030", width=1)  # líneas horizontales

    def actualizar_sliders(self, event=None):
        efecto = self.efecto_var.get()

        # Activamos o desactivamos umbral según el efecto seleccionado
        if efecto in ["threshold", "floyd_steinberg", "solarizacion"]:
            self.slider_umbral.configure(state="normal", button_color=COLOR_NEON)
            self.label_umbral_titulo.configure(text_color=COLOR_NEON)
            self.label_umbral_val.configure(text_color=COLOR_NEON_TENUE)
        else:
            self.slider_umbral.configure(state="disabled", button_color=COLOR_NEON_TENUE)
            self.label_umbral_titulo.configure(text_color=COLOR_NEON_TENUE)
            self.label_umbral_val.configure(text_color="#2a2a2a")

        # Activamos o desactivamos bloque según el efecto seleccionado
        if efecto in ["halftone_lineas", "halftone_puntos"]:
            self.slider_bloque.configure(state="normal", button_color=COLOR_NEON)
            self.label_bloque_titulo.configure(text_color=COLOR_NEON)
            self.label_bloque_val.configure(text_color=COLOR_NEON_TENUE)
        else:
            self.slider_bloque.configure(state="disabled", button_color=COLOR_NEON_TENUE)
            self.label_bloque_titulo.configure(text_color=COLOR_NEON_TENUE)
            self.label_bloque_val.configure(text_color="#2a2a2a")

    def elegir_imagen(self):
        # Abrimos el explorador de archivos para elegir la imagen
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if path:
            self.imagen_path = path
            nombre = path.split("/")[-1]
            self.label_imagen.configure(text=nombre)
            
            # Mostramos la imagen original en el canvas apenas se carga
            preview = Image.open(path).convert("L")
            preview.thumbnail((600, 600))
            self.foto = ImageTk.PhotoImage(preview)
            self.canvas.delete("imagen")
            self.dibujar_grilla()
            self.canvas.create_image(310, 310, image=self.foto, tags="imagen")

    def procesar(self):
        if not self.imagen_path:
            self.label_imagen.configure(text="⚠ elegí una imagen primero")
            return

        # Cargamos y preparamos la imagen
        img = Image.open(self.imagen_path).convert("L")
        img = ImageEnhance.Contrast(img).enhance(self.contraste_var.get())
        pixels = np.array(img, dtype=float)
        height, width = pixels.shape

        efecto = self.efecto_var.get()
        umbral = self.umbral_var.get()
        bloque = self.bloque_var.get()

        # Aplicamos el algoritmo seleccionado
        if efecto == "floyd_steinberg":
            resultado = floyd_steinberg(pixels, height, width, umbral)
        elif efecto == "threshold":
            resultado = threshold(pixels, height, width, umbral)
        elif efecto == "bayer":
            resultado = bayer(pixels, height, width)
        elif efecto == "halftone_lineas":
            resultado = halftone_lineas(pixels, height, width, bloque)
        elif efecto == "halftone_puntos":
            resultado = halftone_puntos(pixels, height, width, bloque)
        elif efecto == "solarizacion":
            resultado = solarizacion(pixels, height, width, umbral)    

        self.imagen_resultado = resultado

        # Mostramos el resultado en el canvas sobre la grilla
        preview = resultado.copy()
        preview.thumbnail((600, 600))
        self.foto = ImageTk.PhotoImage(preview)
        self.canvas.delete("imagen")
        self.dibujar_grilla()
        self.canvas.create_image(310, 310, image=self.foto, tags="imagen")

    def guardar(self):
        if not self.imagen_resultado:
            return
        # Abrimos el explorador para elegir dónde guardar
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG", "*.jpg")])
        if path:
            self.imagen_resultado.save(path)
            print(f"✅ Guardado en {path}")

    def resetear(self):
        # Volvemos todos los sliders a sus valores por defecto
        self.contraste_var.set(2.0)
        self.umbral_var.set(180)
        self.bloque_var.set(20)
        self.label_contraste_val.configure(text="2.0")
        self.label_umbral_val.configure(text="180")
        self.label_bloque_val.configure(text="20")         