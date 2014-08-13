# -*- coding: utf-8 -*-
import numpy as np
import search as sh
import matplotlib.pyplot as plt

# 1c
beta = .95
c = 5
p = np.ones(100)/100
w = np.linspace(2,10,100)

V,choice = sh.solveMcCallModel_noalpha(beta,p,w,c)
fig = plt.figure('Figure 1')
plt.plot(w,V[inf],'-g')

#1d
probA = zeros(50)
i = 0
for b in np.linspace(.9,.97):
    V, choice = sh.solveMcCallModel_noalpha(b,p,w,c)
    probA[i] = p.dot(choice[inf])
    i += 1;
 
fig = plt.figure('Figure 2')
bvec = np.linspace(.9,.97)   
plt.plot(bvec, probA, 'or')    

#2c
alphavec = [0., 0.01, 0.02, 0.03]
for alpha in alphavec:
    V, choice = sh.solveMcCallModel(beta,p,w,c,alpha)
    fig = plt.figure('Figure 3')
    plt.plot(w,V[inf],'-')
    
#2d

#2e
sHist = sh.simulateLife(0,sh.constructTransitionMatrix(p,alpha,choice),100)
count = 0.
for i in sHist:
    if i == 0:
        count += 1
unemplyPerc = count/len(sHist)        
print unemplyPerc

#2f
P = sh.constructTransitionMatrix(p,alpha,choice)
eig_val,eig_vec = np.linalg.eig(P.T)
dist= eig_vec[:,1]/sum(eig_vec[:,1])
fig = plt.figure('Figure 4')
plt.plot(dist,'or')


#3c k = 1,2,5,10,20,50
V, choice = sh.solveMcCallModelFinite_noalpha(beta, p,w,c,50)
klist = [1,2,5,10,20,50]
for k in klist:
    fig = plt.figure('Figure 5')
    plt.plot(V[k], '-')
    
#3d 
    values = np.zeros(51)
for t in range(1,51):
    fig = plt.figure('Figure 6')
    values[t-1] = p.dot(choice[t])

values[50] = p.dot(choice[inf])
tvec = np.linspace(1,51,51)
fig = plt.figure('Figure 6')
plt.plot(tvec,values, '-')

#4d
V, choice = sh.solveMcCallModelFinite_noalpha(beta, p,w,c,60)
T = 60
Plist = np.zeros(T)
for t in range(T):
    Plist[t] = sh.constructTransitionMatrix(p,.02,choice[60-t],60-t)
    
sHist = sh.simulateLife_FiniteHorizon(0,sh.constructTransitionMatrix(p,alpha,choice),100)
count = 0.
for i in sHist:
    if i == 0:
        count += 1
unemplyPerc = count/len(sHist)        
print unemplyPerc    

    
