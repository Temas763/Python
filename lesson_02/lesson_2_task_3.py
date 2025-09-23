def square(side):
    area = side * side
    if not isinstance(side, int):
        area = -(-area // 1)
    return int(area)


print(square(5.2))
