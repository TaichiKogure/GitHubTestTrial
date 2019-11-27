import matplotlib.pyplot as plt
import numpy as np

# 一様分布でさいころを1000回振ってみる
dice_data = np.array([1,2,3,4,5,6])
calc_steps = 10

# 1-6dataのなかから1000回の抽出を実施
dice_rolls = np.random.choice(dice_data, calc_steps)

#それぞれの数字がどれくらいの割合で抽出されたか計算
prob_data = np.array([])
for i in range(1,7):
    p = len(dice_rolls[dice_rolls==i])/ calc_steps
    prob_data = np.append(prob_data, len(dice_rolls[dice_rolls==i]) / calc_steps)

plt.subplot(2,2,1)
plt.bar(dice_data,prob_data)
plt.grid(True)

# 二項分布
np.random.seed(0)

x = np.random.binomial(30,0.5,10000)
plt.subplot(2,2,2)
plt.hist(x)

plt.grid(True)

# パラメータ変えてみる
x = np.random.binomial(30,0.1,10000)
plt.subplot(2,2,3)
plt.hist(x)

plt.grid(True)

