import hashlib
import itertools
import time
from concurrent.futures import ThreadPoolExecutor


def generate_passwords():
    return (''.join(p) for p in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=5))


def hash_password(password, algorithm):
    if algorithm == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()


def find_password(target_hash, algorithm):
    for password in generate_passwords():
        if hash_password(password, algorithm) == target_hash:
            return password
    return None


def single_thread_mode(target_hash, algorithm):
    start_time = time.time()
    result = find_password(target_hash, algorithm)
    end_time = time.time()
    return result, end_time - start_time


def multi_thread_mode(target_hash, algorithm, num_threads):
    def worker(passwords_chunk):
        for password in passwords_chunk:
            if hash_password(password, algorithm) == target_hash:
                return password
        return None

    start_time = time.time()
    passwords = list(generate_passwords())
    chunk_size = len(passwords) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
        results = executor.map(worker, chunks)
        for result in results:
            if result:
                end_time = time.time()
                return result, end_time - start_time
    end_time = time.time()
    return None, end_time - start_time


def detect_algorithm(target_hash):
    if len(target_hash) == 32:
        return "md5"
    elif len(target_hash) == 64:
        return "sha256"
    else:
        raise ValueError("Невозможно определить тип хэша. Убедитесь, что вы ввели корректный MD5 или SHA-256 хэш.")


if __name__ == "__main__":
    print("Введите хэш:")
    target_hash = input().strip()

    try:
        algorithm = detect_algorithm(target_hash)
        print(f"Определённый алгоритм хэширования: {algorithm}")
    except ValueError as e:
        print(e)
        exit(1)

    print("Выберите режим: 1 - однопоточный, 2 - многопоточный")
    mode = int(input().strip())

    if mode == 2:
        print("Введите количество потоков:")
        num_threads = int(input().strip())
    else:
        num_threads = 1

    if mode == 1:
        print("\nЗапуск в однопоточном режиме...")
        result, elapsed_time = single_thread_mode(target_hash, algorithm)
    elif mode == 2:
        print(f"\nЗапуск в многопоточном режиме с {num_threads} потоками...")
        result, elapsed_time = multi_thread_mode(target_hash, algorithm, num_threads)
    else:
        print("Неверный выбор режима!")
        exit(1)

    if result:
        print(f"Найден пароль: {result}")
    else:
        print("Пароль не найден.")
    print(f"Затраченное время: {elapsed_time:.2f} сек.")
