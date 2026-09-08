import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)



def plot_zonal(field_3d, pfull_3d, cminmax):
    zonal_mean = field_3d.mean(dim=['lon'],keep_attrs=True)
    zonal_mean_pfull = pfull_3d.mean(dim=['lon'],keep_attrs=True)

    # Extract values as numpy arrays
    lat = zonal_mean.lat.values
    pressure = zonal_mean_pfull.values  # 2D array (lev, lat)
    print(pressure.max(),pressure.min())
    
    data = zonal_mean.values  # 2D array (lev, lat)
    
    # Use matplotlib's pcolormesh directly
    im = ax.pcolormesh(lat, pressure, data, cmap=cmap, vmin=cminmax[0], vmax=cminmax[1])
    # Add colorbar
    plt.colorbar(im, ax=ax)
    
    ax.set_yscale('log')
    ax.set_ylim([1000, 10])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_ylabel('Pressure (hPa)')
    ax.set_xlabel('Latitude')
    ax.set_title('')


def read_vmr():
    filename = path +'/'+experiment_id+'/'+ variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    print(filename)
    #Read variable:
    model_data = xr.open_mfdataset(filename).sel(time=slice(str(year_period[0]),str(year_period[1])))
    print(model_data.time)

    model_field = model_data[variable_id].mean(dim='time')*unit_fact[unit_variable[variable_id]]   

    #Pressure:
    filename = path +'/'+experiment_id+'/'+ 'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    #Read variable:
    model_data = xr.open_mfdataset(filename).sel(time=slice(str(year_period[0]),str(year_period[1])))
    print(model_data.time)

    pressure_field = model_data['pfull'].mean(dim='time')*0.01 #Convert from Pa to hPa

    model_field.to_netcdf('results_netcdf/'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' 
                          +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    pressure_field.to_netcdf('results_netcdf/'+'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'
                             +str(year_period[0])+'_'+str(year_period[1])+'.nc')

    return model_field, pressure_field

#Read precaluculated netcdf files:
def read_vmr_from_netcdf():
    print('Read precalculated netcdf files')
    filename = 'results_netcdf/'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data = xr.open_dataset(filename)
    filename = 'results_netcdf/'+'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data_pfull = xr.open_dataset(filename)
    return model_data[variable_id], model_data_pfull['pfull']


#Experiment and simulation infor:
table_id = 'monthly'

#model_id = 'OsloCTM3v1-2'
#model_id = 'EMAC-DLR'
#model_id = 'NorESM2-LM-C'
model_id = 'LMDZ-INCA'
#model_id = 'CESM2-v212'
#model_id = 'EC-Earth3-AerChem'
#model_id = 'GFDL-ESM4-c1'


project_id = 'hyway'
time_range = '*'

year_period_list = {'LMDZ-INCA':[2027,2029],
                    'OsloCTM3v1-2':[2022,2023],
                    'CESM2-v212':[2055,2075]}

member_id_list = {'OsloCTM3v1-2':'r2',
                  'EMAC-DLR':'r2',
                  'NorESM2-LM-C':'r1',
                  'LMDZ-INCA':'r1',
                  'CESM2-v212':'r1',
                  'EC-Earth3-AerChem':'r1',
                  'GFDL-ESM4-c1':'r1'}

member_id = member_id_list[model_id]

#Model data
path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/' #+experiment_id +'/'



experiment_id_list = ['ch3ohpert'] #,
#experiment_id_list = ['h2pert','ch4pert']   

#Experiment and simulation infor:

experiment_id = 'cntr'

variable_id = 'ch3oh'
#variable_id = 'h2'





#Make figure: 
noOfCols = 3
noOfRows = 6
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(10,14),constrained_layout=True)


var_list = ['ch3oh','ch4','hcho','o3','oh','h2o']

cminmax_rel = {'ch3oh':[-10,10],
               'ch4':[-1,1],
               'hcho':[-1,1],
               'o3':[-0.15,0.15],
               'oh':[-0.25,0.25],
               'h2o':[-0.0025,0.0025]}

cminmax_abs = {'ch3oh':[-0.1,0.1],
               'ch4':[-1,1],
               'hcho':[-1,1],
               'o3':[-0.2,0.2],
               'oh':[-0.0025,0.0025],
               'h2o':[-0.25,0.25]}

cminmax_cntr = {'ch3oh':[0,1],
                'ch4':[0,3000],
               'hcho':[0,200],
               'o3':[0,100],
               'oh':[0,0.25],
               'h2o':[0,4000]}

unit_variable = {'ch3oh':'ppb',
                 'ch4':'ppb',
                 'hcho':'ppt',
                 'o3':'ppb',
                 'oh':'ppt',
                 'h2o':'ppb'}

unit_fact = {'ppb':1e9,
             'ppt':1e12,
             'vmr':1}


#variable_id = 'ch3oh'

read_prev = False

for v,variable_id in enumerate(var_list):

    year_period = year_period_list[model_id]
    experiment_id = 'cntr'
    if read_prev:
        model_data_cntr, pfull_cntr = read_vmr_from_netcdf()
    else:
        model_data_cntr, pfull_cntr = read_vmr()

    print(model_data_cntr.mean(dim=['lon']))
    print(pfull_cntr.mean(dim=['lon']))

    #Plot control:
    ax = axes[v,0]
    cmap = plt.get_cmap('OrRd')
    plot_zonal(model_data_cntr, pfull_cntr, cminmax_cntr[variable_id])
    ax.set_title('CNTR ' + variable_id + ' [' + unit_variable[variable_id] + ']')

    #Plot absolute difference:
    experiment_id = experiment_id_list[0]
    
    if read_prev:
        model_data_pert, pfull_pert = read_vmr_from_netcdf()
    else:
        model_data_pert, pfull_pert = read_vmr()
    
    ax = axes[v,1]
    cmap = plt.get_cmap('seismic')
    plot_zonal(model_data_pert-model_data_cntr, pfull_cntr, cminmax_abs[variable_id])
    ax.set_title(experiment_id + ' - CNTR')
    ax.set_title('Absolute diff. ' +variable_id+ ' [' + unit_variable[variable_id] + ']')


    #Plot relative difference:
    ax = axes[v,2]
    plot_zonal((model_data_pert-model_data_cntr)/model_data_cntr*100.0, pfull_cntr, cminmax_rel[variable_id])
    ax.set_title('Relative diff. ' +variable_id+ ' [%]')
    


plt.suptitle(model_id + ' ' + experiment_id_list[0]   +' rel to  '+ 'cntr') 
plt.show()
exit()
