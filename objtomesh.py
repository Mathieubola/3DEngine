try:
    from moteur import mesh
except:
    print("Issue while loading the motor lib")
    exit()

def importobj(path):
    fic = open(path)
    ctn = fic.read()
    fic.close()

    vert = []
    faces = []
    
    for ligne in ctn.split('\n'):
        if len(ligne) > 0:
            if 'v ' in ligne:
                vert.append([float(ligne.split(' ')[i]) for i in range(1,4)])
            elif 'f ' in ligne:
                faces.append([int(i.split('/')[0])-1 for i in ligne.split(' ')[1:]])

    return mesh(vert, faces)