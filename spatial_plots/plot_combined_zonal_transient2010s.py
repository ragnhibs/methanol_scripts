import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FormatStrFormatter



def plot_zonal(field_3d, pfull_3d, cminmax,unit):
    zonal_mean = field_3d.mean(dim=['lon'],keep_attrs=True)
    zonal_mean_pfull = pfull_3d.mean(dim=['lon'],keep_attrs=True)

    # Extract values as numpy arrays
    lat = zonal_mean.lat.values
    pressure = zonal_mean_pfull.values  # 2D array (lev, lat)
    print(pressure.max(),pressure.min())
    
    data = zonal_mean.values  # 2D array (lev, lat)
    
    # Use matplotlib's pcolormesh directly
    #im = ax.pcolormesh(lat, pressure, data, cmap=cmap, norm=LogNorm(vmin=cminmax[0], vmax=cminmax[1]))
    im = ax.pcolormesh(lat, pressure, data, cmap=cmap, vmin=cminmax[0], vmax=cminmax[1])

    if m == antmod-1:
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.set_title(unit)
        #cbar.ax.set_label(unit)
    #ax.set_yscale('log')
    ax.set_ylim([1000, 10])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_ylabel('Pressure (hPa)')
    ax.set_xlabel('Latitude')
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



sec_per_year = 365 * 24 * 60 * 60
kg_mg = 1000.0*1000.0
unit_variable = {'prodch3oh':'mg m-3 yr-1',
                 'lossch3oh':'mg m-3 yr-1',
                 'ch3oh':'ppb'}



#level_list =  {'lossch3oh':np.arange(0,2.2,0.2)*1e-11,
#               'prodch3oh':np.arange(0,2.2,0.2)*1e-11,
#               'ch3oh':[0,10,50,100,500,1000,2000,3000,5000,10000,100000]}

cminmax =  {'lossch3oh':[0,0.1],
            'prodch3oh':[0,0.1],
            'ch3oh':[0,1.5]}


project_id = 'hyway'
table_id = 'monthly'
experiment_id = 'transient2010s'
year_period = [2010,2019]

member_id_list =  {'OsloCTM3v1-2':'r1',
                       'NorESM2-LM-C':'r1',
                       'EC-Earth3-AerChem':'r1',
                       'EMAC-DLR':'r5',
                       'LMDZ-INCA':'r2',
                       'CESM2-v212':'r2',
                       'GFDL-ESM4-c1':'r1',
                       'UKESM1-0-LL':'r1'}


model_id_list = ['OsloCTM3v1-2',
                  'NorESM2-LM-C',
                  'EC-Earth3-AerChem',
                  'EMAC-DLR',
                  'LMDZ-INCA',
                  'CESM2-v212',
                  'GFDL-ESM4-c1',
                  'UKESM1-0-LL']
antmod = len(model_id_list)
model_id_list.sort()

fig,axs = plt.subplots(nrows=3,ncols=antmod,figsize=(25,15))
cmap = plt.get_cmap('BuPu')

for m,model_id in enumerate(model_id_list):
    member_id = member_id_list[model_id]
    #year_period = year_period_list[model_id]
        
    
    
    ax = axs[0,m]
    variable_id = comp
    model_data, pfull = read_field_from_netcdf()
    
    #levels = level_list[variable_id]
    plot_zonal(model_data, pfull,cminmax[variable_id],unit_variable[variable_id])
    ax.set_title( model_id + '\n' + 
                  variable_id )

    
    ax = axs[1,m]
    variable_id = 'prod'+comp
    model_data, pfull = read_field_from_netcdf()
    #levels = level_list[variable_id]


   
    

    
    plot_zonal(model_data*sec_per_year*kg_mg, pfull,cminmax[variable_id],unit_variable[variable_id])
    ax.set_title( model_id + '\n' + 
                  variable_id )
    ax = axs[2,m]
    variable_id = 'loss'+comp
    model_data, pfull = read_field_from_netcdf()
    
    plot_zonal(model_data*sec_per_year*kg_mg, pfull,cminmax[variable_id],unit_variable[variable_id])
    ax.set_title( model_id + '\n' + 
                  variable_id )
     
    
        

fig.tight_layout()
fig.savefig('Fig/zonal_plot_transient2010s.png', dpi=300, bbox_inches='tight')
fig.savefig('Fig/zonal_plot_transient2010s.pdf', bbox_inches='tight')

plt.tight_layout()
plt.show()
