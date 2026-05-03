#--------------------
# matica vzdialeností
#--------------------
D = [
    [0, 12, 24, 46, 22, 10, 32, 26, 34, 34],
    [12, 0, 12, 34, 34, 10, 20, 26, 22, 22],
    [24, 12, 0, 22, 46, 22, 22, 20, 10, 10]
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
#---------------------------
# vektory u a v, a matica UV
#---------------------------
u = [None] * len(D)  # vektory
v = [None] * len(D[0])
UV = [[None] * len(D[0]) for row in range(len(D))]
#-----------------------------------------------------
# najväčší prvok nájdený pri stĺpcovom pravidle v MODI
#-----------------------------------------------------
max_i, max_j, min_t = -1, -1, -1
#--------------
# bázické hrany
#--------------
H = []
#----------------------
# požiadavky zákazníkov
#----------------------
b = [10, 30, 40, 20, 10, 20, 50, 30, 10, 20]
b_test = [100, 100, 100, 100, 100]
#-----------------
# kapacity skladov
#-----------------
a = [150, 100, 250]
a_test = [110, 120, 130, 140]


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
        
        return True
    
    return False
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
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# rekurzívne spočíta u a v vektory pre bázické hrany podľa smeru, najskôr sa danej hrane nastaví riadok/stĺpec podľa predošlej aktualizácie, potom si prejde celý svoj riadok/stĺpec 
# direction - 0 horizontálne, 1 vertikálne
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def compute_basic_uv(i, j, direction):
    global u, v, H, D
    
    if direction == 0:   # horizontálne
        for col in range(len(D[0])):  # prejde sa celý riadok a hľadajú sa bázické hrany, aby sa im aktualizoval stĺpec (vektor v) a na nich sa potom rekurzívne volá metóda v druhom smere
            if col != j and X[i][col] > 0:
                v[col] = D[i][col] - u[i] # aktualizuje sa vektor v pre daný stĺpec - metóda teda začína s prvkom i, j, ktorý už má príslušný vektor aktualizovaný
                compute_basic_uv(i, col, 1)
                
    else:   # vertikálne, analogicky k horizontálnemu
        for row in range(len(D)):
            if row != i and X[row][j] > 0:
                u[row] = D[row][j] - v[j]
                compute_basic_uv(row, j, 0)
#--------------------------------
# vypočíta duálny združený vektor
#--------------------------------
def compute_UV_vector():
    global H, UV, u, v, D
    u = [None] * len(D)  # vektory
    v = [None] * len(D[0])
    UV = [[None] * len(D[0]) for row in range(len(D))]  # matica
      
    for i, j in H:  # nastavenie hodnôt pre bázické hrany
        UV[i][j] = D[i][j]
    
    for i in range(len(D)):   # pre všetky riadky, ktoré po prejdení rekurziou cimpute_basic_uv nemajú nastavenú hodnotu vo vektore u sa prejde každý bázický prvok, a zavolá sa rekurzívna metóda na jeho stĺpec
        if u[i] is None:
            u[i] = 0
            for j in range(len(D[0])):
                if UV[i][j] is not None:
                    v[j] = D[i][j] - u[i]
                    compute_basic_uv(i, j, 1)
    
    
    for i in range(len(u)):  # tu sa prejdú nebázické hrany a nastaví sa ich hodnota po dokončení vektorov u a v
        for j in range(len(v)):
            if (UV[i][j] is None):
                UV[i][j] = u[i] + v[j] - D[i][j]
#---------------------------------------------------------------------
# stĺpcové pravidlo MODI - nájde najväčší kladný nebázický prvok/hranu
#---------------------------------------------------------------------                  
def get_max_nonbasic_edge():
    global max_i, max_j
    
    max_value = float('-inf')
    max_i, max_j = -1, -1
    
    for i in range(len(UV)):
        for j in range(len(UV[0])):
            if (X[i][j] == 0) and (UV[i][j] > max_value) and (UV[i][j] > 0):
                max_value = UV[i][j]
                max_i, max_j = i, j
                
    return max_i != -1
#-----------------------------------------------------------------------------------------------------------------------------------------------
# rekurzívna funkcia - hľadá cyklus, posiela sa tam index daného prvku, ako aj 1/-1 pre update
# direction - 0 horizontálne, 1 vertikálne, 2 oba smery - pre prvý prvok
# t je hodnota, o ktorú sa majú meniť prvky v cykle, každý potenciálny cyklus/vetva bude mať t podľa najbližšieho prvku v tej vetve od pôvodného
#-----------------------------------------------------------------------------------------------------------------------------------------------
def find_cycle(i, j, direction, update_coef, t = float('inf')):
    global min_t
    
    cycle_found = False
    t_change = X[i][j] if update_coef == -1 and X[i][j] < t else t  # t sa aktualizuje, ak daný prvok má koeficient -1 a jeho hodnota je menšia, ako doteraz nájdené t
    
    if direction == 0 or direction == 2:  # horizontálny prechod
        for col in range(len(X[0])):
            if col == j:   # sám seba prvok preskočí
                continue
            if col == max_j and i == max_i:    # ak sme v našom smere našli počiatočný prvok - máme cyklus
                cycle_found = True
                min_t = t_change
                break
            if X[i][col] > 0:   # ak máme bázický prvok, rekurzívne na ňom voláme túto metódu
                if direction == 2:
                    t_change = X[i][col]    # pokiaľ je súčasný prvok počiatočný, nastaví t na hodnotu suseda, na ktorom sa ďalej volá rekurzia, ďalej v tejto vetve pôjde rovnaké t
                if find_cycle(i, col, 1, -update_coef, t_change):
                    cycle_found = True
                    break
    
    if (direction == 1 or direction == 2) and not cycle_found:  # vertikálny prechod, analogicky k horizontálnemu
        for row in range(len(X)):
            if row == i:
                continue
            if row == max_i and j == max_j:
                cycle_found = True
                min_t = t_change
                break
            if X[row][j] > 0:
                if direction == 2:
                    t_change = X[row][j]
                if find_cycle(row, j, 0, -update_coef, t_change):
                    cycle_found = True
                    break

    if cycle_found:
        if direction != 2:   # ak sa našiel cyklus a teraz sme v prvku inom, ako počiatočný, aktualizujeme tento prvok, inak sme v počiatočnom a iba počiatočný dáme do H
            X[i][j] += update_coef * min_t
        else:
            H.append((i, j))
            X[i][j] = min_t
        
    return cycle_found
    
#-----------------------------------------------------------------------------------------------------------------------------------------
# tu sa spustí a beží MODI algoritmus - aplikuje sa stĺpcové a riadkové pravidlo a aktualizuje sa riešenie, kým sa spĺňa stĺpcové pravidlo
#-----------------------------------------------------------------------------------------------------------------------------------------
def run_MODI():
    global H, min_t
    while get_max_nonbasic_edge():
        find_cycle(max_i, max_j, 2, 1)
        
        for basic in H:   # ak sa po aktualizácii riešenia nejaký prvok z pôvodného vynuluje, odstráni sa z H
            if X[basic[0]][basic[1]] == 0:
                H.remove(basic)
                
        compute_UV_vector()
        min_t = float('inf')
#----------------
# výpis výsledkov
#----------------
def print_problem_results(fictional_customer):        
    print("/////////////////////////////////////////////////////////////////////")
    print("Transportation Problem")
    print(f"Depots capacities: {a}")
    print(f"Customers demands: {b}")
    print(f"Fictional customer added: {'Yes' if fictional_customer else 'No'}")
    print("Method used: MODI and minimal element for initial basic solution")
    print("---------------------------------------------------------------------")
    print("Optimal solution (decision matrix, X[depots][customers]):")
    for i in range(len(X)):
        print(X[i])
    print("/////////////////////////////////////////////////////////////////////")

       
def main():
    fictional_added = add_fictional_customer()
    get_min_element_X()
    compute_UV_vector() # prvý UV treba tu, keďže v MODI sa to kontroluje cez stĺpcové pravidlo, ktoré už potrebuje UV
    run_MODI()
    print_problem_results(fictional_added)
    
  
main()