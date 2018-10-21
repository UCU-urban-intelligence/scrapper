def create_net(lat1, lng1, lat2, lng2, stepsize):
    arr = []
    while lat1 <= lat2:
        i = lng1
        while i <= lng2:
            arr.append((lat1, i))
            i += stepsize
        lat1 += stepsize
    return arr
