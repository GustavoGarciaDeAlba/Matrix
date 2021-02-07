from datetime import date, datetime
from directorio import Directorio
from inodos import Inodo
import os
lists_Size = 100


class Usuario:

    def __init__(self, _Nombre, _Contraseña):
        self._Nombre = _Nombre
        self._Contraseña = _Contraseña
        self._InodoDelDirectorioActual = 0
        self._InodoDelDirectorioPapa = 0
        self._NombreDelDirectorioActual = ""
        self._LIL = []
        self._LBL = []
        self._Inodo = []
        self._Directorio = []
        self._PathDirectorios = []
        self.myInit()

    def myInit(self):
        self._PathDirectorios.append({0: self._Nombre})
        for i in range(lists_Size):
            self._LIL.append(i)
            self._LBL.append(i)
            self._Inodo.append(Inodo("", 0, "", "", True, ""))
            self._Directorio.append(Directorio())
        # Creación directorio "root"/"Nombre_Usuario"
        # Esta parte es MUY PROBABLE QUE DEBA SER CAMBIADA POR EXTRAER LA INFO DE MEMORIA
        self.crearDirectorio(self._Nombre)

    def crearArchivo(self, nombre_del_archivo):
        """ LISTO
            Algoritmo (En createf y copy):
            *el usuario corre creatf <nombre>
            *Se saca el primer inodo de LIL
            *Se crea el objeto inodo con sus respectivos datos para ese archivo
            *Se añade en el directorio correspondiente la información del nuevo archivo (inodo, nombre)
        """
        # Extremos el primer Inodo libre de LIL
        inodo_del_nuevo_archivo = self._LIL.pop(0)

        # Asignamos los nuevos valores al inodo extraido
        self._Inodo[inodo_del_nuevo_archivo]._Nombre = nombre_del_archivo
        self._Inodo[inodo_del_nuevo_archivo]._Fecha_de_creacion = date.today(
        ).strftime("%d/%m/%Y")
        self._Inodo[inodo_del_nuevo_archivo]._Fecha_ult_modificacion = date.today(
        ).strftime("%d/%m/%Y")
        self._Inodo[inodo_del_nuevo_archivo]._Libre = False
        self._Inodo[inodo_del_nuevo_archivo]._Permisos = "rwx"

        # buscamos indice en directorio
        indice_del_directorio_actual = self.buscarIndiceDeDirectorioPorInodo(
            self._InodoDelDirectorioActual)
        # Asignamos los nuevos valores al directorio correspondiente
        numArchivo = 0
        for inodoFile in self._Directorio[indice_del_directorio_actual]._Inodos:
            if inodoFile == -1:
                self._Directorio[indice_del_directorio_actual]._Inodos[numArchivo] = inodo_del_nuevo_archivo
                self._Directorio[indice_del_directorio_actual]._Nombre[numArchivo] = nombre_del_archivo
                break
            else:
                numArchivo += 1
        self._Directorio[indice_del_directorio_actual]._Libre = False

    def renameFile(self, nombre_del_archivo, nuevo_nombre_del_archivo):
        """ Algoritmo:
            *el usuario corre rename <nombre>
            *Buscar el inodo de ese archivo
            *Cambiamos el nombre del inodo correspondiente al nuevo nombre
            *Actualizamos la informacion dentro del directorio actual
            *Actualizamos archivo
        """
        inodo_del_archivo = self.buscarInodoPorNombreArchivo(
            nombre_del_archivo)
        self._Inodo[inodo_del_archivo]._Nombre = nuevo_nombre_del_archivo
        self.actualizarNombresDeArchivosEnDirectorios()
        self.actualizarArchivo(inodo_del_archivo)
        # LLAMAR A FUNCION ACTUALIZAR DIRECTORIO
        # actualizarArchivo

    def borrarArchivo(self, nombre_del_archivo):
        """ Algoritmo:
        *Buscamos el inodo del archivo que se desea borrar
        *Borramos la información de este archivo del directorio en el que se encuentre (dir_actual)
        *Borramos la información del inodo que poseia
        *Liberar el inodo que poseia
        *Agregar inodo liberado a LIL
    """
        numDirectorio = 0
        index_del_arhivo = 0
        inodo_del_archivo = self.buscarInodoPorNombreArchivo(
            nombre_del_archivo)
        for directorio in self._Directorio:
            if directorio._InodoDir == self._InodoDelDirectorioActual:
                for inodoArchivo in directorio._Inodos:
                    if inodoArchivo == inodo_del_archivo:
                        self._Directorio[numDirectorio]._Inodos[index_del_arhivo] = -1
                        self._Directorio[numDirectorio]._Nombre[index_del_arhivo] = ""
                    else:
                        index_del_arhivo += 1
            else:
                numDirectorio += 1

        # Mandamos llamar a liberar inodo
        self.liberarInodo(inodo_del_archivo)

    def editFile(self, nombre_del_archivo):
        """ Algoritmo: LISTO
        *el usuario corre edit <nombre>
        *Buscar el inodo de ese archivo
        *Actualizamos archivo
    """
        inodoDelArchivo = self.buscarInodoPorNombreArchivo(nombre_del_archivo)
        self.actualizarArchivo(inodoDelArchivo)

    def buscarInodoPorNombreArchivo(self, nombre_del_archivo):
        """ Algoritmo: LISTO
        *Recorrer lista _Inodo hasta que el nombre de uno de ellos coincidia con el ingresado
        *devolver numero de inodo
        """
        num_inodo = 0
        for inodo in self._Inodo:
            if inodo._Nombre == nombre_del_archivo:
                break
            else:
                num_inodo += 1
        return num_inodo

    def actualizar_dir_actual_cada_CD(self, nombre_del_directorio):
        """ Algoritmo: LISTO
        ES PARA ACTUALIZAR EL ATRIBUTO _InodoDelDirectorioActual CADA VEZ QUE SE HAGA CD
        *Si el nombre del archivo es .. eliminamos el directorio del diccionario y a inodo actual asignamos los valores del diccionario
        *Si el nombre del archivo es diferente de .. Recorrer lista _Directorio hasta que el nombre de uno de ellos coincidia con el ingresado
        """
        if nombre_del_directorio == "..":
            self._PathDirectorios.pop(len(self._PathDirectorios)-1)
            self._InodoDelDirectorioActual = list(self._PathDirectorios[len(
                self._PathDirectorios)-1].keys())[0]
            self._NombreDelDirectorioActual = list(self._PathDirectorios[len(
                self._PathDirectorios)-1].values())[0]
            try:
                self._InodoDelDirectorioPapa = list(self._PathDirectorios[len(
                    self._PathDirectorios)-2].keys())[0]
            except:
                self._InodoDelDirectorioPapa = 0
        else:
            for directorio in self._Directorio:
                if directorio._NombreDir == nombre_del_directorio:
                    self._InodoDelDirectorioPapa = list(self._PathDirectorios[len(
                        self._PathDirectorios)-1].keys())[0]
                    self._PathDirectorios.append(
                        {directorio._InodoDir: directorio._NombreDir})
                    self._NombreDelDirectorioActual = nombre_del_directorio
                    self._InodoDelDirectorioActual = directorio._InodoDir
                    break

    def actualizarArchivo(self, inodo_del_archivo):
        """ Algoritmo: LISTO
        *Es llamado por otras funciones
        *Modificamos la fecha de modificacion del inodo correspondiete
        *Modificamos el tamaño del inodo correspondiente
    """
        d1 = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._Inodo[inodo_del_archivo]._Fecha_ult_modificacion = d1
        relative_path = ""
        for element in self._PathDirectorios:
            relative_path += list(element.values())[0] + "/"
        path_for_size = './files/' + relative_path + \
            self._Inodo[inodo_del_archivo]._Nombre + ".txt"
        self._Inodo[inodo_del_archivo]._Tamanio = os.stat(
            path_for_size).st_size

    def crearDirectorio(self, nombre_del_directorio):
        """ Algoritmo: LISTO
        # El usuarios ingresa createdir <nombre_del_directorio>
        # Se busca un directorio libre dentro del arreglo de directorios del usuario
        # Obtener un inodo de la LIL este sera inodo_del_nuevo_directorio
        # inodo_del_nuevo_directorio sera puesto dentro del primer directorio libre que se encuentre de la lista de directoris del usuario
        # Se añadira el nombre_del_directorio al atributo de este directorio
        # Se actualizara su atributo _Libre a False
        # Actualizamos nuestra lista de inodos _Inodo con la inforamción que se acaba de ocupar
        """
        numDir = 0
        for directorioLibre in self._Directorio:
            if directorioLibre._Libre == True:
                inodo_del_nuevo_directorio = self._LIL.pop(0)

                self._Directorio[numDir]._InodoDir = inodo_del_nuevo_directorio
                self._Directorio[numDir]._NombreDir = nombre_del_directorio
                self._Directorio[numDir]._Libre = False
                # Se actualiza Inodo ahora
                self._Inodo[inodo_del_nuevo_directorio]._Nombre = nombre_del_directorio
                self._Inodo[inodo_del_nuevo_directorio]._Fecha_de_creacion = date.today(
                ).strftime("%d/%m/%Y")
                self._Inodo[inodo_del_nuevo_directorio]._Fecha_ult_modificacion = date.today(
                ).strftime("%d/%m/%Y")
                self._Inodo[inodo_del_nuevo_directorio]._Libre = False
                self._Inodo[inodo_del_nuevo_directorio]._Permisos = "rwx"
                break
            else:
                numDir += 1

    def actualizarNombresDeArchivosEnDirectorios(self):
        """ SE VA A UTILIZAR EN RENOMBRAR
        * Se introduce el inodo del directorio al cual queremos actualizar los nombres de sus archivos
        * Buscamos ese directorio dentro de nuestro lista de directorios _Directorio 
        * Buscamos los inodos de sus archivos dentro del arreglo _Inodos[]
        * Actualizamos los valores de _Nombre[] de acuerdo a su igual en el arreglo del usuario _Inodo[]
        """
        numDir = 0
        numNombre = 0
        for directorio_a_comparar in self._Directorio:
            # se selecciona el directorio que vamos a usar
            if self._InodoDelDirectorioActual == directorio_a_comparar._InodoDir:
                for inodoDentroDelDirectorio in directorio_a_comparar._Inodos:
                    if inodoDentroDelDirectorio != -1:  # se filtran los inodos que estan ligados a archivos
                        self._Directorio[numDir]._Nombre[numNombre] = self._Inodo[inodoDentroDelDirectorio]._Nombre
                        numNombre += 1
                    else:
                        break
                break
            numDir += 1

    def borrarDirectorio(self, nombre_del_directorio):
        """
        * Buscamos el directorio que corresponda con el nombre ingresado
        * Inicializamos de vuelta todos sus valores a 0 o null
        * Dar de baja la información de su inodo en el arreglo _Inodo del usuario
        * Se devuelve su inodo a LIL
        """
        numDir = 0
        inodo_del_directorio = self.buscarInodoPorNombreArchivo(
            nombre_del_directorio)
        for directorio in self._Directorio:
            if directorio._InodoDir == inodo_del_directorio:
                for nombreArchivo in self._Directorio[numDir]._Nombre:
                    self.borrarArchivo(nombreArchivo)
                self._Directorio[numDir]._InodoDir = -1
                self._Directorio[numDir]._NombreDir = ""
                self._Directorio[numDir]._Libre = True
                self._Directorio[numDir]._Inodos.clear()
                self._Directorio[numDir]._Nombre.clear()
                for i in range(10):
                    self._Directorio[numDir]._Inodos.append(-1)
                    self._Directorio[numDir]._Nombre.append("")
                break
            else:
                numDir += 1
        self.liberarInodo(inodo_del_directorio)

    def renombrarDirectorio(self, nombre_del_directorio, nuevo_nombre_del_directorio):
        """ Algoritmo:
        *el usuario corre renameDir <nombre>
        *Buscar el inodo del del directorio deseado
        *Cambiamos el nombre del directorio al nuevo nombre, para buscarlo usamos su inodo
        *Actualizamos la informacion dentro del directorio actual
        *Actualizamos fecha_de_modificacion y otras cosas (si hay mas cosas que actualizar)
    """
        numDir = 0
        inodo_del_directorio = self.buscarInodoPorNombreArchivo(
            nombre_del_directorio)
        for directorio in self._Directorio:
            if directorio._InodoDir == inodo_del_directorio:
                self._Directorio[numDir]._NombreDir = nuevo_nombre_del_directorio
                break
            else:
                numDir += 1
        self._Inodo[inodo_del_directorio]._Nombre = nuevo_nombre_del_directorio
        self.actualizarNombresDeArchivosEnDirectorios()
        self.actualizarArchivo(inodo_del_directorio)

    def liberarInodo(self, inodo_a_liberar):
        """ Algoritmo
        * Usamos ese inodo_a_liberar como indice de _Inodo[] del usario
        * Devolvemos todos sus atributos a 0 o null
        * Se agrega ese inodo_a_liberar a _LIL[]
        """
        self._Inodo[inodo_a_liberar]._Nombre = ""
        self._Inodo[inodo_a_liberar]._Tamanio = 0
        self._Inodo[inodo_a_liberar]._Fecha_de_creacion = ""
        self._Inodo[inodo_a_liberar]._Fecha_ult_modificacion = ""
        self._Inodo[inodo_a_liberar]._Libre = True
        self._Inodo[inodo_a_liberar]._Permisos = ""
        self._LIL.append(inodo_a_liberar)
        self._LIL.sort()


    def buscarIndiceDeDirectorioPorInodo(self, inodo_del_directorio):
        numDirectorio = 0
        for directorio in self._Directorio:
            if directorio._InodoDir == inodo_del_directorio:
                break
            else:
                numDirectorio += 1
        return numDirectorio


# Pruebas
'''
usr = Usuario("Jorge", "cisco")
usr.crearDirectorio("DirectorioPrueba")
usr.actualizar_dir_actual_cada_CD("DirectorioPrueba")
usr.crearArchivo("poke")
usr.crearArchivo("poke2")
usr.crearArchivo("poke3")
print("Directorio creado: ", usr._Inodo[1])
print("datos de directorio borrado", usr._Directorio[1]._NombreDir)
print("datos de directorio borrado", usr._Directorio[1]._InodoDir)
print("datos de directorio borrado", usr._Directorio[1]._Libre)
print("datos de directorio borrado", usr._Directorio[1]._Nombre)
print("datos de directorio borrado", usr._Directorio[1]._Inodos)

print("Archivo creado: ", usr._Inodo[2])
print("archivo creado: ", usr._Inodo[3])
print("archivo creado: ", usr._Inodo[4])
usr.borrarDirectorio("DirectorioPrueba")
print("Directorio Borrado: ", usr._Inodo[1])
print("datos de directorio borrado", usr._Directorio[1]._NombreDir)
print("datos de directorio borrado", usr._Directorio[1]._InodoDir)
print("datos de directorio borrado", usr._Directorio[1]._Libre)
print("datos de directorio borrado", usr._Directorio[1]._Nombre)
print("datos de directorio borrado", usr._Directorio[1]._Inodos)

print("Archivo creado: ", usr._Inodo[2])
print("archivo creado: ", usr._Inodo[3])
print("archivo creado: ", usr._Inodo[4])
#usr.editFile("poke")
#print("Archivo creado: ", usr._Inodo[1])'''

