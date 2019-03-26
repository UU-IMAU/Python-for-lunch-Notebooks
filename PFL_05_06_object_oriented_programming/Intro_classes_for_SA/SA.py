# Python for lunch 6 March 2019 IMAU

import numpy as np
import matplotlib.pyplot as plt

#import the class parsetting form the directory model and file module.py
from model.module1 import parsetting  #slow
# from model.module2 import parsetting  #fast, but wrong
# from model.module3 import parsetting    #fast and fixed




# make instance of parsetting class
ps = parsetting()

# make array with different values of plastic
plastic_range = np.linspace(-0.9,0.9,100)

# allocate array for the eigenvalues that we are going to calculate in the loop below.
eigenvalues = np.zeros(len(plastic_range), dtype=complex)

# loop over different albedo values
for i in range(len(plastic_range)):

    ps.plastic = plastic_range[i]         # set the plastic parameter of the instance ps to the right one.
    eigenvalues[i] = ps.solve()[0][0]     # ps.solve()[0] is a list of the eigenvalues, ps.solve()[0][0] is the largest eigenvalue

    percentage = (i+1)*100/len(plastic_range)
    if percentage % 10 == 0:
        print('{:.0f}%'.format(percentage))


#plot the real part of the eigenvalues versus plastic
plt.close()
plt.plot(plastic_range, np.real(eigenvalues), 'k',linewidth=3)
plt.xlim(plastic_range[0],plastic_range[-1])
plt.xlabel('plastic')
plt.ylabel('Re$\{\\lambda_{0}\}$')
plt.tight_layout()
plt.show()
