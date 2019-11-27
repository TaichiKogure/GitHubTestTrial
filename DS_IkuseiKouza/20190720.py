import io

import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile

# //////////////////////////////////////////////
# #散布図
#
# random.seed(0)
# x = np.random.randn(30)
# y = np.sin(x) + np.random.randn(30)
# plt.figure(figsize=(20,6))
# plt.plot(x, y, 'o')
# plt.title('Title name')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.grid(True)
# plt.show()
# //////////////////////////////////////////////
# web~データ取得したりする
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00356/student.zip'
r = requests.get(url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
#//////////////////////////////////////////////


student_data_math = pd.read_csv('student-mat.csv', sep=';')


#//////////////////////////////////////////////
#ヒ
plt.subplot(2,2,1)

plt.hist(student_data_math['absences'])

plt.xlabel('absences')
plt.ylabel('count')
plt.grid(True)
plt.show()

# sns.pairplot(student_data_math)
# plt.show()

plt.subplot(2,2,2)

plt.boxplot([student_data_math['G1'],student_data_math['G2'],student_data_math['G3']])
plt.grid(True)

plt.subplot(2,2,3)

plt.boxplot([student_data_math['age']])
plt.grid(True)

plt.subplot(2,2,4)

plt.boxplot([student_data_math['absences']])
plt.grid(True)


# //////////////////////////////////////////////

# np.random.seed(0)
# dice_data = np.array([1,2,3,4,5,6])
# calc_steps = 1000
# dice_rolls = np.random.choice(dice_data, calc_steps)
# for i in range(1, 7):
#     p = len(dice_rolls[dice_rolls==i]) / calc_steps
#     print(i, '確率', p)

# BOXplot Links
# https://qiita.com/HiromuMasuda0228/items/babdfa175815fb3e3a94#
