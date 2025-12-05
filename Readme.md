This program is run through the python scrpt found in analysis.py. Both the DP approach and Greedy approach use the same logic for reading from the file so that should be identical time complexity for access. That is why the time complexity is measured from the 
python file and not the cpp implementation. The python script will run multiple tests on the cpp files for greedy.


To run the code with the python script first create a virtal enviroment:
    - run: 
        - python -m venv .venv
        - source .venv/bin/activate
        - pip install -r requirments.txt
This will start your venv and allow you to run the python code with python analysis.py
This will run the code on multiple randly generated tests
The length of classes is bounded by a minimum length of 30 minutes and a maximum of 4 hours.
If you want to run the cpp file your self:
    - run: 
        - make
        - ./dp_prog <your input file> <your output file>
        - make sure the infile follows the following input format:
        <number of classes> //this is just for the first line
        <class number> <start time (minutes after 12 am)> < end time (minutes after 12am)>  //do this for the rest of the line

It is also important to note that classes cannot take place accross midnight -> this would be extremely unrealistic so this is 
not handled currently in the case.

    