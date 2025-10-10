import numpy as np

# basic function for calculating masses on each tire
# M = total weight
# weight_dist = weight distribution in % (e.g., 50% you would use 0.50)
# weight_dist is an array: [weight front distribution, rear dist, right dist, left dist]
def calculate_tire_masses(M, weight_dist):
    weight_front = weight_dist[0]
    weight_rear = weight_dist[1]
    weight_right = weight_dist[2]
    weight_left = weight_dist[3]

    wf = M*weight_front
    wr = M*weight_rear
    
    wfl = wf*weight_left
    wfr = wf*weight_right
    wrl = wr*weight_left
    wrr = wr*weight_right

    return [wfl, wfr, wrl, wrr]
