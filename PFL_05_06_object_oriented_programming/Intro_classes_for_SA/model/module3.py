# Python for lunch 6 March 2019 IMAU

import numpy as np
from numpy.random import rand,seed,randint
from scipy.linalg import eig, toeplitz, det
import matplotlib.pyplot as plt



class parsetting(object):
    '''
    class for a parametersetting.
    '''
    
    def __init__(self):
        '''
        constructor that sets all default variable values
        '''
        self.N = 150               # size matrix A
        self.seed = 1              # seed random number generator

        self.albedo = 0.1          # the albedo parameter
        self.amoc = 0              # the amoc parameter
        self.methane = 0.05        # the methane paramater
        self.tide = 1.1            # the tidal parameter
        self.nn = 1e4              # number of times Tn has to be called
        
        self._plastic = 0.5        # the plastic parameter (between -1 and 1)

        self.Tn_dic = {}           # dictionary to speed up.
    


    #make plastic a property by putting the so-called decorator @property above the function (google for more info about decorators). 
    #Note that plastic is now a function, but it is being called without parenthesis
    @property
    def plastic(self):
        return self._plastic  #simply returns the value of the variable _plastic
    
    # the setter of the property plastic
    @plastic.setter
    def plastic(self,value):
        self.Tn_dic = {}  #first clean the Tn dic because those values are not valid anymore when plastic is changed.
        self._plastic = value # then put _plastic to the value you set it to.

    def Tn(self,n):
        '''
        n-th Chebychev at xi = plastic
        '''
        if not n in self.Tn_dic:  #check if the argument n is in a key in the dictonary Tn_dic, if not then caculate it.
            t = np.arccos(self.plastic)  #note that plastic does not have parenthesis
            self.Tn_dic[n] = np.cos(n * t)
        return self.Tn_dic[n] # and return the value in the dir

    def solve(self):
        '''
        Calculate eigenvectors and eigenvalues of matrix A.
        Sorts such that the first eigval has the largest real part.
        returns (eigvals, eigvecs)
        '''

        #set seed for random arrays.
        seed(self.seed)

        # do stuff with Tn very often (for the same argument)
        n_range = randint(0,10, size=int(self.nn))
        F = [self.Tn(n) for n in n_range]

        # populate matrix A which depends on variables amoc, methane, plastic, tide and albedo
        c = np.zeros(self.N,dtype=complex)
        r = np.zeros(self.N,dtype=complex)
        c[:6] = [0, 0,  -4, -2j, 0, 0]
        r[:6] = [0, 2j, -1,   2, 0, 0]
        A = toeplitz(c,r)
        A += np.eye(self.N) * (self.amoc + self.methane - self.tide) * np.tanh(-self.albedo) * np.average(F)

        # calculate eigenvalues and eigenvectors
        eigvals, eigvecs = eig(A)

        #sort on size of realpart of the eigenvalues
        idx = eigvals.argsort()[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:,idx]
        
        return (eigvals, eigvecs)

    
    def plot_eigvals(self):
        '''
        method to plot eigenvalues in complex plane
        '''

        eigvals, eigvecs = self.solve()
        
        plt.close()
        plt.figure(figsize=(9,5))
        plt.title('eigenvalues')
        plt.scatter(np.real(eigvals),np.imag(eigvals), c='k',s=10)
        plt.xlabel('R')
        plt.ylabel('iR')
        plt.tight_layout()
        plt.show()
        

        