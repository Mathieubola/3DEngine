# 3DEngine

Simple 3D Engine working with Python3 and tkinter.

## Instalation

### Install Python

https://www.python.org/

### Install tkinter 

```sh
pip install tkinter
```

or

```
apt install python3-tk
```

### Launch

Launch the `Launch.py` file

## Control :

**ZQSD or ArrowKey :** To move as you would on an fps view

**A and E :** To go Up and down

**Numpad :** to rotate the camera :

- **4 :** Tilt left
- **6 :** Tilt Right
- **8 :** Tilt Up
- **2 :** Tilt Down

## Use a personal .obj file

Move you’re file in the `Obj` folder

Edit `Launch.py` and in the line `moteur.addobj(objtomesh.importobj("Obj/Suzan.obj"), 0, 0, 5)`, change Suzan.obj by you’re file name