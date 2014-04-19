#!/usr/bin/env python
#coding: utf-8

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pandas as pd
import numpy as np
import sqlite3

MIRANDA_DATA = '/Users/alex/Projects/mi-pred/miranda_latest.txt'
MIRANDA_HEAD = '/Users/alex/Projects/mi-pred/mirandaHeaders.tsv'
SEP = '\t'

mir_head = pd.read_csv(MIRANDA_HEAD, sep=SEP)
mir_df = pd.read_csv(MIRANDA_DATA, sep=SEP, header=None)
mir_df.columns = mir_head.columns.values.tolist()


mir_df['target'] = mir_df.mirna + '\t' + mir_df.ensgid

# Cross-validation
mir_df['is_train'] = np.random.uniform(0, 1, len(mir_df)) <= .75

train, test = mir_df[mir_df['is_train'] == True], mir_df[mir_df['is_train'] == False]

features = mir_df.columns[4:-2]

y, _ = pd.factorize(train['target'])

rfc = RandomForestClassifier(n_jobs=2)
rfc.fit(train[features], y)

rf_preds = mir_df.target[rfc.predict(test[features])]
print(pd.crosstab(test['target'], rf_preds, rownames=['actual'], colnames=['rf_preds']))

#
# TODO: SVM goes here
#
svc = svm.SVC(kernel='linear')
svc.fit(train[features], y)

sv_preds = mir_df.target[svc.predict(test[features])]
print(pd.crosstab(test['target'], sv_preds, rownames=['actual'], colnames=['sv_preds']))
