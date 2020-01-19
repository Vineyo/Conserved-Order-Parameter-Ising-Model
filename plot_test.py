from COP_Ising import COP_Ising
import matplotlib.pyplot as plt
n=40
ising=COP_Ising(n=40,T=2.1)
k=0
plt.ion()
while True:
    ising.upDate()
    k+=1
   
    if k%100000==0:
        
        plt.clf()
        plt.imshow(ising.lattice)
        plt.title("Step {}, T={}".format(k,ising.T))
        plt.show()
        plt.pause(0.01)


