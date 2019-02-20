# Python for lunch 20 Feb 2019 IMAU: Use of classes for sensitivity analysis

import numpy as np
import matplotlib.pyplot as plt

#import the class parsetting form the directory model and file module.py
from model.module import parsetting

# make instance of parsetting class
ps = parsetting()

ps.plot_eigvals()
exit()

# make array with different values of albedo
albedo_range = np.linspace(0,5,50)

# allocate array for the eigenvalues that we are going to calculate in the loop below.
eigenvalues = np.zeros(len(albedo_range), dtype=complex)

# loop over different albedo values
for i in range(len(albedo_range)):
    ps.albedo = albedo_range[i]         # set the albedo parameter of the instance ps to the right one.
    eigenvalues[i] = ps.solve()[0][0]   # ps.solve()[0] is a list of the eigenvalues, ps.solve()[0][0] is the largest eigenvalue


#plot the real part of the eigenvalues versus albedo
plt.close()
plt.plot(albedo_range, np.real(eigenvalues), 'k',linewidth=3)
plt.xlim(albedo_range[0],albedo_range[-1])
plt.xlabel('albedo')
plt.ylabel('Re$\{\\lambda_{0}\}$')
plt.tight_layout()
plt.show()
