from cmath import nan
import numpy as np
import sdf 
import happi
import openpmd_api as io
import matplotlib.pyplot as plt
from matplotlib import use
from scipy.constants import micron,c,pi,centi,femto,m_e,epsilon_0,elementary_charge as q_e
import os

#__________________________________________________________
# create plot directory
plot_dir = './plots'
if os.path.exists(plot_dir) is False:
    os.mkdir(plot_dir)

#__________________________________________________________
# simulation parameters
Lx = 70.*micron 
resx = 20. # points per micron 
Ly = 30.*micron
nx = Lx * resx / micron 
dx = Lx/nx

cfl = 0.98
dt = cfl * dx / (c * np.sqrt(2.))

Tsim = 1.5*Lx / c 
nsteps = int(Tsim/dt) 

lambda_SI = 0.8*micron # wavelength
omega_SI = 2.0*pi*c / lambda_SI
n_crit = (m_e*epsilon_0*(2*pi*c)**2)/((q_e*lambda_SI)**2)

my_dpi = 300.

every_fs = np.floor(femto/dt)
out_freq = int(10*every_fs)

steps = np.arange(0,nsteps,out_freq)

# warpx
warpx_dir='./warpx/diags/Fields'
# series to know where the data is
series = io.Series(warpx_dir+"/openpmd_%T.h5",io.Access.read_only)
#reading test particles
warpx_dir='./warpx/diags/Particles'
# series to know where the data is
series_p = io.Series(warpx_dir+"/openpmd_%T.h5",io.Access.read_only)
#If you only had warpx, n and ts could have been taken with the following:
#for n,ts in enumerate(series.iterations):
j = series_p.iterations[0]
id_ionc_w = j.particles["ionc_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
id_ele_w = j.particles["ele_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
n_ionc_w = len(id_ionc_w)
n_ele_w = len(id_ele_w)

#smilei 
smilei_dir = './smilei'
s = happi.Open(smilei_dir) 
micron_s = s.namelist.micron 
fs_s = s.namelist.fs
ele_s = s.TrackParticles(species='ele_test', sort=True, axes=['x', 'y', 'px', 'py', 'pz'])
ionc_s = s.TrackParticles(species='ion_c_test', sort=True, axes=['x', 'y', 'px', 'py', 'pz'])
times = ele_s.getTimes()/fs_s
x_ele_s = ele_s.getData().get('x')/micron_s
y_ele_s = ele_s.getData().get('y')/micron_s
x_ionc_s = ionc_s.getData().get('x')/micron_s
y_ionc_s = ionc_s.getData().get('y')/micron_s
n_ele_s = len(x_ele_s[0,:])
n_ionc_s = len(x_ionc_s[0,:])

# for n, ts in Ey.getAvailableTimesteps():

# epoch
epoch_dir = './epoch/Data/'
filenames=np.genfromtxt(epoch_dir+'fields.visit',dtype='str') 

steps = np.arange(0,nsteps,every_fs)
#for t in range(len(filenames)): 
#plotting electron trajectories 
for n,ts in enumerate(steps, start = 0):
    fig, ax = plt.subplots(2,3,figsize=(3000./my_dpi, 2000./my_dpi), dpi=my_dpi)

    #smilei
    #rho_ele_c = s.Field(0,'Rho_ele_c', units=["um","fs"], timesteps=np.floor(ts/10)).getData()[0]
    #rho_ele_s = s.Field(0,'Rho_ele_s', units=["um","fs"], timesteps=np.floor(ts/10)).getData()[0]
    #rho_ele_f = s.Field(0,'Rho_ele_f', units=["um","fs"], timesteps=np.floor(ts/10)).getData()[0]
    #print(rho_ele_c.dtype)
    #print(rho_ele_c.shape)
    #x =  s.Field(0,'Rho_ele_c', units=["um","fs"], timesteps=np.floor(ts/10)).getAxis('x')
    #y =  s.Field(0,'Rho_ele_c', units=["um","fs"], timesteps=np.floor(ts/10)).getAxis('y')
    #im=ax[0,0].imshow(-np.transpose(rho_ele_c+rho_ele_s+rho_ele_f),alpha=1.0, extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Greys', norm = 'log')
    #cbar = plt.colorbar(im, ax=ax[0,0])
    #cbar.set_label(r'$n_e$ [$n_c$]') 
    #electrons smilei
    for p in range(n_ele_s):
         ax[0,0].plot(x_ele_s[0:n+1,p],y_ele_s[0:n+1,p], zorder=10, lw = 1)
         ax[0,0].scatter(x_ele_s[n,p],y_ele_s[n,p],zorder=11, s=1)

    #rho_ion_c = s.Field(0,'Rho_ion_c', units=["um","fs"], timesteps=np.floor(ts/10)).getData()
    #x =  s.Field(0,'Rho_ion_c', units=["um","fs"], timesteps=np.floor(ts/10)).getAxis('x')
    #y =  s.Field(0,'Rho_ion_c', units=["um","fs"], timesteps=np.floor(ts/10)).getAxis('y')
    #im=ax[1,0].imshow(np.transpose(rho_ion_c),alpha=1.0,  extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Reds', norm = 'log')
    #cbar = plt.colorbar(im, ax=ax[1,0])
    #cbar.set_label(r'$n_i$ [$n_c$]') 
    #ionc smilei
    for p in range(n_ionc_s):
         ax[1,0].plot(x_ionc_s[0:n+1,p],y_ionc_s[0:n+1,p], zorder=10, lw = 1)
         ax[1,0].scatter(x_ionc_s[n,p],y_ionc_s[n,p],zorder=11, s=1)

    ax[0,0].set_title('Electrons trajectories Smilei')
    ax[1,0].set_title('Ions trajectories Smilei')

    #warpx
    #tw = int(np.floor(ts/8/10))*80 #print the previous density
    #j = series.iterations[tw]

    #extracting Rho ele
    #rho_ele_c = j.meshes["rho_elec"][io.Mesh_Record_Component.SCALAR]
    #rho_ele_c = rho_ele_c.load_chunk()
    #rho_ele_f = j.meshes["rho_elef"][io.Mesh_Record_Component.SCALAR]
    #rho_ele_f = rho_ele_f.load_chunk()
    #rho_ele_s = j.meshes["rho_eles"][io.Mesh_Record_Component.SCALAR]
    #rho_ele_s = rho_ele_s.load_chunk()

    #extracting Rho contaminants                                                                                                                                                   
    #rho_ion_c = j.meshes["rho_ionc"][io.Mesh_Record_Component.SCALAR]
    #rho_ion_c = rho_ion_c.load_chunk()

    #series.flush()

    #im=ax[0,1].imshow(-(rho_ele_c+rho_ele_f+rho_ele_s)/n_crit/q_e,alpha=1.0 , extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Greys', norm = 'log')
    #cbar = plt.colorbar(im, ax=ax[0,1])
    #cbar.set_label(r'$n_e$ [$n_c$]')

    tw = int(ts)
    j = series_p.iterations[tw]

    series_p.flush 
    #electrons warpx
    if ts ==0 :
        x_ele_w = j.particles["ele_test"]["position"]["x"].load_chunk()
        y_ele_w = j.particles["ele_test"]["position"]["z"].load_chunk()
        id = j.particles["ele_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
        series_p.flush()
        index = np.argsort(id)
        id_0_ew = id[index]
        x_ele_w = x_ele_w[index]/micron
        y_ele_w = y_ele_w[index]/micron
        for p in range(n_ele_w):
            ax[0,1].scatter(x_ele_w[p],y_ele_w[p],zorder=11, s=1)
    #bubble sort
    else :
        elex=j.particles["ele_test"]["position"]["x"].load_chunk()
        eley=j.particles["ele_test"]["position"]["z"].load_chunk()
        id = j.particles["ele_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
        series_p.flush()
        index = np.argsort(id)
        elex = elex[index]/micron
        eley = eley[index]/micron
        id = id[index]
        diff = np.setdiff1d(id_0_ew,id)
        print(diff)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_0_ew,diff))[0]
            print(id_miss)
            for i in id_miss:
                elex = np.insert(elex, i , nan)
                eley = np.insert(eley, i , nan)
            print(elex)
        x_ele_w = np.vstack([x_ele_w,elex])
        y_ele_w = np.vstack([y_ele_w,eley])
        for p in range(n_ele_w):     
            ax[0,1].plot(x_ele_w[:,p],y_ele_w[:,p], zorder=10, lw = 1)
            ax[0,1].scatter(x_ele_w[n,p],y_ele_w[n,p],zorder=11, s=1)


    #im=ax[1,1].imshow((rho_ion_c/n_crit/q_e),alpha=1.0, extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Reds')
    #cbar = plt.colorbar(im, ax=ax[1,1])
    #cbar.set_label(r'$n_e$ [$n_c$]') 
    #ionc warpx
    if ts ==0 :
        id = j.particles["ionc_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
        x_ionc_w = j.particles["ionc_test"]["position"]["x"].load_chunk()
        y_ionc_w = j.particles["ionc_test"]["position"]["z"].load_chunk()
        series_p.flush()
        index = np.argsort(id)
        id_0_iw = id[index]
        x_ionc_w = x_ionc_w[index]/micron
        y_ionc_w = y_ionc_w[index]/micron
        for p in range(n_ionc_w):
            ax[1,1].scatter(x_ionc_w[p],y_ionc_w[p],zorder=11, s=1)
    #bubble sort
    else :
        elex = j.particles["ionc_test"]["position"]["x"].load_chunk()
        eley = j.particles["ionc_test"]["position"]["z"].load_chunk()
        id =j.particles["ionc_test"]["id"][io.Mesh_Record_Component.SCALAR].load_chunk()
        series_p.flush()
        index = np.argsort(id)
        id = id[index]
        elex = elex[index]/micron
        eley = eley[index]/micron
        diff = np.setdiff1d(id_0_iw,id)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_0_iw,diff))[0]
            for i in id_miss:
                elex = np.insert(elex, i , nan) 
                eley = np.insert(eley, i , nan) 
        x_ionc_w = np.vstack([x_ionc_w,elex])
        y_ionc_w = np.vstack([y_ionc_w,eley])

        for p in range(n_ionc_w):
            ax[1,1].plot(x_ionc_w[:,p],y_ionc_w[:,p], zorder=10, lw = 1)
            ax[1,1].scatter(x_ionc_w[n,p],y_ionc_w[n,p],zorder=11, s=1)

    ax[0,1].set_title('Electrons trajectories Warpx')
    ax[1,1].set_title('Ions trajectories Warpx')


    #epoch
    #fname = epoch_dir+'fields%04d.sdf' % np.floor(ts/10)
    #raw = sdf.read(fname)

    #rho_ele_f = raw.__dict__["Derived_Number_Density_ele_foam"].data
    #rho_ele_s = raw.__dict__["Derived_Number_Density_ele_subs"].data
    #rho_ele_c = raw.__dict__["Derived_Number_Density_ele_cont"].data
    #rho_ion_c = raw.__dict__["Derived_Number_Density_ion_cont"].data

    #im=ax[0,2].imshow(np.transpose((rho_ele_f+rho_ele_s+rho_ele_c)/n_crit),alpha=1.0,  extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Greys', norm='log')
    #cbar = plt.colorbar(im, ax=ax[0,2])
    #cbar.set_label(r'$n_e$ [$n_c$]') 

    fname = epoch_dir+'ele%04d.sdf' % int(ts/8)
    raw = sdf.read(fname)
    #electron epoch
    if ts == 0:
        id_ele_e_f = raw.__dict__["Particles_ID_subset_part_ele_ele_foam"].data
        id_ele_e_s = raw.__dict__["Particles_ID_subset_part_ele_ele_subs"].data
        id_ele_e_c = raw.__dict__["Particles_ID_subset_part_ele_ele_cont"].data
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_foam"].data
        x_ele_e_f = pos[0]
        y_ele_e_f = pos[1]
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_subs"].data
        x_ele_e_s = pos[0]
        y_ele_e_s = pos[1]
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_cont"].data
        x_ele_e_c = pos[0]
        y_ele_e_c = pos[1]
        index = np.argsort(id_ele_e_f)
        id_ele_e_f_0 = id_ele_e_f[index]
        x_ele_e_f = x_ele_e_f[index]/micron
        y_ele_e_f = y_ele_e_f[index]/micron
        index =np.argsort(id_ele_e_s)
        id_ele_e_s_0 = id_ele_e_s[index]
        x_ele_e_s = x_ele_e_s[index]/micron
        y_ele_e_s = y_ele_e_s[index]/micron
        index =  np.argsort(id_ele_e_c)
        id_ele_e_c_0 = id_ele_e_c[index]
        x_ele_e_c = x_ele_e_c[index]/micron
        y_ele_e_c = y_ele_e_c[index]/micron

        for p in range(len(id_ele_e_f)):
            ax[0,2].scatter(x_ele_e_f[p],y_ele_e_f[p],zorder=11, s=1)

        for p in range(len(id_ele_e_s)):
            ax[0,2].scatter(x_ele_e_s[p],y_ele_e_s[p],zorder=11, s=1)

        for p in range(len(id_ele_e_c)):
            ax[0,2].scatter(x_ele_e_c[p],y_ele_e_c[p],zorder=11, s=1)
    #bubble sort
    else:
        id_ele_e_fe = raw.__dict__["Particles_ID_subset_part_ele_ele_foam"].data
        id_ele_e_se = raw.__dict__["Particles_ID_subset_part_ele_ele_subs"].data
        id_ele_e_ce = raw.__dict__["Particles_ID_subset_part_ele_ele_cont"].data
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_foam"].data
        x_ele_e_fe = pos[0]
        y_ele_e_fe = pos[1]
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_subs"].data
        x_ele_e_se = pos[0]
        y_ele_e_se = pos[1]
        pos = raw.__dict__["Grid_Particles_subset_part_ele_ele_cont"].data
        x_ele_e_ce = pos[0]
        y_ele_e_ce = pos[1]
        index = np.argsort(id_ele_e_fe)
        id_ele_e_fe = id_ele_e_fe[index]
        x_ele_e_fe = x_ele_e_fe[index]/micron
        y_ele_e_fe = y_ele_e_fe[index]/micron
        diff = np.setdiff1d(id_ele_e_f_0,id_ele_e_fe)
        print(diff)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_ele_e_f_0,diff))[0]
            print(id_miss)
            for i in id_miss:
                x_ele_e_fe = np.insert(x_ele_e_fe, i , nan)
                y_ele_e_fe = np.insert(y_ele_e_fe, i , nan)
            print(x_ele_e_fe) 
        index =np.argsort(id_ele_e_se)
        id_ele_e_se = id_ele_e_se[index]
        x_ele_e_se = x_ele_e_se[index]/micron
        y_ele_e_se = y_ele_e_se[index]/micron
        diff = np.setdiff1d(id_ele_e_s_0,id_ele_e_se)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_ele_e_s_0,diff))[0]
            for i in id_miss:
                x_ele_e_se = np.insert(x_ele_e_se, i , nan) 
                y_ele_e_se = np.insert(y_ele_e_se, i , nan) 
        index =  np.argsort(id_ele_e_ce)
        id_ele_e_ce = id_ele_e_ce[index]
        x_ele_e_ce = x_ele_e_ce[index]/micron
        y_ele_e_ce = y_ele_e_ce[index]/micron
        diff = np.setdiff1d(id_ele_e_c_0,id_ele_e_ce)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_ele_e_c_0,diff))[0]
            for i in id_miss:
                x_ele_e_ce = np.insert(x_ele_e_ce, i , nan) 
                y_ele_e_ce = np.insert(y_ele_e_ce, i , nan) 
        x_ele_e_s = np.vstack([x_ele_e_s,x_ele_e_se])
        x_ele_e_f = np.vstack([x_ele_e_f,x_ele_e_fe])
        x_ele_e_c = np.vstack([x_ele_e_c,x_ele_e_ce])
        y_ele_e_s = np.vstack([y_ele_e_s,y_ele_e_se])
        y_ele_e_f = np.vstack([y_ele_e_f,y_ele_e_fe])
        y_ele_e_c = np.vstack([y_ele_e_c,y_ele_e_ce])
        for p in range(len(id_ele_e_f)):
            ax[0,2].plot(x_ele_e_f[:,p],y_ele_e_f[:,p], zorder=10, lw = 1)
            ax[0,2].scatter(x_ele_e_f[n,p],y_ele_e_f[n,p],zorder=11, s=1)

        for p in range(len(id_ele_e_s)):
            ax[0,2].plot(x_ele_e_s[:,p],y_ele_e_s[:,p], zorder=10, lw = 1)
            ax[0,2].scatter(x_ele_e_s[n,p],y_ele_e_s[n,p],zorder=11, s=1)

        for p in range(len(id_ele_e_c)):
            ax[0,2].plot(x_ele_e_c[0:n,p],y_ele_e_c[0:n,p], zorder=10, lw = 1)
            ax[0,2].scatter(x_ele_e_c[n,p],y_ele_e_c[n,p],zorder=11, s=1)
    #ion_c epoch
    #im=ax[1,2].imshow(np.transpose(rho_ion_c/n_crit),alpha=1.0, extent=[np.min(x),np.max(x),np.min(y),np.max(y)], cmap='Greys')
    #cbar = plt.colorbar(im, ax=ax[1,2])
    #cbar.set_label(r'$n_e$ [$n_c$]')
    
    fname = epoch_dir+'ionc%04d.sdf' % int(ts/8)
    raw = sdf.read(fname)

    if ts == 0:
        id_ionc_e = raw.__dict__["Particles_ID_subset_part_ionc_ion_cont"].data
        pos = raw.__dict__["Grid_Particles_subset_part_ionc_ion_cont"].data
        x_ionc_e = pos[0]
        y_ionc_e = pos[1]
        index = np.argsort(id_ionc_e)
        id_ionc_e_0 = id_ionc_e[index]
        x_ionc_e = x_ionc_e[index]/micron
        y_ionc_e = y_ionc_e[index]/micron
        for p in range(len(id_ionc_e_0)):
            ax[1,2].scatter(x_ionc_e[p],y_ionc_e[p],zorder=11, s=1)
    #bubble sort 
    else:
        id_ionc_e = raw.__dict__["Particles_ID_subset_part_ionc_ion_cont"].data
        pos = raw.__dict__["Grid_Particles_subset_part_ionc_ion_cont"].data
        x_ionc_ee = pos[0]
        y_ionc_ee = pos[1]
        index = np.argsort(id_ionc_e)
        id_ionc_e = id_ionc_e[index]
        x_ionc_ee = x_ionc_ee[index]/micron
        y_ionc_ee = y_ionc_ee[index]/micron
        diff =  np.setdiff1d(id_ionc_e_0,id_ionc_e)
        if diff.size != 0:
            id_miss = np.where(np.in1d(id_ionc_e_0,diff))[0]
            for i in id_miss:
                x_ionc_ee = np.insert(x_ionc_ee, i , nan) 
                y_ionc_ee = np.insert(y_ionc_ee, i , nan) 
        x_ionc_e = np.vstack([x_ionc_e,x_ionc_ee])
        y_ionc_e = np.vstack([y_ionc_e,y_ionc_ee])
        for p in range(len(id_ionc_e_0)):
            ax[1,2].plot(x_ionc_e[:,p],y_ionc_e[:,p], zorder=10, lw = 1)
            ax[1,2].scatter(x_ionc_e[n,p],y_ionc_e[n,p],zorder=11, s=1)

    ax[0,2].set_title('Electrons trajectories Epoch')
    ax[1,2].set_title('Ions trajectories Epoch')

    fig.suptitle('Particle Trajectories @%04d' %ts)
    image_file_name =plot_dir+'/traj_%04d.png' %ts
    plt.tight_layout()
    plt.savefig(image_file_name,dpi=my_dpi)
    plt.close()
