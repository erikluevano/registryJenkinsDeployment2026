Característica: Iniciar sesión
Como usuario del sistema de cargas académicas
deseo iniciar sesión
para realizar mis actividades.

        Escenario: Credenciales válidas
            Dado que ingreso a la url: "http://app:8000/"
              Y capturo el usuario: "admin" y la contraseña "admin1234"
             Cuando presiono el botón Identificarse
             Entonces puedo ver el mensaje "Bienvenid@: admin al sistema de cargas académicas UAIE"

        Escenario: Credenciales invalidas
            Dado que ingreso a la url: "http://app:8000/"
              Y capturo el usuario: "admins" y la contraseña "admin123"
             Cuando presiono el botón Identificarse
             Entonces puedo ver el mensaje de error "Credenciales inválidas"