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


min_fov = 30
max_fov = 700
default_fov = 90
fov = default_fov
if fov < min_fov:
    fov = min_fov
elif fov > max_fov:
    fov = max_fov
last_fov = fov

pygame.init()

height = 600
width = 800
window_size = (width, height)
window = pygame.display.set_mode(window_size, DOUBLEBUF|OPENGL,pygame.RESIZABLE)

cam_x = 0
cam_y = 0
cam_z = -5

last_cam_x = cam_x
last_cam_y = cam_y
last_cam_z = cam_z

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

move_speed = 0.05
fov_amount = .3

rotationx = 0
rotationy = 0
last_rotx = rotationx
last_roty = rotationy

vertices = importVertices("vertices.txt")

def renderMesh():
    window.fill((0,0,0))
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin(GL_LINES)
    glColor3fv((1,1,1))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 50.0)
glTranslatef(cam_y, cam_x, cam_z)

render_on = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                render_on = not render_on
            if event.key == pygame.K_r:
                fov = default_fov
                cam_x = 0
                cam_y = 0
                cam_z = -5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        cam_x += move_speed
    if keys[pygame.K_LCTRL]:
        cam_x -= move_speed
    if keys[pygame.K_a]:
        cam_y -= move_speed
    if keys[pygame.K_d]:
        cam_y += move_speed
    if keys[pygame.K_w]:
        cam_z -= move_speed
    if keys[pygame.K_s]:
        cam_z += move_speed
    if keys[pygame.K_UP]:
        fov += fov_amount
    if keys[pygame.K_DOWN]:
        fov -= fov_amount

    if pygame.mouse.get_pressed()[0]:
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        mouse_x, mouse_y = pygame.mouse.get_rel()
        rotationx = mouse_x * 0.1
        rotationy = mouse_y * 0.1
    else:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

    if fov != last_fov or cam_z != last_cam_z or cam_x != last_cam_x or cam_y != last_cam_y:
        if fov < min_fov:
            fov = min_fov
        elif fov > max_fov:
            fov = max_fov
        glLoadIdentity()
        gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 50.0)
        glTranslatef(cam_y, cam_x, cam_z)
        last_fov = fov
        last_cam_z = cam_z
        last_cam_x = cam_x
        last_cam_y = cam_y
    
    if rotationx != last_rotx or rotationy != last_roty:
        glRotatef(rotationx, 1, 0, 0)
        glRotatef(-rotationy, 0, 1, 0)
        last_rotx = rotationx
        last_roty = rotationy
    if render_on == True:
        renderMesh()
    else:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()
    pygame.time.delay(10)