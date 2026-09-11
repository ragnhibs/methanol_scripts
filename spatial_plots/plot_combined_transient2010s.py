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
    #year_period = year_period_list[model_id]

    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    kg_mg = 1000.0*1000.0
    #Calculate total sum: kg m-2 /year -> Tg/year

    annual_mean_emis = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    #Plot a map:
    unit = 'mg m-2 year-1'
    plottefield = factor*kg_mg*annual_mean_emis[variable_id]
    mapplot=plottefield.plot(ax=ax,levels=levels,cmap=cmap,add_colorbar=False)

    if m == antmod-1:
        cbar = fig.colorbar(mapplot,
                            ax=ax,
                            ticks=levels,
                            label=unit,
                            orientation='vertical',
                            fraction=0.02,
                            pad=0.01)
        #cbar.ax.set_title(unit)
        #if m == antmod -1:
        #    cbar = mapplot.colorbar
        #    cbar.set_ticks(levels)
        #    cbar.set_label(unit)
        #    #cbar.ax.set_title(unit)
    
    ax.set_global()
    ax.coastlines()
    
    
    if model_id == 'CESM2-v212':
        areaxy['lat'] = annual_mean_emis.lat 
    totsum = (annual_mean_emis[variable_id]*areaxy).sum()*1e-9*factor

        
    ax.set_title(variable_id + ' ' + model_id + ' ' + ' \n '+'{:5.2f}'.format(totsum.values)+' Tg yr$^{-1}$ ')


def plot_surfconc():
    #year_period = year_period_list[model_id]
    annual_mean_surf = xr.open_dataset('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    


    #Convert from ppt to ppb:
    annual_mean_surf[variable_id] = annual_mean_surf[variable_id]*0.001
    unit = 'ppb'

    
    #Plot a map:
    mapplot=annual_mean_surf[variable_id].plot(ax=ax,levels=levels,cmap=cmap,add_colorbar=False) #,transform=ccrs.PlateCarree())
    if m == antmod-1:
        cbar = fig.colorbar(mapplot,
                            ax=ax,
                            ticks=levels,
                            label=unit,
                            orientation='vertical',
                            fraction=0.02,
                            pad=0.01)
        #cbar.ax.set_title(unit)
        #cbar = mapplot.colorbar
        #cbar.set_ticks(levels)
        #cbar.set_label(unit)
        #cbar.ax.set_title(unit)
    ax.set_global()
    ax.coastlines()
    
    #Mean value for the title
    weighted_surf = annual_mean_surf[variable_id].weighted(areaxy)
    globalmean = weighted_surf.mean()
        
    ax.set_title(variable_id + ' ' + model_id + '  \n' + '{:5.2f}'.format(globalmean.values) + ' ppb')
    


    
    
def find_area():
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

    return areaxy

comp = 'ch3oh'

unit = {'prodch3oh':'kg m-2 s-1',
        'lossch3oh':'kg m-2 s-1',
        'drych3oh':'kg m-2 s-1',
        'wetch3oh':'kg m-2 s-1',
        'emich3oh':'kg m-2 s-1',
        'emico':'kg m-2 s-1',
        'ch3oh':'ppt'}

unit_scale = {'ppt':1e12,
              'ppb':1e9}



level_list =  {'emich3oh':[0,50,100,150,300,600,900,1200],
               'lossch3oh':[0,25,50,75,100,125,150,200,300,500],
               'drych3oh':[0,25,50,75,100,125,150,200,300,500],
               'wetch3oh':[0,25,50,75,100,125,150,200,300,500],
               'prodch3oh':[0,25,50,75,100,125,150,200,300,500],
               'ch3oh':[0,0.1,1,5,10,20,30,40,50]}






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


fig,axs = plt.subplots(nrows=6,ncols=antmod,figsize=(44,16),subplot_kw={'projection': ccrs.PlateCarree()}) 
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
fig.savefig('Fig/map_transient2010s_plot.png', dpi=300, bbox_inches='tight')
fig.savefig('Fig/map_transient2010s_plot.pdf', bbox_inches='tight')

plt.show()
