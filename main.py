import os
import string
from datos import *


def main():
    f = True
    etiquetas = []
    while(f):
        os.system("cls")
        name = leer_archivo()
        try:
            archivo = open(name, "r")
            primera_lectura(archivo)
            
        except FileNotFoundError:
            print("No se ha encontrado el archivo")
            print("Inserte s para salir, cualquier otra cosa para continuar")
            option = input()
            if(option == "s"):
                f = False
    


    pass

def leer_archivo():
    name = ""
    print("Inserte el nombre del archivo:", end=" ")
    name = input()
    return name



def primera_lectura(archivo):
    etiquetas = {}
    direccion = None
    palabra = ""
    parametro = [""]
    cont = 0
    cont_lineas = 0
    lineas = []
    nemonico = []
    etiqueta = ""

    for linea in archivo:
        linea = linea.replace('\n', '')
        linea = linea.replace('\t', '')
        for ch in linea:
            if(ch == '\n' or ch == '\t'):
                pass
            elif(ch == " " and cont == 1):
                cont = 2
            elif(ch != " " and cont == 0):
                cont += 1
                palabra += ch
            elif(ch == ":" and cont == 1):
                #etiquetas[palabra] = direccion
                etiqueta = palabra
                palabra = ""
                cont = 0
            elif(ch != " " and cont == 1):
                palabra += ch
            elif(ch != " " and cont >= 2):
                parametro[cont - 2] += ch
            elif(ch == "," and cont >= 2):
                cont += 1
                parametro.append("")


        if(parametro[0] != ""):
            for p in range(0, len(parametro)):
                if(parametro[p] in etiquetas): #Etiquetas como parametro
                    parametro[p] = "$" + etiquetas[parametro[p]]
            


            x = ident_parametro(parametro)

#------------------------------------------------------------- PARAMETROS INVÁLIDOS -----------------------------------------------------------------

            if(False == x):             #ERROR Parametro invalido
                if(palabra in nems):
                    nemonico = nems[palabra]
                    if(parametro[0][0] == "#"):
                        if(nemonico[0] != None):
                            dato = nemonico[0]
                            tam = (int(dato[0]) - 1) * 2
                            lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                            direccion = suma_direcciones(direccion, dato[0])

                    elif(nemonico[1] != None):
                        dato = nemonico[1]
                        tam = (int(dato[0]) - 1) * 2
                        
                        lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda DIR
                        direccion = suma_direcciones(direccion, dato[0])

                    elif(nemonico[2] != None):
                        dato = nemonico[2]
                        tam = (int(dato[0]) - 2) * 2

                        lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda EXT
                        direccion = suma_direcciones(direccion, dato[0])

                    else: #ERROR 
                        dato = nemonico[0]
                        tam = (int(dato[0]) - 1) * 2
                        lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                        direccion = suma_direcciones(direccion, dato[0])
                        pass
                pass


#------------------------------------------------------------- PARAMETROS VÁLIDOS -----------------------------------------------------------------
                
            elif(palabra == "ORG"):
                direccion = x[0]
                lineas.append(Linea(palabra, x, False, None, "", ""))

            elif(palabra == "EQU"):
                etiquetas[etiqueta] = parametro
                lineas.append(Linea("", "", False, None, "", ""))
                pass

            else:
                if(palabra in nems):
                    nemonico = nems[palabra]
                    if(x[0][0] == "#"):
                        if(nemonico[0] != None):
                            x[0] = x[0].replace("#", "")
                            dato = nemonico[0]
                            tam = (int(dato[0]) - 1) * 2
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append(Linea(palabra, x, True, None, direccion, dato[-tam:])) #Guarda IMM
                            
                            direccion = suma_direcciones(direccion, dato[0])
                        
                        elif(nemonico[1] != None):
                            dato = nemonico[1]
                            tam = (int(dato[0]) - 1) * 2
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda DIR
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[2] != None):
                            dato = nemonico[2]
                            tam = (int(dato[0]) - 2) * 2

                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR 
                            dato = nemonico[0]
                            tam = (int(dato[0]) - 1) * 2

                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                            direccion = suma_direcciones(direccion, dato[0])
                            pass

                    elif(len(x[0]) <= 2):
                        if(nemonico[1] != None):
                            dato = nemonico[1]
                            tam = (int(dato[0]) - 1) * 2
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append( Linea(palabra, x, False, None, direccion, dato[-tam:])) #Guarda DIR
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[2] != None):
                            dato = nemonico[2]
                            tam = (int(dato[0]) - 2) * 2
                            x[0] = "00" + x[0]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append( Linea(palabra, x, False, None, direccion, dato[-tam:])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR 

                            pass
                    
                    elif(len(x[0]) <= 4):
                        if(nemonico[2] != None):
                            dato = nemonico[2]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append(Linea(palabra, x, False, None, direccion, dato[2:len(dato)])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[1] != None):
                            dato = nemonico[1]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            lineas.append(Linea(palabra, x, False, "Fuera de Rango", direccion, dato[2:len(dato)])) #Guarda DIR con ERROR
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR

                            pass


                elif(palabra in inherentes):
                    
                    if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                    lineas.append(Linea(palabra, x, False, "Parametro Invalido", direccion, inherentes[palabra])) #Guarda INH con error
                    direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

                elif(palabra in rels):  #
                    
                    if(len(x[0]) <= 4):

                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        lineas.append(Linea(palabra, x, False, None, direccion, rels[palabra])) #Guard REL
                    
                    else:
                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        lineas.append(Linea(palabra, x, "Fuera de Rango", None, direccion, rels[palabra])) #Guarda REL con ERROR
                    direccion = suma_direcciones(direccion, 2)

#------------------------------------------------------------- SIN PARAMETROS -----------------------------------------------------------------

        elif(palabra == "ORG"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            lineas.append( Linea(palabra, parametro, False, "Parametro Invalido", direccion, None))
            pass

        elif(palabra == "END"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            lineas.append( Linea(palabra, "", False, None, direccion, ""))
            pass

        elif(palabra == "START"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            lineas.append( Linea(palabra, "", False, None, direccion, ""))
            direccion = "0000"
            pass

        elif(palabra in inherentes):
            
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            lineas.append(Linea(palabra, x, False, None, direccion, inherentes[palabra])) #Guarda INH
            direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

        cont_lineas += 1
        palabra = ""
        parametro = [""]
        cont = 0
        etiqueta = ""

    escritura(lineas, archivo)
            
    pass

def escritura(lineas, original):
    if(os.path.exists("archivo.txt")):
        os.remove("archivo.txt")
    archivo = open("archivo.txt", "w")
    original.seek(0)
    linea_original = ""
    cont = 0
    texto = ""
    for linea in lineas:
        linea.actualizar_codigos()
        if(linea.error == None):
            texto += str(linea.direccion) + "  " + str(linea.codigo)# + str(linea.parametro)
        else:
            texto += str(linea.direccion) + "  " + linea.error
        for i in range(len(texto), 31):
            texto += " "
        linea_original = original.readline()
        linea_original =  linea_original.replace("\t", "      ")
        texto += linea_original
        archivo.write(texto)
        texto = ""
        linea_original = ""
    
    archivo.close()



    archivo.close()

    pass


def ident_parametro(parametro):
    n_parametro = ""
    n_p = []
    for p in parametro:
        if(p[0] == "#"): #Comprueba IMM
            n_parametro += "#"
            p = p.replace("#", "")

        if(p[0] == "$"): #Comprueba Hexadecimales
            num = comp_hex(p)
            if(num == False):
                return False
            
            n_parametro += num

        elif(p[0] == "@"): #Comprueba Octales
            num = oct_hex(p)
            if(num == False):
                return False
            
            n_parametro += num

        elif(p[0] == "%"): #Comprueba Binarios
            num = bin_hex(p)
            if(num == False):
                return False
            
            n_parametro += num

        else: #Comprueba Decimales
            num = dec_hex(p)
            if(num == False):
                return False
            
            n_parametro += num
        
        n_p.append(n_parametro)


    return n_p

def oct_hex(octal:string):
    nuevo = octal.replace("@", "")

    for ch in nuevo:
        if not(ch in "01234567"):
            return False
    
    num = int(nuevo, 8)
    num = hex(num)
    num = num.replace("0x", "")
    return num.upper()

def comp_hex(hex:string):
    nuevo = hex.replace('$', '')

    try:
        num = int(nuevo, 16)
        return nuevo

    except:
        print("Error de conversion")
        return False
    
def bin_hex(bin:string):
    nuevo = bin.replace("%", "")


    for ch in nuevo:
        if not(ch in "01"):
            return False
    
    num = int(nuevo, 2)
    num = hex(num)
    num = num.replace("0x", "")
    return num.upper()

def dec_hex(dec:string):
    for ch in dec:
        if not(ch in "0123456789"):
            return False
    
    num = hex(int(dec))
    num = num.replace("0x", "")
    return num.upper()

def suma_direcciones(dir1, dir2):
    dirX = int(dir1, 16) + int(dir2)
    dirY = hex(dirX)
    dirZ = dirY.replace("0x", "")
    return dirZ.upper()


main()