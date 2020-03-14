from time import sleep

def print_and_delay():
    print("Get ready for a delay")
    for i in range(5):
        print(f"Delay {i}")
        sleep(0.5)

if __name__ == "__main__":
    print_and_delay()
