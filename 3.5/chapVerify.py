import hashlib
import random
import sys

if __name__ == "__main__":
    randomNumSize = 8   # 随机数长度
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    # 参数错误
    if len(sys.argv) != 2:
        print("Wrong argument number!")
        exit(0)

    pswd = sys.argv[1]  # 密码
    print("Password:    " + pswd)

    # 生成随机数
    # low = 10 ** (randomNumSize - 1)
    # high = (10 ** randomNumSize) - 1
    seed = random.sample(num, randomNumSize)
    seed = ''.join(str(x) for x in seed)
    print("Seed:        " + seed )

    # 生成MD5
    m = hashlib.md5()
    info = seed + pswd
    info = str.encode(info, encoding='utf-8')
    m.update(info)
    res = m.hexdigest()

    print("MD5:         " + res)

