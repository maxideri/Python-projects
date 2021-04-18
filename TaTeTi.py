def play_game(): #Convoco el juego
    print("Bienvenido al Ta - Te - Ti de Maxi")
    
    Tablero=list(range(1,10)) # genero el tablero de juego
    ganador="No"
    
    # para mostrar el tablero de juego
    def mostrar_tablero():
        print (Tablero[0:3])
        print (Tablero[3:6])
        print (Tablero[6:9])
    
    # para chequear si hay 3 en linea
    def check():
        matriz_chequeo=["X","X","X","O","O","O"]
        #inicio de chequeo horizontal
        ha=0
        hb=3
        #inicio de chequeo vertical
        va=0
        vb=7
        while hb < 10:
            if  matriz_chequeo[0:3]== Tablero[ha:hb] or matriz_chequeo[0:3] == Tablero[va:vb:3] or matriz_chequeo[0:3] == Tablero[0:9:4] or matriz_chequeo[0:3] == Tablero[2:7:2] or matriz_chequeo[3:6]== Tablero[ha:hb] or matriz_chequeo[3:6] == Tablero[va:vb:3] or matriz_chequeo[3:6] == Tablero[0:9:4] or matriz_chequeo[3:6] == Tablero[2:7:2]:
                ganador="Si"
                return True
            else:
                ha=ha+3
                hb=hb+3
                va=va+1
                vb=vb+1
        return False
    
    # juego empatado. quieren volver a jugar?
    def jugar_again():
        print ("Han empatado")
        again=input ("Quieren jugar de nuevo: ").capitalize()
        if again == "Si":
            player()
        elif again == "No":
            print ("Esperamos que vuelvan a jugar pronto")
            return 
        else:
            print ("Por vafor, elige entre ´Si´ o ´No´")
            jugar_again()
 
    # Valido X o O
    def player():
        x_o=["X","O"]
        player_1= input("Jugador 1: Quieres ser X o O? ").upper()
        if player_1 in x_o:
            ganador = "No"
            # le asigno al jugador 2 lo que no eligio el jugador 1
            x_o.remove(player_1) 
            player_2=x_o[0]
            
            #armo una lista con las elecciones de los dos jugadores
            players=[player_1,player_2]
            mostrar_tablero()
            
            # itinero sobre cada jugdor por ronda
            var=[1,2] # numero de los jugadores
            turno=0 # ronda de juego
            elegidos=[] # almaceno todos los numeros que eligen los usuarios
            while len(elegidos)!=9: # juego hasta que se hayan elegido nueve numeros distintos, es decir se hayan ocupado todas las posiciones
                posicion=int(input(f"Tu turno jugador {var[turno%2]}. En que posicion lo ubicas? ")) # rondas pares juega J1, impares juega J2
                if posicion <10: #chequeo que eligan un numero dentro del rango
                    if posicion not in elegidos: # chequeo que la posicion no se haya jugado
                        Tablero[posicion-1]=players[turno%2]
                        mostrar_tablero()
                        turno=turno+1
                        elegidos.append(posicion)
                        # Chequeo si con este movimiento el jugador gano
                        if check() == True:
                            print ("Felicitaciones, has ganado!")
                            return
                    else:
                        print ("Ya esta elegida ese posicion. Selecciona otro numero del 1 al 9")
                    continue
                else: # si no eligio un numero del 1 a 9
                    print ("Elige un numero del 1 a 9")
                continue
            jugar_again()
            
        else: # Si no eligio entre X o O
            print ("Elija entre X o O por favor")
            player()
    
    # Estas listo para jugar?
    def jugar():
        listo = input("Estas listo para jugar?: Selecciona Si o No ").capitalize()
        if listo == "Si":
            player()

        elif listo == "No":
            print ("Esperamos que pronto te animes a jugar")
            return 

        else:
            print ("Por vafor, elige entre ´Si´ o ´No´")
            jugar()
    
    jugar()
