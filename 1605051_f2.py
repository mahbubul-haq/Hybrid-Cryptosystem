import _1605051_f4
import _1605051_f3
import time
import socket
import pickle
import sys

def get_private_key():
    try:
        while True:
            try:
                with open("Don't Open this/private_key", "r") as file:
                    time.sleep(3)
                    lines = file.readlines()
                    key = [int(i.strip()) for i in lines]
                    return key

            except:
                pass
            time.sleep(5)
    except:
        pass


def read_server_data():
    s = socket.socket()
    port = 12346
    s.connect(('127.0.0.1', port))
    data = s.recv(500000)
    data_arr = pickle.loads(data) #[cipertex(hex string), encrypted_key(integers), public key(e, n)]
    s.close()
    return  data_arr

arr = read_server_data()

private_key = get_private_key()

arr[1] = _1605051_f4.rsa_decrypt(private_key, arr[1])

plain_text = ''
for i in arr[0]:
    now = [hex(int(i[j:j + 2], 16)) for j in range(0, len(i), 2)]
    now = [[now[j * 4 + k] for k in range(4)] for j in range(4)]
    now_plain_text = _1605051_f3.aes_decrypt(arr[1], now)
    plain_text += "".join(["".join([chr(int(j, 16)) for j in i]) for i in now_plain_text])
print(plain_text)
with open("Don't Open this/dpt", "w") as file:
    file.write(plain_text)

