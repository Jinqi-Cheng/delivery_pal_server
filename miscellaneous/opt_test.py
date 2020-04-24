"""
Create Date , 
@author: 
"""
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sko.GA import GA_TSP
from sko.SA import SA_TSP
from sko.ACA import ACA_TSP
num_points = 50

points_coordinate = np.random.rand(num_points, 2)  # generate coordinate of points
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
print(distance_matrix)
print(type(distance_matrix))

def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    # print(distance_matrix)
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])
from sko.GA import GA_TSP

ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
best_points, best_distance = ga_tsp.run()

# from sko.IA import IA_TSP
#
# ia_tsp = IA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=500, max_iter=800, prob_mut=0.2,
#                 T=0.7, alpha=0.95)
# best_points, best_distance = ia_tsp.run()
print('best routine:', best_points, 'best_distance:', best_distance)

print(best_points)
print(best_points[0])
fig, ax = plt.subplots(1, 2)
best_points_ = np.concatenate([best_points, [best_points[0]]])
best_points_coordinate = points_coordinate[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
ax[1].plot(ga_tsp.generation_best_Y)
plt.show()