#trabajo 4 de programacion de el grupo: 213023A_2204
#Por: Karen, Karol y Andres
#Cliente

import re
import logging
import os
import unicodedata


os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("SoftwareFJ")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    archivo_log = logging.FileHandler(
        "logs/sistema.log",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    archivo_log.setFormatter(formato)
    logger.addHandler(archivo_log)


class ErrorCliente(Exception):
    """Excepcion para errores relacionados con los clientes."""
    pass


class Cliente:

    def __init__(self, nombre, documento, correo):

        self.__nombre = None
        self.__documento = None
        self.__correo = None

        self.set_nombre(nombre)
        self.set_documento(documento)
        self.set_correo(correo)

        logger.info(
            "Cliente registrado correctamente: documento %s",
            self.__documento
        )

    # METODOS GET Y SET DEL NOMBRE

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if self.validar_nombre(nombre):
            self.__nombre = nombre.strip()
            logger.info("Nombre del cliente actualizado.")
        else:
            logger.warning("Intento de registrar un nombre invalido.")
            raise ErrorCliente(
                "El nombre debe contener unicamente letras y espacios."
            )

    # METODOS GET Y SET DEL DOCUMENTO

    def get_documento(self):
        return self.__documento

    def set_documento(self, documento):
        if self.validar_documento(documento):
            self.__documento = str(documento).strip()
            logger.info("Documento del cliente actualizado.")
        else:
            logger.warning("Intento de registrar un documento invalido.")
            raise ErrorCliente(
                "El documento debe contener entre 5 y 15 numeros."
            )

    # METODOS GET Y SET DEL CORREO

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        if self.validar_correo(correo):
            self.__correo = correo.strip()
            logger.info("Correo del cliente actualizado.")
        else:
            logger.warning("Intento de registrar un correo invalido.")
            raise ErrorCliente(
                "El correo electronico no tiene un formato valido."
            )

    # METODOS DE VALIDACION

    def validar_nombre(self, nombre):

        if not isinstance(nombre, str) or not nombre.strip():
            return False

        normalizado = unicodedata.normalize("NFD", nombre)
        normalizado = "".join(
            letra for letra in normalizado
            if unicodedata.category(letra) != "Mn"
        )

        patron = r"^[A-Za-z\s]+$"

        return bool(re.fullmatch(patron, normalizado.strip()))

    def validar_documento(self, documento):

        if not str(documento).strip().isdigit():
            return False

        return 5 <= len(str(documento).strip()) <= 15

    def validar_correo(self, correo):

        if not isinstance(correo, str):
            return False

        patron = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"

        return bool(re.fullmatch(patron, correo.strip()))

    # MOSTRAR INFORMACION DEL CLIENTE

    def mostrar_datos(self):

        print("\n========== DATOS DEL CLIENTE ==========")
        print(f"Nombre: {self.get_nombre()}")
        print(f"Documento: {self.get_documento()}")
        print(f"Correo: {self.get_correo()}")
        print("=======================================\n")


# PRUEBA DEL FUNCIONAMIENTO DE LA CLASE

if __name__ == "__main__":

    print("SISTEMA DE GESTION DE CLIENTES - SOFTWARE FJ")

    try:
        cliente1 = Cliente(
            "Karen Tatiana Morantes",
            "1234567890",
            "cliente@gmail.com"
        )

        print("\nCliente registrado exitosamente.")

        cliente1.mostrar_datos()

        # Consultar informacion mediante los metodos get

        print("Consultando informacion:")
        print("Nombre:", cliente1.get_nombre())
        print("Documento:", cliente1.get_documento())
        print("Correo:", cliente1.get_correo())

        # Modificar informacion mediante los metodos set

        cliente1.set_nombre("Karen Tatiana Morantes Bolivar")
        cliente1.set_correo("karen@gmail.com")

        print("\nDatos actualizados:")
        cliente1.mostrar_datos()

    except ErrorCliente as error:
        print("Error al gestionar el cliente:", error)
        logger.error("Error de cliente: %s", error)

    except Exception as error:
        print("Se presento un error inesperado:", error)
        logger.exception("Error inesperado durante la prueba.")

    finally:
        print("Finalizo la ejecucion del modulo de clientes.")


#Servicio (Abstracta)
from abc import ABC, abstractmethod

class Servicio(ABC):
    
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float):
        self.codigo = codigo
        self.nombre = nombre
        self._tarifa_hora = tarifa_hora

    def _aplicar_ajustes(self, costo, impuesto=0, descuento=0):
        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 100.")

        if impuesto < 0:
            raise DatosInvalidosError("El impuesto no puede ser negativo.")

        costo -= costo * (descuento / 100)
        costo += costo * (impuesto / 100)

        return round(costo, 2)
    
    @abstractmethod
    def calcular_costo(self):
        pass
    
    @abstractmethod
    def describir(self):
        pass
    
    @abstractmethod
    def validar_parametros(self):
        pass  

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
        if not isinstance(duracion, (int, float)) or isinstance(duracion,bool) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")
        costo = self._tarifa_hora * duracion
        return self._aplicar_ajustes(costo, impuesto, descuento)

    def describir(self) -> str:
        return f"Sala: {self.nombre}, capacidad:{self.capacidad} personas"

#Alquiler Equipo
class AlquilerEquipo(Servicio):
    
    def __init__(self, codigo: str, nombre: str, tarifa_hora: float,
                 cantidad_disponible: int, horas_alquiler: int):

        super().__init__(codigo, nombre, tarifa_hora)
        self.cantidad_disponible = cantidad_disponible
        self.horas_alquiler = horas_alquiler

        if not self.validar_parametros():
            raise DatosInvalidosError(
                "Los datos del equipo no son validos "
            )
    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad<= 0:
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser positiva"
            )

        costo = (
            self._tarifa_hora
            * self.horas_alquiler
            * cantidad
        )

        return self._aplicar_ajustes(
            costo, impuesto, descuento
        )

    def describir(self):

        return (
            f"Equipo: {self.nombre}, "
            f"tarifa por hora: ${self._tarifa_hora}, "
            f"horas de alquiler: {self.horas_alquiler}, "
            f"disponibles: {self.cantidad_disponible}"
        )

    def validar_parametros(self, cantidad=1):

        if not self.codigo or not self.nombre:
            raise DatosInvalidosError(
                "El codigo y el nombre son obligatorios."
            )

        if not isinstance(self._tarifa_hora, (int, float)) or self._tarifa_hora <= 0:
            raise DatosInvalidosError(
                "La tarifa debe ser positiva."
            )

        if not isinstance(self.cantidad_disponible, int) or isinstance(self.cantidad_disponible, bool) or self.cantidad_disponible < 0:
            raise DatosInvalidosError(
                "La cantidad disponible no es valida."
            )

        if not isinstance(self.horas_alquiler, int) or isinstance(self.horas_alquiler, bool) or self.horas_alquiler <= 0:
            raise DatosInvalidosError(
                "Las horas de alquiler deben ser positivas."
            )

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser positiva."
            )

        if cantidad > self.cantidad_disponible:
            raise ServicioNoDisponibleError(
                "No hay suficientes equipos disponibles."
            )

        return True

#Asesoria Especializada

import logging


logger = logging.getLogger("SoftwareFJ")


class AsesoriaEspecializada(Servicio):
    """
    Clase encargada de gestionar los servicios
    de asesoria especializada.
    """

    def __init__(self, nombre, especialista, tarifa_hora, duracion):

        super().__init__("ASE001", nombre, tarifa_hora)

        self.__nombre = nombre
        self.__especialista = especialista
        self.__tarifa_hora = tarifa_hora
        self.__duracion = duracion

        self.validar_parametros()

        logger.info("Asesoria especializada creada correctamente.")

    # METODO PARA VALIDAR LOS PARAMETROS

    def validar_parametros(self):

        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ValueError("El nombre de la asesoria no es valido.")

        if not isinstance(self.__especialista, str) or not self.__especialista.strip():
            raise ValueError("El nombre del especialista no es valido.")

        if not isinstance(self.__tarifa_hora, (int, float)):
            raise ValueError("La tarifa por hora debe ser numerica.")

        if self.__tarifa_hora <= 0:
            raise ValueError("La tarifa por hora debe ser mayor que cero.")

        if not isinstance(self.__duracion, (int, float)):
            raise ValueError("La duracion debe ser numerica.")

        if self.__duracion <= 0:
            raise ValueError("La duracion debe ser mayor que cero.")

        return True

    # METODO PARA CALCULAR EL COSTO

    def calcular_costo(self, descuento=0, impuesto=0):

        try:
            self.validar_parametros()

            if not isinstance(descuento, (int, float)):
                raise ValueError("El descuento debe ser numerico.")

            if not isinstance(impuesto, (int, float)):
                raise ValueError("El impuesto debe ser numerico.")

            if descuento < 0 or descuento > 100:
                raise ValueError("El descuento debe estar entre 0 y 100.")

            if impuesto < 0 or impuesto > 100:
                raise ValueError("El impuesto debe estar entre 0 y 100.")

            costo_base = self.__tarifa_hora * self.__duracion

            valor_descuento = costo_base * (descuento / 100)

            subtotal = costo_base - valor_descuento

            valor_impuesto = subtotal * (impuesto / 100)

            costo_total = subtotal + valor_impuesto

            logger.info("Costo de asesoria calculado correctamente.")

            return round(costo_total, 2)

        except ValueError as error:
            logger.error("Error al calcular el costo: %s", error)
            raise

        except Exception as error:
            logger.exception("Error inesperado al calcular el costo.")
            raise RuntimeError(
                "No fue posible calcular el costo de la asesoria."
            ) from error

    # METODO PARA DESCRIBIR EL SERVICIO

    def describir(self):

        return (
            "\n===== ASESORIA ESPECIALIZADA =====\n"
            f"Nombre del servicio: {self.__nombre}\n"
            f"Especialista: {self.__especialista}\n"
            f"Tarifa por hora: ${self.__tarifa_hora:,.2f}\n"
            f"Duracion: {self.__duracion} horas\n"
            f"Costo total: ${self.calcular_costo():,.2f}\n"
            "=================================="
        )


# PRUEBA DEL FUNCIONAMIENTO DE LA CLASE

if __name__ == "__main__":

    print("SISTEMA DE ASESORIAS - SOFTWARE FJ")

    try:
        asesoria = AsesoriaEspecializada(
            "Asesoria en desarrollo de software",
            "Especialista en sistemas",
            50000,
            2
        )

        print(asesoria.describir())

        print("\nCosto con descuento del 10%:")
        print("$", asesoria.calcular_costo(descuento=10))

        print("\nCosto con impuesto del 19%:")
        print("$", asesoria.calcular_costo(impuesto=19))

        print("\nCosto con descuento e impuesto:")
        print("$", asesoria.calcular_costo(
            descuento=10,
            impuesto=19
        ))

    except ValueError as error:
        print("Error de validacion:", error)

    except Exception as error:
        print("Se presento un error:", error)

    finally:
        print("\nFinalizo la ejecucion del modulo de asesoria.")


#Reserva

class Reserva:
    
    def __init__(self, cliente, servicio, duracion, personas=1, cantidad=1):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.personas = personas
        self.cantidad = cantidad
        self.estado = "pendiente"
        
    def confirmar(self):
        
        if self.estado != "pendiente":
            return False
        if isinstance(self.servicio, ReservaSala):
            self.servicio.validar_parametros(
                personas=self.personas
            )

        elif isinstance(self.servicio, AlquilerEquipo):
            self.servicio.validar_parametros(
                cantidad=self.cantidad
            )

            self.servicio.cantidad_disponible -= self.cantidad

        else:
            self.servicio.validar_parametros()

        self.estado = "confirmada"

        return True

    def procesar(self):
        if self.estado == "pendiente":
            if not self.confirmar():
                raise ReservaInvalidaError(
                    "no se puede confirmar reserva"
                )

        if self.estado != "confirmada":
            raise EstadoReservaError(
                "La reserva no esta confirmada."
            )

        elif isinstance(self.servicio, ReservaSala):
            return self.servicio.calcular_costo(
                self.duracion
            )

        elif isinstance(self.servicio, AlquilerEquipo):
            return self.servicio.calcular_costo(
                cantidad=self.cantidad
            )

        elif isinstance(self.servicio, AsesoriaEspecializada):
            return self.servicio.calcular_costo()

        else:
            raise ReservaInvalidaError(
                "Tipo de servicio no reconocido."
            )
        
    def cancelar(self):
        if self.estado == "cancelada":
            return False
        if self.estado == "confirmada":
            if isinstance(self.servicio, AlquilerEquipo):
                self.servicio.cantidad_disponible += self.cantidad
                
        self.estado = "cancelada"
        return True

    def mostrar_reserva(self):

        print("\n========== INFORMACION DE LA RESERVA ==========")
        print("Cliente:", self.cliente.get_nombre())
        print("Servicio:", self.servicio.describir())
        print("Duracion:", self.duracion)
        print("Estado:", self.estado)
        print("================================================")

#Excepciones Personalizadas

class SistemaError(Exception):
    """Excepcion base del sistema."""


class DatosInvalidosError(SistemaError):
    """Datos ingresados no validos."""


class ClienteNoEncontradoError(SistemaError):
    """El cliente solicitado no existe."""


class ServicioNoDisponibleError(SistemaError):
    """El servicio o los recursos no estan disponibles."""


class ReservaInvalidaError(SistemaError):
    """La reserva no puede realizarse."""


class EstadoReservaError(SistemaError):
    """La operacion no corresponde al estado de la reserva."""

#Logger

import logging
import os


class Logger:
    """
    Clase encargada de configurar y gestionar
    los registros de eventos y errores del sistema.
    """

    def __init__(self):
        self.__logger = None
        self.configurar_logger()

    # METODO PARA CONFIGURAR EL LOGGER

    def configurar_logger(self):

        os.makedirs("logs", exist_ok=True)

        self.__logger = logging.getLogger("SoftwareFJ")

        self.__logger.setLevel(logging.INFO)

        # Evitar duplicar los registros
        if not self.__logger.handlers:

            # Configurar archivo de registros
            archivo = logging.FileHandler(
                "logs/sistema.log",
                encoding="utf-8"
            )

            formato = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            archivo.setFormatter(formato)

            self.__logger.addHandler(archivo)

        return self.__logger

    # METODO PARA REGISTRAR EVENTOS

    def registrar_evento(self, mensaje):

        try:
            if not isinstance(mensaje, str) or not mensaje.strip():
                raise ValueError("El mensaje del evento no es valido.")

            self.__logger.info(mensaje)

            print("Evento registrado correctamente.")

        except ValueError as error:
            self.registrar_error(str(error))
            raise

        except Exception as error:
            self.registrar_error(
                "Error inesperado al registrar evento: " + str(error)
            )
            raise

    # METODO PARA REGISTRAR ERRORES

    def registrar_error(self, mensaje):

        try:
            if not isinstance(mensaje, str) or not mensaje.strip():
                raise ValueError("El mensaje del error no es valido.")

            self.__logger.error(mensaje)

            print("Error registrado en el archivo de logs.")

        except Exception as error:
            print("No fue posible registrar el error:", error)


# PRUEBA DEL FUNCIONAMIENTO DE LA CLASE

if __name__ == "__main__":

    print("SISTEMA DE REGISTRO - SOFTWARE FJ")

    registro = Logger()

    try:
        registro.registrar_evento(
            "El sistema inicio correctamente."
        )

        registro.registrar_evento(
            "Se registro un nuevo cliente."
        )

        registro.registrar_evento(
            "Se creo una nueva reserva."
        )

        registro.registrar_error(
            "Error de prueba: servicio no disponible."
        )

        print("\nRegistros realizados correctamente.")

    except Exception as error:
        print("Se presento un problema:", error)

    finally:
        print("Finalizo la ejecucion del modulo Logger.")

#Simulaciones
def ejecutar_prueba(numero, descripcion, funcion):

    print("\n" + "=" * 50)
    print("PRUEBA", numero, ":", descripcion)
    print("=" * 50)

    try:
        funcion()
        print("Resultado: prueba ejecutada correctamente.")

    except Exception as error:
        print("Error controlado:", type(error).__name__, "-", error)


# PRUEBA 1: Registrar cliente valido

def prueba_1():

    global cliente_prueba

    cliente_prueba = Cliente(
        "Andres Felipe",
        "1234567890",
        "andres@gmail.com"
    )

    cliente_prueba.mostrar_datos()


# PRUEBA 2: Registrar cliente con correo invalido

def prueba_2():

    try:
        Cliente("Carlos Perez", "9876543210", "correo_invalido")
    except ErrorCliente as error:
        print("Validacion correcta:", error)


# PRUEBA 3: Crear una sala

def prueba_3():

    global sala_prueba

    sala_prueba = ReservaSala(
        "SAL001",
        "Sala de reuniones",
        50000,
        10
    )

    print(sala_prueba.describir())


# PRUEBA 4: Procesar una reserva de sala

def prueba_4():

    reserva = Reserva(
        cliente_prueba,
        sala_prueba,
        2,
        personas=5
    )

    reserva.confirmar()
    reserva.mostrar_reserva()

    print("Costo total: $", reserva.procesar())


# PRUEBA 5: Superar la capacidad de una sala

def prueba_5():

    try:
        reserva = Reserva(
            cliente_prueba,
            sala_prueba,
            2,
            personas=15
        )

        reserva.confirmar()

    except DatosInvalidosError as error:
        print("Validacion correcta:", error)


# PRUEBA 6: Crear equipo para alquiler

def prueba_6():

    global equipo_prueba

    equipo_prueba = AlquilerEquipo(
        "EQ001",
        "Video Beam",
        20000,
        5,
        3
    )

    print(equipo_prueba.describir())


# PRUEBA 7: Reservar dos equipos

def prueba_7():

    global reserva_equipo

    reserva_equipo = Reserva(
        cliente_prueba,
        equipo_prueba,
        3,
        cantidad=2
    )

    reserva_equipo.confirmar()

    print("Equipos disponibles:", equipo_prueba.cantidad_disponible)
    print("Costo total: $", reserva_equipo.procesar())


# PRUEBA 8: Cancelar alquiler de equipos

def prueba_8():

    reserva_equipo.cancelar()

    print("Estado:", reserva_equipo.estado)
    print("Equipos disponibles:", equipo_prueba.cantidad_disponible)


# PRUEBA 9: Crear asesoria especializada

def prueba_9():

    global asesoria_prueba

    asesoria_prueba = AsesoriaEspecializada(
        "Asesoria en desarrollo de software",
        "Especialista en sistemas",
        50000,
        2
    )

    print(asesoria_prueba.describir())


# PRUEBA 10: Calcular asesoria con descuento

def prueba_10():

    costo = asesoria_prueba.calcular_costo(descuento=10)

    print("Costo con descuento: $", costo)


# PRUEBA 11: Procesar reserva de asesoria

def prueba_11():

    reserva = Reserva(
        cliente_prueba,
        asesoria_prueba,
        2
    )

    reserva.confirmar()
    reserva.mostrar_reserva()

    print("Costo total: $", reserva.procesar())


# PRUEBA 12: Registrar eventos en Logger

def prueba_12():

    registro = Logger()

    registro.registrar_evento(
        "Simulacion finalizada correctamente."
    )

    registro.registrar_error(
        "Error de prueba del sistema."
    )

# PRUEBA 13: Intentar crear una sala con capacidad invalida
def prueba_13():
    try:
        sala_invalida = ReservaSala(
            "SAL002",
            "Sala de capacidad invalida",
            50000,
            0
        )
    except DatosInvalidosError as error:
        print("Validacion correcta:", error)

# EJECUCION DE LAS SIMULACIONES

if __name__ == "__main__":

    print("\nSISTEMA INTEGRAL SOFTWARE FJ")
    print("EJECUCION DE SIMULACIONES")

    ejecutar_prueba(1, "Registrar cliente valido", prueba_1)
    ejecutar_prueba(2, "Validar correo invalido", prueba_2)
    ejecutar_prueba(3, "Crear sala de reuniones", prueba_3)
    ejecutar_prueba(4, "Procesar reserva de sala", prueba_4)
    ejecutar_prueba(5, "Validar capacidad de sala", prueba_5)
    ejecutar_prueba(6, "Crear equipo para alquiler", prueba_6)
    ejecutar_prueba(7, "Reservar dos equipos", prueba_7)
    ejecutar_prueba(8, "Cancelar alquiler de equipos", prueba_8)
    ejecutar_prueba(9, "Crear asesoria especializada", prueba_9)
    ejecutar_prueba(10, "Calcular asesoria con descuento", prueba_10)
    ejecutar_prueba(11, "Procesar reserva de asesoria", prueba_11)
    ejecutar_prueba(12, "Registrar eventos en Logger", prueba_12)
    ejecutar_prueba(13, "Intentar crear una salacon capacidad invalida", prueba_13)

    print("\nFINALIZARON LAS SIMULACIONES")