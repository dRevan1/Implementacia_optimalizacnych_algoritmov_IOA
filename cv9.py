#--------------------
# matica vzdialeností
#--------------------
D = [
    [0, 12, 24, 46, 22, 10, 32, 26, 34, 34],
    [12, 0, 12, 34, 34, 10, 20, 26, 22, 22],
    [24, 12, 0, 22, 46, 22, 22, 20, 10, 10],
    [46, 34, 22, 0, 68, 38, 44, 22, 32, 12]
]
#----------------------------------------------------------------------------------------------------------------
# matica rozhodnutí o množstve tovaru, ktoré daný sklad (riadok) dodá danému zákazníkovi (stĺpec), dfault sú None
#----------------------------------------------------------------------------------------------------------------
X = [
    [None] * len(D[0]) for row in range(len(D)) # pridá len(D) riadkov/listov, v každom bude len(D[0]) prvkov s hodnotou "None" (rovnaký shape ako D)
]
#--------------
# bázické hrany
#--------------
H = []
#----------------------
# požiadavky zákazníkov
#----------------------
b = [10, 30, 40, 20, 10, 20, 50, 30, 10, 20]
#-------------------------------------------------------------
# kapacity skladov (200 bolo doplnené, iba prvé 3 sú v zadaní)
#-------------------------------------------------------------
a = [150, 100, 250, 200]


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# spočíta celkové požiadavky a porovná ich s kapacitami skladov, ak sú požiadavky menšie, doplní sa fiktívny zákazník, aby sa rovnali s celkovou kapacitou skladov
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_fictional_customer():
    global b, a, D, X
    
    total_demand = sum(b)
    total_capacity = sum(a)
    
    if total_demand < total_capacity:  # pridanie fiktívneho zákazníka, aby bola úloha vybilancovaná
        b.append(total_capacity - total_demand)
        for i in range(len(D)):
            D[i].append(0)
            X[i].append(None)
#-----------------------------------------------------------------
# metódou minimálneho prvku vytvorí počiatočné riešenie v matici X
#-----------------------------------------------------------------
def get_min_element_X():
    global X, H
    
    a_ = a.copy()  # voľné kapacity skladov
    b_ = b.copy()  # zostávajúce požiadavky zákazníkov
    visited = [
        [False] * len(D[0]) for row in range(len(D)) # značky pre navštívené pozície v D
    ]
    to_visit = len(D) * len(D[0]) # počet všetkých pozícií v D, ktoré bude treba navštíviť
    
    while to_visit > 0:
        min_element = float('inf')
        min_i, min_j = -1, -1
        
        for i in range(len(D)): # nájdenie najmenšieho prvku
            for j in range(len(D[0])):
                if not visited[i][j] and D[i][j] < min_element:
                    min_element = D[i][j]
                    min_i, min_j = i, j
        
        visited[min_i][min_j] = True   # aktualizácia prejdených prvkov
        to_visit -= 1
        
        min_value = min(a_[min_i], b_[min_j])  # doplnenie množstva na dané miesto v X
        X[min_i][min_j] = min_value
        a_[min_i] -= min_value
        b_[min_j] -= min_value
        
        if min_value > 0:
            H.append((min_i, min_j))
    
            
def main():
    add_fictional_customer()
    get_min_element_X()
    print(H)
    for row in X:
        print(row)
    
    
  
main()