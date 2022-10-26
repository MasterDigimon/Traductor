
nems = {"ADCA":["2-89", "2-99", "3-B2"], "ADCB":["2-C9", "2-D9", "3-F9"], "ADDA":["2-8B", "2-9B", "3-BB"], "ADDB":["2-CB", "2-DB", "3-FB"], "ADDD":["2-C3", "2-D3", "3-F3"], "ANDA":["2-84", "2-94", "3-B4"], "ANDB":["2-C4", "2-D4", "3-F4"], "ANDCC":["2-10"], "ASL":[None, None, "3-78"], "ASR":[None, None, "3-77"], "BCLR":[None, "3-4D", "4-1D"], "BITA":["2-85", "2-95", "3-B5"]}
# 0 - IMM     1 - DIR     2 - EXT
inherentes = {"ABA": "1806", "ASLA" : "48", "ASLB": "58", "ASLD": "59", "ASRA":"47", "ASRB":"57", "BGND":"00"}
rels = {"BCC":"24", "BCS":"25", "BEQ":"27", "BGE":"2C", "BGT":"2E", "BHI":"22", "BHS":"24"}
rels9 = {"DBNE": "20" , "IBNE": "A0", "IBEQ": "80" , "DBEQ": "00" }
# [ A = 0 , B = 1 , D = 4 , X = 5 , Y = 6 , SP = 7 ] TODOS EMPIEZAN CON 04

class Linea:
    def __init__(self, _palabra, _parametro, _direccionamiento, _error, _direccion, codigo):
        self.palabra = _palabra
        self.parametro = _parametro
        self.direccionamiento = _direccionamiento #Falso / Verdadero
        self.error = _error
        self.direccion = _direccion
        self.codigo = codigo

    def actualizar_codigos(self):
        tam = 0
        if(self.palabra in nems and self.error == None):
            if(len(self.parametro) == 1):
                self.codigo += "0"
            self.codigo += self.parametro[0]

        elif(self.palabra in inherentes):
            pass
        
        elif(self.palabra in rels):
            dato = self.calcular_relativos()
            if(len(dato) == 1):
                self.codigo += "0"
            self.codigo += dato
            pass


    

    def calcular_relativos(self):
        resta = int(self.parametro[0], 16) - int(self.direccion,16) - 2
        if(resta < 0 and abs(resta) <= 128):
            nuevo_num = 255
            for i in range(1, abs(resta)):
                nuevo_num -= 1
            
            final = hex(nuevo_num).replace("0x", "").upper()
            if(len(final) == 1):
                final = "F" + final
            return final
        else:
            pass
        pass

    def calcular_rel9(self):
        temp = rels9[self.palabra]
        if(self.parametro[1] == ""):
            self.parametro[1] = "0"

        if(self.parametro[1] < 0):
            temp = hex(int(temp, 16) + 16).replace("0x", "").upper()
        
        if(self.parametro[0] == "B"):

            pass

        pass


    

