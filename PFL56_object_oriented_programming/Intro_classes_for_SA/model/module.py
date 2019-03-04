# Python for lunch 20 Feb 2019 IMAU: Use of classes for sensitivity analysis

import numpy as np
from numpy.random import rand,seed
from scipy.linalg import eig, toeplitz
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
        self.plastic = 0.2         # the plastic parameter


    def solve(self,eps=0):
        '''
        Calculate eigenvectors and eigenvalues of matrix A.
        Sorts such that the first eigval has the largest real part.
        returns (eigvals, eigvecs)
        '''

        # populate matrix A which depends on variables amoc, methane, plastic, tide and albedo
        seed(self.seed)
        c = np.zeros(self.N,dtype=complex)
        r = np.zeros(self.N,dtype=complex)
        c[:6] = [0, 0,  -4, -2j, 0, 0]
        r[:6] = [0, 2j, -1,   2, 0, 0]
        A = toeplitz(c,r)
        A += rand(self.N,self.N)*eps
        A += np.eye(self.N) * (self.amoc + self.methane/ self.plastic - self.tide) * np.tanh(-self.albedo)

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
        

        