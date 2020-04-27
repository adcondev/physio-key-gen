import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import wfdb
def iPulInt(filter, filename, start, step, threshold, toPlot = True):
	"""Función para determinar el IPI de un segmento de tiempo."""
	record = wfdb.rdrecord(filename)
	fs = record.__dict__["fs"]
	begin = start*fs
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
	peaks = np.nonzero(similarity > threshold)
	# IPI es el promedio de las diferencias
	peaks_DxDt = np.dot(np.diff(peaks), 1/fs)
	IPI = np.average(peaks_DxDt[peaks_DxDt > 1/fs])
	# Gráficas
	if toPlot:
		wfdb.plot_wfdb(record=record, title='Record ' + filename[-3:] + ' from MIT-BIH Arrhythmia DB')
	return IPI, record
if __name__ == '__main__':
	ipi,record = iPulInt(5, 'physionet2/103', 94, 2.5, 2, True)
	print("IPI Value:", ipi)
