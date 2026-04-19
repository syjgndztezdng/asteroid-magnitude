import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
import tomllib

#Constants

T_earth = 1 #[years]
a_earth = 1 #[ae]
Solar_constant = 1360.8 #[W / m2]
Solar_magnitude = -26.74 #[m]
AE = 149597870700 #[ae/m]

#Input

with open('parameters.toml', 'rb') as file:
    config = tomllib.load(file)

a_asteroid = config['a_asteroid']
T_asteroid = np.sqrt(np.pow(a_asteroid, 3)) #[years]
start_era = config['start_era']
albedo = config['albedo']
D_asteroid = config['D_asteroid']
number_of_points = config['number_of_points']
end_time = config['end_time']
i = config['i']
latitude = config['latitude']
peri_arg = config['peri_arg']

#Orbit
# a_asteroid = 0.72 #[ae]
# T_asteroid = np.sqrt(np.pow(a_asteroid, 3)) #[years]
# i = np.pi / 6 #[rad] наклон от эклиптики
# latitude = 0 #[rad] омега большая, долгота восх. узла
# peri_arg = 0 #[rad] аргумент перицентра
#
# start_era = 0 #[years]
#
# #Body
# albedo = 0.75
# D_asteroid = 12000 #[km]
#
# #Simulation
# number_of_points = 1000
# end_time = 20 #[years]

#Functions

def earth_position(t: float):
    a = ((t / T_earth) % 1) * 2*np.pi # angle from East of Solar System to Sun to Earth contrclockwise [rad]
    
    x = a_earth * np.cos(a)
    y = a_earth * np.sin(a)
    z = 0

    return np.array([x, y, z])

def asteroid_plane_cirlce_position(t: float):
    a = (((t + start_era) / T_asteroid) % 1) * 2*np.pi

    x = a_asteroid * np.cos(a)
    y = a_asteroid * np.sin(a)
    
    return np.array([x, y])

def asteroid_plane_experemental_position(t: float):
    x = t - 0.5
    y = t - 0.5
    return x, y

def plane_position_to_space(xy: np.ndarray):
    xyz = trans_matrix @ np.array([xy[0], xy[1], 0])
    
    return np.array(xyz).flatten()

def xyz_distance(state1: np.ndarray | list[float],  state2: np.ndarray | list[float]) -> float:
    return np.sqrt(np.pow((state1[0] - state2[0]), 2) + np.pow((state1[1] - state2[1]), 2) + np.pow((state1[2] - state2[2]), 2))

def get_phase(state_earth: np.ndarray,  state_asteroid: np.ndarray) -> float:
    d_sun = xyz_distance([0, 0, 0, 0], state_asteroid) #[ae]
    d_earth = xyz_distance(state_asteroid, state_earth) #[ae]
    r_earth = xyz_distance([0, 0, 0, 0], state_earth) #[ae]

    cos_a = (np.pow(d_earth, 2) + np.pow(d_sun, 2) - np.pow(r_earth, 2)) / (2*d_earth*d_sun)
    alpha = np.arccos(cos_a)

    phase = (np.sin(alpha) + (np.pi - alpha) * np.cos(alpha)) / np.pi

    return phase

def get_magnitude(state_earth: np.ndarray, state_asteroid: np.ndarray) -> float:
    d_sun = xyz_distance([0, 0, 0, 0], state_asteroid) #[ae]
    d_earth = xyz_distance(state_asteroid, state_earth) #[ae]
    
    E_on_asteroid = Solar_constant / (np.pow(d_sun, 2)) #[W / m2]
    P_on_asteroid = E_on_asteroid * np.pi * np.pow(D_asteroid * 1000, 2) / 4 #[W]
    phase = get_phase(state_earth, state_asteroid)

    E_on_earth = P_on_asteroid * albedo * phase / (4 * np.pi * np.pow(d_earth * AE, 2)) + 1e-9 #[W / m2]


    magnitude = -2.5 * np.log10(E_on_earth) - 21.1 #[m]

    return magnitude


# Script

M = latitude
m = peri_arg

trans_matrix = np.matrix([[cos(M)*cos(m) - sin(M)*sin(m)*cos(i), -cos(M)*sin(m)-sin(M)*cos(i)*cos(m), sin(M)*sin(i)],
                          [sin(M)*cos(m) + cos(M)*cos(i)*sin(m), -sin(M)*sin(m)+cos(M)*cos(i)*cos(m), -cos(M)*sin(i)],
                          [sin(i)*sin(m),                        sin(i)*cos(m),                       cos(i)]])


times = np.linspace(0, end_time, number_of_points)
earth_positions = np.zeros((number_of_points, 4), dtype=float)
asteroid_positions = np.zeros((number_of_points, 4), dtype=float)
magnitudes = np.zeros((number_of_points), dtype=float)

for i in range(number_of_points):
    t = times[i]
    
    earth_r = earth_position(t)
    earth_positions[i] = np.array([earth_r[0], earth_r[1], earth_r[2], t])

    asteroid_xy = asteroid_plane_cirlce_position(t)

    asteroid_r = plane_position_to_space(asteroid_xy)

    asteroid_positions[i] = np.array([asteroid_r[0], asteroid_r[1], asteroid_r[2], t])
    

    magnitudes[i] = get_magnitude(earth_positions[i], asteroid_positions[i])


#Plotting

fig = plt.figure(figsize=(12, 5))

def trajectory_plot():
    trajectory = fig.add_subplot(2, 1, 1, projection='3d')

    earth_x = earth_positions[:, 0]
    earth_y = earth_positions[:, 1]
    earth_z = earth_positions[:, 2]

    asteroid_x = asteroid_positions[:, 0]
    asteroid_y = asteroid_positions[:, 1]
    asteroid_z = asteroid_positions[:, 2]

    trajectory.plot(asteroid_x, asteroid_y, asteroid_z, color='blue', label='Астероид')
    trajectory.plot(earth_x, earth_y, earth_z, color='green', label='Земля')
    trajectory.scatter(0, 0, 0, color='yellow', s=100, edgecolors='orange')
    trajectory.axis('equal')
    trajectory.set_xlabel('X, а.е.')
    trajectory.set_ylabel('Y, а.е.')
    trajectory.set_zlabel('Z, а.е.')
    trajectory.set_title('Траектория тел')
    trajectory.legend()

trajectory_plot()


magn_plot = fig.add_subplot(2, 1, 2)
magn_plot.plot(times, magnitudes, label='Блеск астероида')
magn_plot.invert_yaxis()
magn_plot.set_ylabel('Блеск, зв. величины')
magn_plot.set_xlabel('Время, а.е.')
magn_plot.set_title('График блеска по времени')
magn_plot.legend()

plt.savefig('plot.png', dpi=500)
plt.show()
