import matplotlib.pyplot as plt
import numpy as np

#さいころをどんどん降っていきそれまでの平均値をたどる。繰り返していくとその平均は期待値(1.5)に近づいていく
#大数の法則
calc_times = 100

#さいころ
sample_array = np.array([1,2,3,4,5,6])
nuber_cnt = np.arange(1, calc_times + 1 )

#４つのパスを作成

for i in range(8):
    p = np.random.choice(sample_array, calc_times).cumsum()
    plt.plot(p / nuber_cnt)
    plt.grid(True)



