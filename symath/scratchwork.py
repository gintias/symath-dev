def make_parameter_tuples(N):
    parameter_tuples = []

    for n in range(N, -1, -1):          # N, N-1, ..., 0
        if n == 0:
            parameter_tuples.append((N, 0, 0, 0))
        else:
            for k in range(N - n, -1, -1):
                max_i = N - n - k

                for i in range(max_i, -1, -1):
                    parameter_tuples.append((N, n, k, i))

    return parameter_tuples


def tuple_from_parameters(c):
    N, n, k, i = c

    result = [0] * N

    # Put the block of n ones starting at index k
    for j in range(k, k + n):
        result[j] = 1

    # Add the extra trailing 1, if i > 0
    if i > 0:
        result[k + n + i - 1] = 1

    return tuple(result)

def to_indices(t):
    return [index for index, value in enumerate(t) if value == 1]

def build_all_tuples(N):
    parameter_tuples = make_parameter_tuples(N)

    return [
        (c, tuple_from_parameters(c))
        for c in parameter_tuples
    ]


def build_all_indices(N):
    all_tuples = build_all_tuples(N)

    return [
        (c, to_indices(t))
        for c, t in all_tuples
    ]

for c, indices in build_all_indices(4):
    print(c, indices)

