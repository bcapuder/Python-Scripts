# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root
from scipy.optimize import brentq
from scipy.stats import norm

def findUnitEigenvector(A):
    '''
    For a matrix A finds the unit eigenvector
    '''
    eigs,eig_vecs = np.linalg.eig(A)
    
    i = int(np.where(np.abs(eigs-1)<1e-14)[0])
    
    return np.real(eig_vecs[:,i]/eig_vecs[:,i].sum())
    
    

class WorkerProblem:
    '''
    Solves the worker problem for a set of parameters and government policies
    '''
    def __init__(self,beta,p,w,alpha,sigma,c):
        '''
        Initializes worker problem class with
        
        Parameters
        ===========
        
        beta : discount factor worker
        
        p : (ndarray) p[j] is the probability of receiving wage w[j]
        
        w : (ndarray) array of possibe wages the worker can receive
        
        alpha : (float) firing probability
        
        sigma: (float) Risk aversion of the worker
        '''
        self.beta = beta
        self.p = p
        self.w = w
        self.alpha = alpha
        self.sigma = sigma
        self.c = c
        
    def U(self,x):
        '''
        Returns the utility of the agent
        '''
        sigma = self.sigma
        if sigma == 1:
            return np.log(x)
        else:
            return (x**(1-sigma)-1.)/(1.-sigma)
            
    def setCValue(self,c):
        self.c = c
        
    def setSigma(self,sigma):
        self.sigma = sigma
        
    def iterateValueFunction(self,tau,v):
        '''
        Iterates workers bellman equation
        
        Parameters
        ===========
        
        c: (float) unemployment benefits
        
        tau : (float) proportional tax rate
        
        v : (ndarray) current value function
        
        Returns
        ========
        
        vnew : (ndarray) new value function
        
        choice :(ndarrary) optimal decision rule of the worker
        '''
        S = len(self.p)
        Q = self.p.dot(v)# value before wage offer
        #stack value of accepting and rejecting offer on top of each other
        stacked_values = np.vstack((self.U(self.c)*np.ones(S)  + self.beta*Q, self.U((1-tau)*self.w) + (1-self.alpha)*self.beta*v + self.beta*self.alpha*Q ))
        #find whether it is optimal to accept or reject offer
        v_new = np.amax(stacked_values, axis = 0)
        choice = np.argmax(stacked_values, axis = 0)
        return v_new,choice
        
    def solveBellmanEquation(self,tau,eps = 1e-10):
        '''
        Solves workers bellman equation given government policies
        
        Parameters
        ===========
        
        c: (float) unemployment benefits
        
        tau : (float) proportional tax rate
        
        Returns
        ========
        
        V : (ndarray)  value function
        
        Choice :(ndarrary) optimal decision rule of the worker
        '''
        S = len(self.p)
        v = np.zeros(S) #intialize with zero
        diff = 1 #holds difference v_{t+1}-v_t
        V,Choice = {},{} #initialize return variables
        while diff > eps:
            v_new,choice = self.iterateValueFunction(tau,v)
            diff = np.amax( np.abs(v-v_new) )#compute difference between values
            v = v_new #copy v_new into v
        #add in infinte horizon solution
        V[np.inf] = v
        Choice[np.inf] = choice
        return V,Choice
        
    def constructTransitionMatrix(self,tau):
        '''
        Computes the transition matrix of the worker of the infinite horizon
        problem given government policy
         Parameters
        ===========
        
        c: (float) unemployment benefits
        
        tau : (float) proportional tax rate
        
        Returns
        ========
        
        P : (ndarray)  Transition matrix taking s=0 as unemployed
        '''
        S = len(self.p)
        P = np.zeros( (S+1,S+1))
        _,C = self.solveBellmanEquation(tau)
        T = C[np.inf]
        P[0,1:] = C[T]*self.p
        P[0,0] = 1.-C[T].dot(self.p) 
        for j in range(1, S+1):
            if C[T][j-1]==0:
                P[j,0]=1.
            else:
                P[j,0]=self.alpha
                P[j,j]=1-self.alpha
        return P   
        
    def constructSteadyState(self,tau):
        '''
        Finds the steady state distribution of worker productivities
        
        Parameters
        ===========
        
        c: (float) unemployment benefits
        
        tau : (float) proportional tax rate
        
        Returns
        ========
        
        pi : (ndarray)  steady state distribution
        '''
        P = self.constructTransitionMatrix(tau)
        eig_val,eig_vec = np.linalg.eig(P.T)
        pi = eig_vec[:,1]/sum(eig_vec[:,1])
        return pi        
    def computeSS_Deficit(self,tau):
        '''
        Computes the governments budget deficit in the steady state
        
        Parameters
        ===========
        
        c: (float) unemployment benefits
        
        tau : (float) proportional tax rate
        
        Returns
        ========
        
        deficit :   (float) government unemployment payments minus tax income
        '''
        welf = self.computeSS_Welfare(tau)
        pi = self.constructSteadyState(tau)        
        rev = tau*(np.dot(pi[1:],self.w))
        deficit = welf-rev
        return deficit
        
    def computeSS_Welfare(self,tau):
        '''
        Computes the governemnts steady state welfare
        '''
        pi = self.constructSteadyState(tau)        
        return pi[0]*self.c
        
def bracket_and_solve(f):
    '''
    Helper function.  Given a decreasing function f on [0,1] will find the 
    root of that function.
    
    Parameters
    ===========
    
    f   :   A function f:[0,1]->R
    
    Returns
    ========
    x0 such that f(x0) = 0
    '''
    x0 = 0.2
    if f(x0) < 0.:
        x1 = x0/1.1
        while f(x1) < 0:
            x0 = x1
            x1 = x0/1.1
        return brentq(f,x1,x0)
    elif f(x0) > 0:
        x1  =  0.9*x0+0.1
        while f(x1) > 0.:
            x0 = x1
            x1 = 0.9*x0+0.1
        return brentq(f,x0,x1)
    
        

def compute_tau(WP,c):
    '''
    Computes the tax rate that balances the governments budget contraint
    Parameters
    ==========
    
    WP  :   An instance of WorkerProblem class
    
    c   :   Unemployement benefits
    
    Returns
    ========
    
    tau :   Budget constraint balancing tax rate
    '''
    WP.setCValue(c)
    return bracket_and_solve(WP.computeSS_Deficit)
