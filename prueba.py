import numpy as np
hola = [False,True,True,False,True]
hola2 = np.array(np.nonzero(hola))
print(hola2.tolist()[0])
HOLA = [1,2,3,4]
holastr = [str(item) for item in HOLA]
perro = "".join(holastr)
