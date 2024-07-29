import os
import numpy as np
import happi 
import matplotlib.pyplot as plt
import openpmd_api as io
import sdf
from matplotlib import use
from scipy.constants import micron,c,pi,centi,femto,e,epsilon_0,m_e 

#use('AGG')

#__________________________________________________________
# create plot directory
plot_dir = './plots'
if os.path.exists(plot_dir) is False:
    os.mkdir(plot_dir)


#__________________________________________________________
lambda_SI = 0.8*micron # wavelength
omega_SI = 2.0*pi*c / lambda_SI
fs = 1.e-15 * omega_SI;
mc2 = 0.510998950e6 
my_dpi = 300
pemr = 1836.15267343

#__________________________________________________________
# simulation parameters
Lx = 70*micron
resx = 20. # points per micron 
nx = Lx * resx / micron 
dx = Lx/nx
micron_s = 1.e-6 * omega_SI/c
vol = 70*30*micron_s**(2)
n_crit = (m_e*epsilon_0*(2*pi*c)**2)/((e*lambda_SI)**2)
nppc_ic = 16.
delta_E = 40/0.510998950/200
const = delta_E*vol*n_crit*(c/omega_SI)**2

cfl = 0.98
dt = cfl * dx / (c * np.sqrt(2.))

Tsim = 1.5*Lx / c 
nsteps = int(Tsim/dt) 


every_fs = np.floor(femto/dt)
out_freq = int(10*every_fs)

steps = out_freq * np.arange(nsteps)
times = steps * dt/femto

steps = np.arange(0,nsteps,out_freq)

ene_w = np.linspace(0,40,200)

#warpx
warpx_dir='./warpx/diags/reducedfiles'
datah_w = np.loadtxt(warpx_dir+'/ParticleHist.txt')[1:,1:]
t_w = datah_w[:,1]
warpx_dir = './warpx/diags/Fields'
series = io.Series(warpx_dir+'/openpmd_%T.h5',io.Access.read_only)

#smilei
smilei_dir = './smilei'
s = happi.Open(smilei_dir)
den_s = s.ParticleBinning(2,units=['Mev','um','fs'])
t_s = den_s.getAvailableTimesteps()
px_s = s.TrackParticles("ion_c",axes = ['px'] )
py_s = s.TrackParticles("ion_c",axes = ['py'] )
pz_s = s.TrackParticles("ion_c",axes = ['pz'] )
w_s = s.TrackParticles("ion_c",axes = ['w'] )

#epoch
epoch_dir = './epoch/Data/'
filenames=np.genfromtxt(epoch_dir+'enehist.visit',dtype='str')
t_e=len(filenames)
filepart=np.genfromtxt(epoch_dir+'particles.visit',dtype='str')

for T_w,T_s in zip(range(np.size(t_w)),t_s):

    #warpx
    S = T_w*out_freq
    j  = series.iterations[S]
    px_w = j.particles["ionc"]["momentum"]["x"].load_chunk()
    py_w = j.particles["ionc"]["momentum"]["y"].load_chunk()
    pz_w = j.particles["ionc"]["momentum"]["z"].load_chunk()
    w_part_w = j.particles["ionc"]["weighting"][io.Mesh_Record_Component.SCALAR].load_chunk()
    series.flush()
    e_part_w = (((px_w**2+py_w**2+pz_w**2)*c**2+pemr**2*m_e**2*c**4)**0.5-pemr*m_e*c**2)*6.241509e+12
    part_hist_w,u = np.histogram(e_part_w, bins = ene_w , weights = w_part_w)
    #smilei
    pxh = px_s.getData(T_s)
    pxh = pxh['px']
    pyh = py_s.getData(T_s)
    pyh = pyh['py']
    pzh = pz_s.getData(T_s)
    pzh = pzh['pz']
    e_part_s = ((pxh**2+pyh**2+pzh**2+pemr**2)**0.5 -pemr)*mc2*10**(-6)
    w_part_s = (w_s.getData(T_s)['w'])*n_crit*(c/omega_SI)**2
    part_hist_s,u  = np.histogram(e_part_s, bins = ene_w , weights = w_part_s)
    #epoch
    fname = epoch_dir+'particles%04d.sdf' % T_w
    raw = sdf.read(fname)
    px_e = raw.__dict__["Particles_Px_subset_part_ionc_ion_cont"].data
    py_e = raw.__dict__["Particles_Py_subset_part_ionc_ion_cont"].data
    pz_e = raw.__dict__["Particles_Pz_subset_part_ionc_ion_cont"].data
    w_part_e = raw.__dict__["Particles_Weight_subset_part_ionc_ion_cont"].data
    e_part_e = (((px_e**2+py_e**2+pz_e**2)*c**2+pemr**2*m_e**2*c**4)**0.5-pemr*m_e*c**2)*6.241509e+12
    part_hist_e,u = np.histogram(e_part_e , bins = ene_w , weights = w_part_e)
    
    #warpx
    den_w = datah_w[T_w-1,1:]
    #smilei
    den_s = s.ParticleBinning(diagNumber="#2",timesteps=T_s,units=['um','fs'])
    den_s = den_s.getData()
    #epoch
    fname=epoch_dir+'hist%04d.sdf' % T_w
    raw=sdf.read(fname)
    den_e = raw.__dict__["dist_fn_enehist_ion_cont"].data

    my_dpi = 300 
    fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(4000./my_dpi, 1000./my_dpi), dpi=my_dpi, sharex=True)
    
    #smilei
    ax[0].plot(ene_w,np.transpose(np.array(den_s))*const,label='Binning')
    ax[0].plot(ene_w[:199],part_hist_s,label='TrackParticle')
    ax[0].set_title('Smilei')
    ax[0].set_xlabel('Energy [Mev]')
    ax[0].set_ylabel('Particle density')
    ax[0].legend()
    #warpx
    ax[1].plot(ene_w,den_w,label='Binning')
    ax[1].plot(ene_w[:199],part_hist_w,label='TrackParticle')
    ax[1].set_title('Warpx')
    ax[1].set_xlabel('Energy [Mev]')
    ax[1].set_ylabel('Particle density')
    ax[1].legend()
    #epoch
    ax[2].plot(ene_w,den_e,label='Binning')
    ax[2].plot(ene_w[:199],part_hist_e,label='TrackParticle')
    ax[2].set_title('Epoch')
    ax[2].set_xlabel('Energy [Mev]')
    ax[2].set_ylabel('Particle density')
    ax[2].legend()
    
    fig.suptitle('Energy spectrum @%04d' %T_w)
    image_file_name =plot_dir+'/energy_den_%04d.png' %T_w
    plt.tight_layout()
    plt.savefig(image_file_name,dpi=my_dpi)
    plt.close()
#    np.savetxt(plot_dir+'/energy_hist_%04d' %T_s ,part_hist_s)
