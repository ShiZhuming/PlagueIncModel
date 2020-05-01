from GetWorldData import sync
import matplotlib as plt
import numpy as np
import time
save_dir = r'D:\MyData\Python\2019-nCoV'
data_dir = save_dir + r"\data\total_data.txt"

I_china = [0, 27, 28, 41, 94, 170, 260, 403, 526, 771, 1224, 1870, 2631, 4369, 5762, 7417, 9336, 11219, 13776, 16398,
           19411, 22975, 26308, 29032, 31834, 33764, 35982, 37626, 38832, 51860, 55748, 56873, 57416, 57934, 58016,
           57805, 56727, 55389, 53284, 51411, 49824, 47672, 45604, 43258, 39919, 37414, 35329, 32652, 30004, 27433,
           25352, 23784, 22177, 20533, 19016, 17721, 16145, 14831, 13526, 12094, 10734, 9898, 8967, 8056, 7263, 6569]
data_list = [I_china]
name_list = ['I_china']
new_name = ['I_china', 'I_us', 'I_italy', 'I_south_korea', 'I_germany', 'I_france', 'I_iran', 'I_spain', 'I_uk', 'I_turkey',
            'I_switzerland']
popu_list = [1395380000, 3271700001, 60430000, 51640000, 82930000, 66990000, 81800000, 46720000, 66488991, 82000000,
             8508900]

with open(data_dir, 'r') as data:
    country_data = data.readlines()
names = locals()
for _ in country_data:
    entry = _.strip().split('=')
    names[entry[0].strip()] = eval(entry[1].strip())
    data_list.append(names[entry[0].strip()])
    name_list.append(entry[0].strip())
#count = 0
#I_0 = data_list[count]
#country = name_list[count]
#population = popu_list[count]


def simulate(E, I, ind, dt, alphaS=6.394, beta=1/10, gamma=0.13731, delta=0.00885, kN=0.1, expo=1.5):
    alpha = alphaS / ind ** expo
    popu_rate = I[ind]/population
    dI = I[ind] - I[ind - 1]
    E[ind - 1] = 1 / beta * (dI / dt + (gamma + delta) * I[ind - 1])
    E.append(dt * ((alpha * (1-popu_rate) - beta) * E[ind - 1] + alpha * (1 - popu_rate) * kN * I[ind - 1]) + E[ind - 1])
    I.append(dt * (beta * E[ind] - (gamma + delta) * I[ind]) + I[ind])


def distance(listA, listB):
    dist = 0
    for _ in range(0, len(listA)):
        dist += (listA[_] - listB[_])**2
    return (dist / len(listA))**0.5


def calculate(I_real, value):
    alphaS = value[0]
    beta = value[1]
    gamma = value[2]
    delta = value[3]
    kN = value[4]
    expo = value[5]
    population = value[6]
    cek = True
    E = [0]
    I = [0, I_real[1]]
    for day in range(1, 100):
        simulate(E, I, day, 1, alphaS, beta, gamma, delta, kN, expo)
    for _ in I:
        if _ >= population:
            cek = False
            break
    return distance(I_real, I), cek


def optimize(
        I_real,
        popu,
        A=(0.01, 0.5, 10),
        B=(1, 0.5, 14),
        C=(0.01, 0.5, 10),
        D=(0.01, 0.1, 1),
        E=(-1, 0.1, 1),
        F=(0, 0.2, 2),
        duration=100):
    cal_times = 1
    ini = [A, B, C, D, E, F]
    for _ in ini:
        count_1 = (_[2]-_[0])/_[1]
        if count_1 == 0:
            count_1 = 1
        cal_times *= round(count_1)
    result_combination = []
    result_dist = []
    # optimizing A
    A0, As, Ar = A
    B0, Bs, Br = B
    C0, Cs, Cr = C
    D0, Ds, Dr = D
    E0, Es, Er = E
    F0, Fs, Fr = F
    alphaS = A0
    turning_time = B0
    gamma = C0
    delta = D0
    kN = E0
    expo = F0
    count = 0
    s_time = time.time()
    while alphaS <= Ar:
        while turning_time <= Br:
            while gamma <= Cr:
                while delta <= Dr:
                    while kN <= Er:
                        while expo <= Fr:
                            try:
                                res, cek = calculate(I_real, [alphaS, 1/turning_time, gamma, delta, kN, expo, popu])
                            except Exception:
                                cek = False
                            if cek:
                                result_dist.append(res)
                                result_combination.append([alphaS, turning_time, gamma, delta, kN, expo])
                            #print("alphaS={}\tturning_time={}\tgamma={}\tdelta={}"
                            #                          .format(alphaS, turning_time, gamma, delta))
                            count += 1
                            c_time = time.time()
                            print("\r{:.2%} proc {:.1f}s estimate in {:.1f}s".
                                  format(count / cal_times,
                                         c_time - s_time,
                                         (c_time - s_time) / (count / cal_times) * (1 - count / cal_times)),
                                  end='', flush=True)
                            expo += Fs
                        expo = F0
                        kN += Es
                    kN = E0
                    delta += Ds
                delta = D0
                gamma += Cs
            gamma = C0
            turning_time += Bs
        turning_time = B0
        alphaS += As
    print('\nMinimum distance Average:{:.1f}'.format(min(result_dist)))
    result = result_combination[result_dist.index(min(result_dist))]
    print('alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential')
    for thing in result:
        print("{:.5f}".format(thing), end='\t')
    print('\n')
    E = [0]
    I = [0, I_real[1]]
    for day in range(1, duration):
        simulate(E, I, day, 1, result[0], 1/result[1], result[2], result[3], result[4], result[5])
    return result, I, E


def train(batch,
          popu,
          ini=[(0.01, 1, 10), (0.01, 1, 10), (0.01, 1, 10), (0.01, 1, 10), (0.01, 0.1, 1), (0, 0.2, 2)],
          duration=100,
          filename='Result'):
    """
    使用梯度下降最小二乘法拟合参数
    需要传入初值范围，将找到局部最小值
    :param batch: 训练次数，整数，数字越大精度越高
    :param ini: 初值条件，一个列表，包含了所有参数的初始起始值、步长的初始终止值
    :param duration: 最后拟合结果所需要计算的持续时间（天）
    :return: 返回最优解的参数集、预测的感染数和暴露数
    """
    print("Batch to be trained:{}".format(batch))
    for _ in range(batch):
        print("Current Process:{}".format(_ + 1))
        data, I_result, E_result = optimize(I_0, popu, A=ini[0], B=ini[1], C=ini[2], D=ini[3], E=ini[4], F=ini[5],
                                            duration=duration)
        #print(data)
        for num in range(6):
            step = ini[num][1]
            if ini[num][0] < data[num] < ini[num][2]:
                start = data[num] - step
                end = data[num] + step
                n_step = step / 5
            elif ini[num][0] >= data[num]:
                start = ini[num][0] - step
                if start <= 0:
                    start = step / 5
                end = ini[num][0] + step
                n_step = step
            elif ini[num][2] <= data[num]:
                start = ini[num][2] - step
                end = ini[num][2] + step
                n_step = step
            ini[num] = (start, step / 5, end)
    print('<<<<<Training Process Complete>>>>>')
    print('alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential')
    with open(save_dir + r'\results\{}_popu.txt'.format(filename), 'w') as f:
        f.writelines('alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential\n')
        for thing in data:
            print("{:.5f}".format(thing), end='\t')
            f.writelines("{:.5f}\t".format(thing))
        f.writelines('\n')
        print('\n')
        for _ in range(0, len(I_result) - 1):
            print(_, "{:.0f}".format(I_result[_]), "{:.0f}".format(E_result[_]), sep='\t')
            f.writelines("{}\t{:.0f}\t{:.0f}\n".format(_, I_result[_], E_result[_]))


def gradient_descent(I_real, batch=100, step=0.1, initial_value=np.array([2, 2, 0, 0.03648, 0.5, 1])):
    small_step = step / 1000
    cal_mat = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])
    value = initial_value
    dist = calculate(I_real, value)
    while True:
        gradient = np.array([
            calculate(I_real, value + small_step * cal_mat[0])[0] -
            calculate(I_real, value - small_step * cal_mat[0])[0],
            calculate(I_real, value + small_step * cal_mat[1])[0] -
            calculate(I_real, value - small_step * cal_mat[1])[0],
            0,
            0,
            calculate(I_real, value + small_step * cal_mat[2])[0] -
            calculate(I_real, value - small_step * cal_mat[2])[0],
            calculate(I_real, value + small_step * cal_mat[3])[0] -
            calculate(I_real, value - small_step * cal_mat[3])[0]
        ]) / (2 * small_step)
        print(value)
        value = value - step * gradient
        if dist <= calculate(I_real, value):
            break
        else:
            dist = calculate(I_real, value)
    return value, dist

"""
factor, I_res = optimize(I_0, A=(1, 1, 10), B=(0.5, 0.5, 10), C=(0.8, 0.01, 0.9), D=(0.00509, 0.00001, 0.00510), E=(0.01, 0.1, 1))
for _ in range(0, len(I_res)):
    print(_, I_res[_], sep='\t')
"""
# Training the model
for count in range(11):
    #if name_list[count] in ['I_USA']:
    if True:
        new_ind = new_name.index(name_list[count])
        I_0 = data_list[count]
        country = name_list[count]
        population = popu_list[new_ind]
        print('Current Country:{}'.format(country))
        train(10,
              population,
              ini=[
                  (0.01, 0.1, 10),
                  (0.01, 0.1, 10),
                  (0.065339, 0.00001, 0.065339),
                  (0, 0.00001, 0),
                  (0.01, 0.1, 1),
                  (0, 0.2, 2)
              ],
              duration=300,
              filename=country
              )


def contour_plot():
    # Contour Plot
    with open(r'D:/MyData/Python/2019-nCoV/map.txt', 'a+') as f:
        E = [0]
        I = [0, 1]
        for x in range(1, 10001):
            for y in range(1, 10001):
                f.write("{}\t{}\t{}\n".format(x/1000, y/1000, calculate(I_0, [x/1000, y/1000, 0, 0.003648, 0.008, 1])[0]))
            print("\r{:.2%}".format(x/10000), flush=True, end='')

    print('Done!')

"""
result = gradient_descent(I_0, step=0.00001)
print("alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential\n{}\nDistance:{}".format(result[0], result[1][0]))
E = [0]
I = [0, 1]
for day in range(1, 250):
    simulate(E, I, day, 1, result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
for _ in range(1, len(I)):
    print(_, "{:.0f}".format(I[_]), "{:.0f}".format(E[_-1]), sep='\t')
"""