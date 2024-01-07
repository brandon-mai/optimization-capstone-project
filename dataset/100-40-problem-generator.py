import time
import random

def main():
    t = time.localtime()
    filename = (f"input100_{t.tm_mday:0>2d}{t.tm_mon:0>2d}{str(t.tm_year % 100).zfill(2)}"
                f"_{t.tm_hour:0>2d}{t.tm_min:0>2d}{t.tm_sec:0>2d}")
    f = open(f"{filename}.txt", "w")
    f.write("100 40\n")
    for i in range(201):
        for j in range(201):
            if i == j:
                f.write("0 ")
            else:
                f.write(f"{random.randint(1, 100)} ")
        f.write("\n")
    f.close()


if __name__ == "__main__":
    main()
