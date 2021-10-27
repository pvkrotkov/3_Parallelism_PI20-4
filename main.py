from multiprocessing import Pool, Process, Event
from random import randint
from time import sleep
from pathlib import Path


def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    return i, j, res


def write_matrix(matrix, filename):
    with open(filename, 'w') as file:
        for rows in matrix:
            print(', '.join(map(str, rows)), file=file)
        

def create_matrix(rows, columns, random=False):
    if random:
        return [[randint(1, 100) for _ in range(columns)] for _ in range(rows)]
    return [[0] * columns for _ in range(rows)]


def matrix_multiplying(size_matrix, stop):
    count = 1
    while not stop.is_set():
        matrix1 = create_matrix(size_matrix, size_matrix, random=True)
        matrix2 = create_matrix(size_matrix, size_matrix, random=True)
        write_matrix(matrix1, f'random_matrices/generation_number_{count}_random_matrix1.txt')
        write_matrix(matrix2, f'random_matrices/generation_number_{count}_random_matrix2.txt')

        rows = len(matrix1)
        columns = len(matrix2[0])
        matrix3 = create_matrix(rows, columns)

        with Pool(rows * columns) as pool:
            results = []
            for i in range(rows):
                for j in range(columns):
                    results.append(pool.apply_async(element, [(i,j), matrix1, matrix2]))
            for result in results:
                i, j, res = result.get()
                matrix3[i][j] = res
        
        write_matrix(matrix3, f'random_matrices/generation_number_{count}_matrix.txt')
        count += 1
        sleep(1)


if __name__ == '__main__':
    path = Path('random_matrices')
    if not path.is_dir():
        path.mkdir()
    size_matrix = int(input('Введите размер матрицы: '))
    stop = Event()
    process = Process(target=matrix_multiplying, args=[size_matrix, stop])
    process.start()
    while True:
        answer = input('Введите "stop" для остановки: ')
        if answer == 'stop':
            stop.set()
            break

