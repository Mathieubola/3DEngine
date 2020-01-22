from moteur import *
import objtomesh
import math


moteur = moteur(1080/2,1080/2)

#moteur.addobj(mesh(
#[[-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1], [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]],
#[[0,1,2,3], [4,5,6,7], [0,1,5,4], [2,3,7,6], [0,3,7,4], [1,2,6,5]]), 0, 0, 5)

suzan = moteur.addobj(objtomesh.importobj("Obj/Suzan.obj"), 0, 0, 5)

t=0
def loop():
    global t
    t+=1
    suzan.x = math.sin(t)

def key(event):
    t=event.keysym
    if t=='z':
        suzan.y+=1
    elif t=='s':
        suzan.y-=1


moteur.bind('<Loop>', loop)
moteur.bind('<Key>', key)

moteur.mainloop()