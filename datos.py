
nems = {"ADCA":["2-89", "2-99", "3-B2"], "ADCB":["2-C9", "2-D9", "3-F9"], "ADDA":["2-8B", "2-9B", "3-BB"], "ADDB":["2-CB", "2-DB", "3-FB"], "ADDD":["3-C3", "2-D3", "3-F3"], "ANDA":["2-84", "2-94", "3-B4"], "ANDB":["2-C4", "2-D4", "3-F4"], "ANDCC":["2-10"], "ASL":[None, None, "3-78"], "ASR":[None, None, "3-77"], "BCLR":[None, "3-4D", "4-1D"], "BITA":["2-85", "2-95", "3-B5"], "JMP" : [None, None, "3-06"], "CLR" : [None, None, "3-79"]}
# 0 - IMM     1 - DIR     2 - EXT
inherentes = {"ABA": "1806", "ASLA" : "48", "ASLB": "58", "ASLD": "59", "ASRA":"47", "ASRB":"57", "BGND":"00"}
rels = {"BCC":"24", "BCS":"25", "BEQ":"27", "BGE":"2C", "BGT":"2E", "BHI":"22", "BHS":"24", "BNE" : "26"}
rels9 = {"DBNE": "20" , "IBNE": "A0", "IBEQ": "80" , "DBEQ": "00" }
# [ A = 0 , B = 1 , D = 4 , X = 5 , Y = 6 , SP = 7 ] TODOS EMPIEZAN CON 04
rel16 = {"LBNE" : "1826"}
indexados = {"LDAA" : "A6" , "JMP" : "05", "ASL" : "68", "CMPA" : "B1"}

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
        if(self.palabra in nems and self.error == None and len(self.parametro) == 1 and self.direccionamiento == False):

            if(len(self.parametro[0]) == 1 and self.codigo == nems[self.palabra][1][2:]):
                self.codigo += "0"
            elif(len(self.parametro[0]) < 4 and self.codigo == nems[self.palabra][2][2:]):
                for i in range(len(self.parametro[0]), 4):
                    self.codigo += "0"
            

            self.codigo += self.parametro[0]
        
        elif(self.palabra in nems and self.error == None and len(self.parametro) == 1 and self.direccionamiento):
            xd = nems[self.palabra][0][0]
            for i in range(len(self.parametro[0]), (int(xd) - len(self.codigo) //2 ) * 2):
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

        elif(self.palabra in rels9):
            self.calcular_rel9()
        
        elif(self.palabra in rel16):
            self.cal_rel16()

        pass


    

    def calcular_relativos(self):
        resta = int(self.parametro[0], 16) - int(self.direccion,16) - 2
        if(resta < 0 and abs(resta) <= 128):
            nuevo_num = 256 + resta
            
            final = hex(nuevo_num).replace("0x", "").upper()
            if(len(final) == 1):
                final = "F" + final
            return final
        elif(resta >= 0 and resta <= 127):
    
            final = hex(resta).replace("0x", "").upper()
            if(len(final) == 1):
                final = "0" + final

            return final 
        else:
            self.error = "Fuera de Rango"
            return ""
        pass

    def calcular_rel9(self):
        temp = rels9[self.palabra]

        if(self.error != None):
            return

        if(self.parametro[1] == ""):
            self.parametro[1] = "0"

        if(int(self.parametro[1], 16) < 0):
            temp = hex(int(temp, 16) + 16).replace("0x", "").upper()
        

        if(self.parametro[0] == "B"):
            temp = hex(int(temp, 16) + 1).replace("0x", "").upper()
            
        elif(self.parametro[0] == "D"):
            temp = hex(int(temp, 16) + 4).replace("0x", "").upper()

        elif(self.parametro[0] == "X"):
            temp = hex(int(temp, 16) + 5).replace("0x", "").upper()

        elif(self.parametro[0] == "Y"):
            temp = hex(int(temp, 16) + 6).replace("0x", "").upper()

        elif(self.parametro[0] == "SP"):
            temp = hex(int(temp, 16) + 7).replace("0x", "").upper()

        if(len(temp) == 1):
            temp = "0" + temp

        self.codigo += temp

        resta = hex(int(self.parametro[1], 16) - int(self.direccion,16) - 3).replace("0x", "").upper()

        if(int(resta, 16) < 0):
            if(int(resta, 16) >= -256):
                resta = hex(256 + int(resta, 16)).replace("0x", "").upper()

            else: 
                self.error = "Fuera de Rango"

        if(len(resta) > 2):
            self.error = "Fuera de Rango"

        elif(len(resta) == 1):
            resta = "0" + resta

        self.codigo += resta[-2:]

        pass

    def cal_rel16(self):

        resta = int(self.parametro[0], 16) - int(self.direccion,16) - 4

        if(resta < 0 and abs(resta) <= 32768):

            nuevo_num = 65536 + resta
            final = hex(nuevo_num).replace("0x", "").upper()

            self.codigo =  rel16[self.palabra] + final 

        elif(resta >= 0 and resta <= 32767):

            final = hex(resta).replace("0x", "").upper()
            for i in range(len(final), 4):
                final = "0" + final

            self.codigo +=  final   
        pass


    

