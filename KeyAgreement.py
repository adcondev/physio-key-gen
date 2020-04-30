import BloomFilter as bf
import hashlib as hl
import hmac
import InterPulseInterval as iPI
import numpy as np
from random import randint

def fGen(filtRes,filename, start, step, threshold,kbits):
    #iPI.iPulInt(filtRes, filename, start, step, threshold, True, kbits)
    F = [iPI.iPulInt(filtRes, filename, start + i*3 - 2, step, threshold, False, kbits)+
        iPI.iPulInt(filtRes, filename, start + i*3 - 1, step, threshold, False, kbits)+
        iPI.iPulInt(filtRes,filename, start + i*3, step, threshold, False, kbits) for i in range(1,featCount + 1)]
    return F
def bfCrea(features,n,p):
    Bloomf = bf.BloomFilter(n,p)
    for f in features:
        Bloomf.add(f)
    return Bloomf
def sendMsgToR(idDevice,bloomFil,ran):
    return (idDevice,bloomFil,ran)
def fRet(msg, features):
    id = msg[0]
    fil = msg[1]
    No = msg[2]
    inCommon = [str(item) for item in np.array(np.nonzero([fil.check(fr) for fr in features]))[0]]
    return inCommon, No
def KeyGenR(secThrshld, commonf, fR, No):
    print(secThrshld, "<", len(commonf) ,"<", featCount)
    if secThrshld < len(commonf) <= featCount:
        Sr = "".join(fR[int(i)] for i in commonf)
        print(commonf)
        print(Sr)
        H = hl.sha1()
        H.update(bytearray(Sr,'utf-8'))
        Kr = H.hexdigest()
        print(Kr)
        MAC1 = hmac.new(bytearray(Kr, "utf-8"),bytearray("".join(commonf) + No, "utf-8"), hl.sha1)
        print("Llave generada en R")
        return MAC1 , Kr
    else:
        print("Sin coincidencia en patrones...")
        return None, None
def SendMsgToS(idr, mac1, commonf):
    return (idr, mac1, commonf)
def KeyGenS(msg,secThrshld, fS, No):
    id = msg[0]
    MAC1 = msg[1]
    I = msg[2]
    print(secThrshld, "<", len(I) ,"<", featCount)
    if secThrshld < len(I) <= featCount:
        Ss = "".join(fS[int(i)] for i in I)
        print(I)
        print(Ss)
        H = hl.sha1()
        H.update(bytearray(Ss,'utf-8'))
        Ks = H.hexdigest()
        print(Ks)
        MAC2 = hmac.new(bytearray(Ks, "utf-8"),bytearray("".join(I) + No, "utf-8"), hl.sha1)
        print(MAC1.hexdigest())
        print(MAC2.hexdigest())
        if hmac.compare_digest(MAC1.hexdigest(),MAC2.hexdigest()):
            # Se mantiene Kr == Ks
            C = hmac.new(bytearray(Ks,"utf-8"), bytearray(IDs + IDr + No,"utf-8"), hl.sha1)
            print("Correcto acuerdo de llaves")
            return C.hexdigest() , Ks
        else:
            print("Sin coincidencia en MACs...")
            return None, None
    else:
        print("Sin coincidencia en patrones...")
        return None, None
def AgreeWithR(C):
    return C
def main():
    ####    ###################     ####
    ####    GENERACIÓN DE FEATURES  ####
    ####    ###################     ####
    # Datos de protocolo
    Res = 5
    startR = 33840
    startS = 33840
    timeInt = 3
    threshold = 2
    bitsPrec = 13
    toPlot = True
    n = 30 # Número de entradas el filtro de Bloom
    p = 1/1040 # Probabilidad de falsos positivos
    file = 'physionet2/103'
    # PATRONES EN S (Master) #
    fS  = fGen(Res, file, startS,timeInt,threshold, bitsPrec)
    print(fS)
    # PATRONES EN R (Slave) #
    fR = fGen(Res, file, startR,timeInt,threshold, bitsPrec)
    print(fR)
    ####    ###################     ####
    ####    INTERCAMBIO DE FEATURES ####
    ####    ###################     ####
    # PROCESO DE S

    filtro = bfCrea(fS,n,p)
    Ran = "331"#randint(1,100000)
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

    mac1, Key_R = KeyGenR(secureThrshld, indicesEnComun, fR, RanInt)
    msgToS = SendMsgToS(IDr, mac1, indicesEnComun)
    # Generación de Ks
    FinalDigest, Key_S = KeyGenS(msgToS, secureThrshld, fS, Ran)
if __name__ == '__main__':
    IDs = "3112260149"
    IDr = "9408608"
    featCount = 30
    main()
