import streamlit as st
import math
from geopy.geocoders import Nominatim
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import folium
from streamlit_folium import folium_static
from folium.plugins import AntPath

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

def geocode(address):
    """Convert address to latitude and longitude."""
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def distance(origin, destination):
    """Calculate the Haversine distance."""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def optimize_route(locations):
    """
    Use Google OR-Tools to find an optimized route.
    """
    distances = []

    for loc1 in locations:
        row = []
        for loc2 in locations:
            if loc1 == loc2:
                row.append(0)
            else:
                row.append(distance(loc1, loc2))
        distances.append(row)

    data = {}
    data["distance_matrix"] = distances

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data["distance_matrix"][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 30

    solution = routing.SolveWithParameters(search_parameters)
    route = []
    if solution:
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
    return route

def main():
    st.title("Customer Route Optimization")

    st.sidebar.header("Input")
    own_address = st.sidebar.text_input("Enter Your Address")
    address_list = st.sidebar.text_area("Enter Customer Addresses (one per line)").splitlines()

    if own_address:
        address_list.insert(0, own_address)

    if st.sidebar.button("Optimize Route"):
        location_coords = []
        unresolved_addresses = []
        for addr in address_list:
            coords = geocode(addr)
            if coords:
                location_coords.append(coords)
            else:
                unresolved_addresses.append(addr)

        if unresolved_addresses:
            for addr in unresolved_addresses:
                st.sidebar.warning(f"Couldn't resolve address: {addr}")
            return

        optimized_route_indices = optimize_route(location_coords)
        optimized_route = [address_list[i] for i in optimized_route_indices]

        st.sidebar.success("Route optimized successfully!")

        # Display route details
        st.header("Optimized Route Details:")
        total_distance = 0
        previous_coords = None
        for i, idx in enumerate(optimized_route_indices):
            addr = address_list[idx]
            coords = location_coords[idx]
            if previous_coords:
                segment_distance = distance(previous_coords, coords)
                total_distance += segment_distance
                st.markdown(f"{i}. **{addr}** - Distance from previous location: **{segment_distance:.2f} km**")
            else:
                st.markdown(f"{i}. **{addr}** - Starting point")
            previous_coords = coords
        st.markdown(f"### Total distance: **{total_distance:.2f} km**")

        # Show map
        m = folium.Map(location=location_coords[0], zoom_start=12)
        for i in range(len(optimized_route_indices) - 1):
            start = location_coords[optimized_route_indices[i]]
            end = location_coords[optimized_route_indices[i+1]]
            segment_distance = distance(start, end)

            popup_content = f"{optimized_route[i]} to {optimized_route[i+1]}: {segment_distance:.2f} km"
            popup = folium.Popup(popup_content, max_width=300)

            folium.Marker(start, popup=popup).add_to(m)
            AntPath([start, end], color="blue", weight=2.5, opacity=1).add_to(m)
        
        # Add the last marker of the route
        folium.Marker(location_coords[optimized_route_indices[-1]]).add_to(m)
        folium_static(m)

if __name__ == "__main__":
    main()
