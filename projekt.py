import pandas as pd
from scipy.stats import randint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV 
from sklearn import metrics 
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv(
    r"adatbazisok\sadatok2024.csv",
    sep=";",
    encoding="cp1250",
    header=0
)

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
for col in data.columns[1:]:
    data[col] = data[col].str.replace(' ', '').str.replace(',', '.').astype(float)


data.head(32)
data.info()


data['uj_auto_real'] = data['uj_auto'] * (1 + np.random.normal(0, 0.1, size=len(data)))
data['uj_auto_real'] = data['uj_auto_real'].round().astype(int)

data['eletkor_real'] = data['eletkor'] + np.random.normal(0, 2, size=len(data))

numeric_columns = data.select_dtypes(include=['int', 'float'])
new_data = data[numeric_columns.columns]


corr_matrix = new_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()



