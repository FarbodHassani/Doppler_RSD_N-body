import numpy as np
import MAS_library as MASL
import plotting_library as PL
from pylab import *
from matplotlib.colors import LogNorm
# import matplotlib as plt
import matplotlib.pyplot as plt
import Pk_library as PKL
threads = 64;


print("Libraries are loaded","\n")


files = ['gevolution_boxsize_4032_ngrid_4608_lcdm_05062020','gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em7_05062020','kevolut\
ion_boxsize_4032_ngrid_4608_w_0m9_cs2_em4_05062020','gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_1_05062020']
z_redshifts= [3, 2, 1, 0.5, 0 ]

w=-0.9;
# print("H0[1/Mpc]=100h/c: ",H0);
h=0.67556;
c=2.99792458*1.e5; # [Km/s]
H0=100*1/c; #H0 in h/Mpc 0.00033356409519815205 ---- 100. * h /c we have it in unit 1/Mpc which is 0.00022593979933110373
Omega_b=0.022032/h/h; Omega_cdm=0.12038/h/h;
Omega_m=Omega_b+Omega_cdm; Omega_Lambda=0;
Omega_rad=9.1671353942930788e-05;

j=2
i=3
if (j==0):
    w=-1.0
else:
    w=-0.9;
Omega_kessence = 1 -Omega_m-Omega_rad;
def Hubble_conf_Mpc(z, H0, w ,Omega_kessence,Omega_rad,Omega_m):
            a = 1./(1.+z)
            return H0*np.sqrt(Omega_m*(a**-3)+Omega_rad*(a**-4)+Omega_kessence*(a**(-3*(1+w))))*a

Halos_1 = np.loadtxt("/home/hassani/scratch/Halos_Doppler_project/Halos_snapshots_Box/"+files[j]+"/output/halos_snapshot/out_"+str(i)+"_parents.list")
print("Data is loaded","\n")

Halos = Halos_1[Halos_1[:,41]==-1];

# input parameters
grid    = 2500
BoxSize = 4032 #Mpc/h
MAS     = 'TSC'
verbose = True 

# define the array hosting the density field
delta = np.zeros((grid,grid,grid), dtype=np.float32)
print("array hosting density field is defined!","\n")

c=2.99792458*1.e5;
# read the particle positions for gevolution
Num =np.shape(Halos[:,8])[0];
posx = Halos[:Num,8]; posy=Halos[:Num,9];posz=Halos[:Num,10]; #Mpc/h
#Vz=Halos[:Num,13]; #Mpc/h
# We consider that we are observing at z direction and there will be displacemen at that direction due to the velocity of
# each halo in the snapshots!
pos = np.zeros((np.shape(posx)[0],3))
pos[:,0]=posx;
pos[:,1]=posy;
pos[:,2]=posz #+ Vz/Hubble_conf_Mpc(3.0,H0, w ,Omega_kessence,Omega_rad,Omega_m)/c; # Redshift =3
pos = pos.astype(np.float32)   #pos should be a numpy float array

print("The RSD contribution for long distant observor is considered!","\n")


# compute density field
MASL.MA(pos,delta,BoxSize,MAS,verbose=verbose)

print("Density field is computed!","\n")

mean_delta=np.mean(delta, dtype=np.float64);
print("Mean density is computed!","\n")

# compute overdensity field
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0
print("overdensity is computed!","\n")

# Saving density data

#np.save('Halo_delta_data_lattice', delta)

print("delta data is saved!","\n")

#############PowerSpectra##############

verbose = True
MAS="TSC"
axis=0 # axis. Axis along which compute the quadrupole, hexadecapole and the 2D power spectrum. If the field is in real-space set axis=0. If the field is in redshift-space set axis=0, axis=1 or axis=2 if the redshift-space distortions have been placed along the x-axis, y-axis or z-axis, respectively.
Pk = PKL.Pk(delta, BoxSize, axis,MAS, threads, verbose)
print("Powerspectrum is computed!","\n")

# 3D P(k)
k       = Pk.k3D
Pk0     = Pk.Pk[:,0] #monopole
Pk2     = Pk.Pk[:,1] #quadrupole
Pk4     = Pk.Pk[:,2] #hexadecapole
Pkphase = Pk.Pkphase #power spectrum of the phases
Nmodes  = Pk.Nmodes3D

np.save("pk3D_"+files[j]+"_z_"+str(z_redshifts[i]),[k,Pk0,Pk2,Pk4,Pkphase,Nmodes])
print("Powerspectra are printed!","\n")

#############Correlation functions##############
# CF parameters
# compute the correlation function
CF     = PKL.Xi(delta, BoxSize, MAS, axis, threads)
r      = CF.r3D #radii in Mpc/h
xi0    = CF.xi[:,0]  #correlation function (monopole)
xi2    = CF.xi[:,1]  #correlation function (quadrupole)
xi4    = CF.xi[:,2]  #correlation function (hexadecapole)
Nmodes = CF.Nmodes3D #number of modes
np.save("CF_full_"+files[j]+"_z_"+str(z_redshifts[i]),[r,xi0,xi2,xi4,Nmodes])
