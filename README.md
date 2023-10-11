# Customer Route Optimization Web App

**Overview:** <br/>
This web application provides users an optimized route based on their address and a list of customer addresses. By providing the starting address and a list of customer addresses, users can visualize the optimal path to visit each customer, with distances provided for each segment of the journey.

**Features:**<br/>
Address Input: User can provide their starting address and a list of customer addresses they wish to visit.
Optimized Routing: Using Google OR-Tools, the application finds the shortest route to visit all the addresses and returns to the starting point.
Map Visualization: The optimized route is visualized on a map, clearly marking each address. The path between each address is highlighted using blue lines.
Distance Details: The application provides distance details for each segment of the journey and the total distance to be covered.

**Setup and Installation Prerequisites:**<br/>

Ensure you have the following installed:

Python
Streamlit
Geopy
Google OR-Tools
Folium
Streamlit-folium plugin
Installing Dependencies

```
pip install streamlit geopy ortools folium streamlit-folium
```

**Running the app:**<br/>
Navigate to the directory containing the app script and run:

```
streamlit run app_script_name.py
```
(Replace app_script_name.py with the name of your app script)

**Usage:**<br/>
Input your starting address in the "Enter Your Address" field.
Enter the list of customer addresses in the "Enter Customer Addresses" section. Make sure each address is on a new line.
Click the "Optimize Route" button.
View the optimized route details and visualize the route on the map.

**Acknowledgements:**<br/>

Google OR-Tools: Used for route optimization.
Geopy: Used for geocoding the addresses.
Folium: Used for map visualization.

**License:**<br/>
This project is open-source and available to everyone. Feel free to use, modify, and distribute as you see fit.

