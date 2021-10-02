import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import sys
from tkinter import font
import requests
import sqlite3

def precio_dolar_manual():
    ventana.lower()
    while True:
        dolar = tk.simpledialog.askinteger(title="Dolar", prompt="Precio dolar (sin decimales):")
        if dolar != None:
            if dolar > 0: 
                return dolar

def sumar(empanadas):
    empanadas["text"] = empanadas["text"]+1
    total["text"] = total["text"] + dolar

def restar(empanadas):
    if empanadas["text"] > 0:
        empanadas["text"] = empanadas["text"]-1
        total["text"] = total["text"] - dolar
    else:
        empanadas["text"] = 0

def cancelar():
    ccarne["text"] = 0
    cjyq["text"] = 0
    chum["text"] = 0
    total["text"] = 0
    dni.delete("0","end")

def salir():
    r = tk.messagebox.askokcancel(title="Salir", message="¿Desea salir del programa?")
    if r:
        sys.exit()

def confirmar():
    carne = int(ccarne["text"])
    jyq = int(cjyq["text"])
    hum = int(chum["text"])
    compra = carne + jyq + hum
    total = compra*dolar
    if compra == 0:
        tk.messagebox.showerror(title="Error", message="Compra mínima: 1 empanada")
    else:
        try:
            int(dni.get())
            documento = dni.get()
            r =tk.messagebox.askyesno(title="Confirmar compra", message=f"¿Confirma la compra de {compra} empanadas/s por un monto total de ${total}?", parent=ventana)
            if r:
                try:
                    while True:
                        abono = tk.simpledialog.askinteger(title="Pago", prompt="¿Con cuanto abona?", parent=ventana)
                        if abono >= total:
                            tk.messagebox.showinfo(title="Pago", message=f"El vuelto es de ${abono - total}")
                            registrar_pedido(documento, jyq, carne, hum, total)
                            cancelar()
                            break
                        else:
                            tk.messagebox.showwarning(title="Pago", message=f"El pago no puede ser menor al monto total de ${compra*dolar}")
                except:
                    pass
        except:
            tk.messagebox.showerror(title="Error", message="Ingrese un número de DNI")

def registrar_pedido(dni, emp_jyq, emp_carne, emp_humita, total):
    # Conecto/creo base de datos. Recien ahora que la compra esta confirmada tiene sentido crear la conexión
    conn = sqlite3.connect("clientes.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE clientes (dni INTEGER, jyq INTEGER, carne INTEGER, humita INTEGER, total_compra INTEGER)")
        tk.messagebox.showinfo(title="Tabla creada", message="La tabla clientes ha sido creada con exito")
    except:
        pass
    
    cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", (dni, emp_jyq, emp_carne, emp_humita, total))
    tk.messagebox.showinfo(title="Operacion registrada", message=f"Compra de cliente {dni} por un total de ${total} registrada con exito")
    conn.commit()
    conn.close()


################################################
ventana = tk.Tk()
ventana.title("Casa de Empandas")
# ventana.iconbitmap('./favicon.ico')

barra_de_menu = tk.Menu()
menu_ayuda = tk.Menu(barra_de_menu, tearoff=0)
barra_de_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de...", command=lambda: messagebox.showinfo(title="Acerca de..", message="Aplicación de escritorio para crear un registro de pedidos. Por cualquier consulta contactarse con maximiliano.deri@gmail.com"))

ventana.config(width=300, height=350, menu=barra_de_menu)

titulo = tk.Label(text="TOMAR PEDIDOS", font="Helvetica 10 bold")
titulo.place(x=100,y=10)

# API precio dolar
try:
    r = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales") 
    if r.status_code == 200:
        data = r.json()
        dolar = data[0]["casa"]["venta"]
        dolar = dolar.replace(",",".")
        dolar = round(float(dolar))
# Ingreso manual del precio del dolar si el API falla
    else:
        dolar = precio_dolar_manual()
except:
    dolar = precio_dolar_manual()

px= 65
py= 50

ecarne = tk.Label(text="""Empanadas 
de carne: """)
ecarne.place(x=px,y=py)

boton = ttk.Button(text="-", command=lambda: restar(ccarne))
boton.place(x=px+75,y=py+6)
boton.config(width=2)

ccarne = tk.Label(text=0)
ccarne.place(x=px+105,y=py+8)

boton = ttk.Button(text="+", command=lambda: sumar(ccarne))
boton.place(x=px+125,y=py+6)
boton.config(width=2)

ejyq = tk.Label(text="""Empanadas 
de J y Q: """)
ejyq.place(x=px,y=py+50)

boton = ttk.Button(text="-", command=lambda: restar(cjyq))
boton.place(x=px+75,y=py+58)
boton.config(width=2)

cjyq = tk.Label(text=0)
cjyq.place(x=px+105,y=py+58)

boton = ttk.Button(text="+", command=lambda: sumar(cjyq))
boton.place(x=px+125,y=py+58)
boton.config(width=2)

ehumita = tk.Label(text="""Empanadas 
de humita: """)
ehumita.place(x=px,y=py+100)

boton = ttk.Button(text="-", command=lambda: restar(chum))
boton.place(x=px+75,y=py+110)
boton.config(width=2)

chum = tk.Label(text=0)
chum.place(x=px+105,y=py+110)

boton = ttk.Button(text="+", command=lambda: sumar(chum))
boton.place(x=px+125,y=py+110)
boton.config(width=2)

n = tk.Label(text="DNI cliente: ")
n.place(x=px,y=py+145)

dni = ttk.Entry()
dni.place(x=px+78,y=py+145)
dni.config(width=10)

t = tk.Label(text="TOTAL: $", font="Helvetica 10 bold")
t.place(x=px+70,y=py+175)

total = tk.Label(text=0, font="Helvetica 10 bold")
total.place(x=px+130,y=py+175)

bx = 20
by = 260
w = 10
h = 3
boton = tk.Button(text=f"""Cancelar
pedido""", command=cancelar)
boton.place(x=bx,y=by)
boton.config(width=w, height=h)

boton = tk.Button(text="""Confirmar 
pedido""", command=confirmar)
boton.place(x=bx+90,y=by)
boton.config(width=w, height=h)

boton = tk.Button(text="Salir", command=salir)
boton.place(x=bx+180,y=by)
boton.config(width=w, height=h)

ventana.bind("<Return>", lambda x: confirmar())

ventana.mainloop()

