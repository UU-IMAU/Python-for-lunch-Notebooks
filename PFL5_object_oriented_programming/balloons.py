import numpy as np
import matplotlib.pyplot as plt

class balloon(object):
    '''
    class for 2D circular balloons
    '''

    def __init__(self,radius,color):
        '''
        constructor that sets the radius and color of the balloon
        '''
        self.r = radius
        self.color = color

    def circumference(self):
        '''
        returns the circumference of the balloon
        '''
        return 2 * np.pi * self.r 

    def area(self):
        '''
        returns the area of the balloon
        '''
        return np.pi * self.r**2
    
    def show_balloon(self):
        '''
        function to visualize the balloon
        '''
        plt.figure(figsize=(5,5))
        curve = [self.r * np.exp(1j * z) for z in np.linspace(0,2*np.pi,100)]
        plt.fill(np.real(curve), np.imag(curve),color=self.color)
        plt.xlim([-10, 10])
        plt.ylim([-10, 10])
        plt.axis('off')
        plt.show()
        

class tennisballoon(balloon):
    def __init__(self):
        self.color = 'yellow'  #overwrite color

    def quality(self):
        if self.r < 1:
            return 'to small'
        elif self.r > 1 and self.r < 10:
            return 'great tennisballoon'
        else:
            return 'to big'

    