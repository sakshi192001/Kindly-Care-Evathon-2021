import pandas as pd
df = pd.read_csv('fetal_health.csv')
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, f1_score, recall_score, precision_score
import pickle
X = df.drop(["fetal_health"],axis=1)
Y = df["fetal_health"]

std_scale = StandardScaler()
X_sc = std_scale.fit_transform(X)

X_train, X_test, y_train,y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

rf = RandomForestClassifier(n_estimators=2000, criterion='entropy', max_depth=20, max_features='auto')
rf.fit(X_train, y_train)

pickle.dump(rf,open('ml_fetal_health.pkl','wb'))
