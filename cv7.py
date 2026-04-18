#--------------------
# matica vzdialeností
#--------------------
D = [
    [0, 12, 24, 46, 22, 10, 32, 26, 34, 34],
    [12, 0, 12, 34, 34, 10, 20, 26, 22, 22],
    [24, 12, 0, 22, 46, 22, 22, 20, 10, 10],
    [46, 34, 22, 0, 68, 38, 44, 22, 32, 12]
]
#----------------------
# požiadavky zákazníkov
#----------------------
b = [10, 30, 40, 20, 10, 20, 50, 30, 10, 20]
#--------------------------------
# náklady na umiestnenie stredísk
#--------------------------------
y = [2000, 3000, 3000, 1000]
#--------------------------------------------------------------
# jednotlivé riešenia - list riešenia (0/1 vektor) a hodnota ÚF
# best_solution - najlepšie riešenie
# n - počet možných umiestnení stredísk
# c - počet zákazníkov
#--------------------------------------------------------------
combinations = []
n = 4
c = 10
best_solution = (None, float('inf'))

#---------------------------------
# výpočet hodnoty účelovej funkcie
#---------------------------------
def get_target_function_value(solution):
    total_cost = 0
    for i in range(n):
        if solution[i] == 1:
            total_cost += y[i] # náklady na umiestnenie strediska - stredisko * náklady na umiestnenie
            
    for i in range(c):
        min_distance = 400000.0 # alebo float('inf') pre všeobecnú úlohu, nejaké veľké číslo
        for j in range(n):
            if solution[j] == 1:
                min_distance = min(min_distance, D[j][i])
                
        total_cost += b[i] * min_distance # náklady na požiadavku - požiadavka * vzdialenosť (k najbližšiemu stredisku)
        
    return total_cost
#----------------------------------------------------------------------------------------------------
# inicializácia riešenia - vytvoria sa prvé, 1-prvkové riešenia pre všetky možné umiestnenia stredísk
#----------------------------------------------------------------------------------------------------
def init_solutions():
    global best_solution # global pre assign, na read netreba
    
    for i in range(n):
        solution_vector = [1 if j == i else 0 for j in range(n)]
        solution_value = get_target_function_value(solution_vector)
        solution = (solution_vector, solution_value)
        combinations.append(solution)
        
        if solution_value < best_solution[1]:
            best_solution = solution
#---------------------------------------------------------------------------------------------------------
# spraví sa "logický súčet/ OR" dvoch riešení v podobe 0-1 vektorov a vytvorí sa riešenie aj s hodnotou ÚF
#---------------------------------------------------------------------------------------------------------
def combine_solutions(solution1, solution2):
    combined_vector = [max(solution1[0][i], solution2[0][i]) for i in range(n)]
    combined_value = get_target_function_value(combined_vector)
    
    return (combined_vector, combined_value)
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# hlavná metóda, kde sa postupne tvoria o 1 väčšie podmnožiny (kombinácie) umiestnení skladov tak, že sa rozdelia do sekvencí, aby sa postupne tvorili iba o 1 väčšie kombinácie
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
def main():
    global combinations, best_solution
    
    init_solutions()
    level_index, last_index = 0, len(combinations) - 1
    sequence_end_indices = [len(combinations) - 1]
    
    while level_index < last_index:     # keď sa pridá iba 1 nové riešenie, alebo žiadne - nepokračuje sa, prehľadávanie skončilo
        new_sequence_end_indices = []  # tu sa vytvára nový zoznam indexov, kde končia jednotlivé sekvencie riešení
        for i in range(len(sequence_end_indices)):   # riešenia idú po sekvenciách, aby sa neopakovali a aby sa vytvárali iba o 1 väčšie podmnožiny, pričom jednotlivé riešenia sú v "combinations" za sebou
            sequence_start_index = level_index if i == 0 else sequence_end_indices[i-1] + 1
            sequence_end_index = sequence_end_indices[i]
            
            for j in range(sequence_start_index, sequence_end_index):  # 1 sekvencia sú napr. dvojice umiestnení 12, 13, 14, z nich sa postupne spravia všetky trojice a ďalšia sekvencia bude dvojice 23 a 24, atd.
                new_sequence_end_index = len(combinations) - 1
                
                for k in range(j + 1, sequence_end_index + 1):
                    combined_solution = combine_solutions(combinations[j], combinations[k])
                    
                    if combined_solution[1] < combinations[j][1] and combined_solution[1] < combinations[k][1]:        # podmienka na vyradenie vetvy, v tomto prípade sa nepridá do zoznamu kombinácií ako ďalšie riešenie
                        new_sequence_end_index += 1
                        combinations.append(combined_solution)
                    else:
                        continue
                                      
                    if combined_solution[1] < best_solution[1]:
                        best_solution = combined_solution
                                           
                new_sequence_end_indices.append(new_sequence_end_index)
        sequence_end_indices = new_sequence_end_indices.copy()  # prepísanie zoznamu indexov sekvencií
        
        level_index = last_index + 1   # aktualizovanie indexu, kde začínajú nové riešenia, a posledného indexu, potom sa kontroluje voo vonkajšom cykle while
        last_index = len(combinations) - 1


main()
print("Best solution:", best_solution) # optimálne riešenie