def create_random_str(size):
    import random
    return ''.join(random.choice([chr(i) for i in range(
        ord('a'), ord('z'))]) for _ in range(size))
