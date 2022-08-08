def string_to_array(string):
    arr = []
    for i in range(9):
        arr.append(list(string[i * 9: (i + 1) * 9]))
    return arr


def array_to_string(array):
    string = []
    for row in array:
        string.extend(row)
    return "".join([i for i in string])
