import multiprocessing
from multiprocessing import Process, Pool, RLock, Event, Manager
import time
from random import randint

import sys
import os
# ------------------------------------

def write_matrix(matrix_1, matrix_2, name):
    with open(f'matrix_{name}_A.txt', 'w', encoding='utf-8') as matrix_name_1:
        matrix_name_1.write("Матрица A:\n")
        for row in matrix_1:
            matrix_name_1.write(' '.join([str(a) for a in row]) + '\n')
    with open(f'matrix_{name}_B.txt', 'w', encoding='utf-8') as matrix_name_2:
        matrix_name_2.write("Матрица B:\n")
        for row in matrix_2:
            matrix_name_2.write(' '.join([str(a) for a in row]) + '\n')

def generation(size):
    return [[randint(-100, 100)for j in range(size)] for i in range(size)]
def write_result(matrix_3, name):
    with open(f'matrix_{name}_C.txt', 'w', encoding='utf-8') as matrix_name_3:
        matrix_name_3.write("Матрица C (результирующая матрица умножения):\n")
        for row in matrix_3:
            matrix_name_3.write(' '.join([str(a) for a in row]) + '\n')
def element(index, A, B, size):

    i, j = index
    res = 0
    for k in range(size):
        res += A[i][k] * B[k][j]

    return res
def main_matrix(size,event):
    with Pool(processes=size*2) as pool:
        name = 1
        while event.is_set():
            first_matrix = generation(size)
            second_matrix = generation(size)
            write_matrix(first_matrix, second_matrix, name)
            third_matrix = [[] for i in range(size)]
            for i in range(size):
                for j in range(size):
                    result = pool.apply_async(element, ((i, j), first_matrix, second_matrix, size))
                    res_matrix = result.get()
                    third_matrix[i].append(res_matrix)
            write_result(third_matrix, name)
            print(f'{name} файл матриц ')
            name+=1
            time.sleep(5)
        print('Завершение')

def main():
    mn = Manager()
    event = Event()
    Exit = mn.Namespace()
    Exit.comment = ''
    event.set()
    size = int(input("Введите размерность матрицы: "))
    process_matrix = Process(target=main_matrix, args=(size,event))
    print('Чтобы выйти, нажмите q')
    process_matrix.start()
    while Exit.comment != "q":
        Exit.comment = input()
    # while True:
    #     if input('Нажмите q, чтобы выйти:') == 'q':
    #         event.clear()
    #         break
    event.clear()
    process_matrix.join()



if __name__ == '__main__':
   main()