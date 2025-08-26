from util import *
from Init import initial
from GO import cross, mutation
from CNS import CNS
from LS import local_search
from time import time
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import numpy as np
from Best_Whales import Best_Whales


def WOA(J, P, n, whales, best_whales, max_iter=200, k=2):
    history, qe_list = [], []
    with (ProcessPoolExecutor() as executor):
    # for _ in range(1):
        for t in range(max_iter):
            a = 2 - t * (2 / max_iter)
            whale_fitness, future_whales, whale_num = [], [], len(whales)
            for i in range(whale_num):
                # print(f'iter={t}, whale_num={i}')
                r1, r2 = np.random.rand(), np.random.rand()
                A, p = 2 * a * r1 - a, np.random.rand()
                if p < 0.5:
                    temp_best_whale = best_whales.get_by_index(int(r2 * best_whales.size()))[1]
                    if abs(A) < 1:
                        whales[i], new_whales = cross(whales[i], temp_best_whale)
                        future_whales.append(new_whales)
                        x, y = calculate_fitness(n, J, P, whales[i]), calculate_fitness(n, J, P, new_whales)
                        if x > y: whales[i], _ = new_whales, whale_fitness.append(y)
                        else: whale_fitness.append(x)
                    else:
                        whales[i] = mutation(whales[i], P)
                        new_whales = mutation(temp_best_whale, P)
                        # whales[i], new_whales = mutation(whales[i], P), mutation(temp_best_whale, P)
                        future_whales.append(new_whales)
                        x, y = calculate_fitness(n, J, P, whales[i]), calculate_fitness(n, J, P, new_whales)
                        if x > y: whales[i], _ = new_whales, whale_fitness.append(y)
                        else: whale_fitness.append(x)
                else:
                    new_whales = CNS(n, J, P, whales[i])
                    future_whales.append(new_whales)
                    x, y = calculate_fitness(n, J, P, whales[i]), calculate_fitness(n, J, P, new_whales)
                    if x > y: whales[i], _ = new_whales, whale_fitness.append(y)
                    else: whale_fitness.append(x)

            te = T_E(whales, J, P, n, whale_fitness, best_whales)
            # print(f'iter={t},te={te}')
            if te <= 0:
                if len(qe_list) >= k-1 and all(int(q) == 0 for q in qe_list[-(k-1):] if q is not None):
                    whales = list(executor.map(local_search, repeat(n), repeat(J), repeat(P), whales))
                    # for i in range(whale_num):
                    #     whales[i] = local_search(n, J, P, whales[i])
            qe_list.append(te)
            fitnesses = [calculate_fitness(n, J, P, w) for w in whales]
            best_w = np.argmin(fitnesses)
            current_best_f, current_best_whale = fitnesses[best_w], whales[best_w]
            best_whales.add(current_best_f, current_best_whale)
            if best_whales.size() > 0: best_fit, best_whale = best_whales.get_by_index(0)
            else: best_fit, best_whale = current_best_f, current_best_whale
            history.append(best_fit)
    return best_whale, history


if __name__ == '__main__':
    pop_size, max_iter, elite_capcity = input("please input pop_size, max_iter and elite_capcity (split with space)":).split()
    start = time()
    n, J, P = encode('datasets/MK01.fjs')
    # n, J, P = encode('datasets/MK08.fjs')
    whales, best_whales = initial(n, J, P, 100), Best_Whales(20)
    # whales = [np.array(w, dtype=int) for w in whales]

    fitness = [calculate_fitness(n, J, P, s) for s in whales]
    sorted_pairs = sorted(zip(fitness, whales), key=lambda x: x[0])
    for fit, whale in sorted_pairs[:20]: best_whales.add(fit, whale)
    if best_whales.size() > 0:
        Cmax, best_ind = best_whales.get_by_index(0)
    else:
        best_ind, Cmax = whales[0], fitness[0]

    b_w, c_h = WOA(J, P, n, whales, best_whales)
    b_t, history = decode(n, J, P, b_w)[0], [Cmax] + c_h
    print(f'time={time() - start}\n{history}')
    # drawGantt(b_t)

