#!/usr/bin/env python
#coding: utf-8

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pandas as pd
import numpy as np
import sqlite3

FILE_PATH = 'Human-UTR3-Seed-All.txt'
SEPARATOR = '\t'

# Getting data from miRNA - mRNA database
# cnx = sqlite3.connect('mi-pred.sqlite')
#
# mrna_df = pd.io.sql.read_frame('select * from mrna', cnx)
# mirna_df = pd.io.sql.read_frame('select * from mirna', cnx)

# Example data extraction
iris = load_iris()
df = pd.DataFrame(iris.data, columns = iris.feature_names)

# df = pd.read_csv(FILE_PATH, sep=SEPARATOR)
# df['is_target'] = np.random.uniform(0, 1, len(df)) <= .75

#
# TODO: Feature extraction goes here
#

# Cross-validation
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

df['species'] = pd.Categorical(iris.target, iris.target_names)
df.head()

train, test = df[df['is_train'] == True], df[df['is_train'] == False]

features = df.columns[:4]

y, _ = pd.factorize(train['species'])

#
# TODO: Random Forest goes here
#

rfc = RandomForestClassifier(n_jobs = 2)
rfc.fit(train[features], y)

rf_preds = iris.target_names[rfc.predict(test[features])]
print(pd.crosstab(test['species'], rf_preds, rownames=['actual'], colnames=['rf_preds']))

#
# TODO: SVM goes here
#
svc = svm.SVC(kernel='linear')
svc.fit(train[features], y)

sv_preds = iris.target_names[svc.predict(test[features])]
print(pd.crosstab(test['species'], sv_preds, rownames=['actual'], colnames=['sv_preds']))
