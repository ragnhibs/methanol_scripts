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
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path+filename)
    model_data = xr.open_mfdataset(path + filename)
    
    

    if model_id == 'EMAC-DLR':
        field = model_data[variable_id].isel(lev=-1)*unit_scale[unit[variable_id]]
    else:
        field = model_data[variable_id].isel(lev=0)*unit_scale[unit[variable_id]]
    print(field.time)
    field = field.sel(time=slice(str(year_period[0]).zfill(4),str(year_period[1]).zfill(4)))
    
    #Annual mean, weighted by days in month;
    month_length = field.time.dt.days_in_month
    print(month_length)
    weighted_felt = field.weighted(month_length)
    annual_mean_surf = weighted_felt.mean(dim='time')

    annual_mean_surf.to_netcdf('results_netcdf/annual_mean_' + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    
    
    #Plot a map:
    mapplot=annual_mean_surf.plot(ax=ax,levels=levels,cmap=cmap) #,transform=ccrs.PlateCarree())
    cbar = mapplot.colorbar
    cbar.set_ticks(levels)
    ax.set_global()
    
    #Mean value for the title
    weighted_surf = annual_mean_surf.weighted(areaxy)
    globalmean = weighted_surf.mean()
        
    ax.set_title(variable_id + ' ' + unit[variable_id] + ' ' + model_id + ' annual mean:{:5.2f}'.format(globalmean.values))

                
    ax.coastlines()
        
def plot_map_all_months(ax):
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

    #if plot_obs:
    #    plot_scatter_obs_mod(ax,field,df_obs)
    """    
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

    """
    
def plot_scatter_obs_mod(ax,field,df_obs):
    print('Plotting scatter obs-mod')
    
    #fig, axs = plt.subplots(nrows=1,ncols=1,sharex=False,sharey=False,squeeze=True,figsize=(12,10))
    
    antobs = len(df_obs['Latitude'])
    ctmval = np.zeros((12,antobs))
   
  
    for mnd in range(0,12):
        for k  in range(0,antobs):
            ctmval[mnd,k] =  field.isel(time=mnd).sel(lat=df_obs['Latitude'][k],lon=df_obs['Longitude'][k], method='nearest')

    #Colormap to be used.
    cmap = plt.get_cmap('PuOr')

    mndnr = np.arange(0,12) 
    colorlist = cm.rainbow(np.linspace(0,1, len(mndnr)))
    colorlist = cmap(np.linspace(0,1, len(mndnr)))

    ax.plot([0,600],[0,600],color='gray')
    mndlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for mnd in range(0,12):
        obsval = np.zeros(antobs)
        modval = np.zeros(antobs)
        obsval[:] = df_obs[mndlist[mnd]].values
        modval[:] = ctmval[mnd,:]
        df = pd.DataFrame(data=np.array([obsval,modval]).T,columns=['obs','mod'])
        r = df.corr(method='pearson', min_periods=1)
        r2 = r['mod'].loc['obs']
    
        ax.scatter(obsval,modval,s=2, color=colorlist[mnd],label=mndlist[mnd]+ ' ' + f"{r2:2.4f}")
    
    ax.legend()
    ax.set_xlim(0,700)
    ax.set_ylim(0,700)

    ax.set_xlabel('Observed CO')
    ax.set_ylabel('Modelled CO')
    ax.set_title(model_id + ' Obs - mod. [month]')


    
#Experiment and simulation infor:
table_id = 'monthly'
#experiment_id = 'cntr'
experiment_id = 'transient2010s'

project_id = 'hyway'

if experiment_id == 'cntr':


    model_id_list = [#'OsloCTM3v1-2',
                     #'LMDZ-INCA',
                     'CESM2-v212']#,
 

    member_id_list = {'OsloCTM3v1-2':'r2',
                      'EMAC-DLR':'r2',
                      'NorESM2-LM-C':'r1',
                      'LMDZ-INCA':'r1',
                      'CESM2-v212':'r1',
                      'EC-Earth3-AerChem':'r1',
                      'GFDL-ESM4-c1':'r1'}



    year_period_list = {'EMAC-DLR':[2039,2040],
                        'NorESM2-LM-C':[2037,2038],
                        'LMDZ-INCA':[2027,2029],
                        'OsloCTM3v1-2':[2022,2023],
                        'CESM2-v212':[2055,2075],
                        'UKESM1-0-LL':[2010,2014],
                        'GFDL-ESM4-c1':[50,60],
                        'EC-Earth3-AerChem':[2024,2029]}

elif experiment_id == 'transient2010s':
    
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
    
    year_period_list = {'EMAC-DLR':[2010,2019],
                        'NorESM2-LM-C':[2010,2019],
                        'LMDZ-INCA':[2010,2019],
                        'OsloCTM3v1-2':[2010,2019],
                        'CESM2-v212':[2010,2019],
                        'UKESM1-0-LL':[2010,2019],
                        'GFDL-ESM4-c1':[2010,2019],
                        'EC-Earth3-AerChem':[2010,2019]}
else:
    print('Not set up')
    exit()


    
variable_id = 'ch3oh'
#variable_id = 'co'


unit = {'ch3oh':'ppt',
        'co':'ppb'}

unit_scale = {'ppt':1e12,
              'ppb':1e9}

level_list =  {'ch3oh':[0,10,50,100,500,1000,2000,3000,5000,10000,100000],
               'co':np.arange(0,220,20)}

levels = level_list[variable_id]

fig,axs = plt.subplots(nrows=2,ncols=4,figsize=(23,8),subplot_kw={'projection': ccrs.PlateCarree()},constrained_layout=True)
fig2,axs2 = plt.subplots(nrows=2,ncols=4,figsize=(23,8),constrained_layout=True)

cmap = plt.get_cmap('BuPu')
axs = axs.flatten()
axs2 = axs2.flatten()

time_range = '*'
#year = 2019
#yrstr = str(year)

    
for mod, model_id in enumerate(model_id_list):
    member_id = member_id_list[model_id]

    #Model data
    path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id +'/'

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
        print(areaxy)
    
    else:
        filename_area = areapath + 'areacella'+'_fixed_'+model_id+'_'+project_id +'.nc'
        data_area = xr.open_dataset(filename_area) 
        areaxy = data_area['areacella']
    
    year_period = year_period_list[model_id]
    ax = axs[mod]
    plot_map_annual_mean()

    #ax = axs2[mod]
    
    
    #plot_map_all_months(ax)

plt.show()
#plottfelt.to_netcdf('temp_conc.nc')
