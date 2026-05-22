# Crear un entorno virtual con venv

## ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado dentro de tu computadora donde podés instalar librerías de Python sin afectar al resto del sistema.

Esto permite:
- Tener **distintas versiones de una misma librería** en diferentes proyectos
- Evitar conflictos entre dependencias
- Mantener los proyectos organizados y reproducibles

Ejemplo:
Un proyecto puede usar `numpy 1.20` y otro `numpy 1.26` sin problemas.

---

### Paso 1: Crear el entorno

En la terminal, dentro de tu proyecto:

```bash
python -m venv venv 

```

### Paso 2: Activar o desactivar el entorno

En la terminal, activar el entorno virtual:

```bash
venv\Scripts\activate
```
En la terminal, desactivar el entorno virtual:
```bash
venv\Scripts\deactivate
```