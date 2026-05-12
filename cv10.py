import random
#------------------------------------------------------------------------------------------------------------
# matica vzdialeností a parametre problému - max počet iterácií pre GRASP, p, alfa, počet umiestnení stredísk
#------------------------------------------------------------------------------------------------------------
D = [
    [0, 12, 24, 38, 22, 10, 10, 26, 22, 34],
    [12, 0, 12, 26, 34, 10, 20, 26, 22, 22],
    [24, 12, 0, 14, 48, 22, 22, 20, 10, 10],
    [38, 26, 14, 0, 62, 36, 36, 22, 24, 12]
]
max_iter = 100
p = 2
a = 0.5
depots = 4
#----------------------------
# najlepšie nájdené riešenie
#----------------------------
best_sol = []
best_sol_val = float('inf')
random.seed(42)

#------------------------------------------------------
# skontroluje a prípadne aktualizuje najlepšie riešenie
#------------------------------------------------------
def update_best_sol(solution):
    new_sol_val = get_target_value(solution)
    if new_sol_val < best_sol_val:
        best_sol = []
        for i in range(len(solution)):
            best_sol.append(solution[i])
        best_sol_val = new_sol_val
#----------------------------------------
# vráti hodnotu účelovej funkcie reišenia
#----------------------------------------
def get_target_value(solution):
    if len(solution) == 0:
        return float('inf')
    target_value = 0
    customer_value
    
    for i in range(len(D[0])):
        customer_value = float('inf')
        for j in range(solution):
            if D[solution[j]][i] < customer_value:
                customer_value = D[solution[j]][i]
                
        target_value += customer_value    
        
    return target_value
#----------------------------------------------------------------------------------------------------------------------------------------------------------
# funkcia vyhodnocuje úsporu po pridaní prvku o riešenia, pridaný prvok je v tomto prípade vždy na konci, lebo sa používa zoznam indexov miesto 0 1 vektora
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def greedy_function(solution):
    original_min, new, savings = 0
    for i in range(len(D[0])):  # prejdeme všetkých zákazníkov a nájdeme ich predošlé priradenie/najbližšie stredisko, teda ideme všetky prvky v solution okrem posledného, s tým sa potom porovná to nájdené min
        original_min = float('inf')
        new = D[solution[-1]][i]  # toto je vzdialenosť pridaného strediska (ktoré je vždy na konci zoznamu) a daného zákazníka na porovnanie s min vzdialenosťou z predošlých
        
        for j in range(len(solution) - 1):
            if D[solution[j]][i] < original_min:
                original_min = D[solution[j]][i]
        
        if new < original_min: # pripočítanie prípadnej úspory
            savings += (original_min - new)
            
    return savings        

def construct_solution(solution):
    solution = []
    C = list(range(depots))
    
    while len(C) > 0:
        S_min = 0
        S_max = 0
        RCL = []
        
        for i in range(len(C)):  # vytvorenie RCL množiny
            if greedy_function(C[i]) <= (S_min + a*(S_max - S_min)):
                RCL.append(C[i])

        s = random.randrange(len(RCL)) # náhodný výber z RCL
        solution.append(RCL.pop(s))
        
def local_search(solution):
    return 0

def run_GRASP(max_iter, p, a):
    solution = []
    
    for i in range(max_iter):
        construct_solution(solution)
        local_search(solution)
        update_best_sol(solution)
#----------------
# výpis výsledkov
#----------------            
def print_problem_results():  
    print("///////////////////////////////////////////////////////////////////////////////")
    print("p-median problem")
    print(f"Number of possible placements: {p}")
    print(f"p: {p}")
    print(f"alpha (a): {a}")
    print("Method used: GRASP (Greedy Randomized Adaptive Search Procedures) metaheuristic")
    print("-------------------------------------------------------------------------------")
    print(f"max iterations: {max_iter}")
    print(best_sol)
    print(f"Best solution value: {best_sol_val}")
    print("///////////////////////////////////////////////////////////////////////////////")
    
        

def main():
    run_GRASP()
    print_problem_results()
    
main()