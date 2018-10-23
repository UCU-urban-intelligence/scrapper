
def find_nearest_point(net, building):
    avg_point = [0, 0]
    counter = 0
    for i in range(len(building['geometry']['coordinates'])):
        for coordinates in building['geometry']['coordinates'][i]:
            avg_point[0] += coordinates[0]
            avg_point[1] += coordinates[1]
            counter += 1
        avg_point[0] = round(avg_point[0] / counter, 6)
        avg_point[1] = round(avg_point[1] / counter, 6)

    min_distance = 1000
    nearest_point = {}

    for point in net:
        distance = ((point['coordinates'][0] - avg_point[0])**2 + (point['coordinates'][1] - avg_point[1])**2)**(1/2)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    return nearest_point