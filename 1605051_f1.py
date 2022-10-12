import time
import socket
import pickle
import _1605051_f4
import _1605051_f3
import os

key = input("Enter key: ")
plain_text = input("Enter plain text: ")
chunks = (len(plain_text) // 16) + (1 if len(plain_text) % 16 != 0 else 0)
plain_text = plain_text.ljust(chunks * 16, " ")

ciphertext = []
for i in range(0, len(plain_text), 16):
    now = plain_text[i: i + 16]
    cur_ciphertext = _1605051_f3.aes_encrypt(key, now)
    cur_ciphertext = [[i[2:].rjust(2, "0") for i in j] for j in cur_ciphertext]
    cur_ciphertext = ''.join([''.join(i) for i in cur_ciphertext])
    ciphertext.append(cur_ciphertext)

rsa_keys = _1605051_f4.get_rsa_keys(128 // 2)

while len(key) < 16:
    key += '.'
key = key[0: 16]

encrypted_key = _1605051_f4.rsa_encrypt(rsa_keys[0], key)

s = socket.socket()
port = 12346
s.bind(('', port))
s.listen(5)

while True:
    print("Waiting for a client...")
    c, addr = s.accept()
    #print('Got connection from', addr)

    lst = [ciphertext, encrypted_key, rsa_keys[0]]
    data = pickle.dumps(lst)
    c.send(data)
    c.close()
    break

path = os.path.dirname(__file__)
path = os.path.join(path, "Don't Open this")
try:
    os.mkdir(path)
except:
    pass

file_name = "private_key"
with open(os.path.join(path, file_name), 'w') as file:
    file.write(str(rsa_keys[1][0]) + "\n")
    file.write(str(rsa_keys[1][1]))

def get_plain_text():
    try:
        while True:
            try:
                with open("Don't Open this/dpt", "r") as file:
                    return file.readline()

            except:
                pass
            time.sleep(5)
    except:
        pass

plaintext = get_plain_text()
print(plaintext)
print(plain_text)
print(plaintext == plain_text)