
import numpy as np

# Generate major chord templates
major_template = np.array([[1,0,0,0,1,0,0,1,0,0,0,0]])/np.sqrt(3.0)
# Generate monor chord templates
minor_template = np.array([[1,0,0,1,0,0,0,1,0,0,0,0]])/np.sqrt(3.0)



template = np.empty((0,12))


for i in range(12):
    template = np.append(template, np.roll(major_template, i), axis=0)
for i in range(12):
    template = np.append(template, np.roll(minor_template, i), axis=0)

