import math
import mmh3
from bitarray import bitarray

class BloomFilter(object):
    '''Bloom Filter usando murmur3 hash'''
    def __init__(self, items_count,fp_prob):
        '''
        items_count : int
            Elementos esperados a almacenar
        fp_prob : float
            Probabilidad de falso positivo
        '''
        # Falso Positivo
        self.fp_prob = fp_prob
        # Size de array
        self.size = self.get_size(items_count,fp_prob)
        # Número de h(x)
        self.hash_count = self.get_hash_count(self.size,items_count)
        # array de bits
        self.bit_array = bitarray(self.size)
        # Inicio de bits en 0
        self.bit_array.setall(0)

    def add(self, item):
        '''
        Integrar elemento al filtro
        '''
        digests = []
        for i in range(self.hash_count):
            # crear digesto dado un número.
            # i es la semilla de cada murmur3 hash
            # cada digesto es diferente, dada la semilla
            digest = mmh3.hash(item,i) % self.size
            digests.append(digest)
            # set the bit True in bit_array
            self.bit_array[digest] = True
    def get_bit_array(self):
        """Retornar array de bits"""
        return self.bit_array
    def check(self, item):
        '''
        Verificar existencia de elemento
        '''
        for i in range(self.hash_count):
            digest = mmh3.hash(item,i) % self.size
            if self.bit_array[digest] == False:
                # Definitivamente no existe
                return False
            # Posiblemente exista el elemento
            return True

    @classmethod
    def get_size(self,n,p):
        '''
        retorna el size del array m dada la formula:
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            elementos esperados a ser almacenados
        p : float
            Probabilidad de un falso positivo
        '''
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        '''
        Determina la cantidad necesaria de funciones hash dada la fórmula:
        k = (m/n) * lg(2)

        m : int
            tamaño esperado del array
        n : int
            elementos esperados a ser almacenados
        '''
        k = (m/n) * math.log(2)
        return int(k)

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
def main():
    n = 4.47
    k = 13
    print(decToBin(n, k))
    n = 6.986
    k = 13
    print(decToBin(n, k))
    from random import shuffle

    n = 10 #no of items to add
    p = 0.01 #false positive probability

    bloomf = BloomFilter(n,p)
    print("Size of bit array:{}".format(bloomf.size))
    print(bloomf.get_bit_array())
    print("False positive Probability:{}".format(bloomf.fp_prob))
    print("Number of hash functions:{}".format(bloomf.hash_count))

    # words to be added
    word_present = ['hola','adios','perro','gato','cerdo',
                    'yo','tu']

    # word not added
    word_absent = ['aka','bebe','queso','examen','compu',
                   'seguridad','hacks']

    for item in word_present:
        bloomf.add(item)
    print(bloomf.get_bit_array())
    shuffle(word_present)
    shuffle(word_absent)

    test_words = word_present[:3] + word_absent
    shuffle(test_words)
    for word in test_words:
        if bloomf.check(word):
            if word in word_absent:
                print("'{}'  false positive".format(word))
            else:
                print("'{}'  probably present".format(word))
        else:
            print("'{}'  definitely not present".format(word))
if __name__ == "__main__" :
    main()
