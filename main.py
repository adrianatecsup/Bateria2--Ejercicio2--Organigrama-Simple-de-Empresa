# ================================================================
# PROYECTO: ORGANIGRAMA SIMPLE DE EMPRESA
# Curso: Estructura de Datos y Algoritmos
# ================================================================

# ================================================================
# CLASE EMPLEADO: Guarda los datos de cada trabajador.
# ================================================================

class Empleado:

    def __init__(self, id, nombre, cargo, departamento, salario):
        self.id = id
        self.nombre = nombre
        self.cargo = cargo
        self.departamento = departamento
        self.salario = salario

    def __str__(self):
        return (
            f"ID: {self.id} | Nombre: {self.nombre} | "
            f"Cargo: {self.cargo} | Departamento: {self.departamento} | "
            f"Salario: S/ {self.salario:.2f}"
        )


# ================================================================
# CLASE NODO: Cada nodo representa a un empleado dentro del arbol.
# ================================================================

class Nodo:

    def __init__(self, valor, padre):
        self.valor = valor          # Empleado almacenado.
        self.padre = padre          # Nodo del supervisor.
        self.hijo = None            # Lista circular de los subordinados.
        self.nodo_siguiente = None  # Siguiente hermano dentro de la lista circular.


# ================================================================
# CLASE CSLL: Lista Circular Simplemente Enlazada.
# ================================================================

class csll:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    # Inserta un nuevo hijo al final de la lista circular.
    def append(self, valor, padre):
        nuevo_nodo = Nodo(valor, padre)
        return self.append_nodo(nuevo_nodo)

    # Inserta un nodo que ya existe, conservando sus propios hijos.
    # Este metodo se utiliza cuando se cambia de supervisor.
    def append_nodo(self, nuevo_nodo):
        if self.cabeza is None and self.cola is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            self.cola.nodo_siguiente = self.cabeza
        else:
            self.cola.nodo_siguiente = nuevo_nodo
            nuevo_nodo.nodo_siguiente = self.cabeza
            self.cola = nuevo_nodo
        self.tamano += 1
        return nuevo_nodo

    # Recorre la lista una sola vez y ejecuta una accion por cada nodo.
    # La funcion recibida debe ser una funcion definida por el programa.
    def recorrer(self, accion):
        if self.cabeza is None:
            return
        actual = self.cabeza
        while True:
            accion(actual)
            actual = actual.nodo_siguiente

            # Como la lista es circular, detenemos el recorrido 
            # cuando regresamos a la cabeza.
            if actual == self.cabeza:
                break


# ================================================================
# CLASE TREE: Administra el organigrama completo.
# ================================================================

class tree:
    MAX_EMPLEADOS = 30
    def __init__(self):
        self.raiz = None
        self.tamano = 0

    # ------------------------------------------------------------
    # BUSCAR EMPLEADO POR ID: Recorre el arbol en profundidad.
    # ------------------------------------------------------------

    def _buscar_recursivo(self, nodo, id):
        if nodo is None:
            return None
        if nodo.valor.id == id:
            return nodo
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                encontrado = self._buscar_recursivo(actual, id)
                if encontrado is not None:
                    return encontrado
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return None

    def buscar_empleado(self, id):
        return self._buscar_recursivo(self.raiz, id)

    # ------------------------------------------------------------
    # INSERTAR EMPLEADO: 
    # Si el arbol esta vacio, el primer empleado sera la raiz.
    # Los demas empleados se agregan a la CSLL de su supervisor.
    # ------------------------------------------------------------

    def insert(self, empleado, id_supervisor=None):

        if self.tamano >= self.MAX_EMPLEADOS:
            print("No se pueden registrar mas de 30 empleados.")
            return False

        if self.buscar_empleado(empleado.id) is not None:
            print("Error: el ID ya pertenece a otro empleado.")
            return False

        # Caso 1: crear la raiz.
        if self.raiz is None:
            if id_supervisor is not None:
                print("Error: el primer empleado debe ser la raiz.")
                return False

            self.raiz = Nodo(empleado, None)
            self.tamano += 1
            print("Gerente General registrado como raiz.")
            return True

        # Caso 2: el organigrama ya tiene raiz.
        if id_supervisor is None:
            print("Error: todo empleado nuevo debe tener un supervisor.")
            return False

        if empleado.id == id_supervisor:
            print("Error: un empleado no puede ser su propio supervisor.")
            return False

        supervisor = self.buscar_empleado(id_supervisor)

        if supervisor is None:
            print("Error: no existe el supervisor indicado.")
            return False

        # Se crea la lista de hijos si el supervisor aun no tiene.
        if supervisor.hijo is None:
            supervisor.hijo = csll()

        # El nuevo nodo queda enlazado con su padre.
        supervisor.hijo.append(empleado, supervisor)
        self.tamano += 1

        print("Empleado registrado correctamente.")
        return True

    # ------------------------------------------------------------
    # ASIGNAR O CAMBIAR SUPERVISOR:
    # Mueve un empleado existente debajo de otro supervisor.
    # No permite mover la raiz ni crear ciclos.
    # ------------------------------------------------------------

    def asignar_supervisor(self, id_empleado, id_supervisor):
        empleado = self.buscar_empleado(id_empleado)
        supervisor = self.buscar_empleado(id_supervisor)

        if empleado is None:
            print("Error: no existe el empleado.")
            return False
        if supervisor is None:
            print("Error: no existe el supervisor.")
            return False
        if empleado == self.raiz:
            print("Error: el Gerente General es la raiz y no tiene supervisor.")
            return False
        if empleado == supervisor:
            print("Error: un empleado no puede ser su propio supervisor.")
            return False

        # Comprobamos que el nuevo supervisor no este dentro de la
        # rama del empleado. De ser asi, se formaria un ciclo.
        actual = supervisor
        while actual is not None:
            if actual == empleado:
                print("Error: la asignacion crearia un ciclo jerarquico.")
                return False
            actual = actual.padre

        padre_anterior = empleado.padre

        if padre_anterior == supervisor:
            print("El empleado ya tiene ese supervisor.")
            return False

        # Quitamos al empleado de la lista de hijos anterior.
        if not self._eliminar_hijo(padre_anterior, empleado):
            print("Error: no se pudo retirar al empleado de su supervisor anterior.")
            return False

        # Lo agregamos a la lista de hijos del nuevo supervisor.
        if supervisor.hijo is None:
            supervisor.hijo = csll()

        empleado.padre = supervisor
        supervisor.hijo.append_nodo(empleado)
        print("Supervisor actualizado correctamente.")
        return True

    # Elimina un nodo especifico de la lista circular de un padre.
    def _eliminar_hijo(self, padre, empleado):
        if padre is None or padre.hijo is None:
            return False

        lista = padre.hijo
        actual = lista.cabeza
        anterior = lista.cola

        while True:
            if actual == empleado:
                # Caso: solo existe un hijo.
                if lista.tamano == 1:
                    lista.cabeza = None
                    lista.cola = None
                else:
                    anterior.nodo_siguiente = actual.nodo_siguiente
                    if actual == lista.cabeza:
                        lista.cabeza = actual.nodo_siguiente
                    if actual == lista.cola:
                        lista.cola = anterior

                actual.nodo_siguiente = None
                lista.tamano -= 1
                if lista.tamano == 0:
                    padre.hijo = None
                return True
            anterior = actual
            actual = actual.nodo_siguiente
            if actual == lista.cabeza:
                break
        return False

    # ------------------------------------------------------------
    # ACTUALIZAR SALARIO
    # ------------------------------------------------------------

    def actualizar_salario(self, id, nuevo_salario):
        empleado = self.buscar_empleado(id)

        if empleado is None:
            print("No se encontro el empleado.")
            return False

        if nuevo_salario < 0:
            print("El salario no puede ser negativo.")
            return False

        empleado.valor.salario = nuevo_salario
        print("Salario actualizado correctamente.")
        return True

    # ------------------------------------------------------------
    # MOSTRAR SUBORDINADOS DIRECTOS
    # ------------------------------------------------------------

    def mostrar_subordinados(self, id_supervisor):
        supervisor = self.buscar_empleado(id_supervisor)
        if supervisor is None:
            print("No se encontro el supervisor.")
            return
        print(f"\nSubordinados directos de {supervisor.valor.nombre}:")
        if supervisor.hijo is None:
            print("Este empleado no tiene subordinados.")
            return
        actual = supervisor.hijo.cabeza
        while True:
            print(actual.valor)
            actual = actual.nodo_siguiente
            if actual == supervisor.hijo.cabeza:
                break

    # ------------------------------------------------------------
    # LISTAR EMPLEADOS DE UN DEPARTAMENTO
    # Recorre todo el arbol y muestra las coincidencias.
    # ------------------------------------------------------------

    def _listar_departamento(self, nodo, departamento):
        if nodo is None:
            return 0
        encontrados = 0
        if nodo.valor.departamento.lower() == departamento.lower():
            print(nodo.valor)
            encontrados += 1
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                encontrados += self._listar_departamento(actual, departamento)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return encontrados

    def listar_departamento(self, departamento):
        print(f"\nEmpleados del departamento: {departamento}")
        cantidad = self._listar_departamento(self.raiz, departamento)
        if cantidad == 0:
            print("No hay empleados registrados en ese departamento.")

    # ------------------------------------------------------------
    # ENCONTRAR EL JEFE DE UN EMPLEADO:
    # El jefe directo se obtiene mediante la referencia padre.
    # ------------------------------------------------------------

    def encontrar_jefe(self, id):
        empleado = self.buscar_empleado(id)
        if empleado is None:
            print("No se encontro el empleado.")
            return
        if empleado.padre is None:
            print("El Gerente General es la raiz y no tiene jefe.")
        else:
            print("\nJefe directo:")
            print(empleado.padre.valor)

    # ------------------------------------------------------------
    # MOSTRAR EL ORGANIGRAMA: Recorrido recursivo en profundidad.
    # ------------------------------------------------------------

    def _mostrar_arbol(self, nodo, nivel):
        if nodo is None:
            return
        print("    " * nivel + "|-- " + nodo.valor.nombre +
              " (" + nodo.valor.cargo + ")")
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                self._mostrar_arbol(actual, nivel + 1)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break

    def mostrar_organigrama(self):
        if self.raiz is None:
            print("El organigrama esta vacio.")
            return
        print("\n========== ORGANIGRAMA ==========")
        self._mostrar_arbol(self.raiz, 0)

    # ------------------------------------------------------------
    # CALCULAR NOMINA DE UN SUPERVISOR Y TODA SU RAMA:
    # Incluye el salario del propio supervisor.
    # ------------------------------------------------------------

    def _nomina_rama(self, nodo):
        if nodo is None:
            return 0
        total = nodo.valor.salario
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                total += self._nomina_rama(actual)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return total

    def calcular_nomina_supervisor(self, id):
        supervisor = self.buscar_empleado(id)
        if supervisor is None:
            print("No se encontro el supervisor.")
            return
        total = self._nomina_rama(supervisor)
        print(
            f"Nomina total de {supervisor.valor.nombre} "
            f"y sus subordinados: S/ {total:.2f}"
        )
        return total

    # ------------------------------------------------------------
    # CONTAR EMPLEADOS DEBAJO DE UN SUPERVISOR:
    # No incluye al propio supervisor.
    # ------------------------------------------------------------

    def _contar_rama(self, nodo):
        if nodo is None:
            return 0
        total = 1
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                total += self._contar_rama(actual)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return total

    def contar_empleados_bajo_supervisor(self, id):
        supervisor = self.buscar_empleado(id)
        if supervisor is None:
            print("No se encontro el supervisor.")
            return
        if supervisor.hijo is None:
            cantidad = 0
        else:
            cantidad = 0
            actual = supervisor.hijo.cabeza
            while True:
                cantidad += self._contar_rama(actual)
                actual = actual.nodo_siguiente
                if actual == supervisor.hijo.cabeza:
                    break
        print(f"Empleados bajo {supervisor.valor.nombre}: {cantidad}")
        return cantidad

    # ------------------------------------------------------------
    # NOMINA TOTAL DE UN DEPARTAMENTO:
    # Suma los salarios de todos los empleados del departamento.
    # ------------------------------------------------------------

    def _nomina_departamento(self, nodo, departamento):
        if nodo is None:
            return 0
        total = 0
        if nodo.valor.departamento.lower() == departamento.lower():
            total += nodo.valor.salario
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                total += self._nomina_departamento(actual, departamento)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return total

    def calcular_nomina_departamento(self, departamento):
        total = self._nomina_departamento(self.raiz, departamento)
        print(f"Nomina del departamento {departamento}: S/ {total:.2f}")
        return total

    # ------------------------------------------------------------
    # CONTAR NIVELES JERARQUICOS:
    # Devuelve la profundidad maxima del arbol.
    # La raiz cuenta como nivel 1.
    # ------------------------------------------------------------

    def _contar_niveles(self, nodo):
        if nodo is None:
            return 0
        mayor = 0
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                niveles_hijo = self._contar_niveles(actual)
                if niveles_hijo > mayor:
                    mayor = niveles_hijo
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break
        return 1 + mayor

    def contar_niveles(self):
        niveles = self._contar_niveles(self.raiz)
        print(f"Cantidad de niveles jerarquicos: {niveles}")
        return niveles

    # ------------------------------------------------------------
    # MOSTRAR TODOS LOS EMPLEADOS
    # ------------------------------------------------------------

    def _mostrar_empleados(self, nodo):
        if nodo is None:
            return
        print(nodo.valor)
        if nodo.hijo is not None:
            actual = nodo.hijo.cabeza
            while True:
                self._mostrar_empleados(actual)
                actual = actual.nodo_siguiente
                if actual == nodo.hijo.cabeza:
                    break

    def mostrar_empleados(self):
        if self.raiz is None:
            print("No hay empleados registrados.")
        else:
            print("\n========== EMPLEADOS REGISTRADOS ==========")
            self._mostrar_empleados(self.raiz)


# ================================================================
# FUNCIONES DEL MENU
# ================================================================

def mostrar_menu():
    print("\n==========================================")
    print("       ORGANIGRAMA DE LA EMPRESA")
    print("==========================================")
    print("1. Registrar empleado")
    print("2. Asignar o cambiar supervisor")
    print("3. Buscar empleado por ID")
    print("4. Actualizar salario")
    print("5. Mostrar subordinados directos")
    print("6. Listar empleados por departamento")
    print("7. Encontrar jefe de un empleado")
    print("8. Mostrar organigrama completo")
    print("9. Calcular nomina de un supervisor y su rama")
    print("10. Contar empleados bajo un supervisor")
    print("11. Calcular nomina de un departamento")
    print("12. Contar niveles jerarquicos")
    print("13. Mostrar todos los empleados")
    print("0. Salir")
    print("==========================================")


def ejecutar_menu(organigrama):
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            try:
                id = int(input("ID del empleado: "))
                nombre = input("Nombre: ").strip()
                cargo = input("Cargo: ").strip()
                departamento = input("Departamento: ").strip()
                salario = float(input("Salario: "))

                if nombre == "" or cargo == "" or departamento == "":
                    print("Error: los campos de texto no pueden estar vacios.")
                    continue
                if salario < 0:
                    print("Error: el salario no puede ser negativo.")
                    continue
                if organigrama.raiz is None:
                    print("El primer empleado sera el Gerente General.")
                    supervisor_id = None
                else:
                    supervisor_id = int(input("ID del supervisor directo: "))
                empleado = Empleado(id, nombre, cargo, departamento, salario)
                organigrama.insert(empleado, supervisor_id)

            except ValueError:
                print("Error: ingrese un ID entero y un salario numerico.")

        elif opcion == "2":
            try:
                id_empleado = int(input("ID del empleado: "))
                id_supervisor = int(input("ID del nuevo supervisor: "))
                organigrama.asignar_supervisor(id_empleado, id_supervisor)
            except ValueError:
                print("Error: los ID deben ser numeros enteros.")

        elif opcion == "3":
            try:
                id = int(input("ID que desea buscar: "))
                empleado = organigrama.buscar_empleado(id)
                if empleado is None:
                    print("Empleado no encontrado.")
                else:
                    print("\nEmpleado encontrado:")
                    print(empleado.valor)
            except ValueError:
                print("Error: el ID debe ser un numero entero.")

        elif opcion == "4":
            try:
                id = int(input("ID del empleado: "))
                salario = float(input("Nuevo salario: "))
                organigrama.actualizar_salario(id, salario)
            except ValueError:
                print("Error: ingrese valores numericos.")

        elif opcion == "5":
            try:
                id = int(input("ID del supervisor: "))
                organigrama.mostrar_subordinados(id)
            except ValueError:
                print("Error: el ID debe ser un numero entero.")

        elif opcion == "6":
            departamento = input("Nombre del departamento: ").strip()
            if departamento == "":
                print("Debe ingresar un departamento.")
            else:
                organigrama.listar_departamento(departamento)

        elif opcion == "7":
            try:
                id = int(input("ID del empleado: "))
                organigrama.encontrar_jefe(id)
            except ValueError:
                print("Error: el ID debe ser un numero entero.")

        elif opcion == "8":
            organigrama.mostrar_organigrama()

        elif opcion == "9":
            try:
                id = int(input("ID del supervisor: "))
                organigrama.calcular_nomina_supervisor(id)
            except ValueError:
                print("Error: el ID debe ser un numero entero.")

        elif opcion == "10":
            try:
                id = int(input("ID del supervisor: "))
                organigrama.contar_empleados_bajo_supervisor(id)
            except ValueError:
                print("Error: el ID debe ser un numero entero.")

        elif opcion == "11":
            departamento = input("Nombre del departamento: ").strip()

            if departamento == "":
                print("Debe ingresar un departamento.")
            else:
                organigrama.calcular_nomina_departamento(departamento)

        elif opcion == "12":
            organigrama.contar_niveles()

        elif opcion == "13":
            organigrama.mostrar_empleados()

        elif opcion == "0":
            print("Gracias por utilizar el sistema. Hasta pronto.")
            break

        else:
            print("Opcion no valida. Intente nuevamente.")


# ================================================================
# BLOQUE DE PRUEBAS
# Organigrama de ejemplo con tres niveles jerarquicos.
# Se ejecuta cuando se llama directamente a esta funcion.
# ================================================================

def pruebas():
    print("\n========== INICIO DE PRUEBAS ==========")

    empresa = tree()

    # Nivel 1: raiz.
    empresa.insert(
        Empleado(1, "Carlos Ramirez", "Gerente General", "Gerencia", 8000)
    )

    # Nivel 2: subordinados directos de la raiz.
    empresa.insert(
        Empleado(2, "Maria Lopez", "Gerente Administrativa",
                 "Administracion", 5000), 1
    )
    empresa.insert(
        Empleado(3, "Jose Torres", "Gerente de Ventas", "Ventas", 5200), 1
    )

    # Nivel 3: subordinados de Maria y Jose.
    empresa.insert(
        Empleado(4, "Ana Perez", "Asistente", "Administracion", 2200), 2
    )
    empresa.insert(
        Empleado(5, "Luis Rojas", "Contador", "Administracion", 3000), 2
    )
    empresa.insert(
        Empleado(6, "Pedro Diaz", "Supervisor", "Ventas", 2800), 3
    )
    empresa.insert(
        Empleado(7, "Elena Ruiz", "Vendedora", "Ventas", 1800), 3
    )

    empresa.mostrar_organigrama()
    empresa.calcular_nomina_supervisor(2)
    empresa.contar_empleados_bajo_supervisor(1)
    empresa.calcular_nomina_departamento("Ventas")
    empresa.contar_niveles()
    empresa.encontrar_jefe(4)

    print("\n========== FIN DE PRUEBAS ==========")
    return empresa

if __name__ == "__main__":
    empresa = pruebas()
    ejecutar_menu(empresa)