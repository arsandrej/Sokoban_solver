import csv
import numpy as np

def statistics():
    with open('sokoban_stats_combined.csv', 'r') as file:
        switch = 0
        no_deadlock = ()
        yes_deadlock = ()
        differences_time = []
        differences_node = []
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if switch == 0:
                print("-------------------------")
                print("Algorthm ", row["algorithm"], " for level: ", row["level_num"])
            if row["deadlock_checked"] == "No":
                switch = 1
                print("Without deadlock:")
                print("Time: ",row["time_s"],"Explored nodes: ", row["explored_nodes"], "Steps: ", row["steps"])
                no_deadlock = (row["explored_nodes"], row["time_s"])
            else:
                switch = 0
                print("With deadlock:")
                print("Time: ",row["time_s"],"Explored nodes: ", row["explored_nodes"], "Steps: ", row["steps"])
                yes_deadlock = (row["explored_nodes"], row["time_s"])
                print("Difference with deadlock: ")
                print("Time difference: ", float(yes_deadlock[1]) - float(no_deadlock[1]))
                print("Explored Node difference: ", (float(yes_deadlock[0]) - float(no_deadlock[0])))
                differences_time.append(float(yes_deadlock[1]) - float(no_deadlock[1]))
                differences_node.append(float(yes_deadlock[0]) - float(no_deadlock[0]))
        print("-------------------------")
        print("Average Differences in Time: ", np.mean(differences_time))
        print("Average Differences in Explored Node: ", np.mean(differences_node))