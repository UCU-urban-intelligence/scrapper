def create_net(lat1, lng1, lat2, lng2, stepsize):
    arr = []
    while lat1 <= lat2:
        i = lng1
        while i <= lng2:
            arr.append((lat1, i))
            i += stepsize
        lat1 += stepsize
    return arr


def net_by_quantity(lat0, lng0, lat1, lng1, qty=36):
    steps = round(qty**(1/2)) + 1
    step_lat = (lat1 - lat0) / steps
    step_lng = (lng1 - lng0) / steps
    net = []
    for i in range(1, steps):
        for j in range(1, steps):
            net.append((lat0 + i * step_lat, lng0 + j * step_lng))
    return net
