try:
    from tkinter import *
except:
    print("Please, install tkinter (pip install tkinter or apt install python3-tk) and launch again")
    exit()

import math

class mesh:
    def __init__(self, verts = [], faces = []):
        self.verts = verts
        self.faces = faces
    
    def copy(self, mesh2):
        self.verts = mesh2.verts
        self.faces = mesh2.faces

class obj:
    def __init__(self, mesh, x=0, y=0, z=0, rotx=0, roty=0, rotz=0, scalex=1, scaley=1, scalez=1):
        self.mesh = mesh
        self.x = x
        self.y = y
        self.z = z
        self.rotx = rotx
        self.roty = roty
        self.rotz = rotz
        self.scalex = scalex
        self.scaley = scaley
        self.scalez = scalez

        self.modify()
    
    def coords(self, x='x', y='x', z='x', rotx='x', roty='x', rotz='x', scalex='x', scaley='x', scalez='x'):
        if not(int(x) != x):
            self.x = x
        if not(int(y) != y):
            self.y = y
        if not(int(z) != z):
            self.z = z
        if not(int(rotx) != rotx):
            self.rotx = rotx
        if not(int(roty) != roty):
            self.roty = roty
        if not(int(rotz) != rotz):
            self.rotz = rotz
        if not(int(scalex) != scalex):
            self.scalex = scalex
        if not(int(scaley) != scaley):
            self.scaley = scaley
        if not(int(scalez) != scalez):
            self.scalez = scalez

        modify()
    
    def modify(self):
        try:
            self.modifmesh.copy(self.mesh)
        except:
            self.modifmesh = mesh()
            self.modifmesh.copy(self.mesh)
        
        for i in self.modifmesh.verts:
            if not(self.scalex==1 and self.scaley==1 and self.scalez==1):
                i[0] *= self.scalex
                i[1] *= self.scaley
                i[2] *= self.scalez
        
            if not(self.x==0 and self.y==0 and self.z==0):
                i[0] += self.x
                i[1] += self.y
                i[2] += self.z
    
    def getMesh(self):
        return self.modifmesh

class cam:
    def __init__(self, pos=[0,0,0], rot=[0,0,0], vit=1, vrad=0.05):
        self.pos = pos
        self.rot = rot
        self.vit = vit
        self.vrad = vrad
    
    def update(self, event):
        t = event.keysym

        x,y = self.vit * math.sin(self.rot[1]), self.vit * math.cos(self.rot[1])
        
        #Transform
        if t in ['z', 'Z', 'Up']:
            self.pos[0] -= x
            self.pos[2] -= y
        elif t in ['s', 'S', 'Down']:
            self.pos[0] += x
            self.pos[2] += y
        elif t in ['q', 'Q', 'Left']:
            self.pos[0] += y
            self.pos[2] -= x
        elif t in ['d', 'D', 'Right']:
            self.pos[0] -= y
            self.pos[2] += x
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
    
    def bind(self, key, func):
        if key=='<Loop>':
            self.loopdev = func
        elif key=='<Key>':
            self.fen.bind('<Key>', func)
    
    def loopdev(self):
        return 1

    def loop(self):
        global rad
        self.clear()
        self.render()
        self.loopdev()
        self.fen.after(int(1000/self.fps), self.loop)
    
    def clear(self):
        if len(self.displayedObj) > 0:
            for i in self.displayedObj:
                self.can.delete(i)
            self.displayedObj = []
    
    def render(self):
        for obj in self.objs:
            
            vert_l = []
            screen_co = []
            for ox, oy, oz in obj.getMesh().verts:

                px, py, l = self.project(ox, oy, oz, obj, 1)
                vert_l.append(l)

                screen_co.append([int(px), int(py)])

            #Face

            face_l = []
            face_color = []
            depth = []
            for f in range(len(obj.getMesh().faces)):
                face = obj.getMesh().faces[f]

                on_screen = 0

                for i in face:
                    x,y = screen_co[i]
                    if vert_l[i][2]>0 and x>0 and x<self.x and y>0 and y<self.y:
                        on_screen = 1
                        break
                
                if on_screen:
                    coords = [screen_co[i] for i in face]
                    face_l.append(coords)
                    face_color.append('Grey')

                    depth.append(sum(sum(vert_l[j][i] for j in face)**2 for i in range(3)))
                
                order = sorted(range(len(face_l)), key=lambda i: depth[i], reverse=1)
            
            for i in order:
                self.displayedObj.append(self.can.create_polygon(face_l[i], fill=face_color[i], width=3, outline='Black'))

    
    def project(self, ox, oy, oz, obj, needvl = 0):

        #Object coord transform
        #ox += obj.x
        #oy += obj.y
        #oz += obj.z

        #Camera transform
        ox += self.camera.pos[0]
        oy += self.camera.pos[1]
        oz += self.camera.pos[2]

        #Verticle list
        if (needvl):
            vl=[ox, oy, oz]

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

        if needvl:
            return px, py, vl
        else:
            return px, py
                
    
    def mainloop(self):
        self.fen.mainloop()
    
    def addobj(self, mesh, x, y, z, rx, ry, rz, sx, sy, sz):
        obje = obj(mesh, x, y, z, rx, ry, rz, sx, sy, sz)
        self.objs.append(obje)
        return obje

def rotate2d(pos, rad):
    x,y = pos
    s,c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s