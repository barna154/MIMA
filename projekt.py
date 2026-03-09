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
    header=1
)

a = data.head(32)
print(a)
