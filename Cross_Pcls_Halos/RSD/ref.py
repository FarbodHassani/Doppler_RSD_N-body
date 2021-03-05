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

files = ['gevolution_boxsize_4032_ngrid_4608_lcdm_05062020','gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_1_05062020','gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em7_05062020','kevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em4_05062020','kevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em7_05062020']

z_redshifts= [3, 2, 1, 0.5, 0 ]

data = ['lcdm_snap00','w0d9_cs1_gevolution_snap00','w0d9_cs2_em7_gevolution_snap00','kess_cs2e4_4032box_4608_snap00','kess_cs2e7_4032box_4608_snap00']

w=-0.9;
# print("H0[1/Mpc]=100h/c: ",H0);
h=0.67556;
c=2.99792458*1.e5; # [Km/s]
H0=100*1/c; #H0 in h/Mpc 0.00033356409519815205 ---- 100. * h /c we have it in unit 1/Mpc which is 0.00022593979933110373
Omega_b=0.022032/h/h; Omega_cdm=0.12038/h/h;
Omega_m=Omega_b+Omega_cdm; Omega_Lambda=0;
Omega_rad=9.1671353942930788e-05;

j=0
i=0
if (j==0):
    w=-1.0
else:
    w=-0.9;
Omega_kessence = 1 -Omega_m-Omega_rad;
def Hubble_conf_Mpc(z, H0, w ,Omega_kessence,Omega_rad,Omega_m):
            a = 1./(1.+z)
            return H0*np.sqrt(Omega_m*(a**-3)+Omega_rad*(a**-4)+Omega_kessence*(a**(-3*(1+w))))*a

Halos_1 = np.loadtxt("/home/hassani/scratch/Doppler_project/Halos_Doppler_project/Halos_snapshots_Box/"+files[j]+"/output/halos_snapshot/out_"+str(i)+"_parents.list")
print("Data is loaded","\n")
Halos = Halos_1[Halos_1[:,41]==-1];


snapshot = "/home/hassani/scratch/Doppler_project/Doppler_runs/"+files[j]+"/redist_output/"+data[j]+str(i)+"_cdm_redist"
print("Data is loaded","\n")

####### Halos
# input parameters
grid    = 2500
BoxSize = 4032 #Mpc/h
MAS     = 'TSC'

# define the array hosting the density field
delta_halos = np.zeros((grid,grid,grid), dtype=np.float32)
print("array hosting density field is defined!","\n")

c=2.99792458*1.e5;
# read the particle positions for gevolution
Num =np.shape(Halos[:,8])[0];
posx = Halos[:Num,8]; posy=Halos[:Num,9];posz=Halos[:Num,10]; #Mpc/h
Vz=Halos[:Num,13]; #Mpc/h
# We consider that we are observing at z direction and there will be displacemen at that direction due to the velocity of
# each halo in the snapshots!
pos = np.zeros((np.shape(posx)[0],3))
pos[:,0]=posx;
pos[:,1]=posy;
pos[:,2]=posz + Vz/Hubble_conf_Mpc(3.0,H0, w ,Omega_kessence,Omega_rad,Omega_m)/c; # Redshift =3
pos = pos.astype(np.float32)   #pos should be a numpy float array

print("The RSD contribution for long distant observor is considered!","\n")

# compute density field
MASL.MA(pos,delta_halos,BoxSize,MAS)
print("Density field is computed!","\n")


# compute overdensity field
delta_halos /= np.mean(delta_halos, dtype=np.float64);  delta_halos -= 1.0
print("overdensity for the halos is computed!","\n")


################ Particles ############
# input parameters
grid    = 2500
BoxSize = 4032 #Mpc/h
MAS     = 'TSC'
ptypes   = [1]                     #CDM
do_RSD   = True                    #dont do redshif-space distortions
axis     = 2                       #axis along which place RSD; z direction
verbose = True

delta_pcl = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD, axis, verbose)
print("Density field is computed!","\n")

# compute density contrast: delta = rho/<rho> - 1
delta_pcl /= np.mean(delta_pcl, dtype=np.float64);  delta_pcl -= 1.0
print("overdensity for pcls is computed!","\n")

#############PowerSpectra##############

#axis=2 # axis. Axis along which compute the quadrupole, hexadecapole and the 2D power spectrum. If the field is in real-space set axis=0. If the field is in redshift-space set axis=0, axis=1 or axis=2 if the redshift-space distortions have been placed along the x-axis, y-axis or z-axis, respectively.

Pk = PKL.XPk([delta_halos,delta_pcl], BoxSize, axis, MAS, threads)


print("Powerspectrum is computed!","\n")

# 3D P(k)
k      = Pk.k3D
Pk0_1  = Pk.Pk[:,0,0]  #monopole of field 1
Pk0_2  = Pk.Pk[:,0,1]  #monopole of field 2
Pk2_1  = Pk.Pk[:,1,0]  #quadrupole of field 1
Pk2_2  = Pk.Pk[:,1,1]  #quadrupole of field 2
Pk4_1  = Pk.Pk[:,2,0]  #hexadecapole of field 1
Pk4_2  = Pk.Pk[:,2,1]  #hexadecapole of field 2
Pk0_X  = Pk.XPk[:,0,0] #monopole of 1-2 cross P(k)
Pk2_X  = Pk.XPk[:,1,0] #quadrupole of 1-2 cross P(k)
Pk4_X  = Pk.XPk[:,2,0] #hexadecapole of 1-2 cross P(k)
Nmodes = Pk.Nmodes3D

np.save("cross_pk3D_"+files[j]+"_z_"+str(z_redshifts[i]),[k, Pk0_1, Pk0_2, Pk2_1, Pk2_2, Pk4_1, Pk4_2, Pk0_X, Pk2_X, Pk4_X, Nmodes])
print("Powerspectra are printed!","\n")

#############Correlation functions##############
# CF parameters
# compute the cross correlation function

CF = PKL.XXi(delta_halos, delta_pcl, BoxSize, MAS, axis, threads)
r      = CF.r3D #radii in Mpc/h
xi0    = CF.xi[:,0]  #correlation function (monopole)
xi2    = CF.xi[:,1]  #correlation function (quadrupole)
xi4    = CF.xi[:,2]  #correlation function (hexadecapole)
Nmodes = CF.Nmodes3D #number of modes
np.save("cross_CF_full_"+files[j]+"_z_"+str(z_redshifts[i]),[r,xi0,xi2,xi4,Nmodes])
