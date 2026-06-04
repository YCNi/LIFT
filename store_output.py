
import pickle

def store_output(object,name,count):
    path_mean_speed = {}
    for path in object.Paths.values():
        path_mean_speed[path.id] = path.mean_speeds

    link_density = {}
    link_flow = {}
    for link in object.Links.values():
        link_density[link.id] = link.densities
        link_flow[link.id] = link.flows

    with open('path_mean_speed_'+name+repr(count)+'.pickle', 'wb') as handle:
        pickle.dump(path_mean_speed, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('LIFT_density_'+name+'.pickle', 'wb') as handle:
        pickle.dump(link_density, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('LIFT_flow_'+name+'.pickle', 'wb') as handle:
        pickle.dump(link_flow, handle, protocol=pickle.HIGHEST_PROTOCOL)
