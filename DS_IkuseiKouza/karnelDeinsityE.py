import pandas as pd
import matplotlib.pyplot as plt

import requests, zipfile
import io
import io

import matplotlib.pyplot as plt
import pandas as pd
import requests
import zipfile

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00356/student.zip'
r = requests.get(url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

student_data_math = pd.read_csv('student-mat.csv', sep=';')

#カーネル密度関数
student_data_math.absences.plot(kind='kde' , style = 'k--')

student_data_math.absences.hist(density = True)

plt.grid(True)
