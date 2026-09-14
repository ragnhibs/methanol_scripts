import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm



def plot_map_annual_mean():
    
    #Plot a map:
    mapplot=annual_mean_emis_diff.plot(ax=ax,vmin=levels[0],vmax=levels[-1],cmap=cmap,add_colorbar=False,) #,transform=ccrs.PlateCarree())
    #cbar = mapplot.colorbar
    #cbar.set_ticks(levels)
    #cbar.set_label(variable_id + ' [' +unit[variable_id] + ']')
    ax.set_global()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year
    
    
    totsum = (annual_mean_emis_diff*areaxy).sum()*1e-9*factor
    print(totsum.values)

        
    ax.set_title(model_id + ' ' + title + ', annual mean:'+'{:5.2f}'.format(totsum.values) + '  [Tg yr$^{-1}$] ')
    ax.coastlines()

    return mapplot


#Plot diff
experiment_id = 'ch3ohpert'
experiment_id_cntr = 'cntr'

variable_id = 'emich3oh'

unit = {'emich3oh':'kg m-2 s-1',
        'emico':'kg m-2 s-1'}

table_id = 'monthly'
project_id = 'hyway'

level_list =  {'emich3oh':np.arange(0,2.2,0.2)*1e-11,
               'emico':np.arange(0,2.2,0.2)*1e-9}

levels = level_list[variable_id]



model_id_list = ['CESM2-v212','LMDZ-INCA', 'OsloCTM3v1-2']

fig,axs = plt.subplots(nrows=1,ncols=3,figsize=(20,5),subplot_kw={'projection': ccrs.PlateCarree()}) 
fig.subplots_adjust(right=0.9)

cmap = plt.get_cmap('BuPu')






year_period_list = {'EMAC-DLR':[2039,2040],
                    'NorESM2-LM-C':[2037,2038],
                    'LMDZ-INCA':[2027,2029],
                    'OsloCTM3v1-2':[2022,2023],
                    'CESM2-v212':[2055,2075],
                    'UKESM1-0-LL':[2010,2014],
                    'GFDL-ESM4-c1':[50,60],
                    'EC-Earth3-AerChem':[2024,2029]}



member_id_list = {'OsloCTM3v1-2':'r2',
                  'EMAC-DLR':'r2',
                  'NorESM2-LM-C':'r1',
                  'LMDZ-INCA':'r1',
                  'CESM2-v212':'r1',
                  'EC-Earth3-AerChem':'r1',
                  'GFDL-ESM4-c1':'r1'}







for m, model_id in enumerate(model_id_list):
    print(model_id)


    year_period = year_period_list[model_id]
    member_id = member_id_list[model_id]


    
    #Read area:
    if model_id =='EMAC-DLR':
        areapath = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
    elif model_id =='CESM2-v212':
        areapath = '/nird/home/ragnhibs/hyway/tmp/'
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
        print(areaxy.sum())



    annual_mean_emis_cntr = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id_cntr+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    annual_mean_emis_pert = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')


    #print(annual_mean_emis_cntr)
    #print(annual_mean_emis_pert)
    annual_mean_emis_diff = annual_mean_emis_pert[variable_id] - annual_mean_emis_cntr[variable_id]
    print(annual_mean_emis_diff)




    if model_id == 'CESM2-v212':
        areaxy['lat'] = annual_mean_emis_diff['lat']

    

    
    title = experiment_id + ' - ' +experiment_id_cntr
    ax = axs[m]
    mapplot = plot_map_annual_mean()





# Add colorbar axis: [left, bottom, width, height]
cax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
cbar = fig.colorbar(mapplot, cax=cax)
cbar.set_ticks(levels)
cbar.set_label(f'{variable_id} [{unit[variable_id]}]')

"""    
cbar = fig.colorbar(mapplot, # use the last mappable returned
                    ax=axs, # all axes
                    orientation='vertical',
                    pad=0.02,
                    shrink=0.9)

cbar.set_ticks(levels)
cbar.set_label(f'{variable_id} [{unit[variable_id]}]')

"""




#plt.tight_layout()
plt.show()
