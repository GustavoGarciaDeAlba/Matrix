class Directorio:

    def __init__(self):
        self. _NombreDir = ""  # Nombre del directorio
        self._InodoDir = 0  # Inodo del directorio
        self._Libre = True  # Estado del directorio 0 si no existe ese, 1 si ya existe        self. _Inodos = []  # Inodos de los archivos que guarda este directorio
        self._Nombre = []  # Nombre de los archivos que guarda este directorio
        self._Inodos = []  # Inodos de los archivos que guarda este directorio
        self.myInit()

    def myInit(self):
        # cada directorio tendra 10 archivos maximo
        for i in range(10):
            self._Inodos.append(-1)
            self._Nombre.append("")


# def crearDirectorio(self, nombre_del_directorio, inodo_del_directorio):
        # El usuarios ingresa createdir <nombre_del_directorio>
        # Se busca un directorio libre dentro del arreglo de directorios del usuario "esta parte va en usuario"
        # inodo_del_directorio es obtenido desde el obj usuario y se le agega al inodod de este directorio
        # El campo libre de este directorio pasa a estar ocupado, que es 0
        # Nota: quitar inodo de LIL
        # Nota: Actualizar los datos en el arreglo de clase Inodo del usuario con los datos de este nuevo directorio

#    def agregarArchivoADirectorio(self, inodo_del_archivo, nombre_del_archivo):
        # EL usuario llama creatf <nombre_de_archivo> despues de moverse usando cd a este directorio
        # inodo_del_archivo  se saca de la LIL y se le asigna dentro de este directorio
        # inodo_del_archivo y nombre_Del_archivo se actualiza dentro del arreglo Inodo del usuario
