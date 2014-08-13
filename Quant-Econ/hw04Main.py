# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 17:48:36 2014

@author: Local User
"""

import homework04 as hw4
import numpy as np
import matplotlib.pyplot as plt

beta = .95
alpha = .02
sigma = 2.
J = 50
pj = .02
w = np.linspace(1.,10.)
p = pj*np.ones(50)
c = 4.
hwproblem = hw4.WorkerProblem(beta,p,w,alpha,sigma,c)
cvec = np.linspace(4.,7.2)
welfvec = np.zeros(50)
count = 0
for c in cvec:
    welfvec[count]=hwproblem.computeSS_Welfare(hw4.compute_tau(hwproblem,c))
    count += 1
plt.plot(cvec,welfvec)
print "Optimal value is ", cvec[np.argmax(welfvec)]
sigvec = np.array([1.5,3.,5.,10.])
for sig in sigvec:
    count = 0
    hwproblem.setSigma(sig)
    for c in cvec:
        welfvec[count]=hwproblem.computeSS_Welfare(hw4.compute_tau(hwproblem,c))
        count += 1
    plt.plot(cvec,welfvec)
    print "For sigma ",sig, " the optimal value is ", cvec[np.argmax(welfvec)]
