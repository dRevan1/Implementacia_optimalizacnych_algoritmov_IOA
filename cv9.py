#--------------------
# matica vzdialeností
#--------------------
D = [
    [0, 12, 24, 46, 22, 10, 32, 26, 34, 34],
    [12, 0, 12, 34, 34, 10, 20, 26, 22, 22],
    [24, 12, 0, 22, 46, 22, 22, 20, 10, 10],
    [46, 34, 22, 0, 68, 38, 44, 22, 32, 12]
]
D_test = [
    [6, 9, 11, 3, 11],
    [13, 2, 10, 4, 8],
    [10, 4, 11, 8, 1],
    [6, 6, 3, 1, 4]
]
#-----------------------------------------------------------------------------------------------------------------
# matica rozhodnutí o množstve tovaru, ktoré daný sklad (riadok) dodá danému zákazníkovi (stĺpec), default sú None
#-----------------------------------------------------------------------------------------------------------------
X = [
    [None] * len(D[0]) for row in range(len(D)) # pridá len(D) riadkov/listov, v každom bude len(D[0]) prvkov s hodnotou "None" (rovnaký shape ako D)
]
X_test = [
    [None] * len(D_test[0]) for row in range(len(D_test))
]
#--------------
# bázické hrany
#--------------
H = []
#----------------------
# požiadavky zákazníkov
#----------------------
b = [10, 30, 40, 20, 10, 20, 50, 30, 10, 20]
b_test = [100, 100, 100, 100, 100]
#-------------------------------------------------------------
# kapacity skladov (200 bolo doplnené, iba prvé 3 sú v zadaní)
#-------------------------------------------------------------
a = [150, 100, 250, 200]
a_test = [110, 120, 130, 140]


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# spočíta celkové požiadavky a porovná ich s kapacitami skladov, ak sú požiadavky menšie, doplní sa fiktívny zákazník, aby sa rovnali s celkovou kapacitou skladov
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_fictional_customer():
    global b_test, a_test, D_test, X_test
    
    total_demand = sum(b_test)
    total_capacity = sum(a_test)
    
    if total_demand < total_capacity:  # pridanie fiktívneho zákazníka, aby bola úloha vybilancovaná
        b_test.append(total_capacity - total_demand)
        for i in range(len(D_test)):
            D_test[i].append(0)
            X_test[i].append(None)
#-----------------------------------------------------------------
# metódou minimálneho prvku vytvorí počiatočné riešenie v matici X
#-----------------------------------------------------------------
def get_min_element_X():
    global X_test, H
    
    a_ = a_test.copy()  # voľné kapacity skladov
    b_ = b_test.copy()  # zostávajúce požiadavky zákazníkov
    visited = [
        [False] * len(D_test[0]) for row in range(len(D_test)) # značky pre navštívené pozície v D
    ]
    to_visit = len(D_test) * len(D_test[0]) # počet všetkých pozícií v D, ktoré bude treba navštíviť
    
    while to_visit > 0:
        min_element = float('inf')
        min_i, min_j = -1, -1
        
        for i in range(len(D_test)): # nájdenie najmenšieho prvku
            for j in range(len(D_test[0])):
                if not visited[i][j] and D_test[i][j] < min_element:
                    min_element = D_test[i][j]
                    min_i, min_j = i, j
        
        visited[min_i][min_j] = True   # aktualizácia prejdených prvkov
        to_visit -= 1
        
        min_value = min(a_[min_i], b_[min_j])  # doplnenie množstva na dané miesto v X
        X_test[min_i][min_j] = min_value
        a_[min_i] -= min_value
        b_[min_j] -= min_value
        
        if min_value > 0:
            H.append((min_i, min_j))
#--------------------------------------------------------
# vypočíta duálny združený vektor - matica sa potom vráti
#--------------------------------------------------------
def compute_UV_vector():
    global H, D_test
    u = [None] * len(D_test)  # vektory
    v = [None] * len(D_test[0])
    UV = [[None] * len(D_test[0]) for row in range(len(D_test))]  # matica
      
    for i, j in H:  # nastavenie hodnôt pre bázické hrany
        UV[i][j] = D_test[i][j]
    
    for i in range(len(u)):  # nastavenie hodnôt vektorov u a v
        if (u[i] is None):   # ak má riadok (vektor u) None - dá sa 0, inak má už hodnotu podľa stĺpca, ktorý bol nastavený niekde v predošlom riadku
            u[i] = 0
            
        for j in range(len(v)):
            if (UV[i][j] is not None):   # ak je na mieste hodnota (je to bázická hrana), nastaví sa stĺpec (vektor v) ak je tam None - ešte sme ho nenastavovali vyššie, inak sa ide ďalej
                if (v[j] is None):
                    v[j] = UV[i][j] - u[i]
                    for k in range(i + 1, len(u)):  # pri nastavení hodnoty vektore v pre daný stĺpec sa prejde zvyšok stĺpca a všade, kde sú hodnoty (bázické hrany), sa nastaví hodnota vektora u
                        if (UV[k][j] is not None):
                            u[k] = UV[k][j] - v[j]
    
    for i in range(len(u)):  # tu sa prejdú nebázické hrany a nastaví sa ich hodnota po dokončení vektorov u a v
        for j in range(len(v)):
            if (UV[i][j] is None):
                UV[i][j] = u[i] + v[j] - D_test[i][j]
                    
                    
    return UV, u, v

            
def main():
    add_fictional_customer()
    get_min_element_X()
    
    print("----------------------------")
    print("Basic edges (H):")
    print(H)
    
    print("----------------------------")
    print("Decision matrix (X):")
    for row in X_test:
        print(row)
    
    UV, u, v = compute_UV_vector()
    
    print("----------------------------")
    print("UV matrix:")
    for row in UV:
        print(row)
        
    print("----------------------------")
    print(f"Vector u: {u}")
    print(f"Vector v: {v}")
  
main()