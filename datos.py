
nems = {"ADCA":["2-89", "2-99", "3-B2"], "ADCB":["2-C9", "2-D9", "3-F9"], "ADDA":["2-8B", "2-9B", "3-BB"], "ADDB":["2-CB", "2-DB", "3-FB"], "ADDD":["2-C3", "2-D3", "3-F3"], "ANDA":["2-84", "2-94", "3-B4"], "ANDB":["2-C4", "2-D4", "3-F4"], "ANDCC":["2-10"], "ASL":[None, None, "3-78"], "ASR":[None, None, "3-77"], "BCLR":[None, "3-4D", "4-1D"], "BITA":["2-85", "2-95", "3-B5"]}
inherentes = {"ABA": "1806", "ASLA" : "48", "ASLB": "58", "ASLD": "59", "ASRA":"47", "ASRB":"57", "BGND":"00"}
rels = {"BCC":"24", "BCS":"25", "BEQ":"27", "BGE":"2C", "BGT":"2E", "BHI":"22", "BHS":"24"}

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
            
            diversos = nems[self.palabra][0]
            self.codigo += nems[self.palabra][-tam:]

        elif(self.palabra in inherentes):
            pass
        
        elif(self.palabra in rels):
            pass


    

