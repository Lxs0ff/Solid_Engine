import subprocess

try:
    import numpy as np
    print("numpy was already installed")
except ImportError:
    subprocess.run(['python3','-m','pip', 'install', 'numpy'])
    import numpy as np
    print("numpy is now installed")

try:
    from stl import mesh
    print("stl was already installed")
except ImportError:
    subprocess.run(['python3','-m','pip', 'install', 'numpy-stl'])
    from stl import mesh
    print("stl is now installed")

def convert_stl_to_txt(stl_file, vertices_file, edges_file):
    # Load the STL file
    stl_mesh = mesh.Mesh.from_file(stl_file)

    # Extract vertices and edges
    vertices = stl_mesh.vectors.reshape(-1, 3)
    edges = np.arange(len(vertices)).reshape(-1, 2)

    # Save vertices to vertices.txt
    np.savetxt(vertices_file, vertices, fmt='%.6f')

    # Save edges to edges.txt
    np.savetxt(edges_file, edges, fmt='%d')

try:
    convert_stl_to_txt(input("please enter the file name of the stl file you want to convert with .stl at the end (example: example.stl): \n"), 'vertices.txt', 'edges.txt')
    print("Conversion was successful")
except:
    print("Conversion was not successful")
    print("Please make sure the file name is correct and the file is in the same directory as this script")
    print("Please make sure the file name ends with .stl")