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
    year_period = year_period_list[model_id]

    
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    model_data = xr.open_mfdataset(path + filename)
    print(path+filename)
    
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    elif model_id == 'UKESM1-0-LL':
        file_volume = 'volcella'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    else:
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return
    print(volume_full_path)
    #if model_id == 'EC-Earth3-AerChem':
    #    volume = xr.open_mfdataset(volume_full_path,decode_times=False)
    #else:
    volume = xr.open_mfdataset(volume_full_path)
    
    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        areaxy['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']

    if model_id == 'UKESM1-0-LL':
        volume['volume'] = volume['volcella']

    if model_id ==  'GFDL-ESM4-c1':
        print(model_data)
        volume = volume.rename({'pfull':'lev'})
        #volume = volume.sortby('lev',ascending=False)

        print(volume.lev)
        print(model_data.lev)
        
        model_data['lev'] = volume['lev']
    
    

    field = model_data[variable_id]*volume['volume']
    field = field.sum(dim='lev')/areaxy

    field = field.sel(time=slice(str(year_period[0]).zfill(4),str(year_period[1]).zfill(4)))

    
    #Annual mean, weighted by days in month;
    month_length = field.time.dt.days_in_month
    print(month_length)
    weighted_felt = field.weighted(month_length)
    annual_mean = weighted_felt.mean(dim='time')

    annual_mean.name=variable_id
    annual_mean.to_netcdf('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    #Plot a map:
    mapplot=annual_mean.plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*365.0 #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year
    totsum = (annual_mean*areaxy).sum()*1e-9*factor
    print(totsum.values)


        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + ' annual mean [Tg yr$^{-1}$] '+'{:5.2f}'.format(totsum.values))
    
    
    
    if plot_obs:
        print(obslon)
        exit()
        ax.scatter(obslon,obslat,c=obs,cmap=cmap,vmin=levels.min(),
                   vmax=levels.max(),edgecolors='black',
                   transform=ccrs.PlateCarree())
        
    ax.coastlines()
    
def plot_map_month(month):
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    model_data = xr.open_mfdataset(path + filename)
    print(path+filename)
    
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    elif model_id == 'UKESM1-0-LL':
        file_volume = 'volcella'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    else:
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return
    print(volume_full_path)
    #if model_id == 'EC-Earth3-AerChem':
    #    volume = xr.open_mfdataset(volume_full_path,decode_times=False)
    #else:
    volume = xr.open_mfdataset(volume_full_path)
    
    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']

    if model_id == 'UKESM1-0-LL':
        volume['volume'] = volume['volcella']

    if model_id ==  'GFDL-ESM4-c1':
        print(model_data)
        volume = volume.rename({'pfull':'lev'})
        #volume = volume.sortby('lev',ascending=False)

        print(volume.lev)
        print(model_data.lev)
        
        model_data['lev'] = volume['lev']
    
    

    field = model_data[variable_id]*volume['volume']
    field = field.sum(dim='lev')/areaxy

    field = field.where(field.time.dt.year == year, drop=True)
    #Annual mean, weighted by days in month;
    month_length = field.time.dt.days_in_month
    #print(month_length)
    #weighted_felt = field.weighted(month_length)
    month_field = field.isel(time=month)
    mndlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

        
    #Plot a map:
    mapplot=month_field.plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    
    #Mean value for the title
    #Annual mean:
    factor = 60.*60.*24.0*month_length.isel(time=month).values #kg m-2 s-1-> kg m-2 /year
    #Calculate total sum: kg m-2 /year -> Tg/year
    totsum = (month_field*areaxy).sum()*1e-9*factor
    print(totsum.values)


        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' ' + title + ' ' + mndlist[month] + ' mean [Tg yr$^{-1}$] '+'{:5.2f}'.format(totsum.values))
    


    ax.coastlines()
                



        



#Experiment and simulation infor:
table_id = 'monthly'

#model_id = 'OsloCTM3v1-2'
#model_id = 'EMAC-DLR'
#model_id = 'NorESM2-LM-C'
model_id = 'LMDZ-INCA'
#model_id = 'CESM2-v212'
#model_id = 'EC-Earth3-AerChem'
#model_id = 'GFDL-ESM4-c1'

experiment_id = 'cntr'
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


#variable_id = 'prodch3oh'
variable_id = 'lossch3oh'
#variable_id = 'prodco'


#add_obs()
plot_obs = False


unit = {'prodch3oh':'"kg m-2 s-1',
        'lossch3oh':'"kg m-2 s-1',
        'prodco':'"kg m-2 s-1',
        'lossco':'"kg m-2 s-1'}

#unit_scale = {'ppt':1e12,
#              'ppb':1e9}

level_list =  {'prodch3oh':np.arange(0,10.5,0.5)*1e-12,
               'prodco':np.arange(0,1.05,0.05)*1e-9,
               'lossch3oh':np.arange(0,4.5,0.5)*1e-15,
               'lossco':np.arange(0,5.2,0.2)*1e-14}








levels = level_list[variable_id]


fig,axs = plt.subplots(nrows=2,ncols=1,figsize=(10,10),subplot_kw={'projection': ccrs.PlateCarree()}) 
cmap = plt.get_cmap('BuPu')


ax = axs[0]
plot_map_annual_mean()

plt.show()

