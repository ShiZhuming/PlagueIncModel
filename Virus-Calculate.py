I_0 = [0, 41, 45, 62, 121, 198, 291, 440, 571, 830, 1303, 1975, 2762, 4535, 5997, 7711]


def simulate(E, I, ind, dt, alphaS=6.394, beta=1/10, gamma=0.13731, delta=0.00885, kN=0.1, expo=1.5):
    alpha = alphaS / ind ** expo
    dI = I[ind] - I[ind - 1]
    E[ind - 1] = 1 / beta * (dI / dt + (gamma + delta) * I[ind - 1])
    E.append(dt * ((alpha - beta) * E[ind - 1] + alpha * kN * I[ind - 1]) + E[ind - 1])
    I.append(dt * (beta * E[ind] - (gamma + delta) * I[ind]) + I[ind])


def distance(listA, listB):
    dist = 0
    for _ in range(0, len(listA)):
        dist += (listA[_] - listB[_])**2
    return dist ** 0.5


def calculate(I_real, alphaS, beta, gamma, delta, kN, expo):
    cek = True
    E = [0]
    I = [0, 1]
    for day in range(1, 100):
        simulate(E, I, day, 1, alphaS, beta, gamma, delta, kN, expo)
    #for _ in I:
    #    if _ < 0.0:
    #        cek = False
    return distance(I_real, I), cek


def optimize(
        I_real,
        A=(0.01, 0.5, 10),
        B=(1, 0.5, 14),
        C=(0.01, 0.5, 10),
        D=(0.01, 0.1, 1),
        E=(-1, 0.1, 1),
        F=(0, 0.2, 2),
        duration=100):
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
    while alphaS <= Ar:
        while turning_time <= Br:
            while gamma <= Cr:
                while delta <= Dr:
                    while kN <= Er:
                        while expo <= Fr:
                            res, cek = calculate(I_real, alphaS, 1/turning_time, gamma, delta, kN, expo)
                            if cek:
                                result_dist.append(res)
                                result_combination.append([alphaS, turning_time, gamma, delta, kN, expo])
                            #print("alphaS={}\tturning_time={}\tgamma={}\tdelta={}"
                            #                          .format(alphaS, turning_time, gamma, delta))
                            expo += Fs
                        expo = F0
                        kN += Es
                    kN = E0
                    delta += Ds
                delta = D0
                gamma += Cs
            gamma = C0
            print("\r{:.4f}:{:.4f}:{:.4f}".format(alphaS, turning_time, expo), end='', flush=True)
            turning_time += Bs
        turning_time = B0
        alphaS += As
    print('\nMinimum distance:{:.1f}'.format(min(result_dist)))
    result = result_combination[result_dist.index(min(result_dist))]
    print('alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential')
    for thing in result:
        print("{:.5f}".format(thing), end='\t')
    print('\n')
    E = [0]
    I = [0, 1]
    for day in range(1, duration):
        simulate(E, I, day, 1, result[0], 1/result[1], result[2], result[3], result[4], result[5])
    return result, I, E


def train(batch, ini=[(0.01, 1, 10), (0.01, 1, 10), (0.01, 1, 10), (0.01, 1, 10), (0.01, 0.1, 1), (0, 0.2, 2)], duration=100):
    print("Batch to be trained:{}".format(batch))
    for _ in range(batch):
        print("Current Process:{}".format(_ + 1))
        data, I_result, E_result = optimize(I_0, A=ini[0], B=ini[1], C=ini[2], D=ini[3], E=ini[4], F=ini[5], duration=duration)
        #print(data)
        for num in range(6):
            step = ini[num][1]
            if ini[num][0] < data[num] < ini[num][2]:
                start = data[num] - step
                end = data[num] + step
            elif ini[num][0] >= data[num]:
                start = ini[num][0] - step
                if start <= 0:
                    start = step / 5
                end = ini[num][0] + step
            elif ini[num][2] <= data[num]:
                start = ini[num][2] - step
                end = ini[num][2] + step
            n_step = step / 5
            ini[num] = (start, step / 5, end)
    print('<<<<<Training Process Complete>>>>>')
    print('alphaS\t潜伏期\tgamma\tdelta\tkN\tExponential')
    for thing in data:
        print("{:.5f}".format(thing), end='\t')
    print('\n')
    for _ in range(0, len(I_result) - 1):
        print(_, "{:.0f}".format(I_result[_]), "{:.0f}".format(E_result[_]), sep='\t')

"""
factor, I_res = optimize(I_0, A=(1, 1, 10), B=(0.5, 0.5, 10), C=(0.8, 0.01, 0.9), D=(0.00509, 0.00001, 0.00510), E=(0.01, 0.1, 1))
for _ in range(0, len(I_res)):
    print(_, I_res[_], sep='\t')
"""

train(5,
      ini=[
          (0.01, 1, 10),
          (0.01, 1, 10),
          (0.00398, 0.00001, 0.00404),
          (0.00482, 0.00001, 0.00486),
          (0.01, 0.1, 1),
          (0, 0.2, 2)
      ],
      duration=250
      )
