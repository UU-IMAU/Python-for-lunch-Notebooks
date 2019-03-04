# Python for lunch 20 Feb 2019 IMAU: Introduction to classes

import numpy as np
import matplotlib.pyplot as plt

class balloon(object):
    '''
    class for 2D circular balloons
    '''

    def __init__(self, radius, color):
        '''
        constructor that sets the radius and color of the balloon
        '''
        self.radius = radius
        self.color = color

    def __str__(self):
        '''
        method that returns a string that describes the instance.
        '''
        return 'A {} balloon of radius {}'.format(self.color, self.radius)

    def circumference(self):
        '''
        A function in a class is called a method.
        returns the circumference of the balloon
        '''
        return 2 * np.pi * self.radius

    def area(self):
        '''
        returns the area of the balloon
        '''
        return np.pi * self.radius**2
    
    def show_balloon(self):
        '''
        method to visualize the balloon
        '''
        plt.figure(figsize=(5,5))
        curve = [self.radius * np.exp(1j * z) for z in np.linspace(0,2*np.pi,100)]
        plt.fill(np.real(curve), np.imag(curve),color=self.color)
        plt.xlim([-10, 10])
        plt.ylim([-10, 10])
        plt.axis('off')
        plt.show()
        

class hotairballoon(balloon):
    def __init__(self,radius,color,basket_size):
        super().__init__(radius,color) # set radius and color from class above it.
        self.basket_size = basket_size # set basket_size 

    def __str__(self):
        '''
        method that overwrites the __str__ method of the balloon class.
        '''
        return 'A {} hot air balloon of radius {}, that fits {:.0f} persons in its basket'.format(self.color, self.radius, self.places())

    def quality(self):
        '''
        method to calculate the quality
        '''
        if self.radius < 3:
            return 'to small'
        elif self.radius >= 3 and self.radius < 10:
            return 'great hotairballoon'
        else:
            return 'to big'

    def places(self):
        '''
        method to calculate the number of people that fit in the basket.
        '''
        return self.basket_size // 5


# b1 = balloon(2,'darkgreen')   # b1 is called an instance of the balloon class
# b2 = balloon(2,'darkorange')  # b2 is another instance of the balloon class
# b3 = balloon(2,'crimson')     
b1 = balloon()
b1.radius = 3

b1.color='yellow'
print(b1)

# print(b1.radius)
# print(b2.area() )
# b1.show_balloon()

# print(b1.circumference())
# print(b1.area())
# b1.show_balloon()

# print(b2)

# for b in [b1,b2,b3]:
#     b.show_balloon()
# print(b1)



# ab = hotairballoon(10,'yellow',11)
# print(ab)


