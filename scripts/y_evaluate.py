import sys
import pandas as pd
import numpy as np


def noise(f):
    def noise_wrapper(*args):
        v = f(*args) * np.random.normal(1, 0.1)
        if v > 10:
            v = 10
        if v < 0:
            v = 0
        return v
    return noise_wrapper


def magic(row):
    if row["inappropriate_type"] == 1:
        return 0

    AIR_QUALITY_COEFF = 0.115
    AREA_COEFF = 0.125
    CLOSEST_SHOP_COEFF = 0.025
    CLOUD_COVER_COEFF = 0.065
    HUMIDITY_COEFF = 0.065
    SHOPS_AMOUNT_COEFF = 0.055
    TEMPERATURE_COEFF = 0.065
    ROFF_TYPE_COEFF = 0.185
    ERROR_COEFF = 0.3

    air_quality = calc_air_quality(row["air_quality"])
    area = calc_area(row["area"])
    closest_shop = calc_closest_shop(row["closest_shop"])
    cloud_cover = calc_cloud_cover(row["cloud_cover"])
    humidity = calc_humidity(row["humidity"])
    shops_amount = calc_shops_amount(row["shops_amount"])
    temperature = calc_temperature(row["temperature"])
    roof_type = calc_roof_type(row["flat_roof"], row["gabled_roof"], row["round_roof"])
    error = np.random.uniform(0, 10)

    y = AIR_QUALITY_COEFF * air_quality +\
        AREA_COEFF * area +\
        CLOSEST_SHOP_COEFF * closest_shop +\
        CLOUD_COVER_COEFF * cloud_cover +\
        HUMIDITY_COEFF * humidity +\
        SHOPS_AMOUNT_COEFF * shops_amount +\
        TEMPERATURE_COEFF * temperature +\
        ROFF_TYPE_COEFF * roof_type +\
        ERROR_COEFF * error

    y = round(y)
    if y > 10:
        y = 10
    if y < 0:
        y = 0
    return y


@noise
def calc_air_quality(a_q):
    if a_q < 0:
        return 0
    if a_q < 50:  # x: 0-50, y: 0-2
        return linear_dependence(0, 2, 0, 50, a_q)
    if a_q < 80:  # x: 50-80, y: 2-8
        return custom_sin(2, 8, 50, 80, a_q)
    if a_q < 100: # x: 80-100, y: 8-10
        return linear_dependence(8, 10, 80, 100, a_q)
    return 10

@noise
def calc_area(area):
    if area < 9:
        return 0
    if area < 60:  # x: 9-60, y: 0-4
        return linear_dependence(0, 4, 9, 60, area)
    if area < 900:  # x: 60-900, y: 4-10
        return linear_dependence(4, 10, 60, 900, area)
    return 10

@noise
def calc_closest_shop(c_s):
    if c_s < 0:
        return 10
    if c_s < 100:  # x: 0-100, y: 10-9
        return linear_dependence(9, 10, 0, 100, c_s, True)
    if c_s < 500:  # x: 100-500, y: 9-6
        return linear_dependence(6, 9, 100, 500, c_s, True)
    if c_s < 1000:  # x: 500-1000, y: 6-5
        return linear_dependence(5, 6, 500, 1000, c_s, True)
    if c_s < 2000:  # x: 1000-2000, y: 5-2
        return linear_dependence(2, 5, 1000, 2000, c_s, True)
    if c_s < 10000:  # x: 2000-10000, y: 2-0
        return linear_dependence(0, 2, 2000, 10000, c_s, True)
    return 0

@noise
def calc_cloud_cover(c_c):
    if c_c < 0:
        return 0
    if c_c < 0.35:  # x: 0-0.35, y: 0-10
        return custom_sin(0, 10, 0, 0.35, c_c)
    if c_c < 1:  # x: 0.35-1, y: 10-0
        return custom_sin(0, 10, 0.35, 1, c_c, True)
    return 0

@noise
def calc_humidity(humidity):
    if humidity < 0:
        return 0
    if humidity < 0.65:  # x: 0-0.65, y: 0-10
        return custom_sin(0, 10, 0, 0.65, humidity)
    if humidity < 1:  # x: 0.65-1, y: 10-0
        return custom_sin(0, 10, 0.65, 1, humidity, True)
    return 0

@noise
def calc_shops_amount(s_a):
    if s_a < 0:
        return 0
    if s_a < 10:  # x: 0-10, y: 0-7
        return linear_dependence(0, 7, 0, 10, s_a)
    if s_a < 20:  # x: 10-20, y: 7-9
        return linear_dependence(7, 9, 10, 20, s_a)
    if s_a < 40:  # x: 20-40, y: 9-10
        return linear_dependence(9, 10, 20, 40, s_a)
    return 10

@noise
def calc_temperature(temperature):
    if temperature < 0:
        return 0
    if temperature < 11:  # x: 0-11, y: 0-10
        return custom_sin(0, 10, 0, 11, temperature)
    if temperature < 21:  # x: 11-21, y: 10-0
        return custom_sin(0, 10, 11, 21, temperature, True)
    return 0

@noise
def calc_roof_type(f_r, g_r, r_r):
    if f_r:
        return 10
    if g_r:
        return 4
    if r_r:
        return 1.5
    return 7

def linear_dependence(min_score, max_score, min_x, max_x, x, inv = False):
    temp = ((x - min_x) / (max_x - min_x)) * (max_score - min_score)
    if (inv):
        return max_score - temp
    return min_score + temp

def custom_sin(min_score, max_score, min_x, max_x, x, inv = False):
    k = -1 if inv else 1
    return min_score + (
            k * np.sin(((x - min_x) / (max_x - min_x)) * np.pi - np.pi / 2) + 1
    ) / 2 * (max_score - min_score)


if __name__ == '__main__':
    file_name = sys.argv[1]

    df = pd.read_csv(file_name)

    df['efficiency'] = df.apply(magic, axis=1)

    df.to_csv(file_name)
