
Hola

Algunas personas me han comentado sobre  ciertos  problemas relacionados a la versión de SqlAlchemy.
Al querer acomodar las carpetas y archivos del proyecto tal como vimos en clase, la última versión genera algunos problemas  (no le gustan los import repetidos, que generan algunas dependencias cíclicas).

Recuerden que con el comando pip list pueden ver qué han instalado y las respectivas versiones
En mi caso, tenía la versión 1.3.3, pero decidí actualizar así trabajo con la misma que tienen uds. La 1.3.5
Para actualizar: pip install SQLAlchemy --upgrade
Eso me pasó a la versión 1.3.5

Veamos una forma alternativa de organizar el proyecto.
Como Flask es un micro framework, no viene con una estructura pre-armada, como sí lo hace Django por ejemplo
Esta organización que les mando acá, es una agrupación posible, pero hay varias opciones, incluso hay algo que se llama Blueprint que es especialmente útil para esto (queda para el avanzado, pueden ir investigando).

Dentro del directorio del proyecto tenemos
- apptrivia.py
- config.py
- routes.py
- models/
- templates/

Doy un pantallazo de cada elemento:
- apptrivia: Inicializa flask y la base de datos (valiéndose de config,py) Levanta las rutas y lanza flask
- config.py: Básicamente tiene la ubicación de la bd. Se podrían incluir otras configuraciones globales
- routes.py: Ya lo conocen, se definen las rutas, en este caso, sólo agregué 2, una que usa modelos (categoria) y la otra no. Una que usa template y la otra no,
- models/ tiene la definición de los modelos y la bd
- templates/ tiene una template base y otra que usar para mostrar las categorías leídas desde la BD

El proyecto que les mando, es un sólo un ejemplo recortado de Trivia (solo está modelado categoría)
El código está bastante comentado.
Lo levantan, desde una consola de Win o Linux así: python apptrivia.py
Van a responder estos 2 recursos:
- http://localhost:5000/trivia
- http://localhost:5000/trivia/categorias

¡Cualquier cosa nos escriben!
Saludos

Acá pueden ver una buena explicación de que les comenté arriba
https://www.youtube.com/watch?v=_5OXmXvkU_E


