
#author
#Digvijaysinh Gohil






import imageio
import numpy as np
import os
import os.path
from os import listdir
from os.path import isfile, join
import encryption

flag=1

Mod = 256



Enc = imageio.imread('Encrypted.png')                           #Reading Encrypted Image to Decrypt
nl = int(Enc.shape[0])
# Loading the key
#A = imageio.imread('Key.png')
A = encryption.key
n = int(A.shape[0] - 1)
l = int(A[-1][0] * Mod + A[-1][1]) # The length of the original image 
w = int(A[-1][2] * Mod + A[-1][3]) # The width of the original image
A = A[0:-1]

Decrypted = np.zeros((nl,w,3))
for i in range(int(nl/n)):
    Dec1 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,0] % Mod)) % Mod
    Dec2 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,1] % Mod)) % Mod
    Dec3 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,2] % Mod)) % Mod
    
    Dec1 = np.resize(Dec1,(Dec1.shape[0],Dec1.shape[1],1))
    Dec2 = np.resize(Dec2,(Dec2.shape[0],Dec2.shape[1],1))
    Dec3 = np.resize(Dec3,(Dec3.shape[0],Dec3.shape[1],1))
    Decrypted[i * n:(i + 1) * n,:] += np.concatenate((Dec1,Dec2,Dec3), axis = 2)                #Dec = A * Enc

if (flag):
    Decrypted = (Decrypted - encryption.img3) % 256

Decrypted = Decrypted[:l,:w,:]                                            #Returning Dimensions to the real image

imageio.imwrite('Decrypted.png', Decrypted)
