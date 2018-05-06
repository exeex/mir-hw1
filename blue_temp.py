
import numpy as np

major_template = np.array([[1,0,0,1,0,1,1,1,0,1,0,1]])
minor_template = np.array([[1,0,0,1,0,1,0,1,0,1,0,1]])


# Generate major key templates
# major_template = np.array([[1,0,1,0,1,1,0,1,0,1,0,1]])
# Generate monor key templates
# minor_template = np.array([[1,0,1,1,0,1,0,1,1,0,1,0]])

template = np.empty((0,12))


for i in range(12):
    template = np.append(template, np.roll(major_template, i), axis=0)
for i in range(12):
    template = np.append(template, np.roll(minor_template, i), axis=0)





def R(x : np.ndarray ,y : np.ndarray ):

    a = sum([(x[k]-x.mean()) * (y[k]-y.mean()) for k in range(12)])
    b = sum([(x[k]-x.mean())**2 * (y[k]-y.mean())**2 for k in range(12)]) ** 0.5
    return a/b


'''
gamma = 1
----------------------------------------------
 [('pop', 0.139), ('blues', 0.14), ('metal', 0.03), ('rock', 0.062), ('hiphop', 0.106)] 
------------------------------------------
gamma = 10
----------------------------------------------
 [('pop', 0.139), ('blues', 0.14), ('metal', 0.03), ('rock', 0.062), ('hiphop', 0.106)] 
------------------------------------------
gamma = 100
----------------------------------------------
 [('pop', 0.139), ('blues', 0.14), ('metal', 0.03), ('rock', 0.062), ('hiphop', 0.106)] 
------------------------------------------
gamma = 1000
----------------------------------------------
 [('pop', 0.139), ('blues', 0.14), ('metal', 0.03), ('rock', 0.062), ('hiphop', 0.106)] 
------------------------------------------


Process finished with exit code 0

'''