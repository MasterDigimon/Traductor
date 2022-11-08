from ast import For
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
            etiquetas = primera_lectura(archivo)
            archivo.close()
            archivo = open(name, "r")
            segunda_lectura(archivo, etiquetas)
            
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
        
        for ch in linea:
            if(ch == " " and cont == 1):
                cont = 2
            elif(ch != " " and cont == 0):
                cont += 1
                palabra += ch
            elif(((ch == ":" or ch == "\t")or ch == "\t")and cont == 1):
                #etiquetas[palabra] = direccion
                etiqueta = palabra
                palabra = ""
                cont = 0
            elif(ch == '\n' or ch == '\t'):
                pass
            elif(ch == '\n' or ch == '\t'):
                pass
            elif(ch != " " and cont == 1):
                palabra += ch
            elif(ch == "," and cont >= 2):
                cont += 1
                parametro.append("")
            elif(ch != " " and cont >= 2):
                parametro[cont - 2] += ch
            

        palabra = palabra.replace('\n', '')
        palabra = palabra.replace('\t', '')


        if(parametro[0] != "" and len(parametro) == 1):
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
                            #lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                            direccion = suma_direcciones(direccion, dato[0])

                    elif(nemonico[1] != None):
                        dato = nemonico[1]
                        tam = (int(dato[0]) - 1) * 2
                        
                        #lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda DIR
                        direccion = suma_direcciones(direccion, dato[0])

                    elif(nemonico[2] != None):
                        dato = nemonico[2]
                        tam = (int(dato[0]) - 2) * 2

                        #lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda EXT
                        direccion = suma_direcciones(direccion, dato[0])

                    else: #ERROR 
                        dato = nemonico[0]
                        tam = (int(dato[0]) - 1) * 2
                        #lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                        direccion = suma_direcciones(direccion, dato[0])
                        pass
                elif(palabra == "FCC"):
                    codigo = ""
                    
                    for i in range(1, len(parametro[0]) -1):
                        temp =  hex(ord(parametro[0][i])).replace("0x", "").upper()
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp
                    

                    #lineas.append( Linea("", "", False, None, direccion, codigo)) 
                    direccion = suma_direcciones(direccion, len(codigo) / 2)
                pass


#------------------------------------------------------------- PARAMETROS VÁLIDOS -----------------------------------------------------------------
                
            elif(palabra == "ORG"):
                direccion = x[0]
                #lineas.append(Linea(palabra, x, False, None, "", ""))

            elif(palabra == "EQU"):
                etiquetas[etiqueta] = transformar_parametro(parametro[0])
                #lineas.append(Linea("", "", False, None, "", ""))
                pass

            elif(palabra == "DC.B"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo

                #lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 1)

            elif(palabra == "DC.W"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "0000"
                elif(int(x[0], 16)):
                    codigo += x[0][-4:]
                    for i in range(len(codigo), 4):
                        codigo = "0" + codigo

                #lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 2)


            elif(palabra == "BSZ"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                
                for i in range(0,int (parametro[0])):
                    codigo += "00"
                    
                #lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, len(codigo)/ 2)
            
            elif(palabra == "FCB"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo

                #lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 1)

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
                            #lineas.append(Linea(palabra, x, True, None, direccion, dato[-tam:])) #Guarda IMM
                            
                            direccion = suma_direcciones(direccion, dato[0])
                        
                        elif(nemonico[1] != None):
                            dato = nemonico[1]
                            tam = (int(dato[0]) - 1) * 2
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda DIR
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[2] != None):
                            dato = nemonico[2]
                            tam = (int(dato[0]) - 2) * 2

                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append( Linea(palabra, "", False, "Parametro Invalido", direccion, dato[-tam:])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR 
                            dato = nemonico[0]
                            tam = (int(dato[0]) - 1) * 2

                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append(Linea(palabra, "", True, "Parametro Invalido", direccion, dato[-tam:])) #Guarda IMM con ERROR de Parametro
                            direccion = suma_direcciones(direccion, dato[0])
                            pass

                    elif(len(x[0]) <= 2):
                        if(nemonico[1] != None):
                            dato = nemonico[1]
                            tam = (int(dato[0]) - 1) * 2
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append( Linea(palabra, x, False, None, direccion, dato[-tam:])) #Guarda DIR
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[2] != None):
                            dato = nemonico[2]
                            tam = (int(dato[0]) - 2) * 2
                            x[0] = "00" + x[0]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append( Linea(palabra, x, False, None, direccion, dato[-tam:])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR 

                            pass
                    
                    elif(len(x[0]) <= 4):
                        if(nemonico[2] != None):
                            dato = nemonico[2]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append(Linea(palabra, x, False, None, direccion, dato[2:len(dato)])) #Guarda EXT
                            direccion = suma_direcciones(direccion, dato[0])

                        elif(nemonico[1] != None):
                            dato = nemonico[1]
                            
                            if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                            #lineas.append(Linea(palabra, x, False, "Fuera de Rango", direccion, dato[2:len(dato)])) #Guarda DIR con ERROR
                            direccion = suma_direcciones(direccion, dato[0])

                        else: #ERROR

                            pass


                elif(palabra in inherentes):
                    
                    if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                    #lineas.append(Linea(palabra, x, False, "Parametro Invalido", direccion, inherentes[palabra])) #Guarda INH con error
                    direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

                elif(palabra in rels):  #
                    
                    if(len(x[0]) <= 4):

                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        #lineas.append(Linea(palabra, x, False, None, direccion, rels[palabra])) #Guard REL
                    
                    else:
                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        #lineas.append(Linea(palabra, x,None , "Fuera de Rango", direccion, rels[palabra])) #Guarda REL con ERROR
                    direccion = suma_direcciones(direccion, 2)

                elif(palabra in rel16):  #
                    
                    if(len(x[0]) <= 4):

                        if(etiqueta != ""):
                            etiquetas[etiqueta] = direccion
                        #lineas.append(Linea(palabra, x, False, None, direccion, rel16[palabra])) #Guard REL16
                    
                    else:
                        if(etiqueta != ""):
                            etiquetas[etiqueta] = direccion
                        #lineas.append(Linea(palabra, x,None , "Fuera de Rango", direccion, rel16[palabra])) #Guarda REL16 con ERROR

                    direccion = suma_direcciones(direccion, 4)

#------------------------------------------------------------- PARAMETROS MULTIPLES -----------------------------------------------------------------

        elif(len(parametro) > 1):
            codigo = ""
            temp = ""
            if(palabra == "DC.B"):
                for p in parametro:
                    if(p == ""):
                        codigo += "00"
                    elif(int(p) <= 255):
                        temp += hex(int(p)).replace("0x", "")[-2:]
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp
                        temp = ""
                #lineas.append(Linea(palabra, parametro, None, None, direccion, codigo.upper()))
                direccion = suma_direcciones(direccion, len(parametro))

            elif(palabra ==  "DC.W"):
                for p in parametro:
                    temp = ""
                    if(p == ""):
                        codigo += "0000"
                    elif(int(p) <= 65535):
                        temp += hex(int(p)).replace("0x", "")[-4:]
                        if(len(temp) < 4):
                            for i in range (len(temp), 4):
                                codigo += "0"
                        codigo += temp
                #lineas.append(Linea(palabra, parametro, None, None, direccion, codigo.upper()))
                direccion = suma_direcciones(direccion, len(parametro)*2)
                pass

            elif(palabra == "FILL"):
                codigo = ""
                if(len(parametro) > 2):

                    pass
                else:
                    for i in range(0, int(parametro[1])):
                        temp = hex(int(parametro[0])).replace("0x", "").upper()[-2:]
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp

                    #lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                    direccion = suma_direcciones(direccion, len(codigo)/2)
                
            
            
            elif(palabra in rels9 and len(parametro) == 2):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = "04"

                x = transformar_parametro(parametro[1])

                if(parametro[0] in ["A", "B", "D", "X", "Y", "SP"] and x != False):
                    parametro[1] = x
                    #lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                else:
                    #lineas.append(Linea(palabra, parametro, None, "Parametro Invalido", direccion, codigo))
                    pass

                direccion = suma_direcciones(direccion, 3)
                
                pass
            
            elif(palabra in indexados):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion

                codigo = ident_index(parametro)
                if(codigo == False):
                    #lineas.append(Linea(palabra, parametro, None, "Parametro Invalido", direccion, codigo))
                    direccion = suma_direcciones(direccion, 2)

                else:
                    codigo = indexados[palabra] + codigo

                    #lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                    direccion = suma_direcciones(direccion, len(codigo) / 2)

                pass



#------------------------------------------------------------- SIN PARAMETROS -----------------------------------------------------------------
        elif(palabra == "DC.B"):

            #lineas.append(Linea(palabra, parametro, None, None, direccion, "00"))
            direccion = suma_direcciones(direccion, 1)


                

        elif(palabra ==  "DC.W"):
                
            #lineas.append(Linea(palabra, parametro, None, None, direccion, "0000"))
            direccion = suma_direcciones(direccion, 2)

        elif(palabra == "ORG"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            #lineas.append( Linea(palabra, parametro, False, "Parametro Invalido", direccion, None))
            pass

        elif(palabra == "END"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            #lineas.append( Linea(palabra, "", False, None, direccion, ""))
            pass

        elif(palabra == "START"):
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            #lineas.append( Linea(palabra, "", False, None, direccion, ""))
            direccion = "0000"
            pass



        elif(palabra in inherentes):
            
            if(etiqueta != ""):
                etiquetas[etiqueta] = direccion
            #lineas.append(Linea(palabra, x, False, None, direccion, inherentes[palabra])) #Guarda INH
            direccion = suma_direcciones(direccion, len(inherentes[palabra]) / 2)

        cont_lineas += 1
        palabra = ""
        parametro = [""]
        cont = 0
        etiqueta = ""

    return etiquetas

def segunda_lectura(archivo, nuevas_et):
    etiquetas = nuevas_et
    direccion = None
    palabra = ""
    parametro = [""]
    cont = 0
    cont_lineas = 0
    lineas = []
    nemonico = []
    etiqueta = ""

    for linea in archivo:
        
        for ch in linea:
            if(ch == " " and cont == 1):
                cont = 2
            elif(ch != " " and cont == 0):
                cont += 1
                palabra += ch
            elif(((ch == ":" or ch == "\t")or ch == "\t")and cont == 1):
                #etiquetas[palabra] = direccion
                etiqueta = palabra
                palabra = ""
                cont = 0
            elif(ch == '\n' or ch == '\t'):
                pass
            elif(ch == '\n' or ch == '\t'):
                pass
            elif(ch != " " and cont == 1):
                palabra += ch
            elif(ch == "," and cont >= 2):
                cont += 1
                parametro.append("")
            elif(ch != " " and cont >= 2):
                parametro[cont - 2] += ch
            

        palabra = palabra.replace('\n', '')
        palabra = palabra.replace('\t', '')

        if(parametro[0] != "" and len(parametro) == 1):
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
                elif(palabra == "FCC"):
                    codigo = ""
                    
                    for i in range(1, len(parametro[0]) -1):
                        temp =  hex(ord(parametro[0][i])).replace("0x", "").upper()
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp
                    

                    lineas.append( Linea("", "", False, None, direccion, codigo)) 
                    direccion = suma_direcciones(direccion, len(codigo) / 2)
                pass


#------------------------------------------------------------- PARAMETROS VÁLIDOS -----------------------------------------------------------------
                
            elif(palabra == "ORG"):
                direccion = x[0]
                lineas.append(Linea(palabra, x, False, None, "", ""))

            elif(palabra == "EQU"):
                etiquetas[etiqueta] = transformar_parametro(parametro[0])
                lineas.append(Linea("", "", False, None, "", ""))
                pass

            elif(palabra == "DC.B"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo

                lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 1)

            elif(palabra == "DC.W"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "0000"
                elif(int(x[0], 16)):
                    codigo += x[0][-4:]
                    for i in range(len(codigo), 4):
                        codigo = "0" + codigo

                lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 2)


            elif(palabra == "BSZ"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                
                for i in range(0,int (parametro[0])):
                    codigo += "00"
                    
                lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, len(codigo)/ 2)
            
            elif(palabra == "FCB"):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = ""
                if(parametro[0] == ""):
                    codigo += "00"
                elif(int(x[0], 16) <= 255):
                    codigo += x[0][-2:]
                    if(len(codigo) == 1):
                        codigo = "0" + codigo

                lineas.append(Linea("", "", False, None, direccion,codigo))
                direccion = suma_direcciones(direccion, 1)

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
                            lineas.append(Linea(palabra, x, True, None, direccion, dato[2:])) #Guarda IMM
                            
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
                        lineas.append(Linea(palabra, x,None , "Fuera de Rango", direccion, rels[palabra])) #Guarda REL con ERROR
                    direccion = suma_direcciones(direccion, 2)

                elif(palabra in rel16):  #
                    
                    if(len(x[0]) <= 4):

                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        lineas.append(Linea(palabra, x, False, None, direccion, rel16[palabra])) #Guard REL16
                    
                    else:
                        if(etiqueta != ""):
                                etiquetas[etiqueta] = direccion
                        lineas.append(Linea(palabra, x,None , "Fuera de Rango", direccion, rel16[palabra])) #Guarda REL16 con ERROR

                    direccion = suma_direcciones(direccion, 4)

#------------------------------------------------------------- PARAMETROS MULTIPLES -----------------------------------------------------------------

        elif(len(parametro) > 1):
            for p in range(0, len(parametro)):
                if(parametro[p] in etiquetas): #Etiquetas como parametro
                    parametro[p] = "$" + etiquetas[parametro[p]]
            codigo = ""
            temp = ""
            if(palabra == "DC.B"):
                for p in parametro:
                    if(p == ""):
                        codigo += "00"
                    elif(int(p) <= 255):
                        temp += hex(int(p)).replace("0x", "")[-2:]
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp
                        temp = ""
                lineas.append(Linea(palabra, parametro, None, None, direccion, codigo.upper()))
                direccion = suma_direcciones(direccion, len(parametro))

            elif(palabra ==  "DC.W"):
                for p in parametro:
                    temp = ""
                    if(p == ""):
                        codigo += "0000"
                    elif(int(p) <= 65535):
                        temp += hex(int(p)).replace("0x", "")[-4:]
                        if(len(temp) < 4):
                            for i in range (len(temp), 4):
                                codigo += "0"
                        codigo += temp
                lineas.append(Linea(palabra, parametro, None, None, direccion, codigo.upper()))
                direccion = suma_direcciones(direccion, len(parametro)*2)
                pass

            elif(palabra == "FILL"):
                codigo = ""
                if(len(parametro) > 2):

                    pass
                else:
                    for i in range(0, int(parametro[1])):
                        temp = hex(int(parametro[0])).replace("0x", "").upper()[-2:]
                        if(len(temp) == 1):
                            codigo += "0"
                        codigo += temp

                    lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                    direccion = suma_direcciones(direccion, len(codigo)/2)
                
            
            
            elif(palabra in rels9 and len(parametro) == 2):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion
                codigo = "04"

                x = transformar_parametro(parametro[1])

                if(parametro[0] in ["A", "B", "D", "X", "Y", "SP"] and x != False):
                    parametro[1] = x
                    lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                else:
                    lineas.append(Linea(palabra, parametro, None, "Parametro Invalido", direccion, codigo))

                direccion = suma_direcciones(direccion, 3)
                
                pass
            
            elif(palabra in indexados):
                if(etiqueta != ""):
                    etiquetas[etiqueta] = direccion

                codigo = ident_index(parametro)
                if(codigo == False):
                    lineas.append(Linea(palabra, parametro, None, "Parametro Invalido", direccion, codigo))
                    direccion = suma_direcciones(direccion, 2)

                else:
                    codigo = indexados[palabra] + codigo

                    lineas.append(Linea(palabra, parametro, None, None, direccion, codigo))
                    direccion = suma_direcciones(direccion, len(codigo) / 2)

                pass



#------------------------------------------------------------- SIN PARAMETROS -----------------------------------------------------------------
        elif(palabra == "DC.B"):

            lineas.append(Linea(palabra, parametro, None, None, direccion, "00"))
            direccion = suma_direcciones(direccion, 1)


                

        elif(palabra ==  "DC.W"):
                
            lineas.append(Linea(palabra, parametro, None, None, direccion, "0000"))
            direccion = suma_direcciones(direccion, 2)

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

def transformar_parametro(parametro):
    if(parametro[0] == "$"):#Comprueba Hexadecimales
        num = comp_hex(parametro)
        if(num == False):
            return False
        
    elif(parametro[0] == "@"):#Comprueba Octales
        num = oct_hex(parametro)
        if(num == False):
            return False
        
    elif(parametro[0] == "%"): #Comprueba Binarios
        num = bin_hex(parametro)
        if(num == False):
            return False
        

    else: #Comprueba Decimales
        num = dec_hex(parametro)
        if(num == False):
            return False

    return num


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

def ident_index(parametros):
    codigo = ""
    corcehetes = False
    negativo = False 
    p_f4 = None
    aa = None
    num = None
    if(parametros[0] == ""):
        parametros[0] = "0"

    if("[" == parametros[0][0] and "]" == parametros[1][len(parametros[1]) - 1]):
        corcehetes = True
        parametros[0] = parametros[0][1:]
        parametros[1] = parametros[1][:len(parametros[1]) - 1]
    
    if(len(parametros[0]) >= 2):
        if("-" == parametros[0][0]):
            negativo = True
            parametros[0] = parametros[0][1:]

        elif("-" == parametros[0][1] and parametros[0][0] in "$@%"):
            negativo = True
            parametros[0] = parametros[0][1:] + parametros[0][2:]
    
    if("-" in parametros[1] and negativo == False):

        if(parametros[1][0] == "-"):
            negativo = True
            parametros[1] = parametros[1].replace("-", "", 1)
            p_f4 = "0"

        elif(parametros[1][-1] == "-"):
            negativo = True
            p_f4 = "1"
            parametros[1] = parametros[1].replace("-", "", 1)

    elif("+" in parametros[1] and negativo == False):

        if(parametros[1][0] == "+"):
            p_f4 = "0"
            parametros[1] = parametros[1].replace("+", "", 1)

        elif(parametros[1][-1] == "+"):
            p_f4 = "1"
            parametros[1] = parametros[1].replace("+", "", 1)


    if(parametros[1] == "Y"):
        rr = "01"
    elif(parametros[1] == "X"):
        rr = "00"
    elif(parametros[1] == "SP"):
        rr = "10"
    elif(parametros[1] == "PC"):
        rr = "11"
    
    else:
        return False
    
    if(parametros[0] == "D"):
        aa = "10"

    elif(parametros[0] == "A"):
        aa = "00"

    elif(parametros[0] == "B"):
        aa = "01"

    else:
        num = transformar_parametro(parametros[0])


    if(num == False):
        return False
    
    if(aa != None and corcehetes == False): #FORMULA 5
        codigo = hex(int("111" + rr + "1" + aa, 2)).replace("0x", "").upper()

    elif(aa == "10"): #FORMULA 6
        codigo = hex(int("111" + rr + "111", 2)).replace("0x", "").upper()


    elif(int(num, 16) <= 15 and negativo == False and corcehetes == False and p_f4 == None):#FORMULA 1 Positiva
        codigo  = rr + "00"

        for i in range(len(bin(int(num, 16)).replace("0b", "")), 4):
            codigo += "0"
        
        codigo += bin(int(num, 16)).replace("0b", "")
        codigo = hex(int(codigo, 2)).replace("0x", "").upper()

    elif(int(num, 16) <= 16 and negativo == True and corcehetes == False and p_f4 == None):#FORMULA 1 Negativa
        codigo  = rr + "01"
        num = hex(16 - int(num, 16)).replace("0x", "").upper()

        for i in range(len(bin(int(num, 16))), 4):
            codigo += "0"

        codigo = hex(int(codigo, 2)).replace("0x", "").upper()
        codigo += num
        
        
        
    elif(int(num, 16) <= 65535 and negativo == False and corcehetes == False and p_f4 == None):#FORMULA 2 POSITIVA
        codigo  = "111" + rr + "0"
        if(int(num, 16) <= 255):
            codigo += "00"
        else:
            codigo += "10"

        if(len(num) % 2 == 1):
            num = "0" + num
        
        codigo = hex(int(codigo, 2)).replace("0x", "").upper() + num

    elif(int(num, 16) <= 65536 and negativo and corcehetes == False and p_f4 == None):#FORMULA 2 NEGATIVA
        codigo  = "111" + rr + "0"
        if(int(num, 16) <= 256):
            num = hex(256 - int(num, 16)).replace("0x", "").upper()
            codigo += "01"
        else:
            num = hex(65536 - int(num, 16)).replace("0x", "").upper()
            codigo += "11"

        
        if(len(num) % 2 == 1):
            num = "0" + num

        codigo = hex(int(codigo, 2)).replace("0x", "").upper() + num
    
    elif(int(num, 16) <= 65535 and negativo == False and corcehetes == True): #FORMULA 3
        codigo  = hex(int("111" + rr + "011", 2)).replace("0x", "").upper()

        for i  in range(len(num), 4):
            codigo += "0"
        codigo += num

    elif(int(num, 16) <= 8 and int(num, 16) > 0 and p_f4 != None and rr != "11"): #FORMULA 4
        codigo = hex(int(rr + "1" + p_f4, 2)).replace("0x", "").upper()
        
        if(negativo):
            codigo += hex(16 - int(num, 16)).replace("0x", "").upper()
        else: 
            codigo += hex(int(num, 16) - 1).replace("0x", "").upper()
    elif(int(num, 16) <= 8 and int(num, 16) > 0 and p_f4 != None and rr == "11"):
        return False
    
    elif(negativo and corcehetes):
        return False

    return codigo


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
    for i in range(len(dirZ), 4):
        dirZ = "0" + dirZ
    return dirZ.upper()


main()