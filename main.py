import numpy as np
import math as m
import tkinter as tk

file_name = "VCAM/coords.txt"
cubes_file = "VCAM/new_coords.txt"
sides_file = "VCAM/sides.txt"
EDGES = np.ones(shape=(48,6))
CENTER = 350.0
CUBE = np.ones(shape=(32, 4))
NUM = np.ones(shape=(12, 2))
SIDES = []# np.ones(shape=(6, 2))
COLORS = ['orange', 'yellow', 'black', 'green', 'blue', 'red']

def projection(x, y, z):
   r = 0.0001
   matrix_2d = np.array([[x/(r*z +1), y/(r*z +1)]])
   return matrix_2d

class App(tk.Tk):
       def __init__(self):
              super().__init__()
              self.canv = tk.Canvas(self, bg = 'white')
              self.canv["width"] = 700
              self.canv["height"] = 700
              self.canv.focus_set()
              # self.draw()
              self.draw_cubes()
              self.canv.bind("<Up>", self.process_movements)
              self.canv.bind("<Down>", self.process_movements)
              self.canv.bind("<Right>", self.process_movements)
              self.canv.bind("<Left>", self.process_movements)
              self.canv.bind("0", self.process_movements)
              self.canv.bind("9", self.process_movements)
              self.canv.bind("+", self.process_zoom)
              self.canv.bind("-", self.process_zoom)
              self.canv.bind("w", self.process_rotation)
              self.canv.bind("s", self.process_rotation)
              self.canv.bind("a", self.process_rotation)
              self.canv.bind("d", self.process_rotation)
              self.canv.bind("<space>", self.covering)
              self.canv.pack()

       def draw(self):
              for edge in EDGES:
                     coords_1 = projection(edge[0], edge[1], edge[2])
                     coords_2 = projection(edge[3], edge[4], edge[5])
                     side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])
       
       def draw_cubes(self):
              for n in NUM:
                     first, second = int(n[0]), int(n[1])
                     for n in range (4):
                            coords_1 = projection(CUBE[first][0], CUBE[first][1], CUBE[first][2])
                            coords_2 = projection(CUBE[second][0], CUBE[second][1], CUBE[second][2])
                            side = self.canv.create_line(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1])
                            first += 8
                            second += 8
              # self.canv.create_polygon(120, 20, 120, 200, 300, 200, 300, 20, outline="green", fill="white")

       def update_drawing(self):
              self.canv.delete("all")
              self.draw_cubes()

       def process_movements(self, event):
              MOVE_X = 0
              MOVE_Y = 0
              MOVE_Z = 0
              if event.keysym == 'Up':
                     MOVE_Y = 10
              if event.keysym == 'Down':
                     MOVE_Y =-10
              if event.keysym == 'Right':
                     MOVE_X =-10
              if event.keysym == 'Left':
                     MOVE_X = 10
              if event.keysym == '0':
                     MOVE_Z =-50
              if event.keysym == '9':
                     MOVE_Z = 50

              move_matrix = np.eye(4)
              move_matrix[0:3, 3] = MOVE_X, MOVE_Y, MOVE_Z
              for point in range (32):
                     CUBE[point, :] = move_matrix.dot(CUBE[point, :])

              self.update_drawing()

       def process_zoom(self, event):
              SX, SY, SZ = 0, 0, 0
              if event.keysym == 'plus':
                     SX, SY, SZ = 1.3, 1.3, 1.3
              if event.keysym == 'minus':
                     SX, SY, SZ = 0.9, 0.9, 0.9
              zoom_matrix = np.array([[SX, 0, 0, 0], [0, SY, 0, 0], [0, 0, SZ, 0], [0, 0, 0, 1]])
              for point in range (32):
                     CUBE[point, :] = zoom_matrix.dot(CUBE[point, :])

              self.update_drawing()

       def process_rotation(self, event):
              axis = 'x'
              angle = (7*m.pi)/180
              if event.keysym == 's':
                     axis = 'y'
                     angle = angle * (-1)
              if event.keysym == 'w':
                     axis = 'y'
              if event.keysym == 'a':
                      angle = angle * (-1)
              if axis == 'y':
                     rotate_matrix = np.array([[1, 0, 0, 0], [0, m.cos(angle), -m.sin(angle), 0], [0, m.sin(angle), m.cos(angle), 0], [0, 0, 0, 1]])
              if axis == 'x':
                     rotate_matrix = np.array([[m.cos(angle), 0, m.sin(angle), 0], [0, 1, 0, 0], [-m.sin(angle), 0, m.cos(angle), 0], [0, 0, 0, 1]])
              for point in range (32):
                     CUBE[point, :] = rotate_matrix.dot(CUBE[point, :])

              self.update_drawing()
       
       def find_walls(self):
              read_sides(sides_file)
              sorted_sides = sorted(SIDES, key = lambda x: (x[1][2], x[3][2])) #, reverse = True)

              for n, side in enumerate(sorted_sides):
                     coords_1 = projection(side[0][0], side[0][1], side[0][2])
                     coords_2 = projection(side[1][0], side[1][1], side[1][2])
                     coords_3 = projection(side[2][0], side[2][1], side[2][2])
                     coords_4 = projection(side[3][0], side[3][1], side[3][2])
                     self.canv.create_polygon(coords_1[0][0], coords_1[0][1], coords_2[0][0], coords_2[0][1], coords_3[0][0], coords_3[0][1], coords_4[0][0], coords_4[0][1], outline="black", fill='yellow')

       def covering(self, event):
              self.find_walls()


def read_data(file_name):
       f = open(file_name, "r")
       mod = 3
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              x1, y1, z1, x2, y2, z2 = float(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])
              EDGES[n,:] = (x1, y1, z1, x2, y2, z2)


def read_cubes(file_name):
       f = open(file_name, "r")
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              if n < 32:
                     CUBE[n,:3] = float(line[0]), float(line[1]), float(line[2])
              else:
                     NUM[n-32,:] = int(line[0]), int(line[1])      

def read_sides(file_name):
       global SIDES
       SIDES = []
       f = open(file_name, "r")
       for n, line in enumerate(f):
              line = line.replace("\n", "")
              line = line.split(",")
              x = 0
              for i in range(4):
                     point_1, point_2, point_3, point_4 = CUBE[int(line[0]) + x, :], CUBE[int(line[1]) + x, :], CUBE[int(line[2]) + x, :], CUBE[int(line[3]) + x, :]
                     SIDES.append([point_1, point_2, point_3, point_4])
                     x += 8



if __name__ == "__main__":
       read_cubes(cubes_file)
       #read_data(file_name)
       app = App()
       app.title("Grafika komputerowa")
       app.mainloop()