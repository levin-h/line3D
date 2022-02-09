import sys, os
import numpy as np

def number_to_string(number, dtype):
    
    #sign
    str_sign=''
    if number < 0.: str_sign='-'

    number=np.abs(number)

    if dtype == 'dp':
        if number == 0.:
            str_all = '0.d0'            
        elif number > 1.:
            iexp=0
            fdum=1.
            for i in np.arange(1,100):
                if number/fdum < 10.: break
                fdum = fdum*10.
                iexp = iexp+1
            number = number/fdum
            str_all = str_sign + '{number:}'.format(number=number) + 'd{iexp:}'.format(iexp=iexp)
        elif number < 1.:
            iexp = 0
            fdum=1.
            for i in np.arange(1,100):
                if number*fdum > 0.1: break
                fdum = fdum*10.
                iexp = iexp-1
            number = number*fdum*10.  #this weird formalism only to have a nice representation of numbers after the comma
            iexp=iexp-1
            str_all = str_sign + '{number:}'.format(number=number) + 'd{iexp:}'.format(iexp=iexp)
        else:
            number = '1.'
            iexp = 0
            str_all = str_sign + '1.d0'

    elif dtype == 'int':
        str_all = str_sign + '{number:}'.format(number=number)
    else:
        exit('error in number_to_string: dtype not properly specified')
        
    return str_all
#
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#
def copy_to_directory(dir_out):
    #
    print('########### copy to output directory ##################')
    print('output_dir: ', dir_out)
    print()

    command00 = 'mkdir ' + dir_out
    command02 = 'mv output_model.log ' + dir_out
    command02 = 'mv output_sc3d.log ' + dir_out
    command03 = 'mv output_modelspec.log ' + dir_out    
    command01 = 'mv output_spec.log ' + dir_out
    command06 = 'cp model.eo ' + dir_out
    command06 = 'cp sc3d.eo ' + dir_out        
    command04 = 'cp modelspec.eo ' + dir_out
    command05 = 'cp spec.eo ' + dir_out
    command07 = 'cp indat_sc3d_florian.nml ' + dir_out    
    command08 = 'cp indat_modelspec_florian.nml ' + dir_out
    command09 = 'cp indat_spec_florian.nml ' + dir_out
    command10 = 'mv ./outputFILES/modspec_model00.h5 ' + dir_out
    command11 = 'mv ./outputFILES/output_model00.h5 ' + dir_out        
    command12 = 'mv ./outputFILES/spec_surface* ' + dir_out
    command13 = 'mv ./outputFILES/FLUXEM* ' + dir_out

    print(command00)    
    print(command01)
    print(command02)
    print(command03)
    print(command04)
    print(command05)
    print(command06)
    print(command07)
    print(command08)
    print(command09)
    print(command10)
    print(command11)
    print(command12)
    print(command13)        

    os.system(command00)    
    os.system(command01)
    os.system(command02)
    os.system(command03)
    os.system(command04)
    os.system(command05)
    os.system(command06)
    os.system(command07)
    os.system(command08)
    os.system(command09)
    os.system(command10)
    os.system(command11)
    os.system(command12)
    os.system(command13)

    print('done')
    print()
#
#------------------------------------------------------------------
#
#------------------------------------------------------------------
#   
def set_indat_spec(fname='indat_spec_florian.nml', vmicro=None, opt_surface=False):

    lerr=False
    if vmicro == None: lerr=True
    if lerr: exit('error in set_indat_spec: argument not specified')

    vmicro_str = number_to_string(vmicro, 'dp')
    if opt_surface:
        opt_surface_str='t'
    else:
        opt_surface_str='f'
        
    print('########### setting indat file ########################')
    print('output_file: ' + fname)
    print('')

    file = open(fname, "w")
    file.write("&input_options\n")
    file.write("input_mod = 2                                   ! 0 - 1D model ; 2 - 3D Cartesian model ; 2 - 3D Spherical model\n")
    file.write("input_file = './outputFILES/modspec_model00.h5'  ! name of input file - generated by modelspec.eo\n")
    file.write("output_dir = './outputFILES'                    ! output directory \n")
    file.write("opt_photprof = 0                                ! Photospheric profile: 0 - Plank illumination ; 1 - from Herrero ; 2 - from Kuricz  (not active)\n")
    file.write("opt_obsdir_read = t                             ! Observers direction: t - from file in_alpha/gamma.dat; f - equidistant (see below \alpha , \gamma)\n")
    file.write("opt_surface = " + opt_surface_str + "                                 ! t - to calculate surface brightness ; f - emergent fluxes \n")
    file.write("opt_int2d = f                                   ! t - intensity along the all rays ( for debugging)\n")
    file.write("opt_incl_gdark = f                              ! t - include gravity darkening \n")
    file.write("opt_incl_sdist = f                              ! t - include the surface distortion \n")
    file.write("nalpha = 1                                      ! number of alpha angles of observers direction -\n")
    file.write("ngamma = 1                                      ! number of gamma angles of observers direction - if opt_obsdir_read=f nalpha=1 alpha=0\n")
    file.write("/\n")
    file.write("\n")   
#
    file.write("&input_model\n")
    file.write("vrot = 0.d0            ! Surface rotational velocity ; also for opt_incl_gdark and opt_incl_sdist\n")
    file.write("vth_fiducial = 1.d2\n")
    file.write("vmicro = " + vmicro_str + "          ! Micro turbulent\n")
    file.write("rmin = 1.d0            ! Minimum radius as in modelspec\n")
    file.write("rmax = 5.6d0         ! Maximum radius < the one in modelspec to avoid extrapolation errors\n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&input_surface\n")
    file.write("nsurfb = 17\n")
    file.write("alpha_surface = 1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0,\n")
    file.write("                1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0,\n")
    file.write("                1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0, 1.570796d0\n")
    file.write("                1.570796d0, 1.570796d0\n")
    file.write("gamma_surface = 0.d0, 0.d0, 0.d0, 0.d0, 0.d0,\n")
    file.write("                0.d0, 0.d0, 0.d0, 0.d0, 0.d0,\n")
    file.write("                0.d0, 0.d0, 0.d0, 0.d0, 0.d0\n")
    file.write("                0.d0, 0.d0\n")
    file.write("xobs_surface = -10.d0, -8.75d0, -7.5d0, -6.25d0, -5.d0,\n")
    file.write("               -3.75d0, -2.5d0, -1.25d0, 0.d0, 1.25d0, 2.5d0,\n")
    file.write("                3.75d0, 5.d0, 6.25d0, 7.5d0, 8.25d0\n")
    file.write("                10.d0\n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&dum\n")
    file.write("/\n")
    file.write("\n")
    file.close

    print('done')
    print()


def set_indat_modelspec(fname='indat_modelspec_florian.nml',
                        kcont=None,
                        kline=None,
                        vmicro=None,
                        iline=None):
    #set indat_modelspec_nico.nml file


    lerr=False
    if kcont == None: lerr=True
    if kline == None: lerr=True
    if vmicro == None: lerr=True
    if iline == None: lerr=True        
    if lerr: exit('error in set_indat_modelspec: argument not specified')

    vmicro_str = number_to_string(vmicro, 'dp')
    iline_str = number_to_string(iline, 'int')    
    kcont_str = number_to_string(kcont, 'dp')
    kline_str = number_to_string(kline, 'dp')      
    
    print('########### setting indat file ########################')
    print('output_file: '+ fname)
    print()

    file = open(fname, "w")
    file.write("&input_options\n")
    file.write("input_file = './outputFILES/output_model00.h5'\n")
    file.write("input_file2 = './inputFILES/model2d.h5'          ! file generated by ./model.eo \n")
    file.write("output_file = './outputFILES/modspec_model00.h5'\n")
    file.write("input_mod = 13 \n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&input_model\n")
    file.write("teff = 40.d3\n")
    file.write("trad = 40.d3\n")
    file.write("xlogg = 3.6d0      ! Currently not used \n")
    file.write("rstar = 20.015520723398144d0       ! R in R_odot\n")
    file.write("rmax = 5.9895d0       ! R_max in R_star\n")
    file.write("tmin = 1.d0        ! used for case of beta velocity \n")
    file.write("xmloss = 2.d-6     ! used for case of beta velocity\n")
    file.write("vmin = 1.d0       ! used for case of beta velocity in km/sec\n")
    file.write("vmax = 2.8d3        ! used for case of beta velocity in km/sec\n")
    file.write("vmicro = " + vmicro_str + "      ! micro turbulence velocity in km/sec  - For full 3d hydro can be 10 ( but runs faster for higher)\n")
    file.write("vth_fiducial=1.d2\n")
    file.write("beta = 1.d0        ! used for beta law \n")
    file.write("yhe = 0.1d0        ! He number abundance fraction Y (12.25 corresponds to mass-fraction 0.98)\n")
    file.write("hei = 2.d0         ! number ogf free electrons per helium atom    \n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&input_line\n")
    file.write("iline = " + iline_str + "       ! case ID to set line as defined in ./scr/mod_iline.f90 - if iline=0, read from element_z, element_i, element_ll, element_lu\n")
    file.write("eps_line = 0.d0   ! thermalisation parameter  --- not used \n")
    file.write("kline = " + kline_str + "     ! line strength \n")
    file.write("kappa0 = 1.d0     ! not used \n")
    file.write("alpha = 0.d0      ! not used \n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&dum\n")
    file.write("/\n")

    file.close()
    #
    #
    print('done')
    print()

def set_indat_model(fname='indat_sc3d_florian.nml',
                    vmicro=None,
                    kcont=None,
                    kline=None,
                    opt_method=None,                    
                    fname_model=None):

    lerr=False
    if fname_model == None: lerr=True
    if kcont == None: lerr=True
    if kline == None: lerr=True
    if opt_method == None: lerr=True
    if vmicro == None: lerr=True    
    if lerr: exit('error in set_indat_model: argument not specified')

    kcont_str = number_to_string(kcont, 'dp')
    kline_str = number_to_string(kline, 'dp')    
    vmicro_str = number_to_string(vmicro, 'dp')
    opt_method_str = number_to_string(opt_method, 'int')    
        

    print('########### setting model indat file ##################')
    print('output_file: ' +fname)
    print()

    file = open(fname, "w")    
    file.write("&input_options\n")
    file.write("model_dir = 'inputFILES'                     ! Name of the output directory \n")
    file.write("output_file = 'output_model00.h5'  ! name of the output model file \n")
    file.write("input_mod = 12                               ! Model read in instruction 12 = read 2dLDI\n")
    file.write("input_mod_dim = 2                            ! Dimensionality of the problem 1,2,3D\n")
    file.write("spatial_grid1d = 5\n")
    file.write("spatial_grid3d = 2\n")
    file.write("opt_opac = 0\n")
    file.write("opt_opal = 0\n")
    file.write("opt_angint_method = 9\n")
    file.write("opt_method = " + opt_method_str + "\n")
    file.write("opt_sol2d = f\n")
    file.write("opt_ltec = 0\n")
    file.write("opt_incl_cont = f\n")
    file.write("opt_start_cont = t\n")
    file.write("opt_ng_cont = t\n")
    file.write("opt_ait_cont = f\n")
    file.write("opt_incl_line = t\n")
    file.write("opt_start_line = t\n")
    file.write("opt_ng_line = t\n")
    file.write("opt_ait_line = f\n")
    file.write("opt_alo_cont = 1\n")
    file.write("opt_alo_line = 3\n")
    file.write("opt_incl_gdark = f\n")
    file.write("opt_incl_sdist = f\n")
    file.write("/\n")
    file.write("\n")
    #
    file.write("&input_mod_1d\n")
    file.write("teff = 40.d3\n")
    file.write("trad = 40.d3\n")
    file.write("xlogg = 3.6d0\n")
    file.write("rstar = 20.015520723398144d0 \n")
    file.write("rmax = 5.9895d0 \n")
    file.write("tmin = 1.d0\n")
    file.write("xmloss = 2.d-6\n")
    file.write("vmin = 1.d0\n")
    file.write("vmax = 2.8d3\n")
    file.write("vmicro = " + vmicro_str + "\n")
    file.write("vth_fiducial = 1.d2\n")
    file.write("vrot = 0.d0\n")
    file.write("beta = 1.d0\n")
    file.write("yhe = .1d0\n")
    file.write("hei = 2.d0\n")
    file.write("xnue0 = 1.93798d15\n")
    file.write("na = 12\n")
    file.write("/\n")
    file.write("\n")
    file.write("&input_infreg\n")
    file.write("rmin = 1.d0\n")
    file.write("rlim = 5.9d0\n")
    file.write("/\n")
    file.write("\n")
    file.write("&input_cont\n")
    file.write("eps_cont = 0.d0\n")
    file.write("kcont = " + kcont_str + "\n")
    file.write("/\n")    
    file.write("\n")
    file.write("&input_line\n")
    file.write("eps_line = 0.d0\n")
    file.write("kline = " + kline_str + "\n")
    file.write("kappa0 = 5.d-1\n")
    file.write("alpha = 0.d0 \n")
    file.write("/\n")
    file.write("\n")
    file.write("&dimensions_1d\n")
    file.write("n1d = 27\n")
    file.write("n1d_t = 81\n")
    file.write("n1d_r = 22\n")
    file.write("delv = 0.3333333d0\n")
    file.write("/\n")
    file.write("\n")
    file.write("&dimensions_3d\n")
    file.write("ncx=19\n")
    file.write("ncy=19\n")
    file.write("ncz=19\n")
    file.write("delx_max=0.7d0\n")
    file.write("dely_max=0.7d0\n")
    file.write("delz_max=0.7d0\n")
    file.write("/\n")
    file.write("\n")
    file.write("&dimensions_freq\n")
    file.write("deltax = 0.3333333d0\n")
    file.write("xcmf_max = 3.d0\n")
    file.write("/\n")
    file.write("\n")
    file.write("&dimensions_angles\n")
    file.write("n_theta = 16\n")
    file.write("/\n")
    file.write("\n")
    file.write("&benchmark\n")
    file.write("benchmark_mod = 0\n")
    file.write("im_source = 3\n")
    file.write("im_opacity = 2\n")
    file.write("im_vel = 0\n")
    file.write("tau_min = 0.d0\n")
    file.write("tau_max = 5.d0\n")
    file.write("source_min = 0.1d0\n")
    file.write("source_max = 1.d-6\n")
    file.write("n_y = 0.d0\n")
    file.write("n_z = 0.707107d0\n")
    file.write("/\n")
    file.write("\n")

    file.write("&input_usr\n")
    file.write("fname_model='" + fname_model + "'       ! name of the input models \n")
    file.write("/\n")
    file.write("\n")
    file.write("&test\n")
    file.write("/\n")
    file.write("\n")
    file.write("test")
    file.close()

    print('done')
    print()

def run_model():
    input_file='in_sc3d'
    output_file='output_model.log'
    print('########### calculating model atmosphere ##############')
    print('input_file: ' + input_file)
    print('output_file: ' + output_file)
    command01 = 'model.eo < ' + input_file + ' > ' + output_file
    print(command01)
    os.system(command01)    
    print('done')
    print()
#
def run_sc3d():
    input_file='in_sc3d'
    output_file='output_sc3d.log'
    print('######### calculating solution of source fct ##########')
    print('input_file: ' + input_file)
    print('output_file: ' + output_file)
    command01 = 'sc3d.eo < ' + input_file + ' > ' + output_file
    print(command01)
    os.system(command01)    
    print('done')
    print()
#
def run_modelspec():
    #calculate model-file for final formal solution
    input_file='in_modelspec'
    output_file='output_modelspec.log'
    print('###### calculating model-file for formal solution #####')
    print('input_file: ' + input_file)
    print('output_file: ' + output_file)

    command01 = 'modelspec.eo < ' + input_file + ' > ' + output_file
    print(command01)
    os.system(command01)    
    print('done')
    print()
#
def run_spec():
    #calculate formal solution
    input_file='in_spec'
    output_file='output_spec.log'
    print('############# calculating formal solution #############')
    print('input_file: ' + input_file)
    print('output_file: ' + output_file)
    command01 = 'spec.eo < ' + input_file + ' > ' + output_file
    print(command01)
    os.system(command01)        
    print('done')
    print()
#
#run program
#
#-------------------------------------------------------------------
#
#set indat_*.nml files
vmicro=100.   #10.
kcont=1.0
kline=1.e4
iline=10  #iline=11
opt_method = -1
file_base='./models/florian/qbar2000/'
opt_surface=False
#
#--------------------------------------------
#
for isnap in np.arange(100,101):

    fname_model = file_base + 'ldi{isnap:04d}.h5'.format(isnap=isnap)

    #set the model indat file
    set_indat_model(fname='indat_sc3d_florian.nml',
                    vmicro=vmicro,
                    kcont=kcont,
                    kline=kline,
                    opt_method=opt_method,
                    fname_model=fname_model)
    
    #run the model
    run_model()

    #run the ALI scheme
    run_sc3d()



    #set the indat file for modelspec.eo
    set_indat_modelspec(fname='indat_modelspec_florian.nml',
                        kcont=kcont,
                        kline=kline,
                        vmicro=vmicro,
                        iline=iline)

#    run_modelspec()
    #
    #set the indat file for spec.eo
    set_indat_spec(fname='indat_spec_florian.nml',
                   vmicro=vmicro,
                   opt_surface=opt_surface)

    #calculate opacities, etc. and run the formal solution
    run_spec()

    #copy everything to an appropriate directory
#    dir_out='/lhome/levin/Postdoc/papers/paperIV/models/WR_3D_alpha_LTE_longbox/snap{isnap:}_heII4686_vmicro1d2_sresol'.format(isnap=isnap)
    dir_out='/STER/levin/models_florian/model_ken_0G_highres/kline1d4/vmicro1d2/snap{isnap:04d}'.format(isnap=isnap)
#    dir_out='/lhome/levin/Postdoc/TRASH/florian'
    copy_to_directory(dir_out)