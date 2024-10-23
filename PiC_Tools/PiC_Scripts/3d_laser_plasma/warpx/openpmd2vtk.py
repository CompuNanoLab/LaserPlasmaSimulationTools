import vtk 
import numpy as np
from vtk.util import numpy_support
from scipy.constants import * 
import openpmd_api as io
import os

z = np.linspace(0,30,10*30)
y = np.linspace(-5,5,10*10)
x = np.linspace(-5,5,10*10)
dx = micron/20
T_sim = 0.6*30/c
dt = 0.98 * dx /(c*np.sqrt(3))
lambda_SI = 0.8 * micron
omega_SI = 2.0 * pi * c / lambda_SI
n_crit= (m_e*epsilon_0*(2*pi*c)**2)/((e*0.8e-6)**2)

every_fs = np.floor(femto/dt)
out_freq = int(10*every_fs)
nsteps = int(T_sim/dt)

field_dir = './Fields_vtk/'
if os.path.exists(field_dir) is False:
    os.mkdir(field_dir)

steps = np.linspace(0,nsteps,out_freq)
#loading data series
series = io.Series("./diags/Fields/openpmd_%T.h5",io.Access.read_only)
tw = 637
i = series.iterations[tw]                                                                                                                                                      
gx = x
gy = y
gz = z
dx = gx[1] - gx[0]
dy = gy[1] - gy[0]
dz = gz[1] - gz[0]
ox = gx[0]
oy = gy[0]
oz = gz[0]

Bz = i.meshes["B"]["y"]
Bz = Bz.load_chunk()
series.flush()
Bz = np.asarray(Bz[::2,::2,::2])

imdata = vtk.vtkImageData()
depthArray = numpy_support.numpy_to_vtk(np.ravel(Bz, order='F'), deep=True, array_type=vtk.VTK_DOUBLE)
imdata.SetDimensions(Bz.shape)
imdata.SetSpacing([dx,dy,dz])
imdata.SetOrigin([ox,oy,oz])
imdata.GetPointData().SetScalars(depthArray)

#saving vtk file
writer = vtk.vtkMetaImageWriter()
out_file = field_dir+'B_z_%4d.mhd' %int(tw)
writer.SetFileName(out_file)
writer.SetInputData(imdata)
writer.Write()

for n,t in enumerate(steps, start = 0):
    tw = n*8*10
    i = series.iterations[tw]
#    rho_ele = i.meshes["rho_ele"][io.Mesh_Record_Component.SCALAR]
#    rho_ele = rho_ele.load_chunk()
#    series.flush()

    #modifying data type into vtk 
#    rho_ele = np.asarray(rho_ele[::2,::2,::2])
    gx = x
    gy = y
    gz = z
    dx = gx[1] - gx[0]
    dy = gy[1] - gy[0]
    dz = gz[1] - gz[0]
    ox = gx[0]
    oy = gy[0]
    oz = gz[0]
#    imdata = vtk.vtkImageData()
#    depthArray = numpy_support.numpy_to_vtk(np.ravel(rho_ele, order='F'), deep=True, array_type=vtk.VTK_DOUBLE)
#    imdata.SetDimensions(rho_ele.shape)
#    imdata.SetSpacing([dx,dy,dz])
#    imdata.SetOrigin([ox,oy,oz])
#    imdata.GetPointData().SetScalars(depthArray)

    #saving vtk file
#    writer = vtk.vtkMetaImageWriter()
#    for j in np.linspace(1,10,1):
#        out_file = field_dir+'rho_ele_%4d.mhd' %int(tw*j)
#        writer.SetFileName(out_file)
#        writer.SetInputData(imdata)
#        writer.Write()
    
#    rho_ele = []

    Bz = i.meshes["B"]["y"]
    Bz = Bz.load_chunk()
    series.flush()
    Bz = np.asarray(Bz[::2,::2,::2])

    imdata = vtk.vtkImageData()
    depthArray = numpy_support.numpy_to_vtk(np.ravel(Bz, order='F'), deep=True, array_type=vtk.VTK_DOUBLE)
    imdata.SetDimensions(Bz.shape)
    imdata.SetSpacing([dx,dy,dz])
    imdata.SetOrigin([ox,oy,oz])
    imdata.GetPointData().SetScalars(depthArray)

    #saving vtk file
    writer = vtk.vtkMetaImageWriter()
    out_file = field_dir+'B_z_%4d.mhd' %int(tw/10)
    writer.SetFileName(out_file)
    writer.SetInputData(imdata)
    writer.Write()
    #deleting data series
del series
