# cs224w_project

Please contact us if you would like to run this code (the dataset is private). These are the important files in the repo:


script.sh: Run this to run the code. 

parser_two_graphs: Parses the data and converts it into SNAP graphs.

centrality.py: Calculates PageRank, Eigen centrality. 

create_input_PR: Reads in communities that were detected by Infomap. 

nodes_at_hop.py: Calculates the distance between nodes for each community. 

recommend.py: Generates recommendations for all users. 

recommend_analyze: Calculates accuracy of the recommendations by comparing against ground truth. 
