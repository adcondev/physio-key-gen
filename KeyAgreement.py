import BloomFilter as bf
import hashlib as hl
import hmac
import InterPulseInterval as iPI
import numpy as np
from random import randint, shuffle

def fGen(filtRes,filename, start, step, threshold,kbits):
    """Creación de vector de patrones biométricos (Inter Pulse Interval<<IPI>> de ECG) en sensor S.
        El sensor R crea el suyo a la par.
        El vector consta de strings donde cada posición representa una concatenación de 3 IPIs
        de segmentos consecutivas. La diferencia entre cada segmento es de una muestra(360 sps)"""
    F = [iPI.iPulInt(filtRes, filename, start + i*3 - 2, step, threshold, False, kbits) +
        iPI.iPulInt(filtRes, filename, start + i*3 - 1, step, threshold, False, kbits) +
        iPI.iPulInt(filtRes,filename, start + i*3, step, threshold, False, kbits) for i in range(1,featCount + 1)]
    return F
def bfCrea(features,n,p):
    """Creación de filtro de Bloom en sensor S con un array de elementos a agregar al filtro. Toma los
        parametros n y p, para determinar la longitud necesaria del array de bits con la probabilidad
        de falsos positivos deseada."""
    Bloomf = bf.BloomFilter(n,p)
    for f in features:
        Bloomf.add(f)
    return Bloomf
def sendMsgToR(idDevice,bloomFil,ran):
    """Representación de mensaje."""
    print("Los patrones de S son desconocidos para R.")
    print("RNG por S(S lo memoriza):", ran)
    return (idDevice,bloomFil,ran)
def fRet(msg, features):
    """Feature Retrieve: Sensor R obtiene el mensaje de S(id,filtro,noAleatorio)"""
    id = msg[0]
    fil = msg[1]
    No = msg[2]
    Mask = [fil.check(fr) for fr in features]
    print("Busqueda de patrones R en FB de S(Máscara):", Mask)
    inCommon = [str(item) for item in np.array(np.nonzero(Mask))[0]]
    return inCommon, No
def KeyGenR(secThrshld, commonf, fR, No):
    if secThrshld < len(commonf) <= featCount:
        Sr = "".join(fR[int(i)] for i in commonf)
        print("Indices de valores en común: ",commonf)
        print("Concatenación de patrones en R que cumplen la Máscara:",Sr)
        H = hl.sha1()
        H.update(bytearray(Sr,'utf-8'))
        Kr = H.hexdigest()
        print("La llave en R es generada por el digesto SHA-1 de la concatenación de patrones en R")
        print("Key R(Permanece en R):", Kr)
        print("Se genera un HMAC que es clave para el acuerdo de llaves HMAC(Key, msg) = SHA-1(Kr,Sr||No)")
        MAC1 = hmac.new(bytearray(Kr, "utf-8"),bytearray("".join(commonf) + No, "utf-8"), hl.sha1)
        print("Llave generada en R.")
        return MAC1 , Kr
    else:
        print("Sin coincidencia en patrones...")
        return None, None
def SendMsgToS(idr, mac1, commonf):
    """Representación de mensaje."""
    return (idr, mac1, commonf)
def KeyGenS(msg,secThrshld, fS, No):
    """Generación de llave en S. Se válida el HMAC de R"""
    id = msg[0]
    MAC1 = msg[1]
    I = msg[2]
    if secThrshld < len(I) <= featCount:
        Ss = "".join(fS[int(i)] for i in I)
        print("Indices de valores en común(Recibido de R): ",I)
        print("Concatenación de patrones en S que cumplen los índices:",Ss)
        H = hl.sha1()
        H.update(bytearray(Ss,'utf-8'))
        Ks = H.hexdigest()
        print("Generación de llave en S, Ks:",Ks)
        print("S genera otro HMAC, verifica que los índices no hayan sido manipulados y si R uso su RNG.")
        MAC2 = hmac.new(bytearray(Ks, "utf-8"),bytearray("".join(I) + No, "utf-8"), hl.sha1)
        print("Representación en hexadecimal de HMAC-R:",MAC1.hexdigest())
        print("Representación en hexadecimal de HMAC-S:",MAC2.hexdigest())
        if hmac.compare_digest(MAC1.hexdigest(),MAC2.hexdigest()):
            print("Si las MACs coinciden entonces, se mantiene Kr == Ks, sin que ninguno conozca la del otro.")
            C = hmac.new(bytearray(Ks,"utf-8"), bytearray(IDs + IDr + No,"utf-8"), hl.sha1)
            print("Correcto acuerdo de llaves")
            return C , Ks
        else:
            print("Sin coincidencia en MACs...")
            return None, None
    else:
        print("Sin coincidencia en patrones...")
        return None, None
def AgreeWithR(Cs, Kr, Ran):
    try:
        Cr = hmac.new(bytearray(Kr,"utf-8"), bytearray(IDs + IDr + Ran,"utf-8"), hl.sha1)
        return True if hmac.compare_digest(Cs.hexdigest(),Cr.hexdigest()) else False
    except:
        print("C no coincide, fallo en protocolo.")
def main():
    ####    ###################     ####
    ####    GENERACIÓN DE FEATURES  ####
    ####    ###################     ####
    # Datos de protocolo
    Res = 5
    startR = 33900
    startS = 33900
    timeInt = 3
    threshold = 2
    bitsPrec = 13
    toPlot = True
    n = 30 # Número de entradas el filtro de Bloom
    p = 1/1040 # Probabilidad de falsos positivos
    file = 'physionet2/103'
    iPI.iPulInt(Res, file, startS, timeInt, threshold, toPlot, bitsPrec)
    # PATRONES EN S (Master) #
    fS  = fGen(Res, file, startS,timeInt,threshold, bitsPrec)
    print("Patrones en S:",fS)
    # PATRONES EN R (Slave) #
    fR = fGen(Res, file, startR,timeInt,threshold, bitsPrec)
    print("Patrones en R:",fR)
    ####    ###################     ####
    ####    INTERCAMBIO DE FEATURES ####
    ####    ###################     ####
    # PROCESO DE S
    filtro = bfCrea(fS,n,p)
    Ran = str(randint(1,100000))
    msgToR = sendMsgToR(IDs, filtro, Ran)
    # PROCESO DE R
    indicesEnComun, RanInt = fRet(msgToR, fR)
    print("Indices en común: ", indicesEnComun)
    ####    ###################     ####
    ####    GENERACIÓN DE LLAVES    ####
    ####    ###################     ####
    # Para S y R
    secureThrshld = 8
    # Generación de Kr
    #RanInt = "TAMPERED"
    mac1, Key_R = KeyGenR(secureThrshld, indicesEnComun, fR, RanInt)
    #shuffle(indicesEnComun)
    msgToS = SendMsgToS(IDr, mac1, indicesEnComun)
    # Generación de Ks
    FinalDigest, Key_S = KeyGenS(msgToS, secureThrshld, fS, Ran)
    # Validación final en R
    if AgreeWithR(FinalDigest,Key_R, Ran):
        print("Correcto acuerdo de llaves...")
    else:
        print("Fallo en la verificación de llaves.")
if __name__ == '__main__':
    IDs = "3112260149"
    IDr = "9408608"
    featCount = 30
    main()
