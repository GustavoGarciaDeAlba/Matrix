import os

lista_de_path = [{0: "Jorge"}]
lista_de_path.append({1: "DirA"})
lista_de_path.append({3: "DirB"})
print(lista_de_path)

path_size = ""
for element in lista_de_path:
    path_size += list(element.values())[0] + "/"
print(path_size)
"""
FALTA
    PRIORIDAD CONCEPTO
    2   |   GUARDAR INFORMACION EN MEMORIA
    2   |   EXTRAER INFORMACION DE MEMORIA - LINEA 31 usuario.py
    2   |   METER FUNCIONES DE REGISTROS EN app.py (GUSTAVO)
    3   |   CREAR COMANDO PARA MOSTRAR EN QUE CARPETA ESTAMOS
    4   |   CREAR COMANDO PARA ABRIR ARCHIVO TXT start <file_name> usando os.startfile('file.txt')
    5   |   POSIBLE (CREAR COMANDO PARA MOVER ARCHIVO DE LUGAR)
"""
# El tamaño de la carpeta actual se actualiza cuando un archivo es creado/editado/borrado
# El tamano de un archivo se actualiza cuando ese archivo es editado
