import pickle
from collections import deque
from numpy.random import uniform

def generate_crash_times(no_of_nodes, out_location, crash_time_file_name):
   """Generates activity crash times in percentage
   
   Parameters
   ----------
   no_of_nodes : int
      Number of nodes (activities) in the network
      
   Returns
   ----------
   N/A
   """
   crash_time = deque(uniform(0.1, 0.5, no_of_nodes))
   crash_time.appendleft(0.0)
   crash_time.append(0.0)
   
   crash_time=list(crash_time)
   
   file_name = out_location + crash_time_file_name + '.pkl'
   output_file = open(file_name, 'wb+')
   pickle.dump(crash_time, output_file)
   output_file.close()
   
   return


def generate_crash_cost(no_of_nodes, out_location, crash_cost_file_name):
   """Generates activity crash costs
   
   Parameters
   ----------
   no_of_nodes : int
      Number of nodes (activities) in the network
      
   Returns
   ----------
   N/A
   """   
   crash_cost = deque(uniform(100, 200, no_of_nodes))
   crash_cost.appendleft(0.0)
   crash_cost.append(0.0)
   
   crash_cost = list(crash_cost)
   
   file_name = out_location + crash_cost_file_name + '.pkl'
   output_file = open(file_name, 'wb+')
   pickle.dump(crash_cost, output_file)
   output_file.close()
   
   return


