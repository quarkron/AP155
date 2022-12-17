import numpy as np
from random import *
from numpy.random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import matplotlib.animation as animation

#Constants
J = 1 
T = 1
N = 30   # size of lattice 
kB = 1
beta = 1/(kB*T)

def total_energy(grid, J=1):
    vertical = np.sum(grid[:-1,:]*grid[1:, :])
    horizontal = np.sum(grid[:,:-1]*grid[:,1:])
    return -J*(vertical+horizontal)

def metropolis( lattice, oldE) : 
    # flip a random spin and calculate $dE$
    i, j = randint( N, size=2 )
    lattice[i,j] *= -1    # flip the ij spin
    E = total_energy(lattice, J=1)
    deltaE = E - oldE

    # these are the Metropolis tests 
    if deltaE < 0 : 
        # keep the flipped spin because it lowers the energy
        return lattice, E
    if rand() < np.exp( - deltaE / T ) : 
        # keep the spin flip because the random number is less than $e^{-dE/T}$
        return lattice, E

    # the spin flip is rejected 
    lattice[i,j] *= -1    # flip the ij spin back
    E = oldE        # and keep the old energy
    return lattice, E

N=30        #number of spins 
steps = 100000
def initIsing(N):
    global isingImage, spinLattice

    # this is the initial, random, t=0, state
    spinLattice = np.random.choice([1,-1], (N,N))
    
    isingImage = plt.imshow(spinLattice, interpolation='none', cmap='gray')
    return ( isingImage, )

def animateIsing(i) : 
    global isingImage, spinLattice 
    
    E = total_energy( spinLattice ) 
    for i in range(steps) : 
        spinLattice, E = metropolis( spinLattice, E ) 
    isingImage.set_data( spinLattice ) 
    return ( isingImage, ) 

# i'm using little m metropolis from above instead of this function
def Metropolis( s, i ) : 
    # this should update isingData for t=t[i] using the Metropolis algorithm
    isingData = rand( N, N )  < i / (2*n) + 0.5 
    return isingData 
    
def makeAnimation( T, n ) : 
    # set up the figure
    fig = plt.figure()
    plt.subplot( )
    plt.xticks( [] )
    plt.yticks( [] )
    # plt.title( r'$k_{\rm B}T/J=%3.2f$' % T )
    # and create the animation
    anim = FuncAnimation(fig, animateIsing, init_func=initIsing(N),
                                frames=n, interval=20, blit=True)
    return anim

n = 100000
T = 1
anim = makeAnimation(T, n//steps) # because animateIsing() runs metropolis() steps times

    