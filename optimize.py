import pickle
import time
import sqlite3
import random
import SBB
import generator_infrastructure
import numpy as np
import multiprocessing as mp

def optimize(pool, method, bootstrap=True):
    """
    Sets main problem parameters, loads data, and starts the optimization
    
    Parameters
    ----------
    pool : multiprocessing.pool.Pool
      Parallel pool to execute the main process
    
    method : str
       String stating the desired sample node selection method:
          KG (Knowledge Gradient with Correated Beliefs)
          Random_1
          Random
          Uniform
          Distance
          Pareto_Inverse
          Pareto_Boltzman
    
    bootstrap : binary
       State for adding bootstrap to the SB&B
    
    Returns
    ----------
    N/A
    """

    # Location for pickle and result files
    out_location = "RUNS/"
    conn = sqlite3.connect(out_location + "DB/" + "Results.db")

    # Project network pickle file
    project_file_name = "ProjectNetwork"

    # Scenarios pickle file
    scenarios_file_name = "Scenarios"

    # Crash times pickle file
    crashtime_file_name = "crashtime"

    # Crash costs pickle file
    crashcost_file_name = "crashcost"
    
    # Number of network nodes excluding start and stop
    no_of_nodes = 100

    # Number of network skeleton layers excluding start and stop layers
    no_of_layers = 8

    # Number of scenarios to be used for estimation at each B&B iteration
    # (must be >= 10)
    num_scenerios_per_estimation = 40
    
    # Number of scenarios (we must add some padding to avoid errors)
    # num_scenarios must be divisible by numnum_scenerios_per_estimation
    num_scenarios = 10000 +  4*num_scenerios_per_estimation
    
    # Parameters for penalty function
    penalty_type = "linear" # Either "linear" or "exponential"
    m = 15.0
    b1 = 21.0

    # Generate network, activity times distributions, and scenarios
    generator_infrastructure.generate_infrastructure(no_of_nodes,
                                                     no_of_layers,
                                                     num_scenarios,
                                                     out_location,
                                                     project_file_name,
                                                     scenarios_file_name,
                                                     crashtime_file_name,
                                                     crashcost_file_name)

    # Load project network
    project_network_file = open(out_location + project_file_name + ".pkl", 'rb')
    project_network = pickle.load(project_network_file)
    project_network_file.close()

    # Load scenarios
    scenario_file = open(out_location + scenarios_file_name + ".pkl", 'rb')
    scenarios = pickle.load(scenario_file)
    scenario_file.close()

    # Load PERT and penalty function parameters
    penalty_file = open(out_location + "penalty_values" + ".pkl", 'rb')
    optimistic_duration = pickle.load(penalty_file)
    most_likely_duration = pickle.load(penalty_file)
    pessimistic_duration = pickle.load(penalty_file)
    t_init = pickle.load(penalty_file)
    t_final = pickle.load(penalty_file)
    penalty_file.close()

    # Load crashing times
    crashtime_file = open(out_location + crashtime_file_name + ".pkl", 'rb')
    crashtime = pickle.load(crashtime_file)
    crashtime_file.close()
    
    # Load crashing costs
    crashcost_file = open(out_location + crashcost_file_name + ".pkl", 'rb')
    crashcost= pickle.load(crashcost_file)
    crashcost_file.close()

    # Bootstrap parameters
    bosst_samples = 1000 #number of bootstrap resamples
    alpha = 0.05  # confidence inteval
    #DEBUG: Not used!!
    b2 = 10

    # Beta used for pareto probability calculation
    beta = 1.5
    
    # KG parameters
    KG_sigma = 0.5
    KG_l = 3.0
    
    # Push experiment details in DB
    c = conn.cursor()
    try:
        c.execute("INSERT INTO EXPERIMENT (ID,METHOD,NO_NODES,NO_LAYERS,NO_SCENARIOS,FIRST_BOOTSTRAP_SIZE,SECOND_BOOTSRAP_SIZE)\
                   VALUES (null,'{me}', {nn}, {nl}, {ns},{nb},{nb2})".format(me=method, nn=no_of_nodes, nl=no_of_layers, ns=num_scenarios, nb=bosst_samples, nb2=b2))

        experiment_id = c.lastrowid
    except sqlite3.IntegrityError:
        print("Error pushing data into the DatBase!!!")
    conn.commit()

    # Initialize attributes
    attribute_dict = SBB.initialize_common_attributes(pool,
                                                      project_network,
                                                      scenarios,
                                                      crashtime,
                                                      crashcost,
                                                      t_init,
                                                      t_final,
                                                      out_location,
                                                      bosst_samples,
                                                      b2,
                                                      alpha,
                                                      experiment_id,#Debug: this is obtained from the database
                                                      conn,
                                                      method,
                                                      num_scenerios_per_estimation,
                                                      beta,
                                                      pessimistic_duration,
                                                      penalty_type,
                                                      m,
                                                      b1,
                                                      KG_sigma,
                                                      KG_l,
                                                      bootstrap)

    # Run SB&B algorithm
    starttime = time.clock()
    # try:
    data = SBB.branch_bound_algorithm(attribute_dict)
    
    # except Exception as inst:
        # print(inst)

    # finally:
        # Inserting time taken for this run in
    endtime = time.clock()
    
    #DEBUG
    #Output some interesting metrics (Needs to be improved massively)
    if bootstrap==True:
        print('Solution {} bootstrap: {}'.format(method, data['E_solution']))
        #print(data['E_data'])
    else:
        print('Solution {}: {}'.format(method, data['E_solution']))

    # Push results into DB
    c = conn.cursor()
    try:
        c.execute("UPDATE EXPERIMENT SET TOTAL_TIME={time}\
               where ID={id}".format(time=endtime - starttime, id=experiment_id))

    except sqlite3.IntegrityError:
        print("Error inserting time in Experiment table")
    conn.commit()

    return


# main method which calls optimize above
if __name__ == "__main__":
  
    # DEBUG: We need to figure out how many processors are 
    # optimal in our program
    processes = mp.cpu_count()
    #pool = mp.Pool(processes)
    #pool = mp.Pool(int(processes/2))
    pool = mp.Pool(10)

    # Select from 6 methods:
    # KG
    # Random_1
    # Random
    # Uniform
    # Distance
    # Pareto_Inverse
    # Pareto_Boltzman
    
    method_list = ["KG", "Random_1", "Random", "Uniform", "Distance", "Pareto_Inverse", "Pareto_Boltzman"]
    #method_list = ["Random_1", "Random", "Uniform", "Distance", "Pareto_Inverse", "Pareto_Boltzman"]
    #method_list = ["KG"]
    #method_list = ["Random"]
    #method_list = ["Random_1"]
    #method_list = ["Uniform"]
    #method_list = ["Distance"]
    #method_list = ["Pareto_Boltzman"]
    #method_list = ["Pareto_Inverse"]
    
    
    seed1 = 28623
    seed2 = 13672
    for i in range(2):
        # Set random seeds to consioder same problems
        # across all methods on this iteration
        seed1 = random.randint(0,10000)
        seed2 = random.randint(0,10000)        
        for method in method_list:
            #Set random seeds to consider same problems
            random.seed(seed1)
            np.random.seed(seed2)
            
            bootstrap = False
            starttime = time.clock()            
            # Solve problem with given method
            optimize(pool, method, bootstrap)
            endTime = time.clock()
            print("Total Time taken to execute {} is {}".format(method, endTime - starttime))
            
            #Set random seeds to consider same problems
            random.seed(seed1)
            np.random.seed(seed2)            
            
            bootstrap = True
            starttime = time.clock()            
            # Solve problem with given method
            optimize(pool, method, bootstrap)
            endTime = time.clock()
            print("Total Time taken to execute {} bootstrap is {}\n".format(method, endTime - starttime))            
        
        
