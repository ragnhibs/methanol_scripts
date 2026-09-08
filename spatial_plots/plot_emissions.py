import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm

def read_annual_mean():
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    model_data = xr.open_mfdataset(path + filename)
    print(path+filename)
    
    
    #if model_id == 'GFDL-ESM4-c1':
    #    model_data = model_data.rename({variable_id.upper() + '_dvmr':variable_id})

    field = model_data[variable_id].sel(time=slice(str(year_period[0]).zfill(4),str(year_period[1]).zfill(4)))


    #Annual mean, weighted by days in month;
    month_length = field.time.dt.days_in_month
    print(month_length)
    weighted_felt = field.weighted(month_length)
    annual_mean_emis = weighted_felt.mean(dim='time')

    print(annual_mean_emis)
    annual_mean_emis.to_netcdf('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    #Plot a map:
    mapplot=annual_mean_emis.plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year
    totsum = (annual_mean_emis*areaxy).sum()*1e-9*factor
    print(totsum.values)


        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + title + ' annual mean [Tg yr$^{-1}$] '+'{:5.2f}'.format(totsum.values))
    
    

    
def plot_map_annual_mean():
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    model_data = xr.open_mfdataset(path + filename)
    print(path+filename)
    
    
    #if model_id == 'GFDL-ESM4-c1':
    #    model_data = model_data.rename({variable_id.upper() + '_dvmr':variable_id})

    field = model_data[variable_id]

    field = field.where(field.time.dt.year == year, drop=True)
    #Annual mean, weighted by days in month;
    month_length = field.time.dt.days_in_month
    print(month_length)
    weighted_felt = field.weighted(month_length)
    annual_mean_emis = weighted_felt.mean(dim='time')
    
    #Plot a map:
    mapplot=annual_mean_emis.plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year
    totsum = (annual_mean_emis*areaxy).sum()*1e-9*factor
    print(totsum.values)


        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + title + ' annual mean [Tg yr$^{-1}$] '+'{:5.2f}'.format(totsum.values))
    
    
    
    if plot_obs:
        print(obslon)
        exit()
        ax.scatter(obslon,obslat,c=obs,cmap=cmap,vmin=levels.min(),
                   vmax=levels.max(),edgecolors='black',
                   transform=ccrs.PlateCarree())
        
    ax.coastlines()
        
def plot_map_all_months():
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)
    model_data = xr.open_mfdataset(path + filename)

    if model_id == 'GFDL-ESM4-c1':
        model_data = model_data.rename({variable_id.upper() + '_dvmr':variable_id})

    if model_id == 'EMAC-DLR':
        field = model_data[variable_id].isel(lev=-1)*unit_scale[unit[variable_id]]
    elif model_id == 'GFDL-ESM4-c1':
        field = model_data[variable_id].isel(pfull=-1)*unit_scale[unit[variable_id]]
    else:
        field = model_data[variable_id].isel(lev=0)*unit_scale[unit[variable_id]]

    field = field.where(field.time.dt.year == year, drop=True)

    fig,axs = plt.subplots(nrows=4,ncols=3,figsize=(20,15),subplot_kw={'projection': ccrs.PlateCarree()}) 
    cmap = plt.get_cmap('BuPu')

    axs = axs.flatten()
    mndlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for mnd in np.arange(0,12):
        ax = axs[mnd]
        mapplot=field.isel(time=mnd).plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
        cbar = mapplot.colorbar
        cbar.set_ticks(levels)
        ax.set_global()
        #Mean value for the title
        weighted_surf = field.isel(time=mnd).weighted(areaxy)
        globalmean = weighted_surf.mean()
        
        ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + title + ' ' + mndlist[mnd]+ ':{:5.2f}'.format(globalmean.values))
        ax.coastlines()


        



#Experiment and simulation infor:
table_id = 'monthly'

#model_id = 'OsloCTM3v1-2'
#model_id = 'EMAC-DLR'
#model_id = 'NorESM2-LM-C'
#model_id = 'LMDZ-INCA'
model_id = 'CESM2-v212'
#model_id = 'EC-Earth3-AerChem'
#model_id = 'GFDL-ESM4-c1'

experiment_id = 'cntr'

project_id = 'hyway'


year_period_list = {'EMAC-DLR':[2039,2040],
                    'NorESM2-LM-C':[2037,2038],
                    'LMDZ-INCA':[2027,2029],
                    'OsloCTM3v1-2':[2022,2023],
                    'CESM2-v212':[2055,2075],
                    'UKESM1-0-LL':[2010,2014],
                    'GFDL-ESM4-c1':[50,60],
                    'EC-Earth3-AerChem':[2024,2029]}

year_period = year_period_list[model_id]

member_id_list = {'OsloCTM3v1-2':'r2',
                  'EMAC-DLR':'r2',
                  'NorESM2-LM-C':'r1',
                  'LMDZ-INCA':'r1',
                  'CESM2-v212':'r1',
                  'EC-Earth3-AerChem':'r1',
                  'GFDL-ESM4-c1':'r1'}

member_id = member_id_list[model_id]

#Model data
path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id +'/'

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


variable_id = 'emich3oh'
#variable_id = 'emico'


#add_obs()
plot_obs = False


unit = {'emich3oh':'kg m-2 s-1',
        'emico':'kg m-2 s-1'}

#unit_scale = {'ppt':1e12,
#              'ppb':1e9}

level_list =  {'emich3oh':np.arange(0,2.2,0.2)*1e-10,
               'emico':np.arange(0,2.2,0.2)*1e-9}



levels = level_list[variable_id]


fig,axs = plt.subplots(nrows=2,ncols=1,figsize=(10,10),subplot_kw={'projection': ccrs.PlateCarree()}) 
cmap = plt.get_cmap('BuPu')

time_range = '*'

title= model_id
ax = axs[0]
read_annual_mean()


#year = 2015
#title = str(year) #'2015'
#ax = axs[0]
#plot_map_annual_mean()

#year = 2019
#title = str(year)

#time_range = '*'
#ax = axs[1]
#plot_map_annual_mean()

#plot_map_all_months()

plt.show()
#plottfelt.to_netcdf('temp_conc.nc')
