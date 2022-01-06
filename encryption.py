#authors
#Digvijaysinh Gohil
#Karan Shah
#Meet Jhaveri
#Pankil Sheth
#Sarjil Patel




import imageio
import numpy as np
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

flag = 1

#---------------Read Image to Encrypt---------------
img = imageio.imread('test.png')



#----------------Password Protected-----------------
if os.path.isfile('password.txt'):
    while True:
        password = str(input("Enter password: "))
        p = ''
        with open("password.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            print("Correct Password process is done!")
            break
        else:
            print("Wrong Password!")
else:
    while True:
        password = str(input("Setting up stuff. Enter a password that will be used for Encrypiton/Decryption: "))
        repassword = str(input("Confirm password: "))
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
    f = open("password.txt", "w+")
    f.write(password)
    f.close()


   

nl = l = img.shape[0]   #nl records the size of the matrix
w = img.shape[1]
n = 4
if l%n:
    nl = (int((l - 1) / n) + 1) * n
img2 = np.zeros((nl,w,3))
img2[:l,:w,:] += img
print(nl)
def f(x, y):
    return x * x + y * y + 10 * x + 10 * y

if (flag):
    img3 = np.zeros((nl,w,3))
    for x in range(nl):
        for y in range(w):
            v = f(x, y)
            img3[x, y, 0] = v
            img3[x, y, 1] = v
            img3[x, y, 2] = v
    img2 = (img2 + img3) % 256
   # imageio.imwrite('Step.png', img2)

#-------------Generating Encryption Key-------------
Mod = 256
k = 23                                                          #Key for Encryption

d = np.random.randint(256, size = (int(n/2),int(n/2)))          #Arbitrary Matrix, should be saved as Key also
I = np.identity(int(n/2))     #defining an indentity matrix
a = np.mod(-d,Mod)      #this is the first step A11


b = np.mod((k * np.mod(I - a,Mod)),Mod)    #this is the second step A12
k = np.mod(np.power(k,127),Mod)  
c = np.mod((I + a),Mod)    #third step A11 = - A22
c = np.mod(c * k, Mod)





A1 = np.concatenate((a,b), axis = 1)
A2 = np.concatenate((c,d), axis = 1)
A = np.concatenate((A1,A2), axis = 0)
Test = np.mod(np.matmul(np.mod(A,Mod),np.mod(A,Mod)),Mod)       #making sure that A is an involutory matrix, A*A = I
#print(A)
# Saving key as an image
key = np.zeros((n + 1, n))
key[:n, :n] += A
# Adding the dimension of the original image within the key
# Elements of the matrix should be below 256
key[-1][0] = int(l / Mod)
key[-1][1] = l % Mod
key[-1][2] = int(w / Mod)
key[-1][3] = w % Mod
#imageio.imwrite("Key.png", key)

#-------------Encrypting-------------
#print(key)

Encrypted = np.zeros((nl,w,3))
for i in range(int(nl/n)):
    Enc1 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,0] % Mod)) % Mod
    Enc2 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,1] % Mod)) % Mod    # why % mod because we want to keep dimension of each pixel less than 256
    Enc3 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,2] % Mod)) % Mod
    
    Enc1 = np.resize(Enc1,(Enc1.shape[0],Enc1.shape[1],1))
    Enc2 = np.resize(Enc2,(Enc2.shape[0],Enc2.shape[1],1))
    Enc3 = np.resize(Enc3,(Enc3.shape[0],Enc3.shape[1],1))
    Encrypted[i * n:(i + 1) * n,:] += np.concatenate((Enc1,Enc2,Enc3), axis = 2)                #Enc = A * image

imageio.imwrite('Encrypted.png',Encrypted)







