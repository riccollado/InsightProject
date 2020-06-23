import time
import stochastic

def optimize(problem, method, seeds=None):
    """
    Commits problem to db and the branch & bound method
    
    Parameters
    ----------
    problem : 
    
    method : 
    
    Returns
    ----------
    N/A
    """

    # Initialize attributes
    attributes = stochastic.initialize_attributes(problem, method)
    
    # Here we'll have code to push the attributes into the database.
    # This will be the table holding the problem description.
    #
    # From tis we get experiment_id
    #
    #
    #
    #------------------------------------------------------------------
    
    #DEBUG: we will get this from the database
    experiment_id = 0
    
    # Run SB&B algorithm
    start_time = time.clock()
    solution = stochastic.branch_bound_algorithm(attributes, experiment_id)
    elapsed_time = time.clock() - start_time
    
    # Here we'll have code to push the solution into the database.
    # This will be the table holding the problem solution
    #
    #
    #
    #------------------------------------------------------------------    

    return
