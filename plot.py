import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

colnames = ['categoryId']
data = pd.read_csv('category.csv', names=colnames)

categoryId = data.categoryId.tolist()
categoryId = categoryId[1:]
categoryId = [float(i) for i in categoryId]
#categoryId = [np.log10(int(i)+1) for i in categoryId]

plt.hist(categoryId, normed=False, bins=30)
plt.xlabel('CategoryIds');
plt.ylabel('Frequency')
sns.set(color_codes=True)
plt.savefig('histogram-categoryId.png')
