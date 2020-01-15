try:
    from tkinter import *
except:
    print("Please, install tkinter (pip install tkinter or apt install python3-tk)")
    exit()

try:
    import math
except:
    print("Issue while loading the math library")
    exit()

class mesh:
    def __init__(self, verts = [], edges = []):
        self.verts = verts
        self.edges = edges

class obj:
    def __init__(self, mesh, x, y, z):
        self.mesh = mesh
        self.x = x
        self.y = y
        self.z = z

class cam:
    def __init__(self, pos=[0,0,0], rot=[0,0,0], vit=1, vrad=0.05):
        self.pos = pos
        self.rot = rot
        self.vit = vit
        self.vrad = vrad
    
    def update(self, event):
        t = event.keysym
        
        #Transform
        if t in ['z', 'Z', 'Up']:
            self.pos[2] -= self.vit
        elif t in ['s', 'S', 'Down']:
            self.pos[2] += self.vit
        elif t in ['q', 'Q', 'Left']:
            self.pos[0] += self.vit
        elif t in ['d', 'D', 'Right']:
            self.pos[0] -= self.vit
        elif t in ['a', 'A']:
            self.pos[1] += self.vit
        elif t in ['e', 'E']:
            self.pos[1] -= self.vit
        
        #Rotation
        elif t == 'KP_4':
            self.rot[1] -= self.vrad
        elif t == 'KP_6':
            self.rot[1] += self.vrad
        elif t == 'KP_8':
            self.rot[0] -= self.vrad
        elif t == 'KP_2':
            self.rot[0] += self.vrad


class moteur:
    def __init__(self, x, y, fps = 25):
        self.x = x
        self.y = y
        self.fps = fps

        #Init camera

        self.camera = cam()

        #tkinter
        self.fen = Tk()
        self.fen.geometry(str(int(x))+"x"+str(int(y)))
        self.fen.title("3D Graph")

        self.can = Canvas(self.fen, width=x, height=y, bg='Black')
        self.can.pack()

        self.fen.bind('<Key>', self.camera.update)
        
        #3D stuff
        self.cx, self.cy = self.x//2, self.y//2
        self.displayedObj = []
        
        #Mesh
        self.objs = []


        self.loop()
    
    def loop(self):
        global rad
        self.clear()
        self.render()
        self.fen.after(int(1000/self.fps), self.loop)
    
    def clear(self):
        if len(self.displayedObj) > 0:
            for i in self.displayedObj:
                self.can.delete(i)
            self.displayedObj = []
    
    def render(self):
        for obj in self.objs:
            for ox,oy,oz in obj.mesh.verts:

                px, py = self.project(ox, oy, oz, obj)
                
                self.displayedObj.append(self.can.create_oval(px-3, py-3, px+3, py+3, fill='white'))
            
            for edge in obj.mesh.edges:
                points = []
                for ox, oy, oz in (obj.mesh.verts[edge[0]], obj.mesh.verts[edge[1]]):

                    px, py = self.project(ox, oy, oz, obj)

                    points.append([int(px), int(py)])
                self.displayedObj.append(self.can.create_line(points[0][0], points[0][1], points[1][0], points[1][1], fill='White'))
    
    def project(self, ox, oy, oz, obj):

        #Object coord transform
        ox += obj.x
        oy += obj.y
        oz += obj.z

        #Camera transform
        ox += self.camera.pos[0]
        oy += self.camera.pos[1]
        oz += self.camera.pos[2]

        #Camera rotation
        ox, oz = rotate2d((ox, oz), self.camera.rot[1])
        oy, oz = rotate2d((oy, oz), self.camera.rot[0])

        try:
            fx=(self.x/2)/oz
            fy=(self.y/2)/oz
        except:
            fx=999
            fy=999

        px,py = ox*fx, oy*fy
        px+=self.x/2
        py+=self.y/2

        return px, py
                
    
    def mainloop(self):
        self.fen.mainloop()
    
    def addobj(self, mesh, x, y, z):
        obje = obj(mesh, x, y, z)
        self.objs.append(obje)
        return self.objs.index(obje)

def rotate2d(pos, rad):
    x,y = pos
    s,c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s

moteur = moteur(400,400)


moteur.addobj(mesh(
[[-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1], [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]],
[[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4], [0,4], [1,5], [2,6], [3,7]]), 0, 0, 5)

moteur.mainloop()