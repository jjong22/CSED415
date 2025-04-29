import crypt
from itertools import product

s = "dave"
prefix = ""
salt = "RByrWzKkQroXD"
hashed ="jgzSfKmMS/O.6pP0TEIZitkB.gUSqEy5s1vLoklivU5"

CRYPT_SALT = f"$5${salt}$"
CHARS = ''.join(chr(c) for c in range(0x20, 0x7F))

def brute_force():
    for c1, c2, c3 in product(CHARS, repeat=3):
        prefix = f"{c1}{c2}{c3}"
        pwd = prefix + s
        full = crypt.crypt(pwd, CRYPT_SALT)      # '$5$salt$hash'

        print(full)

        if full.endswith(hashed):
            return prefix, full

    return None

if __name__ == "__main__":
    res = brute_force()
    if res:
        prefix, full_hash = res
        # 제어 문자·널 바이트 확인용 이스케이프 표현
        print("FOUND !")
        print("prefix (raw bytes):", prefix.encode('latin-1'))
        print("prefix (repr)     :", repr(prefix))
        print("full hash         :", full_hash)
    else:
        print("Not found.")