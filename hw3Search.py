# -*- coding: utf-8 -*-
"""
search.py

Skeleton code for homework03
"""
import numpy as np

def random_choice(s,p):
    '''
    Chooses random element from set s based on probability weights p
    
    Parameters
    -----------
    s : list of values to choose from
    p : probability weights on these values
    
    Returns
    --------
    s_rand: random choice from s
    
    '''
    cump = np.cumsum(p)
    r = np.random.random_sample()
    for i,cp in enumerate(cump):
        if r < cp:
            break
    return s[i]

def iterateValueFunction_noalpha(beta, p, w, c, v):
    '''
    Iterates McCall search value function v
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    v - (n array) continuation value function if offered w[s] next period
    
    Returns
    --------
    v_new - (n array) current value function if offered w[s] this period
    choice - (n array) do we accept or reject wage w[s]
    '''
    S = len(p)
    #stack the two value of two choices together
    stacked_values = np.vstack( (c*np.ones(S)  + beta*p.dot(v), 
                                 w + beta*v) )
    #use amax to choose maximal value
    v_new = np.amax(stacked_values, axis = 0)
    choice = np.argmax(stacked_values, axis = 0)
    return v_new,choice

def solveMcCallModel_noalpha(beta,p,w,c,eps = 1e-10):
    '''
    Solves infinite horizon McCall search model
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    eps - (float) convergence criterion for infinite horizon 
    
    Returns
    --------
    V - (n array) optimal V[s] value function if offered w[s] 
    Choice - (n array) Choice[s] do we accept or reject wage w[s]
    '''
    S = len(p)
    v = np.zeros(S) #intialize with zero
    diff = 1 #holds difference v_{t+1}-v_t
    V,Choice = {},{} #initialize return variables
    while diff > eps:
        v_new,choice = iterateValueFunction_noalpha(beta,p,w,c,v)
        diff = np.amax( np.abs(v-v_new) )#compute difference between values
        v = v_new #copy v_new into v
    #add in infinte horizon solution
    V[np.inf] = v
    Choice[np.inf] = choice

    return V,Choice
    
def iterateValueFunction(beta,p,w,c,alpha,v):
    '''
    Iterates McCall search value function v with alpha
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    alpha - (float) probability of .....
    v - (n array) continuation value function if offered w[s] next period
    
    Returns
    --------
    v_new - (n array) current value function if offered w[s] this period
    choice - (n array) do we accept or reject wage w[s]
    '''
    S = len(p)
    Q = p.dot(v)# value before wage offer
    #stack value of accepting and rejecting offer on top of each other
    stacked_values = np.vstack((c*np.ones(S)  + beta*Q, 
                                w + (1-alpha)*beta*v  ))
    #find whether it is optimal to accept or reject offer
    v_new = np.amax(stacked_values, axis = 0)
    choice = np.argmax(stacked_values, axis = 0)
    return v_new,choice

def solveMcCallModel(beta,p,w,c,alpha,eps = 1e-10):
    '''
    Solves the infinite horizon McCall search model.
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    alpha - (float) probability of ......
    eps - (float) convergence criterion for infinite horizon 
    
    Returns
    --------
    V - (n array) optimal V[s] value function if offered w[s] 
    Choice - (n array) Choice[s] do we accept or reject wage w[s]
    '''
    S = len(p)
    v = np.zeros(S) #intialize with zero
    diff = 1 #holds difference v_{t+1}-v_t
    V,Choice = {},{} #initialize return variables
    while diff > eps:
        v_new,choice = iterateValueFunction(beta,p,w,c,alpha,v)

        diff = np.amax( np.abs(v-v_new) )#compute difference between values
        v = v_new #copy v_new into v
    #add in infinte horizon solution
    V[np.inf] = v
    Choice[np.inf] = choice
    return V,Choice


def solveMcCallModelFinite_noalpha(beta,p,w,c,T, eps = 1e-10):
    '''
    Solves Finite horizon McCall search model
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    T - (int) number of periods the worker will be alive for
    eps - (float) convergence criterion for infinite horizon 
    
    Returns
    --------
    V - (list or dict) optimal V[t][s] value function if offered w[s] with
    t periods left to live
    Choice - (list or dict) Choice[t][s] do we accept or reject wage w[s] with
    t periods left to live
    '''
    S = len(p)
    v = np.zeros(S) #intialize with zero
    t = 1
    diff = 1 #holds difference v_{t+1}-v_t
    V,Choice = {},{} #initialize return variables
    while diff > eps:
        v_new,choice = iterateValueFunction_noalpha(beta,p,w,c,v)
        if t in range(T+1):
            V[t] = v_new
            Choice[t] = choice
        t += 1
        diff = np.amax( np.abs(v-v_new) )#compute difference between values
        v = v_new #copy v_new into v
    #add in infinte horizon solution
    V[np.inf] = v
    Choice[np.inf] = choice
    return V,Choice
    
def solveMcCallModelFinite(beta,p,w,c,T,alpha, eps = 1e-10):
    '''
    Solves Finite horizon McCall search model with alpha
    
    Parameters
    ----------
    beta - (float) discount factor
    p  - (n array) p[s] is the probability of state s
    w - (n array) w[s] is the wage in state s
    c - (float) unemployment benefit
    T - (int) number of periods the worker will be alive for
    alpha - (float) probability of ......
    eps - (float) convergence criterion for infinite horizon 
    
    Returns
    --------
    V - (list or dict) optimal V[t][s] value function if offered w[s] with
    t periods left to live
    Choice - (list or dict) Choice[t][s] do we accept or reject wage w[s] with
    t periods left to live
    '''
    S = len(p)
    v = np.zeros(S) #intialize with zero
    t = 1
    diff = 1 #holds difference v_{t+1}-v_t
    V,Choice = {},{} #initialize return variables
    while diff > eps:
        v_new,choice = iterateValueFunction(beta,p,w,c,alpha,v)
        if t in T:
            V[t] = v_new
            Choice[t] = choice
        t += 1
        diff = np.amax( np.abs(v-v_new) )#compute difference between values
        v = v_new #copy v_new into v
    #add in infinte horizon solution
    V[np.inf] = v
    Choice[np.inf] = choice
    return V,Choice
    


def constructTransitionMatrix(p,alpha,C,T=np.inf):
    '''
    Constructs the transition matrix for a worker given policy function C
    
    Parameters
    -----------
    p  - (J array) p[j] is the probability of wage w_j
    alpha - (float) probability of .....
    C - (J array) C[j] =1 if worker accepts wage offer, C[j] = 0 if worker rejects
    offer
    
    Returns
    --------
    P : (J+1xJ+1 array) P[s,sprime] is the probability that the worker transitions
    from state s to state sprime where s=0 represents the woker being unemployed,
    s= j >0 represents the worker being employed with wage w_j
    '''

    S = 100
    P = np.zeros( (S+1,S+1))
    P[0,1:] = C[T]*p
    P[0,0] = 1.-C[T].dot(p)
    
    for j in range(1, S+1):
        if C[T][j-1]==0:
            P[j,0]=1.
        else:
            P[j,0]=alpha
            P[j,j]=1-alpha
    return P        

def simulateLife(s0,P,T):
    '''
    Simulates the life of an agent given initial state s0 for $T$ periods
    
    Parameters
    -----------
    s0 - (int) initial state of the agent
    P - (SxS array) Transition matrix
    
    Returns
    --------
    sHist - (T array) life history of the agent
    '''
   
    s = np.linspace(0,len(P),len(P))
    sHist = np.zeros(T)
    sHist[0] = s0
    for i in range(1,T):
        sHist[i] = random_choice(s,P[sHist[i-1],:])
        
        
    return sHist

def simulateLife_FiniteHorizon(s0,P,T):
    '''
    Simulates the life of an agent given initial state s0 with $T$ periods
    left to live
    
    Parameters
    -----------
    s0 - (int) initial state of the agent
    P - (dict or list) P[k] Transition matrix for agent with k periods left to live 
    
    Returns
    --------
    sHist - (T array) life history of the agent (do whatever order feels natural)
    '''
    
    s = np.linspace(0,len(P[0]),len(P[0]))
    sHist = np.zeros(T)
    sHist[0] = s0
    for i in range(1,T):
        sHist[i] = random_choice(s,P[i][sHist[i-1],:])
        
        
    return sHist
        
