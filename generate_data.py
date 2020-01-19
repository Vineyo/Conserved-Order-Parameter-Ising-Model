from multiprocessing import Pool
from COP_Ising import COP_Ising
import numpy as np

def run_ising(n,steps,T):
    ising=COP_Ising(n=n,T=T)
    i=0
    while i<=steps:
        ising.upDate()
        i+=1

    return ising.lattice

if __name__=="__main__":

    pool=Pool(processes=12)
    result=[]
    n=40
    steps=2000000
    X=np.empty(shape=[0,n**2])
    T=[]
    for T_i in np.arange(1.6,3.0,0.1).repeat(100):
        result.append(((pool.apply_async(run_ising,args=(n,steps,T_i))),T_i))
        print("Processesing T=",T_i)
    for i in result:
        X=np.row_stack((X,i[0].get().flatten()))
        T.append(i[1])

    np.savez("COP_warmed_size_{0}_stpes_{1}".format(n,steps),X,T)
    print("Done!")