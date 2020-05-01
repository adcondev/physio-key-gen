import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import wfdb
def decToBin(num, kbits):
    """Programa para convertir un número decimal a binario con k-bits de precision de punto flotante"""
    toBin = ""
    # Parte entera.
    Integral = int(num)
    # Parte fraccional
    fract = num - Integral
    # Decimal => binario. Parte entera (Iterativo hasta que Integral sea 0)
    while (Integral):
        # Obtener residuo
        rem = Integral % 2
        # Añadir numero. Se obtiene el número binario en little endian.
        toBin += str(rem)
        # División entera. Corresponde al valor para el siguiente dígito.
        Integral //= 2
    # Invertir array para obtener el número el big endian.
    toBin = toBin[::-1]

    # Punto decimal.
    toBin += '.'

    # Decimal => binario. Parate fraccionaria (Iterativo)
    while (kbits):
        # Determinar bits en fracción. Proceso inverso respecto a la división entera usada.
        fract *= 2
        fract_bit = int(fract)
        if (fract_bit == 1) :
            fract -= fract_bit
            toBin += '1'
        else:
            toBin += '0'
        kbits -= 1
    return toBin
def iPulInt(filter, filename, start, step, threshold, toPlot = False, kbits = 13):
    """Función para determinar el IPI de un segmento de tiempo."""
    record = wfdb.rdrecord(filename)
    fs = record.__dict__["fs"]
    begin = start
    end = int(step*fs)
    # encontrar pico dado un umbral
    record.__dict__['p_signal'] = record.__dict__['p_signal'][begin:begin + end]
    ecg_signal = np.array([lista[0] for lista in record.__dict__['p_signal']])
    # Vector lineal de función senoidal de 0.5 pi a 1.5 pi con n muestras(filtro)
    t = np.linspace(0.5 * np.pi, 1.5 * np.pi, filter)
    # Usar la función senoidal para determinar el tiempo entre pulsos
    qrs_filter = np.sin(t)
    # Computa cross correlation entre el ECG y el filtro propuesto
    similarity = np.correlate(ecg_signal, qrs_filter, mode="same")
    for i in range(end):
    	record.__dict__['p_signal'][i][1] = similarity[i]
    peaks = np.array(np.nonzero(similarity > threshold))
    # IPI es el promedio de las diferencias
    peaks_DxDt = np.dot(np.diff(peaks), 1/fs)
    IPI = np.average(peaks_DxDt[peaks_DxDt > 1/fs])
    # Gráficas
    if toPlot:
        wfdb.plot_wfdb(record=record, title='Record ' + filename[-3:] + ' from MIT-BIH Arrhythmia DB')
        print("Datos de señal:", record.__dict__)
    return decToBin(IPI, kbits)
def main():
    n = 4.47
    k = 13
    print(decToBin(n, k))
    n = 6.986
    k = 13
    print(decToBin(n, k))
    ipi = iPulInt(5, 'physionet2/103', 33840, 2.5, 2, True)
    print("IPI Value:", ipi)
if __name__ == '__main__':
    main()
