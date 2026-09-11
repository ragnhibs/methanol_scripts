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
    print('Filename:')
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


model_id_list  =  ['OsloCTM3v1-2',
                   'NorESM2-LM-C',
                   'EC-Earth3-AerChem',
                   'EMAC-DLR',
                   'LMDZ-INCA',
                   'CESM2-v212',
                   'GFDL-ESM4-c1',
                   'UKESM1-0-LL']


project_id = 'hyway'
time_range = '*'

member_id_list =  {'OsloCTM3v1-2':'r1',
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r5',
                   'LMDZ-INCA':'r2',
                   'CESM2-v212':'r2',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r1'}



year_period_list = {'EMAC-DLR':[2010,2019],
                    'NorESM2-LM-C':[2010,2019],
                    'LMDZ-INCA':[2010,2019],
                    'OsloCTM3v1-2':[2010,2019],
                    'CESM2-v212':[2010,2019],
                    'UKESM1-0-LL':[2010,2019],
                    'GFDL-ESM4-c1':[2010,2019],
                    'EC-Earth3-AerChem':[2010,2019]}












experiment_id = 'transient2010s'





#Make figure: 
noOfCols = 4
noOfRows = 2
fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(10,14),constrained_layout=True)
axes = axes.flatten()

variable_id = 'ch3oh'

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




read_prev = False

for mod,model_id in enumerate(model_id_list):
    #Model data
    path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/' #+experiment_id +'/'
    member_id = member_id_list[model_id]
    year_period = year_period_list[model_id]
    
    if read_prev:
        model_data_cntr, pfull_cntr = read_vmr_from_netcdf()
    else:
        model_data_cntr, pfull_cntr = read_vmr()

    print(model_data_cntr.mean(dim=['lon']))
    print(pfull_cntr.mean(dim=['lon']))

    #Plot control:
    ax = axes[mod]
    cmap = plt.get_cmap('OrRd')
    plot_zonal(model_data_cntr, pfull_cntr, cminmax_cntr[variable_id])
    ax.set_title( variable_id + ' [' + unit_variable[variable_id] + ']')

 



plt.suptitle(model_id + ' ' + experiment_id)
plt.show()
exit()
