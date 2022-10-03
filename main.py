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
    parametro = ""
    cont = 0
    cont_lineas = 0
    lineas = []
    nemonico = []

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
                etiquetas[palabra] = direccion
                palabra = ""
                cont = 0
            elif(ch != " " and cont == 1):
                palabra += ch
            elif(ch != " " and cont == 2):
                parametro += ch

        if(parametro != ""):
            if(parametro in etiquetas): #Etiquetas como parametro
                parametro = etiquetas[parametro]
                pass
            else:
                x = ident_parametro(parametro)
                if(x == False):             #ERROR Parametro invalido
                    pass
                    
                elif(palabra == "ORG"):
                    direccion = x
                    lineas.append(Linea(palabra, x, False, None, "", ""))

                else:
                    if(palabra in nems):
                        nemonico = nems[palabra]
                        if(x[0] == "#"):
                            if(nemonico[0] != None):
                                dato = nemonico[0]
                                lineas.append(Linea(palabra, x, True, None, direccion, dato[2-len(dato)])) #Guarda IMM
                                direccion = suma_direcciones(direccion, dato[0])


                        elif(len(x) <= 2):
                            if(nemonico[1] != None):
                                dato = nemonico[1]
                                
                                lineas.append( Linea(palabra, x, False, None, direccion, dato[2:len(dato)])) #Guarda DIR
                                direccion = suma_direcciones(direccion, dato[0])

                            elif(nemonico[2] != None):
                                dato = nemonico[2]
                                
                                lineas.append( Linea(palabra, x, False, None, direccion, dato[2:len(dato)])) #Guarda EXT
                                direccion = suma_direcciones(direccion, dato[0])

                            else: #ERROR 

                                pass
                        
                        elif(len(x) <= 4):
                            if(nemonico[2] != None):
                                dato = nemonico[2]
                                
                                lineas.append(Linea(palabra, x, False, None, direccion, dato[2:len(dato)])) #Guarda EXT
                                direccion = suma_direcciones(direccion, dato[0])

                            elif(nemonico[1] != None):
                                dato = nemonico[1]
                                
                                lineas.append(Linea(palabra, x, False, "Fuera de Rango", direccion, dato[2:len(dato)])) #Guarda DIR con ERROR
                                direccion = suma_direcciones(direccion, dato[0])

                            else: #ERROR

                                pass


                    elif(palabra in inherentes):
                        
                        lineas.append(Linea(palabra, x, False, "Parametro Invalido", direccion, inherentes[palabra])) #Guarda INH con error
                        direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

                    elif(palabra in rels):  #
                        direccion = suma_direcciones(direccion, 2)
                        if(len(x) <= 4):
                            lineas.append(Linea(palabra, x, False, None, direccion, rels[palabra])) #Guard REL
                        
                        else:
                            lineas.append(Linea(palabra, x, "Fuera de Rango", None, direccion, rels[palabra])) #Guarda REL con ERROR


        elif(palabra == "ORG"):
            lineas.append( Linea(palabra, parametro, False, "Parametro Invalido", direccion, None))
            pass

        elif(palabra == "END"):

            pass

        elif(palabra in inherentes):
            
            lineas.append(Linea(palabra, x, False, None, direccion, inherentes[palabra])) #Guarda INH
            direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

        cont_lineas += 1
        palabra = ""
        parametro = ""
        cont = 0

    escritura(lineas, archivo)
            
    pass

def escritura(lineas, original):
    archivo = open("archivo.txt", "w")
    original.seek(0)
    linea_original = ""
    cont = 0
    texto = ""
    for linea in lineas:
        if(linea.error == None):
            texto += str(linea.direccion) + "  " + str(linea.codigo)
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

def busqueda_nem():
    pass

def ident_parametro(parametro):
    n_parametro = ""
    if(parametro[0] == "#"): #Comprueba IMM
        n_parametro += "#"
        parametro = parametro.replace("#", "")

    if(parametro[0] == "$"): #Comprueba Hexadecimales
        num = comp_hex(parametro)
        if(num == False):
            return False
        
        n_parametro += num

    elif(parametro[0] == "@"): #Comprueba Octales
        num = oct_hex(parametro)
        if(num == False):
            return False
        
        n_parametro += num

    elif(parametro[0] == "%"): #Comprueba Binarios
        num = bin_hex(parametro)
        if(num == False):
            return False
        
        n_parametro += num

    else: #Comprueba Decimales
        num = dec_hex(parametro)
        if(num == False):
            return False
        
        n_parametro += num



    return n_parametro

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