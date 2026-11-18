#trabajo 4 de programacion de el grupo: 213023A_2204

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
#remplacen esta linea de texto completa con el codigo

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

#Alquiler Equipo
#remplacen esta linea de texto completa con el codigo

#Asesoria Especializada

import logging
from servicio import Servicio


logger = logging.getLogger("SoftwareFJ")


class AsesoriaEspecializada(Servicio):
    """
    Clase encargada de gestionar los servicios
    de asesoria especializada.
    """

    def __init__(self, nombre, especialista, tarifa_hora, duracion):

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
#remplacen esta linea de texto completa con el codigo

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
#remplacen esta linea de texto completa con el codigo

#Simulaciones
#remplacen esta linea de texto completa con el codigo