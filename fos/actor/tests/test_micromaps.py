""" An actor to visualize time-depended electrical potential data """

sensor_positions : (N,3)
    Location of the sensor positions
connectivity : (M,3)
    Triangular connectivity of the sensors to make up the surface
    
sampling_frequency :
data : (S, N, T)
    Number of subjects S, for each sensor N, across time duration T
plot_data :
    For each subject and time frame, additional data array
    (e.g. probability for microstate)
    
nr_maps_to_show : int
    The number of maps to show simultaneously for each subject
    
# look for delaunay triangulation of a 2d projected coordinate frame as preprocessing step
