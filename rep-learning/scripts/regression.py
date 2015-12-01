# -*- coding: utf-8 -*-
"""
Script for performing regression of data using PLS/CCA

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSCanonical, PLSRegression, CCA

def get_PLS_predictor(X, Y, n_components=3):
    predictor = PLSRegression(n_components=n_components)
    predictor.fit(X, Y)
    return predictor    
    
def PLS_predict(PLS_predictor, M):
    return PLS_predictor.predict(M)
    
#n = 1000
#q = 3
#p = 10
#X = np.random.normal(size=n * p).reshape((n, p))
#B = np.array([[1, 2] + [0] * (p - 2)] * q).T
## each Yj = 1*X1 + 2*X2 + noize
#Y = np.dot(X, B) + np.random.normal(size=n * q).reshape((n, q)) + 5
#
#pls2 = PLSRegression(n_components=3)
#pls2.fit(X, Y)
#print("True B (such that: Y = XB + Err)")
#print(B)
## compare pls2.coef_ with B
#print("Estimated B")
#print(np.round(pls2.coefs, 1))
#pls2.predict(X)