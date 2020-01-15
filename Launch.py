try:
    from moteur import *
except:
    print("Issue while loading the motor lib")
    exit()

#try:
import objtomesh
#except:
    #print("Issue while loading the ObjToMesh lib")
    #exit()


moteur = moteur(1080/2,1080/2)

#moteur.addobj(mesh(
#[[-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1], [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]],
#[[0,1,2,3], [4,5,6,7], [0,1,5,4], [2,3,7,6], [0,3,7,4], [1,2,6,5]]), 0, 0, 5)

moteur.addobj(objtomesh.importobj("Obj/Suzan.obj"), 0, 0, 5)

moteur.mainloop()