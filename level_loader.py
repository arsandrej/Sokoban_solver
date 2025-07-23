def load_level(file_path):
    with open(file_path) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines
