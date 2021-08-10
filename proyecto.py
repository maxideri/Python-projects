
import os
import requests
import sqlite3

#############################################################
# Validar ingreso de input numéricos
def validar (cantidad):
    while True:
        try:
            cantidad = int(cantidad)
            break
        except:
            print ("""
    Error""")
        cantidad = input ("""
    Ingrese un valor numérico: """)
    return cantidad

def confirmar_pedido (total):
    os.system("cls")
    
    print(f"""
    El pedido fue confirmado
    TOTAL: ${total} """)
    
    while True:
        pago = input("""
    Monto abonado: """)
        pago = validar(pago)
        
        if pago < total:
            print("""
    El monto abonado no puede ser menor al total""")
        
        elif pago == total:
            print("""
    Pago justo""")
            break

        else:
            print(f"""
    Vuelto: {pago - total}""")
            break

def registrar_pedido(dni, emp_jyq, emp_carne, emp_humita, total):
    # Conecto/creo base de datos. Recien ahora que la compra esta confirmada tiene sentido crear la conexión
    conn = sqlite3.connect("clientes.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE clientes (dni INTEGER, jyq INTEGER, carne INTEGER, humita INTEGER, total_compra INTEGER)")
        print ("""
    La tabla clientes ha sido creada con exito""")
    except:
        print("""
    Conexión a tabla de clientes exitosa""")
    
    cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", (dni, emp_jyq, emp_carne, emp_humita, total))
    print(f"""
    Compra de cliente {dni} por un total de ${total} registrada con exito""")
    conn.commit()
    conn.close()
    input("""
    Presione ENTER para continuar...""")
    os.system("cls")


###################################################################

# API precio dolar
r = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales") 
if r.status_code == 200:
    data = r.json()
    dolar = data[0]["casa"]["venta"]
    dolar = dolar.replace(",",".")
    dolar = round(float(dolar))
 # Ingreso manual del precio del dolar si el API falla
else:
    dolar = input("""
    Ingrese precio del dolar: """)
    dolar =validar(dolar)


# Inicia programa
while True:
    os.system("cls")
    print (f"""
    CASA DE EMPANADAS
    Precio de cada empanada: ${dolar} """)
    opcion = (input ("""
    1 - Tomar pedido
    2 - Salir
    Que desea realizar: """))

    opcion = validar(opcion)

    # Tomar pedido
    if opcion == 1:        
        cliente = input("""
    DNI del cliente sin puntos (o ingrese 0): """)
        cliente =validar(cliente)

        EnCompra = True # para volver al incio de este while si se desea modificar el pedido
        while EnCompra == True: # Si se cancela o confirma la compra, EnCompra == False y se sale del bucle
            os.system("cls")

            # Ingresar pedido
            print("""
    ----- Cantidad de empanadas -----""")
            jyq = input("""
    Cantidad de empanadas de JyQ: """)
            jyq =validar(jyq)
            carne = input("""
    Cantidad de empanadas de Carne: """)
            carne =validar(carne)
            humita = input("""
    Cantidad de empanadas de Humita: """)
            humita =validar(humita)
            monto = (jyq + carne + humita)*dolar
            
            os.system("cls")
            
            # Resumen del pedido
            print(f"""
    PEDIDO:
    {jyq} empadanadas de JyQ
    {carne} empanadas de Carne
    {humita} empanadas de humita
    Total: ${monto}
    """)

            # Opciones de compra
            while True: 
                opcion2 = input("""
    1 - Confirmar pedido
    2 - Modificar pedido
    3 - Cancelar pedido 
    Que desea hacer: """)

                opcion2 = validar (opcion2)
                
                # Confirmar pedido
                if opcion2 == 1:
                    confirmar_pedido(monto)
                    registrar_pedido(cliente, jyq, carne, humita, monto)
                    EnCompra = False ### Para salir del bucle Tomar Pedido
                    break

                # Modificar pedido
                elif opcion2 == 2: ### Aca no se setea compra para que se vuelva a hacer el pedido
                    os.system("cls")
                    break
                
                # Cancelar pedido
                elif opcion2 == 3:
                    print("""
    Pedido cancelado
            """)
                    input("""
    Presione ENTER para continuar...""")
                    os.system("cls")
                    EnCompra = False ### Para salir del bucle Tomar Pedido
                    break

                else:
                    print("""
    Ingrese una opción válida""")

    elif opcion == 2:
        break
    
    else:
        print("""
    Ingrese una opción válida""")
