from multiprocessing import Manager, Event, Pool, Process
import random
import time

def generate_matrix(size):
    return [[random.randint(1, 100) for i in range(size)] for j in range(size)]

def write(matrix, name, number):
    with open(f'{number}_matrix_{name}.txt', 'w', encoding='utf-8') as m:
        for row in matrix:
            m.write(' '.join([str(i) for i in row]) + '\n')

def element(index, A, B):
    i, j = index
    res = 0
    for k in range(len(A) or len(B)):
        res += A[i][k] * B[k][j]
    return res

def calculation(size, event):
    with Pool(processes=size * 2) as pool:
        num = 1
        while event.is_set():
            first = generate_matrix(size)
            write(first, 'A', num)
            second = generate_matrix(size)
            write(second, 'B', num)
            result = [[] for i in range(size)]
            for i in range(size):
                for j in range(size):
                    res = pool.apply_async(element, ((i, j), first, second))
                    result[i].append(res.get())
            write(result, 'C', num)
            print(f'Файлы для {num} набора матриц созданы')
            num += 1
            time.sleep(3)


def main():
    manager = Manager()
    event = Event()
    event.set()
    size = int(input('Введите размер матрицы: '))
    print('Чтобы остановить создание матриц, напишите stop')
    answer = manager.Namespace()
    answer_comment = ''
    process_matrix = Process(target=calculation, args=(size, event))
    process_matrix.start()
    while answer_comment != "stop":
        answer_comment = input()
    event.clear()
    process_matrix.join()

if __name__ == '__main__':
    main()