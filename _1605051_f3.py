import _1605051_f5
import time

def aes_encrypt(key, plain_text):

    while len(key) < 16:
        key += '.'
    key = key[0:16]

    words = _1605051_f5.key_expansion(key, _1605051_f5.Sbox)

    state = [[ hex(ord(plain_text[i * 4 + j])) for j in range(4)] for i in range(4)]
    #initial round
    state = [[hex(int(words[0][i][j], 16) ^ int(state[i][j], 16)) for j in range(4)] for i in range(4)]

    for x in range(10):
        #sub_bytes
        state = _1605051_f5.sub_bytes(state, _1605051_f5.Sbox)
        #shift_rows
        state = [[state[j][i] for j in range(4)] for i in range(4)]
        state = [_1605051_f5.left_shift(state[i], i) for i in range(4)]
        state = [[state[j][i] for j in range(4)] for i in range(4)]
        #mix columns
        if x != 9: state = _1605051_f5.mix_columns(state, _1605051_f5.Mixer)
        #add roundkeys
        for i in range(4):
            for j in range(4):
                state[i][j] = hex(int(state[i][j], 16) ^ int(words[x + 1][i][j], 16))
    return state

def aes_decrypt(key:str, ciphertext:list):

    while len(key) < 16:
        key += '.'
    key = key[0:16]

    words = _1605051_f5.key_expansion(key, _1605051_f5.Sbox)

    state = ciphertext

    for x in range(10):

        # add roundkeys
        for i in range(4):
            for j in range(4):
                state[i][j] = hex(int(state[i][j], 16) ^ int(words[10 - x][i][j], 16))

        # mix columns
        if x != 0: state = _1605051_f5.mix_columns(state, _1605051_f5.InvMixer)

        # shift_rows
        state = [[state[j][i] for j in range(4)] for i in range(4)]
        state = [_1605051_f5.right_shift(state[i], i) for i in range(4)]
        state = [[state[j][i] for j in range(4)] for i in range(4)]

        state = _1605051_f5.sub_bytes(state, _1605051_f5.InvSbox)

    # final round
    state = [[hex(int(words[0][i][j], 16) ^ int(state[i][j], 16)) for j in range(4)] for i in range(4)]
    return state

if __name__ == "__main__":
    key = input("Enter key: ")
    plaintext = input("Enter plain text: ")
    if len(plaintext) < 16: plaintext = plaintext.ljust(16, ' ')
    plaintext_hex = ''.join([hex(ord(i))[2:].rjust(2, "0") for i in plaintext])

    while len(key) < 16: key += '.'
    key = key[0: 16]

    start = time.time()
    words = _1605051_f5.key_expansion(key, _1605051_f5.Sbox)
    key_scheduling = time.time() - start

    start = time.time()
    state = aes_encrypt(key, plaintext)
    cipher_text = ''.join([''.join([j[2:].rjust(2, "0") for j in i]) for i in state])
    cipher_text_ascii = ''.join([chr(int(cipher_text[i: i + 2], 16)) for i in range(0,len(cipher_text), 2)])
    encryption_time = time.time() - start

    start = time.time()
    state = aes_decrypt(key, state)
    deciphered_text = ''.join([''.join([j[2:].rjust(2, "0") for j in i]) for i in state])
    deciphered_text_ascii = ''.join([chr(int(deciphered_text[i: i + 2], 16)) for i in range(0, len(deciphered_text), 2)])

    decryption_time = time.time() - start

    state = "".join(["".join([chr(int(i[2:], 16)) for i in j]) for j in state])
    #print(state == plaintext)

    hex_key = ''.join([hex(ord(i))[2:].rjust(2,"0") for i in key])
    hex_plain_text = ''.join([hex(ord(i))[2:].rjust(2, "0") for i in plaintext])

    print("\nPlain Text:")
    print(plaintext + "\n" + plaintext_hex + "\n")
    print("Key:\n" + key + "\n" + hex_key + "\n")
    print("Cipher Text:\n" + cipher_text + "\n" + cipher_text_ascii + "\n")
    print("Deciphered Text:\n" + deciphered_text + "\n" + deciphered_text_ascii)

    print("\nExecution Time")
    print("Key Scheduling:", key_scheduling, "seconds")
    print("Encryption Time:", encryption_time, "seconds")
    print("Decryption Time:", decryption_time, "seconds")