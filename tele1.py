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
            message = np.array([int(b) for b in format(byte_val, '08b')])  # Zamiana na listę bitów (numpy array)

            # Poprawiona operacja: mnożymy wiadomość przez 8 pierwszych kolumn macierzy
            check = np.dot(matrix_H[:, :BIT_NR], message) % 2

            # Tworzymy zakodowany ciąg bitów
            encoded_bits = np.concatenate((message, check))
            outfile.write("".join(map(str, encoded_bits)) + "\n")

            byte = infile.read(1)

    print("Plik został zakodowany.")


def decode(encoded_file, output_file):
    with open(encoded_file, "r") as infile, open(output_file, "wb") as outfile:
        for line in infile:
            encoded_bits = [int(b) for b in line.strip()]
            message = encoded_bits[:BIT_NR]
            received_check = encoded_bits[BIT_NR:]

            # Obliczanie błędów (syndrom)
            mistakes = [sum(encoded_bits * matrix_H[i]) % 2 for i in range(BIT_NR)]

            if sum(mistakes) == 0:
                pass  # Brak błędów
            else:
                # Sprawdzanie czy są dwa błędy (próbujemy wykryć dwie błędne kolumny)
                error_found = False
                for i in range(16):
                    for j in range(i + 1, 16):
                        # Sprawdzamy, czy kombinacja dwóch błędów może prowadzić do danego syndromu
                        if all(mistakes[k] == (matrix_H[k][i] ^ matrix_H[k][j]) for k in range(BIT_NR)):
                            # Naprawiamy oba błędy
                            encoded_bits[i] ^= 1
                            encoded_bits[j] ^= 1
                            error_found = True
                            break
                    if error_found:
                        break

                # Jeśli to pojedynczy błąd, naprawiamy tylko ten jeden błąd
                if not error_found:
                    for i in range(16):
                        if all(mistakes[j] == matrix_H[j][i] for j in range(BIT_NR)):
                            encoded_bits[i] ^= 1  # Naprawiamy pojedynczy błąd
                            break

            # Konwersja naprawionej wiadomości na bajt
            byte_val = int("".join(map(str, encoded_bits[:BIT_NR])), 2)
            outfile.write(byte_val.to_bytes(1, 'big'))

    print("Plik został zdekodowany.")


# Menu wyboru
if __name__ == "__main__":
    print("1. Kodowanie pliku")
    print("2. Dekodowanie pliku")
    choice = input("Wybierz opcję: ")

    if choice == "1":
        file_name = input("Podaj nazwę pliku do zakodowania: ")
        encode(file_name, "encoded.txt")
    elif choice == "2":
        decode("encoded.txt", "decoded.bin")
    else:
        print("Nieprawidłowy wybór.")
