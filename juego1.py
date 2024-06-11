import random #generar posiciones aleatorias
from functools import lru_cache #memorizar resultados de funciones mejorando la eficiencia
import tkinter as tk # crear la interfaz grafica
from tkinter import messagebox  # Importar messagebox de tkinter # mostrar mensajes en la interfaz grafica
from PIL import Image, ImageTk  # Importar PIL para manejar imágenes y redimensionar

# Clase que representa el tablero del juego
class Tablero:
    def __init__(self, filas, columnas, pos_gato, pos_raton, pos_salida): #  Inicializa el tablero con las filas, columnas y posiciones del gato, ratón y salida.
        self.filas = filas
        self.columnas = columnas
        self.pos_gato = pos_gato
        self.pos_raton = pos_raton
        self.pos_salida = pos_salida

    def mostrar(self): #Muestra el tablero en la consola, con G para el gato, R para el ratón y S para la salida.
        for f in range(self.filas):
            for c in range(self.columnas):
                if (f, c) == self.pos_gato:
                    print("G", end=' ')
                elif (f, c) == self.pos_raton:
                    print("R", end=' ')
                elif (f, c) == self.pos_salida:
                    print("S", end=' ')
                else:
                    print(".", end=' ')
            print()
        print()

# Movimientos posibles (arriba, abajo, izquierda, derecha)
MOVIMIENTOS = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1)
}

# Función para obtener movimientos válidos
def movimientos_validos(tablero, pos):
    movimientos = []
    for movimiento in MOVIMIENTOS.values():
        nueva_pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
        if 0 <= nueva_pos[0] < tablero.filas and 0 <= nueva_pos[1] < tablero.columnas:
            movimientos.append(nueva_pos)
    return movimientos

# Función para verificar si el juego ha terminado
def es_fin_del_juego(tablero):
    return tablero.pos_gato == tablero.pos_raton or tablero.pos_raton == tablero.pos_salida

# Función de evaluación (distancia Manhattan)
def evaluar(tablero):
    return -distancia_manhattan(tablero.pos_gato, tablero.pos_raton)

# Función para calcular la distancia Manhattan
def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Movimiento aleatorio del ratón
def mover_raton_aleatorio(tablero):
    movimientos = movimientos_validos(tablero, tablero.pos_raton)
    tablero.pos_raton = random.choice(movimientos)

# Movimiento inteligente del gato utilizando Minimax
def mover_gato_inteligente(tablero):
    mejor_movimiento = None 
    mejor_valor = float("-inf")
    for movimiento in movimientos_validos(tablero, tablero.pos_gato):
        posicion_original = tablero.pos_gato
        tablero.pos_gato = movimiento 
        valor = minimax(tablero, 3, False)
        tablero.pos_gato = posicion_original
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = movimiento
    tablero.pos_gato = mejor_movimiento

# Caching de la evaluación del tablero
@lru_cache(maxsize=None)
def evaluar(tablero_hash):
    pos_gato, pos_raton, pos_salida = tablero_hash
    return -distancia_manhattan(pos_gato, pos_raton)

# Convertir el tablero a una representación hash
def tablero_a_hash(tablero):
    return (tablero.pos_gato, tablero.pos_raton, tablero.pos_salida)

# Función Minimax
def minimax(tablero, profundidad, maximizando_gato):
    tablero_hash = tablero_a_hash(tablero)
    if es_fin_del_juego(tablero) or profundidad == 0:
        return evaluar(tablero_hash)
    
    if maximizando_gato:
        max_eval = float("-inf")
        for movimiento in movimientos_validos(tablero, tablero.pos_gato):
            posicion_original = tablero.pos_gato
            tablero.pos_gato = movimiento
            evaluacion = minimax(tablero, profundidad - 1, False)
            tablero.pos_gato = posicion_original
            max_eval = max(max_eval, evaluacion)
        return max_eval
    else:
        min_eval = float("inf")
        for movimiento in movimientos_validos(tablero, tablero.pos_raton):
            posicion_original = tablero.pos_raton
            tablero.pos_raton = movimiento
            evaluacion = minimax(tablero, profundidad - 1, True)
            tablero.pos_raton = posicion_original
            min_eval = min(min_eval, evaluacion)
        return min_eval

# Clase principal del juego
class Juego:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Juego del Gato y el Ratón")
        self.tablero = Tablero(5, 5, (4, 4), (0, 0), (random.randint(0, 4), random.randint(0, 4)))
        self.cargar_imagenes()
        self.crear_interfaz()
        self.actualizar_interfaz()

    # Cargar imágenes del gato, ratón y destino
    def cargar_imagenes(self):
        self.imagen_gato = ImageTk.PhotoImage(Image.open("static/gato.jpg").resize((100, 100)))
        self.imagen_raton = ImageTk.PhotoImage(Image.open("static/raton.jpg").resize((100, 100)))
        self.imagen_destino = ImageTk.PhotoImage(Image.open("static/destino.jpg").resize((100, 100)))

    # Crear la interfaz gráfica
    def crear_interfaz(self):
        self.canvas = tk.Canvas(self.raiz, width=500, height=500)
        self.canvas.pack()
        self.boton_jugar = tk.Button(self.raiz, text="Jugar", command=self.jugar)
        self.boton_jugar.pack()
        self.boton_reiniciar = tk.Button(self.raiz, text="Reiniciar", command=self.reiniciar)
        self.boton_reiniciar.pack()

    # Actualizar la interfaz gráfica
    def actualizar_interfaz(self):
        self.canvas.delete("all")
        for f in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                x1 = c * 100
                y1 = f * 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                if (f, c) == self.tablero.pos_gato:
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.imagen_gato)
                elif (f, c) == self.tablero.pos_raton:
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.imagen_raton)
                elif (f, c) == self.tablero.pos_salida:
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.imagen_destino)

    # Iniciar el juego
    def jugar(self):
        self.turno_raton = True  # Indica si es el turno del ratón o del gato
        self.realizar_movimiento()

    # Método para reiniciar el juego
    def reiniciar(self):
        self.tablero = Tablero(5, 5, (4, 4), (0, 0), (random.randint(0, 4), random.randint(0, 4)))
        self.actualizar_interfaz()
        self.jugar()

    # Realizar movimientos en el juego
    def realizar_movimiento(self):
        if not es_fin_del_juego(self.tablero):
            if self.turno_raton:
                mover_raton_aleatorio(self.tablero)
            else:
                mover_gato_inteligente(self.tablero)
            self.turno_raton = not self.turno_raton
            self.actualizar_interfaz()
            self.raiz.update_idletasks()
            self.raiz.after(1000, self.realizar_movimiento)  # Esperar 1000 ms antes del próximo movimiento
        else:
            if self.tablero.pos_raton == self.tablero.pos_salida:
                messagebox.showinfo("Juego terminado", "El ratón ha escapado")
            else:
                messagebox.showinfo("Juego terminado", "El gato atrapó al ratón")

# Ejecutar la aplicación
if __name__ == "__main__":
    raiz = tk.Tk()
    juego = Juego(raiz)
    raiz.mainloop()
