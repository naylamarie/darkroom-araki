from gui import App
import customtkinter as ctk

# ─────────────────────────────────────────
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ─────────────────────────────────────────

# Este es el archivo que arranca todo.
# Crea la ventana principal y lanza la aplicación.

root = ctk.CTk()
app = App(root)

# Definimos un tamaño inicial y centramos la ventana
ancho = 950
alto = 700
x = (root.winfo_screenwidth() // 2) - (ancho // 2)
y = (root.winfo_screenheight() // 2) - (alto // 2)
root.geometry(f"{ancho}x{alto}+{x}+{y}")
root.mainloop()