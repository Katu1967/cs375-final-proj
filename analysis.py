"""The purpose of this script is to run tests on the cpp files for the greedy and dynamic programming approaches to the 
class room assignment problem"""

import subprocess
import numpy as np
import os
import random
import time
import matplotlib.pyplot as plt


def generateInputs(num_classes, output_file):
    """
    Generate pseudorandom class schedule inputs and write to a file

    """
    with open(output_file, 'w') as f:
        #write the number of classes
        f.write(f"{num_classes}\n")
        
        #generate data for the infile
        for class_num in range(1, num_classes + 1):
            start_time = random.randint(0, 1409)
            
            #add bounds of max 4 hours and minumum 30 minutes for the time 
            max_end = min(1439, start_time + 240)  
            min_end = start_time + 30 
            end_time = random.randint(min_end, max_end)
            
            #write to the file 
            f.write(f"{class_num:02d} {start_time} {end_time}\n")


def testCode(test_sizes=None):
    """
    Generate multiple test cases with different input sizes and track runtime.
    """

    
    # Compile the program once
    print("Compiling dp_prog...")
    os.system("make dp_prog")
    print()
    
    runtimes = []
    test_filename = "test_input.txt"
    
    #get rid of cold start penalty so data is not skewed
    print("Performing warm-up run...")
    generateInputs(10, test_filename)
    os.system(f"./dp_prog {test_filename} outfile.txt > /dev/null 2>&1")
    
    for size in test_sizes:
        generateInputs(size, test_filename)
        print(f"Testing with {size} classes...")
        
        #measure time
        start_time = time.time()
        os.system(f"./dp_prog {test_filename} outfile.txt")
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        runtimes.append(elapsed_time)
        
        print(f"  Runtime: {elapsed_time:.6f} seconds")
        print()
    
    return test_sizes, runtimes


def plotRuntimes(sizes, runtimes, algorithm_name, save_path):
    """
    Plot runtime vs input size 
    """
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, runtimes, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Number of Classes', fontsize=12)
    plt.ylabel('Runtime (seconds)', fontsize=12)
    plt.title(f'{algorithm_name} - Runtime vs Input Size', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot saved to {save_path}")
    plt.show()


#run the cpp code 
if __name__ == "__main__":
    print("=" * 60)
    print("Running DP Algorithm Performance Tests")
    print("=" * 60)
    print()
    
    #run tests
    sizes, runtimes = testCode([10, 15, 20, 30, 40, 50, 100, 500, 700, 800,  1000, 1500, 2000, 3000, 10000, 15000, 20000, 30000, 40000])
    
    print("=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    for size, runtime in zip(sizes, runtimes):
        print(f"  {size:6d} classes: {runtime:.6f} seconds")
    print()
    
    #plot the runtimes for the dynamic progarmming solution
    plotRuntimes(sizes, runtimes, "DP Algorithm", "dp_runtime_plot.png")








