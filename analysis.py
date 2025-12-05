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
    output_filename = "outfile.txt"
    
    #get rid of cold start penalty so data is not skewed
    print("Performing warm-up run...")
    generateInputs(10, test_filename)
    os.system(f"./dp_prog {test_filename} {output_filename} > /dev/null 2>&1")
    
    for size in test_sizes:
        generateInputs(size, test_filename)
        print(f"Testing with {size} classes...")
        
        # Run the program
        os.system(f"./dp_prog {test_filename} {output_filename}")
        # read from file
        try:
            with open(output_filename, 'r') as file:
                num_rooms_line = file.readline().strip()
                runtime_line = file.readline().strip()

                
                num_rooms = int(num_rooms_line.split()[-1])
                
                # Convert runtime from milliseconds to seconds
                runtime_ms = float(runtime_line)
                runtime_sec = runtime_ms / 1000.0
                
                runtimes.append(runtime_sec)
                print(f"  Rooms needed: {num_rooms}, Runtime: {runtime_sec:.6f} seconds")

        except FileNotFoundError:
            print(f"Error: The file '{output_filename}' was not found.")
        except (ValueError, IndexError) as e:
            print(f"Error parsing output: {e}")
        
        print()
    
    return test_sizes, runtimes


def plotRuntimes(sizes, runtimes, algorithm_name, save_path):
    """
    Plot runtime with input size
    """
    plt.figure(figsize=(10, 6))
    
    #create scatter plot
    plt.scatter(sizes, runtimes, s=100, alpha=0.6, color='blue', label='Measured Runtime')
    
    #calc linear line of best fit
    coefficients_linear = np.polyfit(sizes, runtimes, 1)
    polynomial_linear = np.poly1d(coefficients_linear)
    line_x = np.linspace(min(sizes), max(sizes), 100)
    line_y_linear = polynomial_linear(line_x)
    
    plt.plot(line_x, line_y_linear, color='red', linewidth=2, label='Linear Fit')
    

    nlogn_values = sizes * np.log(sizes)
    coefficients_nlogn = np.polyfit(nlogn_values, runtimes, 1)
    line_y_nlogn = coefficients_nlogn[0] * line_x * np.log(line_x) + coefficients_nlogn[1]
    
    
    plt.plot(line_x, line_y_nlogn, color='green', linewidth=2, label='n*log(n) Fit')
    
    plt.xlabel('Number of Classes', fontsize=12)
    plt.ylabel('Runtime (milliseconds)', fontsize=12)
    plt.title(f'{algorithm_name} - Runtime vs Input Size', fontsize=14)
    plt.legend(fontsize=11)
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

    num = 100
    test_vals = []

    while num <= 100000:
        test_vals.append(num)
        num = num + 100


    sizes, runtimes = testCode(test_vals)
    
    print("=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    for size, runtime in zip(sizes, runtimes):
        print(f"  {size:6d} classes: {runtime:.6f} seconds")
    print()
    
    #plot the runtimes for the dynamic progarmming solution
    plotRuntimes(sizes, runtimes, "DP Algorithm", "dp_runtime_plot.png")








