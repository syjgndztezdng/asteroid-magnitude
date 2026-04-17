import numpy as np
import matplotlib.pyplot as plt
# import tomllib

#Constants

T_earth = 1 #[years]
a_earth = 1 #[ae]
Solar_constant = 1360.8 #[W / m2]
Solar_magnitude = -26.74 #[m]
AE = 149597870700 #[ae/m]

#Input
#
# with open('parameters.toml', 'rb') as file:
#     config = tomllib.load(file)
#
# a_asteroid = config['a_asteroid']
# T_asteroid = np.sqrt(np.pow(a_asteroid, 3)) #[years]
# start_era = config['start_era']
# albedo = config['albedo']
# D_asteroid = config['D_asteroid']
# number_of_points = config['number_of_points']
# end_time = config['end_time']


a_asteroid = 1.5 #[ae]
T_asteroid = np.sqrt(np.pow(a_asteroid, 3)) #[years]
start_era = 0 #[years]
albedo = 0.25
D_asteroid = 17 #[km]
number_of_points = 100
end_time = 5 #[years]

#Functions

def earth_position(t: float):
    a = ((t / T_earth) % 1) * 2*np.pi # angle from East of Solar System to Sun to Earth contrclockwise [rad]
    
    x = a_earth * np.cos(a)
    y = a_earth * np.sin(a)
    z = 0

    return x, y, z

def asteroid_plane_cirlce_position(t: float):
    a = (((t + start_era) / T_asteroid) % 1) * 2*np.pi

    x = a_asteroid * np.cos(a)
    y = a_asteroid * np.sin(a)
    
    return x, y

def asteroid_plane_experemental_position(t: float):
    x = t - 0.5
    y = t - 0.5
    return x, y

def plane_position_to_space(x_plane: float, y_plane: float):
    x = x_plane
    y = y_plane
    z = 0
    
    return x, y, z

def xyz_distance(state1: list[float],  state2: list[float]) -> float:
    return np.sqrt(np.pow((state1[1] - state2[1]), 2) + np.pow((state1[2] - state2[2]), 2) + np.pow((state1[3] - state2[3]), 2))

def get_phase(state_earth: list[float],  state_asteroid: list[float]) -> float:
    d_sun = xyz_distance([0, 0, 0, 0], state_asteroid) #[ae]
    d_earth = xyz_distance(state_asteroid, state_earth) #[ae]
    r_earth = xyz_distance([0, 0, 0, 0], state_earth) #[ae]

    cos_a = (np.pow(d_earth, 2) + np.pow(d_sun, 2) - np.pow(r_earth, 2)) / (2*d_earth*d_sun)

    return (cos_a + 1) / 2

def get_magnitude(state_earth: list[float],  state_asteroid: list[float]) -> float:
    d_sun = xyz_distance([0, 0, 0, 0], state_asteroid) #[ae]
    d_earth = xyz_distance(state_asteroid, state_earth) #[ae]
    
    E_on_asteroid = Solar_constant / (np.pow(d_sun, 2)) #[W / m2]
    P_on_asteroid = E_on_asteroid * np.pi * np.pow(D_asteroid * 1000, 2) / 4 #[W]
    phase = get_phase(state_earth, state_asteroid)

    E_on_earth = P_on_asteroid * albedo * phase / (4 * np.pi * np.pow(d_earth * AE, 2))

    magnitude = Solar_magnitude + (2.5 * np.log10(Solar_constant / E_on_earth))

    return magnitude


# Script

times = np.linspace(0, end_time, number_of_points)
earth_positions = np.zeros((number_of_points, 4), dtype=float)
asteroid_positions = np.zeros((number_of_points, 4), dtype=float)
magnitudes = np.zeros((number_of_points), dtype=float)

for i in range(number_of_points):
    t = times[i]
    
    x1, y1, z1 = earth_position(t)
    earth_positions[i] = [t, x1, y1, z1]

    x_plane, y_plane = asteroid_plane_cirlce_position(t)

    x2, y2, z2 = plane_position_to_space(x_plane, y_plane)
    asteroid_positions[i] = [t, x2, y2, z2]

    magnitudes[i] = get_magnitude([t, x1, y1, z1], [t, x2, y2, z2])


#Plotting

fig = plt.figure(figsize=(12, 5))

def trajectory_plot():
    trajectory = fig.add_subplot(2, 1, 1, projection='3d')

    earth_x = earth_positions[:, 1]
    earth_y = earth_positions[:, 2]
    earth_z = earth_positions[:, 3]

    asteroid_x = asteroid_positions[:, 1]
    asteroid_y = asteroid_positions[:, 2]
    asteroid_z = asteroid_positions[:, 3]

    trajectory.plot(asteroid_x, asteroid_y, earth_z, color='blue', label='Земля')
    trajectory.plot(earth_x, earth_y, earth_z, color='green', label='Астероид')
    trajectory.scatter(0, 0, 0, color='yellow', s=100, edgecolors='orange')
    trajectory.set_xlabel('X, а.е.')
    trajectory.set_ylabel('Y, а.е.')
    trajectory.set_zlabel('Z, а.е.')
    trajectory.set_title('Траектория тел')
    trajectory.legend()

# trajectory_plot()


magn_plot = fig.add_subplot()
magn_plot.plot(times, magnitudes, label='Блеск астероида')
magn_plot.invert_yaxis()
magn_plot.set_ylabel('Блеск, а.е.')
magn_plot.set_xlabel('Время, а.е.')
magn_plot.set_title('График блеска по времени')
magn_plot.legend()

plt.savefig('plot.png', dpi=500)
plt.show()
