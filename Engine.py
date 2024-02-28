import subprocess
import math

try:
    subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"])
    print("Pip has been updated")
except:
    pass

try:
    import pygame
    print("Pygame already installed")
except ImportError:
    subprocess.run(["python3", "-m", "pip", "install", "pygame"])
    import pygame
    print("Pygame has been installed")

try:
    import OpenGL
    print("PyOpenGL already installed")
except ImportError:
    subprocess.run(["python3", "-m", "pip", "install", "pyopengl"])
    import OpenGL
    print("PyOpenGL has been installed")

try:
    import numpy as np
    print("Numpy already installed")
except ImportError:
    subprocess.run(["python3", "-m", "pip", "install", "numpy"])
    import numpy as np
    print("Numpy has been installed")

import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


fov = int(input("Please enter the field of view (fov): \n"))
min_fov = 30
max_fov = 700
default_fov = (min_fov + max_fov) / 2
if fov < min_fov:
    fov = min_fov
elif fov > max_fov:
    fov = max_fov
last_fov = fov

distance = -(int(input("Please enter the distance from the camera to the object: \n")))

pygame.init()

height = 600
width = 800
window_size = (width, height)
window = pygame.display.set_mode(window_size, DOUBLEBUF|OPENGL)

def importEdges(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        edges = []
        for line in lines:
            edge = []
            for vertex in line.split():
                edge.append(int(vertex))
            edges.append(edge)
    print(str(edges))
    return edges

edges = importEdges("edges.txt")

def importVertices(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        vertices = []
        for line in lines:
            vertex = []
            for coord in line.split():
                vertex.append(float(coord))
            vertices.append(vertex)
    print(str(vertices))
    return vertices

vertices = importVertices("vertices.txt")

x_speed = 0
y_speed = 0
z_speed = 1

def renderMesh():
    window.fill((0,0,0))
    glRotatef(1,x_speed,y_speed,z_speed)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, distance)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if fov != last_fov:
        if fov < min_fov:
            fov = min_fov
        elif fov > max_fov:
            fov = max_fov
        gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, distance)
        last_fov = fov
    renderMesh()
    pygame.display.flip()
    pygame.time.delay(10)