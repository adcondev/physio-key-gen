import math
import hashlib as hl
from bitarray import bitarray

class BloomFilter(object):
    '''Bloom Filter usando SHA-1'''
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
    def get_bitarray_size(self):
        return self.size
    def add(self, item):
        '''
        Integrar elemento al filtro
        '''
        digests = []
        for i in range(self.hash_count):
            # crear digesto dado un número.
            # i es la semilla de cada murmur3 hash
            # cada digesto es diferente, dada la semilla
            H = hl.sha1()
            H.update(bytearray(item,'utf-8'))
            H.update(bytearray(str(i),'utf-8'))
            digest = int.from_bytes(H.digest(), 'big') % self.size
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
            H = hl.sha1()
            H.update(bytearray(item,'utf-8'))
            H.update(bytearray(str(i),'utf-8'))
            digest = int.from_bytes(H.digest(), 'big') % self.size
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


def main():
    from random import shuffle

    n = 30 #no of items to add
    p = 1/1040 #false positive probability

    bloomf = BloomFilter(n,p)
    print("Longitud de array de bits:{}".format(bloomf.get_bitarray_size()))
    print(bloomf.get_bit_array())
    print("Probabilidad de Falsos Positivos:{}".format(bloomf.fp_prob))
    print("Número de funciones Hash:{}".format(bloomf.hash_count))

    # words to be added
    word_present = ['hola','adios','perro','gato','cerdo',
                    'yo','tu','aka','bebe','queso']

    # word not added
    word_absent = ['examen','compu',
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
                print("'{}'  falso positivo".format(word))
            else:
                print("'{}'  probablemente presente".format(word))
        else:
            print("'{}'  definitivamente no está presente".format(word))
if __name__ == "__main__" :
    x = BloomFilter()
    main()
