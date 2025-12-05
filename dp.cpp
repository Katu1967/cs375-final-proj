/*

    Need to figure out the case 

*/


#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>



using namespace std;


//struct for classes after they are split into start and end events 
struct Events {
    long time;
    bool type; //1 for an end event 0 for a start event
    long class_num;
};

//struct for classes before they are processed
struct Classes {
    long class_num;
    long start;
    long end;
};

//helper struct for custom comparisons
struct comparisons{
    bool operator()(const Events& a, const Events& b) const{

        if(a.time != b.time){
            return a.time < b.time;
        }
        return a.type > b.type;
    }
};



//helper function to create events for all of the classes
vector <Events> createEvents(vector<Classes>raw_data){

    vector <Events> final_events;

    //loop through and create the events , still o (n) here
    for(Classes c : raw_data){

        Events temp1, temp2;

        temp1.time = c.start;
        temp1.type = false;
        temp1.class_num = c.class_num;

        temp2.time = c.end;
        temp2.type = true;
        temp2.class_num = c.class_num;

        //add them to the final array
        final_events.push_back(temp1);
        final_events.push_back(temp2);
    }



    // cout << "The list of events is:" << endl;
    // for(Events e: final_events){

    //     cout << "Time: " << e.time << ", Class Number: " << e.class_num << ", Type: " << (e.type ? "end" : "start") << endl;
    // }



    return final_events;
}



//helper function to sort the events 
void sortEvents(vector <Events> &event_list){
    sort(event_list.begin(), event_list.end(), comparisons());

    // cout << "The list of events is:" << endl;
    // for(Events e: event_list){

    //     cout << "Time: " << e.time << ", Class Number: " << e.class_num << ", Type: " << (e.type ? "end" : "start") << endl;
    // }

}

//actual DP logic
long findMinRooms(vector <Classes> class_list){

    //call helpers
    vector <Events> event_list = createEvents(class_list);
    sortEvents(event_list);

    vector <long> dp_table;
    dp_table.resize(event_list.size() + 1);
    long min_rooms = 0;
    //initially zero, index is 1
    dp_table[0] = 0;
    long idx = 1;

    for(Events e : event_list){
        
        //the case where it is a start event, add one and update the min_rooms
        if(e.type == false){
            dp_table[idx] = dp_table[idx - 1] + 1;
            min_rooms = max(dp_table[idx], min_rooms);
        }else{  
            //else its a end event so subtract one, no need to check min_rooms
            dp_table[idx] = dp_table[idx - 1] - 1;
        }

        // cout << "The current nubmer of rooms is: " << dp_table[idx] << endl;

        //update the index counter
        idx++;
    }
    //return the min number of rooms
    return min_rooms;

}





int main(int argv, char* argc[]){

    string in_file = argc[1];
    string out_file = argc[2];


    //read data from the file
    
    ifstream infile(in_file);
    if (!infile.is_open()) {
        cerr << "Error: file not open " << in_file << endl;
        return 0;
    }


    long n, class_num, begin, finish;

    infile >> n; 


    vector<Classes>raw_data;


    while(infile >> class_num >> begin >> finish ){

        //add all the classes to an vector 
        Classes temp;
        temp.class_num = class_num;
        temp.start = begin;
        temp.end = finish;
        raw_data.push_back(temp);
    }

    
    auto start = chrono::high_resolution_clock::now();
    long min_rooms =  findMinRooms(raw_data);    
    auto stop = chrono::high_resolution_clock::now();
    chrono::duration<double, micro> duration = stop - start;

    ofstream outfile(out_file);

    outfile << min_rooms << endl;

    outfile << duration.count() << endl;


    return 0;


}