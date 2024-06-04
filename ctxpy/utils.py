def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def flatten(lofl):
    return [item for l in lofl for item in l]
