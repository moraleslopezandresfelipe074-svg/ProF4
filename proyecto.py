#trabajo 4 de programacion de el grupo: 213023A_2204

# Reserva Sala
class ReservaSala(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float,
                 capacidad: int):
        super().__init__(codigo, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, **kwargs) -> None:
        personas = kwargs.get("personas")
        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise DatosInvalidosError("Debe indicar una cantidad valida de personas.")
        if personas > self.capacidad:
            raise DatosInvalidosError("La cantidad de personas supera la capacidad.")

    def calcular_costo(self, duracion: float, *args,
                       impuesto: float = 0, descuento: float = 0,
                       **kwargs) -> float:
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")
        costo = self._tarifa_hora * duracion
        return self._aplicar_ajustes(costo, impuesto, descuento)

    def describir(self) -> str:
        return f"Sala: {self.nombre}, capacidad {self.capacidad}class ReservaSala(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float,
                 capacidad: int):
        super().__init__(codigo, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, **kwargs) -> None:
        personas = kwargs.get("personas")
        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise DatosInvalidosError("Debe indicar una cantidad valida de personas.")
        if personas > self.capacidad:
            raise DatosInvalidosError("La cantidad de personas supera la capacidad.")

    def calcular_costo(self, duracion: float, *args,
                       impuesto: float = 0, descuento: float = 0,
                       **kwargs) -> float:
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")
        costo = self._tarifa_hora * duracion
        return self._aplicar_ajustes(costo, impuesto, descuento)

    def describir(self) -> str:
        return f"Sala: {self.nombre}, capacidad {self.capacidad}