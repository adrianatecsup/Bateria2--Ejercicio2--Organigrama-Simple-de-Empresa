# Bateria-2--Ejercicio-2--Organigrama-Simple-de-Empresa
# Organigrama Simple de Empresa

## Integrantes
- **Alejandro Celis**
- **Adriana Guillen**

**Curso:** Estructura de Datos y Algoritmos  
**Lenguaje:** Python 3  
**Año:** 2026

## 1. Descripción del proyecto

El proyecto consiste en desarrollar un sistema que permita gestionar el organigrama de una empresa mediante un **árbol genérico (n-ario)**.

Cada empleado puede tener varios subordinados, pero únicamente un supervisor directo. El sistema permite organizar trabajadores, consultar sus relaciones jerárquicas y calcular nóminas utilizando recursividad.

## 2. Objetivo

Implementar un sistema de gestión de empleados para una empresa de hasta 30 trabajadores, aplicando árboles genéricos, listas circulares simplemente enlazadas y algoritmos recursivos.

## 3. Tecnologías y estructuras utilizadas

- Python 3.
- Árbol genérico (n-ario).
- Lista circular simplemente enlazada (CSLL).
- Recursividad.
- Recorrido en profundidad.
- Interfaz mediante consola.

## 4. Funcionalidades

### Gestión de empleados
- Registrar empleados con ID, nombre, cargo, departamento y salario.
- Asignar o cambiar supervisores.
- Buscar empleados por ID.
- Actualizar salarios.

### Consultas jerárquicas
- Mostrar subordinados directos.
- Listar empleados por departamento.
- Identificar al jefe de un empleado.
- Visualizar el organigrama completo.

### Cálculos recursivos
- Calcular la nómina de un supervisor y sus subordinados.
- Contar empleados bajo un supervisor.
- Calcular la nómina de un departamento.
- Contar los niveles jerárquicos del organigrama.

## 5. Estructura del código

| Clase | Función |
|---|---|
| `Empleado` | Almacena la información de cada trabajador. |
| `Nodo` | Representa un empleado dentro del árbol. |
| `csll` | Administra los subordinados mediante una lista circular. |
| `tree` | Gestiona el organigrama, las consultas y los cálculos recursivos. |

## 6. Ejemplo del organigrama

```text
Carlos Ramírez (Gerente General)
│
├── María López (Gerente Administrativa)
│   ├── Ana Pérez (Asistente)
│   └── Luis Rojas (Contador)
│
└── José Torres (Gerente de Ventas)
    ├── Pedro Díaz (Supervisor)
    └── Elena Ruiz (Vendedora)
```

El ejemplo contiene siete empleados distribuidos en tres niveles jerárquicos.

## 7. Ejecución del programa

Para ejecutar el proyecto, es necesario tener Python 3 instalado.

**Paso 1.** Clonar el repositorio o descargar los archivos del proyecto.

**Paso 2.** Abrir una terminal en la carpeta del proyecto.

**Paso 3.** Ejecutar:

```bash
python main.py
```

El programa ejecutará primero las pruebas con los empleados de ejemplo y después mostrará el menú interactivo.

No se requieren librerías externas.

## 8. Menú del sistema

```text
========== ORGANIGRAMA DE LA EMPRESA ==========

1. Registrar empleado
2. Asignar o cambiar supervisor
3. Buscar empleado por ID
4. Actualizar salario
5. Mostrar subordinados directos
6. Listar empleados por departamento
7. Encontrar jefe de un empleado
8. Mostrar organigrama completo
9. Calcular nómina de un supervisor y su rama
10. Contar empleados bajo un supervisor
11. Calcular nómina de un departamento
12. Contar niveles jerárquicos
13. Mostrar todos los empleados
0. Salir
```

## 9. Validaciones del sistema

El programa permite:

- Evitar registros con ID duplicados.
- Impedir salarios negativos.
- Limitar el registro a 30 empleados.
- Evitar que un empleado sea su propio supervisor.
- Impedir ciclos en la jerarquía.
- Mantener al nodo raíz sin supervisor.

## 10. Resultados de las pruebas

| Prueba | Resultado esperado |
|---|---|
| Empleados registrados inicialmente | 7 |
| Niveles jerárquicos | 3 |
| Nómina de María López y sus subordinados | S/ 10,200.00 |
| Subordinados del Gerente General | 6 |
| Nómina del departamento Ventas | S/ 9,800.00 |

## 11. Conclusiones

1. Se implementó un árbol genérico que permite representar la estructura jerárquica de una empresa.

2. Se aplicó la recursividad para realizar búsquedas, cálculos de nómina y conteo de trabajadores.

3. Se utilizó una lista circular simplemente enlazada para administrar los subordinados de cada empleado.

4. Se desarrolló un menú interactivo que facilita la gestión y consulta de la información de los trabajadores.

---

**Desarrollado por Alejandro Celis y Adriana Guillen.**

**Proyecto académico — Estructura de Datos y Algoritmos, 2026.**
