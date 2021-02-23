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

j=0
i=4

snapshot = "/home/hassani/scratch/Doppler_project/Doppler_runs/"+files[j]+"/redist_output/"+data[j]+str(i)+"_cdm_redist"
print("Data is loaded","\n")



# input parameters
grid    = 2304
BoxSize = 4032 #Mpc/h
MAS     = 'CIC'
ptypes   = [1]                     #CDM
do_RSD   = True                    #dont do redshif-space distortions
axis     = 2                       #axis along which place RSD; z direction
verbose = True

delta = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD, axis, verbose)
print("Density field is computed!","\n")

# compute density contrast: delta = rho/<rho> - 1
delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0

print("overdensity is computed!","\n")


#############PowerSpectra##############

Pk = PKL.Pk(delta, BoxSize, axis,MAS, threads, verbose)
print("Powerspectrum is computed!","\n")

# 3D P(k)
k       = Pk.k3D
Pk0     = Pk.Pk[:,0] #monopole
Pk2     = Pk.Pk[:,1] #quadrupole
Pk4     = Pk.Pk[:,2] #hexadecapole
Pkphase = Pk.Pkphase #power spectrum of the phases
Nmodes  = Pk.Nmodes3D

np.save("test_CIC_pk3D_"+files[j]+"_z_"+str(z_redshifts[i]),[k,Pk0,Pk2,Pk4,Pkphase,Nmodes])
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
np.save("test_CIC_pk3D_CF_full_"+files[j]+"_z_"+str(z_redshifts[i]),[r,xi0,xi2,xi4,Nmodes])
