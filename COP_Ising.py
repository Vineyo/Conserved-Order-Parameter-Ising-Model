import numpy as np


class COP_Ising():

    def __init__(self,
                 n=20,
                 H=0,
                 J=1,
                 T=1):

        self.n = n
        self.lattice = np.random.choice([1, -1], size=(n, n))
        self.H = H
        self.J = J
        self.T = T

        self.up_spin = []
        self.down_spin = []
        self.up_date_spin_list()

        while len(self.down_spin) < len(self.up_spin):
            self.down_spin.append(self.up_spin.pop())
            self.lattice[self.down_spin[-1]] = -1

        while len(self.down_spin) > len(self.up_spin):
            self.up_spin.append(self.down_spin.pop())
            self.lattice[self.up_spin[-1]] = 1

        self.spins = [self.spin()]

    def spin(self):
        return np.sum(self.lattice)

    def neighbours(self, point):
        return [((point[0]-1) % self.n, point[1]),
                ((point[0]+1) % self.n, point[1]),
                (point[0], (point[1]+1) % self.n),
                (point[0], (point[1]-1) % self.n)]

    def upDate(self):
        n1 = np.random.choice(len(self.up_spin))
        n2 = np.random.choice(len(self.down_spin))
        up_point = self.up_spin[n1]
        down_point = self.down_spin[n2]
        up_point_neighbours = self.neighbours(up_point)
        down_point_neighbours = self.neighbours(down_point)
        dE = 0

        if ((up_point[0]-down_point[0])**2+(up_point[1]-down_point[1])**2) > 1:
            for up_n in up_point_neighbours:
                dE += 2*self.J*self.lattice[up_n]
            for down_n in down_point_neighbours:
                dE -= 2*self.J*self.lattice[down_n]

        else:
            for up_n in up_point_neighbours:
                dE += 2*self.J*self.lattice[up_n]
            for down_n in down_point_neighbours:
                dE -= 2*self.J*self.lattice[down_n]
            dE += 4*self.J

        if dE <= 0 or (np.random.random() < np.exp(-dE/self.T)):

            self.lattice[up_point] = -1
            self.lattice[down_point] = 1
            self.up_spin[n1] = down_point
            self.down_spin[n2] = up_point

#        self.spins.append(self.spin())

    def up_date_spin_list(self):
        self.up_spin = []
        self.down_spin = []
        
        for i in range(self.n):
            for j in range(self.n):
                if self.lattice[i, j] == 1:
                    self.up_spin.append((i, j))
                else:
                    self.down_spin.append((i, j))

    def kawasaki_Update(self):
        mikoto = (np.random.randint(self.n), np.random.randint(self.n))
        kuroko = ((mikoto[0]+np.random.choice([-1, 1]))%self.n,
                  (mikoto[1]+np.random.choice([-1, 1]))%self.n)

        if self.lattice[mikoto] != self.lattice[kuroko]:
            mikoto_n=self.neighbours(mikoto)
            kuroko_n=self.neighbours(kuroko)

            dE=0
            for up_n in mikoto_n:
                dE += 2*self.lattice[mikoto]*self.J*self.lattice[up_n]
            for down_n in kuroko_n:
                dE += 2*self.J*self.lattice[kuroko]*self.lattice[down_n]
            dE += 4*self.J

            if dE <= 0 or (np.random.random() < np.exp(-dE/self.T)):
                self.lattice[kuroko] *= -1
                self.lattice[mikoto] *= -1
