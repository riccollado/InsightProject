from generator_network import generate_network
from generator_corr_mat import generate_corr_mat
from generator_distribution import generate_geometrics
from generator_distribution import generate_betas
from generator_scenario import generate_scenarios
from generator_crash import generate_crash_times
from generator_crash import generate_crash_cost

def generate_infrastructure(no_of_nodes,
                            no_of_layers,
                            no_of_scenarios,
                            out_location,
                            project_file_name,
                            scenarios_file_name,
                            crashtime_file_name,
                            crashcost_file_name):
    """Generates problem infrastructure (netwoork, corr. matrix, activity distributions, 
    geometric probabilities, scenarios, crash times and costs)
    
    Parameters
    ----------
    no_of_nodes : int
       Number of nodes (activities) in the network
    no_of_layers : int
       Number of layers in the network skeleton
    activities : dictionary
       Probabilities for Geometric distributions used to
       select the activities' Beta distributions
    no_of_scenarios : int
       Number of scenarios
    
    Returns
    ----------
    N/A       
    """
    
    # Generate a network
    project_network = generate_network(no_of_nodes, no_of_layers, out_location, project_file_name)
    
    # Generate a correlation Matrix
    M = generate_corr_mat(no_of_nodes)
    
    # Generate geometric probabilities
    geom_prob = generate_geometrics(no_of_nodes, out_location)
    
    # Generate beta distributions of activity times
    distribution_dict = generate_betas(project_network, geom_prob, out_location)
    
    # Generate scenarios
    generate_scenarios(no_of_nodes, no_of_scenarios, M, distribution_dict, out_location, scenarios_file_name)
    
    # Generate crash times
    generate_crash_times(no_of_nodes, out_location, crashtime_file_name)
    
    # Generate crash costs
    generate_crash_cost(no_of_nodes, out_location, crashcost_file_name)
    
    return
