import random


def flaky_task(name):
    if random.random() < 0.6:
        raise Exception("Random failure")
    print(f"Task succeeded for {name}")

def always_success_task(name):
    print(f"Always succeeds for {name}")
