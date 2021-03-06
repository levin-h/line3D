import matplotlib.pyplot as plt
import numpy as np
import h5py
import cartopy
import cartopy.crs as ccrs
import lev_misc
import lev_interpol3d
import read_benchmarks

def muc(xp, yp, zp, phi):
#
#;calculate critical mu (tangential ray at surface) at point (xp,yp,zp)
#;for a given phi-angle
#;
   a=np.cos(phi)*xp+np.sin(phi)*yp
   b=zp
   c=-np.sqrt(xp**2+yp**2+zp**2-1.)
#
   disc=a**2+b**2-c**2
   if disc >= 0.:
      muc1 = (-b*c-a*np.sqrt(disc))/(a**2+b**2)
      muc2 = (-b*c+a*np.sqrt(disc))/(a**2+b**2)
      f1=a*np.sqrt(1.-muc1**2)+b*muc1+c
      f2=a*np.sqrt(1.-muc2**2)+b*muc2+c
      if np.abs(f1) > 1.e-6:
         muc1=10.
      if np.abs(f2) > 1.e-6:
         muc2=10.
   else:
#return dummy value if no tangential ray exists at all
      muc1 = 10.
      muc2 = 10.
#
   mucmin=min([muc1,muc2])
   mucmax=max([muc1,muc2])
   muc1=mucmin
   muc2=mucmax
   return muc1, muc2

######################################################################

fig1 = plt.figure(1)
fig2 = plt.figure(2)
fig3 = plt.figure(3)

xsize=18. #in cm
xsize=xsize/2.54 #in inches
aspect_ratio=2.6
ysize=xsize/aspect_ratio
fig4 = plt.figure(4,figsize=(xsize,ysize))

plt.ion()
plt.show()


fname = './benchmark11.h5'
opt_angint_method, ndxmax, ndymax, ndzmax, \
dim_omega, n1d_angdep, x, y, z, \
xcoord_angdep, ycoord_angdep, zcoord_angdep, \
n_x, n_y, n_z, weight_omega, nodes_mu, nodes_phi, \
mint3d_sc, mint3d_fvm, mint3d_theo, mask3d, \
intsc_angdep, intfvm_angdep \
= read_benchmarks.benchmark11(fname=fname)


nodes_mu_unique=np.unique(nodes_mu)
nodes_phi_unique=np.unique(nodes_phi)
dim_mu_unique = nodes_mu_unique.size
dim_phi_unique = nodes_phi_unique.size
#
#----------------------print the errors--------------------------------
#
print('------errors for sc method------')
#errors3d, mint3d_sc, mint3d_theo, mask3d, erri, errm, err_max, devm
print('')
print('-----errors for fvm method------')
#errors3d, mint3d_fvm, mint3d_theo, mask3d, erri, errm, err_max, devm
#
#-----------------------------------------------------------------------
#
#********************plot mean intensities******************************
#
#-----------------------define range------------------------------------
#
#define radius
r3d = np.zeros(shape=(ndxmax,ndymax,ndzmax))#,ndymax,ndzmax)
for i in range(0,ndxmax):
   for j in range(0,ndymax):   
      for k in range(0,ndzmax):
         r3d[i,j,k]=0. #dummy value
         if mask3d[i,j,k] == 1:
            r3d[i,j,k]=np.sqrt(x[i]**2+y[j]**2+z[k]**2)
         if mask3d[i,j,k] == 2:
            r3d[i,j,k]=np.sqrt(x[i]**2+y[j]**2+z[k]**2)
         if mask3d[i,j,k] == 3:
            r3d[i,j,k]=np.sqrt(x[i]**2+y[j]**2+z[k]**2)            

         dum = mint3d_sc[i,j,k]*r3d[i,j,k]**2
         if dum > 0. and dum < 0.1:
            print(i, j, k, r3d[i,j,k], x[i], y[j], z[k])

#
#-----------------------------------------------------------------------
#
ax = fig1.subplots(2)
#
#first plot
xlim=[.9,12.]
ylim=[-0.05,0.6]
ax[0].set_xlabel(r'$r$')
ax[0].set_ylabel(r'$J\cdot r^2$')
ax[0].set_xlim(xlim)
ax[0].set_ylim(ylim)
#
ax[0].scatter(r3d, mint3d_theo*r3d**2, marker='o', color='black', s=0.01, lw=0, label='theoretical (from dilution)')
ax[0].scatter(r3d, mint3d_sc*r3d**2, marker='o', color='blue', s=0.01, lw=0, label='3d short characteristics')
ax[0].scatter(r3d, mint3d_fvm*r3d**2, marker='o', color='red', s=0.01, lw=0, label='3d finite volume method')
#
ax[0].legend()
#

#second plot
xlim=[.9,12.]
ylim=[0.,2.]
ax[1].set_xlabel(r'$r$')
ax[1].set_ylabel(r'$J(num)/J(theo)$')
ax[1].set_xlim(xlim)
ax[1].set_ylim(ylim)
#
ax[1].scatter(r3d, mint3d_sc/mint3d_theo, marker='o', color='blue', s=0.01, lw=0, label='3d short characteristics')
ax[1].scatter(r3d, mint3d_fvm/mint3d_theo, marker='o', color='red', s=0.01, lw=0, label='3d finite volume method')
#
ax[1].legend()
#
#fig1.savefig('./ps_files/benchmark11_a.png', bbox_inches='tight')
#fig1.savefig('./ps_files/benchmark11_a.ps', bbox_inches='tight')
#
#********plot mean intensities at a certain radius on a sphere**********
#
n_theta=31
n_phi=2*n_theta-1

mu_grid = lev_misc.grid_equi(0.,np.pi,n_theta)*180./np.pi
phi_grid = lev_misc.grid_equi(0.,2.*np.pi,n_phi)*180./np.pi


mint2d_sc=np.zeros(shape=(n_theta,n_phi))
mint2d_fvm=np.zeros(shape=(n_theta,n_phi))
#
#perform interpolation onto 2d surface at given radius
radius = 2.
#
#------interpolate mint3d onto sphere with radius and angle-grids------
#
pp=np.zeros(3)
for i in range(0,n_theta):
   for j in range(0,n_phi):
      pp[0]=radius*np.sin(mu_grid[i])*np.cos(phi_grid[j])
      pp[1]=radius*np.sin(mu_grid[i])*np.sin(phi_grid[j])
      pp[2]=radius*np.cos(mu_grid[i])
#
#find indices of cube-vertices for interpolation
      indx_x1, indx_x2, indx_y1, indx_y2, \
      indx_z1, indx_z2, expol = lev_interpol3d.get_xyz_indx(pp[0], pp[1], pp[2], x, y, z, ndxmax, ndymax, ndzmax)
#store all spatial values on cube-vertices for interpolation and check if
#interpolation in logspace is allowed
      x1,x2,y1,y2,z1,z2, \
      rada,radb,radc,radd,rade,radf,radg,radh,radp,\
      llogx,llogy,llogz=lev_interpol3d.get_xyz_values1(pp[0], pp[1], pp[2], x, y, z, ndxmax, ndymax, ndzmax, \
                                                       indx_x1, indx_x2, indx_y1, indx_y2, indx_z1, indx_z2)
#
#------------------------for short characteristics----------------------
#
#store all physical values on cube-vertices for interpolation
      vala,valb,valc,vald,vale,valf,valg,valh,llogf=lev_interpol3d.get_xyz_values2(ndxmax, ndymax, ndzmax, mint3d_sc, \
                                                               indx_x1, indx_x2, indx_y1, indx_y2, indx_z1, indx_z2)

#following statements can switch to pure linear interpolation
#      llogx=0
#      llogy=0
#      llogz=0
#      llogf=0
#here, can decide if values shall be interpolated by function*r^2
      lr2=1
#actual interpolation
      valp = lev_interpol3d.trilin_complete(pp[0], pp[1], pp[2], x1, x2, y1, y2, z1, z2, \
                                           vala, valb, valc, vald, vale, valf, valg, valh, \
                                           rada, radb, radc, radd, rade, radf, radg, radh, radp, \
                                           expol, llogx, llogy, llogz, llogf, lr2)

      mint2d_sc[i,j]=valp
#
#--------------------------------for fvm--------------------------------
#
#store all physical values on cube-vertices for interpolation
      vala,valb,valc,vald,vale,valf,valg,valh,llogf=lev_interpol3d.get_xyz_values2(ndxmax, ndymax, ndzmax, mint3d_fvm, \
                                                               indx_x1, indx_x2, indx_y1, indx_y2, indx_z1, indx_z2)

#following statements can switch to pure linear interpolation
#      llogx=0
#      llogy=0
#      llogz=0
#      llogf=0
#here, can decide if values shall be interpolated by function*r^2
      lr2=1
#actual interpolation
      valp = lev_interpol3d.trilin_complete(pp[0], pp[1], pp[2], x1, x2, y1, y2, z1, z2, \
                                           vala, valb, valc, vald, vale, valf, valg, valh, \
                                           rada, radb, radc, radd, rade, radf, radg, radh, radp, \
                                           expol, llogx, llogy, llogz, llogf, lr2)
      mint2d_fvm[i,j]=valp

dilfac=1.-np.sqrt(1.-1./radius/radius)
mint_theo=0.5*dilfac
#
mint2d_sc=mint2d_sc/mint_theo
mint2d_fvm=mint2d_fvm/mint_theo
#
#-----------------------------------------------------------------------
#
mu_grid=mu_grid-90.
phi_grid,mu_grid=np.meshgrid(phi_grid,mu_grid)

ax0 = fig2.add_subplot(1,2,1, projection=ccrs.Orthographic(45, 45))
ax1 = fig2.add_subplot(1,2,2, projection=ccrs.Orthographic(45, 45))


#color range
cmin=1.
cmax=1.2
dcol=(cmax-cmin)/99.
clevels=np.arange(cmin,cmax+dcol,dcol)

contourplot0 = ax0.contourf(phi_grid, mu_grid, mint2d_sc,
               levels=clevels,
               transform=ccrs.PlateCarree(),
               cmap='jet')

contourplot1 = ax1.contourf(phi_grid, mu_grid, mint2d_fvm,
               levels=clevels,
               transform=ccrs.PlateCarree(),
               cmap='jet')
ax0.set_title('SC')
ax1.set_title('FVM')

cbar = fig2.colorbar(contourplot0,ax=fig2.get_axes(),orientation='horizontal')
#cbar = fig2.colorbar(contourplot0,ax=ax0,orientation='horizontal')
#cbar = fig2.colorbar(contourplot1,ax=ax1,orientation='horizontal')
cbar.set_label(r'$J/J_{theo}$')

#fig2.savefig('./ps_files/benchmark11_b.png', bbox_inches='tight')
#fig2.savefig('./ps_files/benchmark11_b.ps', bbox_inches='tight')
#
#*****************plot intensities as function of angle A***************
#
#-----------------------define range------------------------------------
#
xlim=[0.,np.pi]
ylim=[0.,2.*np.pi]
#
zmin=np.min([np.min(intsc_angdep),np.min(intfvm_angdep)])
zmax=np.max([np.max(intsc_angdep),np.max(intfvm_angdep)])
#
dz=zmax-zmin
if dz == 0.:
   zmin=zmin-0.1
   zmax=zmax+0.1
else:
   zmin=zmin-0.1*dz
   zmax=zmax+0.1*dz
zlim=[zmin,zmax]


#color range
cmin=0.01
cmax=1.
dcol=(cmax-cmin)/99.
clevels=np.arange(cmin,cmax+dcol,dcol)
#
#----------------------for contour plot---------------------------------
#
for i in range(0,n1d_angdep):
   xp=xcoord_angdep[i]
   yp=ycoord_angdep[i]
   zp=zcoord_angdep[i]
   ax = fig3.subplots(1,2)
   intsc_angdep1d = np.zeros(dim_omega)
   intfvm_angdep1d = np.zeros(dim_omega)   
#   for j in range(0,dim_omega):
#      intsc_angdep1d[j] = intsc_angdep[j][i]
#      intfvm_angdep1d[j] = intfvm_angdep[j][i]      


#   ax0 = ax[0].tricontourf(nodes_mu,nodes_phi,intsc_angdep1d, levels=clevels, cmap='jet')
#   ax1 = ax[1].tricontourf(nodes_mu,nodes_phi,intfvm_angdep1d, levels=clevels, cmap='jet')
#   ax[0].set_xlabel(r'$\theta$')
#   ax[0].set_ylabel(r'$\phi$')
#   ax[1].set_xlabel(r'$\theta$')
#   ax[1].set_ylabel(r'$\phi$')
#   ax[0].set_title('SC')
#   ax[1].set_title('FVM')
#
#----------------------overplot the grid--------------------------------
#
#   if opt_angint_method == 0:
#      for j in range(0,dim_mu_unique):
#         ax[0].plot([nodes_mu_unique[j],nodes_mu_unique[j]],ylim,color='black', lw=.8)
#         ax[1].plot([nodes_mu_unique[j],nodes_mu_unique[j]],ylim,color='black', lw=0.8)
#      for j in range(0,dim_phi_unique):         
#         ax[0].plot(xlim,[nodes_phi_unique[j],nodes_phi_unique[j]],color='black', lw=0.8)
#         ax[1].plot(xlim,[nodes_phi_unique[j],nodes_phi_unique[j]],color='black', lw=0.8)                  

   
#legend
#   cbar = fig3.colorbar(ax0,ax=ax)
#   cbar.set_label(r'$I(\mu,\phi)$')

#   fig3.suptitle(r'at point $(x,y,z)=({xp:.4f},{yp:.4f},{zp:.4f})$'.format(xp=xp,yp=yp,zp=zp))
   
#   fig3.savefig('./ps_files/benchmark11_c.png', bbox_inches='tight')
#   fig3.savefig('./ps_files/benchmark11_c.ps', bbox_inches='tight')
#   input("Press [enter] to continue.")


#
#*****************plot intensities as function of angle A'**************
#
#-----------------------define range------------------------------------
#
xlim=[0.,np.pi]
ylim=[0.,2.*np.pi]
#
zmin=np.min([np.min(intsc_angdep),np.min(intfvm_angdep)])
zmax=np.max([np.max(intsc_angdep),np.max(intfvm_angdep)])
#
dz=zmax-zmin
if dz == 0.:
   zmin=zmin-0.1
   zmax=zmax+0.1
else:
   zmin=zmin-0.1*dz
   zmax=zmax+0.1*dz
zlim=[zmin,zmax]

#color range
cmin=0.01
cmax=1.
dcol=(cmax-cmin)/99.
clevels=np.arange(cmin,cmax+dcol,dcol)
#
#----------------------for contour plot---------------------------------
#
indx_plot = np.array([0,24,6,30])
nplots=indx_plot.size

ax = fig4.subplots(1,nplots)

k=0
for i in indx_plot:
   xp=xcoord_angdep[i]
   yp=ycoord_angdep[i]
   zp=zcoord_angdep[i]
   
   intsc_angdep1d = np.zeros(dim_omega)
   intfvm_angdep1d = np.zeros(dim_omega)   
   for j in range(0,dim_omega):
      intsc_angdep1d[j] = intsc_angdep[j][i]
      intfvm_angdep1d[j] = intfvm_angdep[j][i]      


   ax0 = ax[k].tricontourf(nodes_mu,nodes_phi,intsc_angdep1d, levels=clevels, cmap='jet')
   ax[k].set_xlabel(r'$\theta$')
   if k == 0:
      ax[k].set_ylabel(r'$\phi$')
   else:
      ax[k].yaxis.set_ticklabels([])

#   ax[k].set_title(r'k={kk:}'.format(kk=i),fontsize=10)
#
#----------------------overplot the grid--------------------------------
#
   if opt_angint_method == 0:
      for j in range(0,dim_mu_unique):
         ax[k].plot([nodes_mu_unique[j],nodes_mu_unique[j]],ylim,color='black', lw=.1)
      for j in range(0,dim_phi_unique):         
         ax[k].plot(xlim,[nodes_phi_unique[j],nodes_phi_unique[j]],color='black', lw=.1)
   k=k+1

   
#legend
cbar = fig4.colorbar(ax0,ax=ax)
cbar.set_label(r'$I(\mu,\phi)$')

fig4.savefig('./ps_files/benchmark11_d.png', bbox_inches='tight')
fig4.savefig('./ps_files/benchmark11_d.ps', bbox_inches='tight')

for i in range(1,10):
   sdum=input("Press [q] to quit.")
   if sdum == 'q':
      exit()

exit
