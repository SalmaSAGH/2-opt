import streamlit as st
import pandas as pd
import numpy as np


def read_excel_file(file_path):
    
    try:
        df = pd.read_excel(file_path, index_col=0)
        return df.values, df.index.tolist()
    except FileNotFoundError:
        st.error("Error: File not found")
        return None, None


def la_2_opt(distances):
    
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
    
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i], route[i + 1]]
    return total_distance

#ici le titre de l'app
st.title("Optimisation problème de voyageur")


uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    
    distance_matrix, city_names = read_excel_file(uploaded_file)

    if distance_matrix is not None:
        
        best_route, best_distance = la_2_opt(distance_matrix)

        st.header("Résultats")
        st.subheader("La route optimale est:")
        st.write(" -> ".join([city_names[i] for i in best_route]))
        st.write(best_distance)
else:
    st.info("Entrer le fichier excel")
