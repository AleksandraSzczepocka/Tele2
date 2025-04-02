#--------------------------------------
#  Autorzy:
#  Dawid Pakos 251604
#  Aleksandra Szczepocka 251642                               
#--------------------------------------


import numpy as np

matrix_H = np.array([
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
])

BIT_NR = 8  # Liczba bitów wiadomości


def encode(input_file, encoded_file):
    with open(input_file, "rb") as infile, open(encoded_file, "w") as outfile:
        byte = infile.read(1)
        while byte:
            byte_val = ord(byte)  # Konwersja bajtu na wartość liczbową
            content = np.array([int(b) for b in format(byte_val, '08b')])  # Zamiana na listę bitów

            # Mnożenie wiadomości przez 8 pierwszych kolumn macierzy
            check = np.dot(matrix_H[:, :BIT_NR], content) % 2

            # Tworzenie zakodowanych ciągów bitów
            encoded_bits = np.concatenate((content, check))
            outfile.write("".join(map(str, encoded_bits)) + "\n")

            byte = infile.read(1)

    print(f"Plik '{input_file}' został zakodowany do '{encoded_file}'.")


def decode(encoded_file, output_file):
    with open(encoded_file, "r") as infile, open(output_file, "wb") as outfile:
        for line in infile:
            encoded_bits = [int(b) for b in line.strip()]

            # Obliczanie błędów (syndrom)
            mistakes = [sum(encoded_bits * matrix_H[i]) % 2 for i in range(BIT_NR)]

            if sum(mistakes) == 0:
                pass  # Brak błędów
            else:
                # Dwa błędy
                error_found = False
                for i in range(16):
                    for j in range(i + 1, 16):
                        # Sprawdzanie, czy kombinacja dwóch kolumn może prowadzić do danego syndromu
                        if all(mistakes[k] == (matrix_H[k][i] ^ matrix_H[k][j]) for k in range(BIT_NR)):
                            # Naprawianie błędów
                            encoded_bits[i] ^= 1
                            encoded_bits[j] ^= 1
                            error_found = True
                            break
                    if error_found:
                        break

                # Pojedynczy błąd
                if not error_found:
                    for i in range(16):
                        if all(mistakes[j] == matrix_H[j][i] for j in range(BIT_NR)):
                            encoded_bits[i] ^= 1  # Naprawianie błędu
                            break

            # Konwersja naprawionej wiadomości na bajt
            byte_val = int("".join(map(str, encoded_bits[:BIT_NR])), 2)
            outfile.write(byte_val.to_bytes(1, 'big'))

    print(f"Plik '{encoded_file}' został zdekodowany do '{output_file}'.")


# Menu wyboru
if __name__ == "__main__":
    print("1. Kodowanie pliku")
    print("2. Dekodowanie pliku")
    choice = input("Wybierz opcję: ")

    if choice == "1":
        input_file = input("Podaj nazwę pliku do zakodowania z rozszerzeniem: ")
        encoded_file = input("Podaj nazwę pliku wyjściowego z rozszerzeniem .txt/.bin (zakodowanego): ")
        encode(input_file, encoded_file)
    elif choice == "2":
        encoded_file = input("Podaj nazwę pliku zakodowanego z rozszerzeniem: ")
        output_file = input("Podaj nazwę pliku wyjściowego z rozszerzeniem .txt/.bin (zdekodowanego): ")
        decode(encoded_file, output_file)
    else:
        print("Nieprawidłowy wybór.")
