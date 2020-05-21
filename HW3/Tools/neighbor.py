


def neighbor(size, pos):
    '''get neighboring blocks'''
    (x, y) = pos
    ret = []
    for (dx, dy) in neighbor.neighbor_list:
        if (x + dx < 0 or x + dx >= size[0] or
                y + dy < 0 or y + dy >= size[1]):
            continue
        ret.append((x + dx, y + dy))

    return ret

neighbor.neighbor_list = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]
