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
                v = ligne.split(' ')
                vert.append([float(v[1]), float(v[2]), float(v[3])])
            elif 'f ' in ligne:
                f_temp = []
                for i in ligne.split(' ')[1:]:
                    f_temp.append(int(i.split('/')[0])-1)
                faces.append(f_temp)

    return mesh(vert, faces)