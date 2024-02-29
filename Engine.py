import subprocess
import math
import time

subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"])

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

try:
    import imgui
    print("imgui already installed")
except:
    subprocess.run(["python3", "-m", "pip", "install", "imgui"])
    import imgui
    print("imgui has been installed")

try:
    import numpy as np
    print("numpy already installed")
except ImportError:
    subprocess.run(['python3','-m','pip', 'install', 'numpy'])
    import numpy as np
    print("numpy has been installed")

try:
    from stl import mesh
    print("stl already installed")
except ImportError:
    subprocess.run(['python3','-m','pip', 'install', 'numpy-stl'])
    from stl import mesh
    print("stl has been installed")


import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.pygame import PygameRenderer
import ctypes

def convert_stl_to_txt(stl_file):
        stl_mesh = mesh.Mesh.from_file(stl_file)

        vertices = stl_mesh.vectors.reshape(-1, 3)
        edges = np.arange(len(vertices)).reshape(-1, 2)
        
        try:
            os.remove('vertices.txt')
            os.remove('edges.txt')
        except:
            pass

        np.savetxt('vertices.txt', vertices, fmt='%.6f')
        np.savetxt('edges.txt', edges, fmt='%d')

min_fov = 30
max_fov = 700
default_fov = 90
fov = default_fov
last_fov = fov

pygame.init()

height = 600
width = 800

user32 = ctypes.windll.user32

min_width = 800
min_height = 600

max_width = user32.GetSystemMetrics(0)
max_height = user32.GetSystemMetrics(1)

window_size = (width, height)
window = pygame.display.set_mode(window_size, DOUBLEBUF|OPENGLBLIT,pygame.RESIZABLE)

cmd_list = {
    "windowsize",
    "clear",
    "loadmodel",
    "help",
    "exit",
}
class CommandWindow:
    def  __init__(self) -> None:
        self.executing_command = False
        self.command = ""
        self.command_history = []

    def draw(self):
        imgui.set_next_window_size(width - 40, height - 40)
        imgui.set_next_window_position(20, 20)

        imgui.begin("Command Window")

        changed, self.command = imgui.input_text("Command", self.command, 256,imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
        if changed:
            self.executing_command = True
            self.execute_command(self.command)
            self.executing_command = False
            self.command = ""
        
        imgui.text("Output: ")
        for command in self.command_history:
            imgui.text(command)

        imgui.end()

    def execute_command(self, command):
        self.command_history.append(command)
        if command == "exit":
            pygame.quit()
            quit()
        elif command == "clear":
            self.command_history.clear()
        elif 'loadmodel' in command:
            command = command.replace('loadmodel', '')
            command = command.replace(' ', '')
            file = str(command)
            if file.endswith('.stl'):
                print(file)
                convert_stl_to_txt(file)
                self.command_history.append("Model loaded successfully \n")
            else:
                self.command_history.append("Invalid parameters, please put '.stl' after the file name and make sure it is a .stl file \n")
                pass
        elif 'windowsize' in command:
            global width
            global height
            global window
            command = command.replace('windowsize ', '')
            new_height, new_width = str(command).split(' ')
            if new_height < str(min_height):
                new_height = min_height
            elif new_height > str(max_height):
                new_height = max_height
            if new_width < str(min_width):
                new_width = min_width
            elif new_width > str(max_width):
                new_width = max_width
            try:
                width = int(new_width)
                height = int(new_height)
                window_size = (width, height)
                window = pygame.display.set_mode(window_size, DOUBLEBUF|OPENGLBLIT,pygame.RESIZABLE)
            except:
                self.command_history.append("Someting went wrong, size not valid")
        elif command == "help":
            tick = 0
            self.command_history.append("\nCommand List: \n")
            for cmd in cmd_list:
                tick += 1
                self.command_history.append(str(tick) + " -> " + cmd)
            self.command_history.append("\n")

imgui.create_context()
io = imgui.core.get_io()
io.display_size = window_size
renderer = PygameRenderer()

command_window = CommandWindow()

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
mouse_speed = 0.05
fov_amount = .3

rotationx = 0
rotationy = 0
last_rotx = rotationx
last_roty = rotationy

def renderMesh():
    global render_on
    try:
        edges = importEdges("edges.txt")
        vertices = importVertices("vertices.txt")
        window.fill((0,0,0))
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glBegin(GL_LINES)
        glColor3fv((1,1,1))
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
    except:
        if render_on:
            render_on = False
            print("An error happened with the render switching to cmd")

gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 50.0)
glTranslatef(cam_y, cam_x, cam_z)

render_on = True

pygame.display.set_caption("Solid 3D Engine")
pygame.display.set_icon(pygame.image.load('icon.png'))

clock = pygame.time.Clock()
while True:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        renderer.process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                render_on = not render_on

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
        rotationx = mouse_x * mouse_speed
        rotationy = mouse_y * mouse_speed
    else:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

    if fov != last_fov or cam_z != last_cam_z or cam_x != last_cam_x or cam_y != last_cam_y:
        if fov < min_fov:
            fov = min_fov
        elif fov > max_fov:
            fov = max_fov
        glLoadIdentity()
        gluPerspective(fov, (window_size[0]/window_size[1]), 0.1, 1000.0)
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

    window.fill((0,0,0))
    
    if render_on == True:
        renderMesh()
    else:
        imgui.new_frame()
        command_window.draw()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        imgui.render()
        renderer.render(imgui.get_draw_data())
    
    
    pygame.display.flip()
    pygame.time.delay(10)