def save_netcdf_fields(x, y, u, v, time, seed, slope, alpha, output):

    if time == None:
        time = datetime.datetime(1989, 8, 12)

    Nx, Ny, Nt = len(x), len(y), 1

    nc = Dataset(output, 'w', format='NETCDF4')

    time_units = 'hours since 1900-01-01 00:00:00'
    calendar = 'julian'

    input_vars = {}
    input_vars['u'] = {}
    input_vars['u']['units'] = 'm/s'
    input_vars['u']['long_name'] = 'eastward surface velocity'
    #input_vars['u']['scale_factor'] = 0.00001

    input_vars['v'] = {}
    input_vars['v']['units'] = 'm/s'
    input_vars['v']['long_name'] = 'northward surface velocity'
    #input_vars['v']['scale_factor'] = 0.00001

    time_dim = nc.createDimension('time', Nt)
    x_dim = nc.createDimension('x', Nx)
    y_dim = nc.createDimension('y', Ny)

    vars={}
    vars['time'] = nc.createVariable('time', '<f4', ('time',))
    vars['x'] = nc.createVariable('x', '<f4', ('x',))
    vars['y'] = nc.createVariable('y', '<f4', ('y',))


    vars_att = ['units', 'long_name']
    #vars_att = ['units', 'long_name', 'scale_factor']
    for var in input_vars.keys():
        vars[var] = nc.createVariable(var,'<f8' , ('time','y','x'),\
            fill_value=netCDF4.default_fillvals['f8'])
        for a in vars_att:
            setattr(vars[var], a, input_vars[var][a])

    for var_all in vars.keys():
        vars[var_all].set_auto_maskandscale(True)

    setattr(vars['y'], 'units', 'm')
    setattr(vars['x'], 'units', 'm')

    time_att = {}
    time_att['units'] = time_units
    time_att['calendar'] = calendar

    for a in time_att:
        setattr(vars['time'], a, time_att[a])

    vars['y'][:] = y
    vars['x'][:] = x
    vars['time'][:] = date2num(time, nc.variables['time'].units)
    vars['v'][:] = v
    vars['u'][:] = u

    if seed:
        nc.random_seed = 'random seed for phase generation: %s' %seed
    if slope:
        nc.spectral_slope = 'prescribed spectral slope: %s' %slope
    if alpha:
        nc.divergence_fraction = 'fraction of divergence used for spectral decomposition: %s' %alpha

    nc.close()

