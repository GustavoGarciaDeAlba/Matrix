class Inodo:

    def __init__(self, _Nombre, _Tamanio, _Fecha_de_creacion, _Fecha_ult_modificacion, _Libre, _Permisos):
        self._Nombre = _Nombre
        self._Tamanio = _Tamanio
        self._Fecha_de_creacion = _Fecha_de_creacion
        self._Fecha_ult_modificacion = _Fecha_ult_modificacion
        self._Libre = _Libre
        self._Permisos = _Permisos

    def __str__(self):
        return "{} {} {} {} {} {}".format(self._Nombre, self._Tamanio, self._Fecha_de_creacion, self._Fecha_ult_modificacion, self._Libre, self._Permisos)
