import streamlit as st
import pandas as pd
import numpy as np


def read_excel_file(file_path):
    """
    Reads the distance matrix from an uploaded Excel file.

    Args:
        file_path (str): Path to the uploaded Excel file.

    Returns:
        tuple: A tuple containing the distance matrix (2D array) and city names (list).

    Raises:
        FileNotFoundError: If the specified file is not found.
    """

    try:
        df = pd.read_excel(file_path, index_col=0)
        return df.values, df.index.tolist()
    except FileNotFoundError:
        st.error("Error: File not found. Please upload a valid Excel file.")
        return None, None


def la_plus_forte_descente_2_echanges(distances):
    """
    Apply the 2-opt algorithm to find the best route.
    """
    n = len(distances)
    # Initialize the current route randomly
    current_route = np.random.permutation(n)
    best_distance = calculate_distance(current_route, distances)

    improvement = True
    while improvement:
        improvement = False
        for i in range(n):
            for j in range(i + 2, n + (i > 0)):
                new_route = current_route.copy()
                new_route[i:(j % n) + 1] = list(reversed(current_route[i:(j % n) + 1]))
                new_distance = calculate_distance(new_route, distances)
                if new_distance < best_distance:
                    current_route = new_route
                    best_distance = new_distance
                    improvement = True

    return current_route, best_distance
def calculate_distance(route, distances):
    """
    Calculate the total distance of a route.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i], route[i + 1]]
    return total_distance


# Streamlit app
st.title("Tour Optimization App")

# Option 1: Upload an Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read the distance matrix and city names (if file uploaded)
    distance_matrix, city_names = read_excel_file(uploaded_file)

    if distance_matrix is not None:
        # Run the optimization algorithm if the file is valid
        best_route, best_distance = la_plus_forte_descente_2_echanges(distance_matrix)

        st.header("Results")
        st.subheader("Optimal Route")
        st.write(" -> ".join([city_names[i] for i in best_route]))
        st.write(best_distance)
else:
    st.info("Please upload an Excel file containing the distance matrix.")