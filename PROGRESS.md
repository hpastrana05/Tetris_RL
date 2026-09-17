# Seguimiento

He conseguido crear el juego completo y jugable. Luego he aprendido a usar gymnasium para entrenar un modelo, en este caso un DQN.

Para ello he tenido que meter el juego en una especie de Wrap llamado TetrisENV, clase la cual hereda de la clase gym.Env y que sirve para crear entornos para poder correr los modelos de manera mas controlada.

En esta clase he definido la forma de los rewards, el espacio de acciones y el espacio de observación.

## Primera propuesta
En la primera propuesta que me parecía la correcta, he definido acciones todos los movimientos posibles que se pueden hacer en el juego.

 **Reward:**
```text

reward = 10 × lines + pieces_locked_this_step - 0.1 × Δ height - 2 × Δ holes - 0.1 × Δ bumpiness

```


Con esto definido y el espacio de observación bien implementado, he entrenado los primeros modelos y con la .
1. Las primeras veces, el modelo buscaba perder el máximo tiempo posible si colocar piezas haciéndolas girar.
2. Luego seguía intentando perder el tiempo pero esta vez no lo conseguía por cambios que hice en el juego, pero como no buscaba la mejor colocación, directamente perdía la partida

## Segunda propuesta
Después de un poco de investigación, cambié el enfoque de como definir las acciones que puede hacer el modelo.

En vez de dejarle hacer cualquier tipo de acción posible, acoté las acciones a rotación + posición de pieza.

Para hacerlo he elegido una manera de guardarlo todo en números enteros del 0 al 39:
- El numero de las decenas es la rotación
- El numero de las unidades es la columna de posición

Esto hace que en cada acción que recibo del modelo lo tengo que pasar a una lista de acciones, comprobar que funcionan y después aplicarlas

==Sigue sin aprender a colocar las piezas de manera efectiva==

## Tercera propuesta

En este tercer cambio, voy a enfocarlo de otra manera. En vez de cambiar la manera en la que corre el entorno, voy a subir el tiempo de entrenamiento.