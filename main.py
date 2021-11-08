import random
import time
from multiprocessing import Process, Pool, Event, Manager, Value
import keyboard

def el(index, A, B, size):
    i, j = index
    res = 0
    for k in range(size):
        res += A[i][k] * B[k][j]
    return res

def main():
    ev = Event()
    ev.set()
    size = int(input("Размер матрицы: "))
    main_event = Process(target=general_operations, args=(size, ev))
    main_event.start()
    while keyboard.read_key() == "p":
        print("You pressed pause, exit")
        break
    ev.clear()
    main_event.join()

def set_matrix_size(size):
    return [[random.randint(-100, 100) for j in range(size)] for i in range(size)]

def write_matrix(matrix, filename):
    for id, item in enumerate(matrix):
        with open(f'{filename[id]}_{random.randint(1, 100)}.txt', 'w') as file:
            file.write(f"Матрица {id}:\n")
            for i in item:
                file.write(' '.join([str(j) for j in i]) + '\n')

def get_result(arrays, size, pool):
    for i in range(size):
        for j in range(size):
            result = pool.apply_async(el, ((i, j), arrays[0], arrays[1], size))
            res_matrix = result.get()
            arrays[2][i].append(res_matrix)
    return arrays[2]

def general_operations(size, event_stop):
        while event_stop.is_set():
            with Pool(processes=size * 2) as pool:
                array1, array2 = set_matrix_size(size), set_matrix_size(size)
                write_matrix([array1, array2], ['matrix_1', 'matrix_2'])
                array3 = [[] for i in range(size)]
                array3 = get_result([array1,array2,array3], size, pool)
                write_matrix([array3], ['maxtix_3'])
                time.sleep(5)



if __name__ == '__main__':
    main()
