import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm

def plot_emis():
    year_period = year_period_list[model_id]
    
    annual_mean_emis = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    #Plot a map:
    mapplot=annual_mean_emis[variable_id].plot(ax=ax,levels=levels,cmap=cmap)
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    ax.coastlines()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year


    if model_id == 'CESM2-v212':
        areaxy['lat'] = annual_mean_emis.lat 
    totsum = (annual_mean_emis[variable_id]*areaxy).sum()*1e-9*factor
    
        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + ' annual mean [Tg yr$^{-1}$] '+'{:5.2f}'.format(totsum.values))


def plot_surfconc():
    year_period = year_period_list[model_id]
    annual_mean_surf = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    
    #Plot a map:
    mapplot=annual_mean_surf[variable_id].plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    ax.coastlines()
    
    #Mean value for the title
    weighted_surf = annual_mean_surf[variable_id].weighted(areaxy)
    globalmean = weighted_surf.mean()
        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + ' annual mean:{:5.2f}'.format(globalmean.values))
    


    
    
def find_area():
    #Read area:
    if model_id =='EMAC-DLR':
        areapath = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'
    elif model_id == 'EC-Earth3-AerChem':
        areapath =  '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
    else:
        areapath = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'
        
    if model_id == 'CESM2-v212':
        file_area = 'areacella_'+model_id+'_'+project_id +'_transient2010s_'+member_id +'.nc'
        area = xr.open_dataset(areapath + file_area)
        area = area.isel(time=0).drop_vars('time')
        areaxy = area['areacella']
        print(areaxy.sum())
    
    else:
        filename_area = areapath + 'areacella'+'_fixed_'+model_id+'_'+project_id +'.nc'
        data_area = xr.open_dataset(filename_area) 
        areaxy = data_area['areacella']

    return areaxy

comp = 'ch3oh'
#variable_id = 'emich3oh'
#variable_id = 'emico'

unit = {'prodch3oh':'kg m-2 s-1',
        'lossch3oh':'kg m-2 s-1',
        'drych3oh':'kg m-2 s-1',
        'wetch3oh':'kg m-2 s-1',
        'emich3oh':'kg m-2 s-1',
        'emico':'kg m-2 s-1',
        'ch3oh':'ppt'}

unit_scale = {'ppt':1e12,
              'ppb':1e9}



level_list =  {'emich3oh':np.arange(0,2.2,0.2)*1e-10,
               'lossch3oh':np.arange(0,2.2,0.2)*1e-11,
               'drych3oh':np.arange(0,2.2,0.2)*1e-11,
               'wetch3oh':np.arange(0,2.2,0.2)*1e-11,
               'prodch3oh':np.arange(0,2.2,0.2)*1e-11,
               'emico':np.arange(0,2.2,0.2)*1e-9,
               'ch3oh':[0,10,50,100,500,1000,2000,3000,5000,10000,100000]}






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

fig,axs = plt.subplots(nrows=6,ncols=3,figsize=(20,25),subplot_kw={'projection': ccrs.PlateCarree()}) 
cmap = plt.get_cmap('BuPu')

for m,model_id in enumerate(model_id_list):
    member_id = member_id_list[model_id]

    #Model data
    path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id +'/'
                    
    areaxy = find_area()
    
    
    ax = axs[0,m]
    variable_id = 'emi'+comp 
    levels = level_list[variable_id]
    plot_emis()
    
    ax = axs[1,m]
    variable_id = 'prod'+comp 
    levels = level_list[variable_id]
    
    plot_emis()

    ax = axs[2,m]
    variable_id = 'loss'+comp 
    levels = level_list[variable_id]
    plot_emis()

        


    ax = axs[3,m]
    variable_id = 'dry'+comp 
    levels = level_list[variable_id]
    plot_emis()

    ax = axs[4,m]
    variable_id = 'wet'+comp 
    levels = level_list[variable_id]
    plot_emis()

    ax = axs[5,m]
    variable_id = comp
    levels = level_list[variable_id]
    plot_surfconc()

    
plt.tight_layout()
plt.show()
