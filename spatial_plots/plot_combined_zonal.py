import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FormatStrFormatter



def plot_zonal(field_3d, pfull_3d, cminmax):
    zonal_mean = field_3d.mean(dim=['lon'],keep_attrs=True)
    zonal_mean_pfull = pfull_3d.mean(dim=['lon'],keep_attrs=True)

    # Extract values as numpy arrays
    lat = zonal_mean.lat.values
    pressure = zonal_mean_pfull.values  # 2D array (lev, lat)
    print(pressure.max(),pressure.min())
    
    data = zonal_mean.values  # 2D array (lev, lat)
    
    # Use matplotlib's pcolormesh directly
    im = ax.pcolormesh(lat, pressure, data, cmap=cmap, norm=LogNorm(vmin=cminmax[0], vmax=cminmax[1]))
    # Add colorbar
    plt.colorbar(im, ax=ax)
    
    #ax.set_yscale('log')
    ax.set_ylim([1000, 10])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_ylabel('Pressure (hPa)')
    #ax.set_xlabel('Latitude')
    ax.set_title('')

    
#Read precaluculated netcdf files:
def read_field_from_netcdf():
    print('Read precalculated netcdf files')
    filename = 'results_netcdf/'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data = xr.open_dataset(filename)
    filename = 'results_netcdf/'+'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data_pfull = xr.open_dataset(filename)
    return model_data[variable_id], model_data_pfull['pfull']




comp = 'ch3oh'
#variable_id = 'emich3oh'
#variable_id = 'emico'

unit_variable = {'prodch3oh':'kg m-3 s-1',
                 'lossch3oh':'kg m-3 s-1',
                 'ch3oh':'ppb'}

unit_scale = {'ppt':1e12,
              'ppb':1e9}




level_list =  {'lossch3oh':np.arange(0,2.2,0.2)*1e-11,
               'prodch3oh':np.arange(0,2.2,0.2)*1e-11,
               'ch3oh':[0,10,50,100,500,1000,2000,3000,5000,10000,100000]}
cminmax =  {'lossch3oh':[1e-18,1e-14],
            'prodch3oh':[1e-18,1e-14],
            'ch3oh':[0.01,10]}
project_id = 'hyway'
table_id = 'monthly'
experiment_id = 'cntr'
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

model_id_list = ['CESM2-v212',
                 'LMDZ-INCA',
                 'OsloCTM3v1-2']

fig,axs = plt.subplots(nrows=3,ncols=3,figsize=(20,25))
cmap = plt.get_cmap('BuPu')

for m,model_id in enumerate(model_id_list):
    member_id = member_id_list[model_id]
    year_period = year_period_list[model_id]
        
    
    
    ax = axs[0,m]
    variable_id = comp
    model_data, pfull = read_field_from_netcdf()
    
    #levels = level_list[variable_id]
    plot_zonal(model_data, pfull,cminmax[variable_id])
    ax.set_title('CNTR '+ model_id + ' ' + 
                  variable_id + ' [' + unit_variable[variable_id] + ']')

    
    ax = axs[1,m]
    variable_id = 'prod'+comp
    model_data, pfull = read_field_from_netcdf()
    #levels = level_list[variable_id]
    
    plot_zonal(model_data, pfull,cminmax[variable_id])
    ax.set_title('CNTR '+ model_id + ' ' + 
                  variable_id + ' [' + unit_variable[variable_id] + ']')
    ax = axs[2,m]
    variable_id = 'loss'+comp
    model_data, pfull = read_field_from_netcdf()
    
    plot_zonal(model_data, pfull,cminmax[variable_id])
    ax.set_title('CNTR '+ model_id + ' ' + 
                  variable_id + ' [' + unit_variable[variable_id] + ']')
     

 
    
plt.tight_layout()
plt.show()
