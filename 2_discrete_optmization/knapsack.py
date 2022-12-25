# x elements with diff weight and value, max value subject to a certain max weight
# each element can be used only once


import copy

class Elemento:
    def __init__(self, id, peso, valor):
        self.id = id
        self.peso = peso
        self.valor = valor

    def __repr__(self):
        return str(f"x{self.id}: {{peso: {self.peso} valor: {self.valor}}}")



class Optimal:
    def __init__(self, all_elementos, capacity):
        self.all_elementos = all_elementos
        self.capacity = capacity
        self.tabla = [[Bag(c, []) for _ in range(len(all_elementos)+1)] for c in range(capacity + 1)]


    def __repre__(self):
        return str(f"hasta {self.hasta_elemento} elementos, hasta {self.capacity} capacidad")

    #def __getitem__(self, item):

    def get_possible_elements(self, hasta_elemento):
        elems = self.all_elementos[:hasta_elemento]
        return elems

    def evaluate_adding_element(self, hasta_capacidad, hasta_elemento, element):
        bag_misma_capacidad_sin_elem = self.tabla[hasta_capacidad][hasta_elemento - 1]
        peso_misma_capacidad_sin_elem = bag_misma_capacidad_sin_elem.suma_pesos()

        valor_add = 0
        valor_replace = 0

        # mantiene el bag de la misma capacidad sin el elemento
        bag_keep = copy.copy(bag_misma_capacidad_sin_elem)
        valor_keep = bag_keep.suma_valor()

        # sumar a la bag anterior (misma capacidad un elemento menos)
        if peso_misma_capacidad_sin_elem + element.peso <= hasta_capacidad:
            elementos_elegidos = copy.copy(bag_misma_capacidad_sin_elem.elementos_elegidos)
            elementos_elegidos.append(element)
            bag_add = Bag(capacidad=hasta_capacidad, elementos_elegidos=elementos_elegidos)
            valor_add = bag_add.suma_valor()
        # buscar la bag sin este elemento a la que le entra y sumarlo
        if hasta_capacidad - element.peso >= 0:
            bag_sin_capac_para_elem = self.tabla[hasta_capacidad - element.peso][hasta_elemento - 1]
            elementos_elegidos = copy.copy(bag_sin_capac_para_elem.elementos_elegidos)
            elementos_elegidos.append(element)
            bag_replace = Bag(capacidad=hasta_capacidad, elementos_elegidos=elementos_elegidos)
            valor_replace = bag_replace.suma_valor()

        if valor_add > 0 and valor_add >= valor_keep and valor_add >= valor_replace:
            self.tabla[hasta_capacidad][hasta_elemento] = bag_add
        elif valor_replace > 0 and valor_replace >= valor_keep:
            self.tabla[hasta_capacidad][hasta_elemento] = bag_replace
        elif valor_keep > 0 and valor_keep >= valor_replace:
            self.tabla[hasta_capacidad][hasta_elemento] = bag_keep

    def get_optimal_bag(self):
        for hasta_elemento in range(1, len(self.all_elementos) + 1):
            for hasta_capacidad in range(0, self.capacity + 1):
                possible_elements = self.get_possible_elements(hasta_elemento)
                self.evaluate_adding_element(hasta_capacidad, hasta_elemento, possible_elements[-1])
        return self.tabla




class Bag:
    def __init__(self, capacidad, elementos_elegidos):
        self.capacidad = capacidad
        self.elementos_elegidos = elementos_elegidos

    def suma_pesos(self):
        return sum([e.peso for e in self.elementos_elegidos])


    def suma_valor(self):
        return sum([e.valor for e in self.elementos_elegidos])

    def __repr__(self):
        return str(f"capacidad: {self.capacidad}, peso: {self.suma_pesos()}, valor: {self.suma_valor()}, elegidos: {self.elementos_elegidos}")




all_elementos = [
    Elemento(1, 4, 5),
    Elemento(2, 5, 6),
    Elemento(3, 2, 3)
]

capacity = 9

# one option choose by value//weight,si capacity es un numero chico en relacion a los valores d elos elmentos no va a ser optimo.


# solve a problem for items 1, items 1 and 2 and item1,2,3 iterating over i  in range(0, capacity+1).



def test_kanpsack():
    all_elementos = [
        Elemento(1, 4, 5),
        Elemento(2, 5, 6),
        Elemento(3, 2, 3)
    ]

    capacity = 9

    o = Optimal(all_elementos, capacity)
    tabla = o.get_optimal_bag()

    assert tabla[5][3].suma_valor() == 6
    assert tabla[5][3].suma_pesos() == 5

    assert tabla[6][3].suma_valor() == 8
    assert tabla[6][3].suma_pesos() == 6

    assert tabla[9][3].suma_valor() == 11
    assert tabla[9][3].suma_pesos() == 9




