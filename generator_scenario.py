import pickle
import numpy as np
from scipy.stats import norm
from numpy.random import multivariate_normal


def generate_scenarios(num_activities, num_scenarios, correlation_matrix, distribution_dict, out_location, out_name):
    """Generates scenarios based on activities and correlation matrix
    
    Parameters
    ----------
    num_activities : int
       Number of activities
    num_scenarios : int
       Number of scenarions to generate
    correlation_matrix : numpy.ndarray
       Correlation matrix
    distribution_dict : dictionary
       Dictionary with nodes as keys and values the corresponding
       beta distribution of activity times
       
    Returns
    ----------
    N/A
    """   
    # Generate samples via Gaussian Copula
    mean = np.zeros(num_activities)    
    B = norm.cdf(multivariate_normal(mean,
                                     correlation_matrix,
                                     size=num_scenarios,
                                     check_valid='raise'))
    S = np.array(())
    k_list = []
    
    for i in range(num_activities):
        k = np.array(distribution_dict[i + 1].ppf(B[:, i]))
        k_list.append(k)
    
    # Start node duration = 0
    S = np.zeros(num_scenarios)
    
    # End node duration = 0
    k_list.append(np.zeros(num_scenarios))
    
    for k in k_list:
        S = np.column_stack((S, k))
    
    # Save generated scenarios in a file
    file_name = out_location + out_name + '.pkl'
    output_file = open(file_name, 'wb+')
    pickle.dump(S, output_file)
    output_file.close()

    return



def dynamic_samples(num_activities, num_scenarios, correlation_matrix, distribution_dict):
    """Generates samples based on activities and correlation matrix
    
    Parameters
    ----------
    num_activities : int
       Number of activities
    num_scenarios : int
       Number of scenarios to generate
    correlation_matrix : numpy.ndarray
       Correlation matrix
    distribution_dict : dictionary
       Dictionary with nodes as keys and values the corresponding
       beta distribution of activity times
       
    Returns
    ----------
    S : numpy.ndarray
       Numpy array with samples (columns=actiivities, rows=samples)
    """
    # Generate samples via Gaussian Copula
    mean = np.zeros(num_activities)    
    B = norm.cdf(multivariate_normal(mean,
                                     correlation_matrix,
                                     size=num_scenarios,
                                     check_valid='raise'))
    S = np.array(())
    k_list = []
    
    for i in range(num_activities):
        k = np.array(distribution_dict[i + 1].ppf(B[:, i]))
        k_list.append(k)
    
    # Start node duration = 0
    S = np.zeros(num_scenarios)
    
    # End node duration = 0
    k_list.append(np.zeros(num_scenarios))
    
    for k in k_list:
        S = np.column_stack((S, k))
    
    return S


