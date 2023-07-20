# Diagenda

Los sistemas distribuidos se han convertido en una herramienta fundamental para el manejo de grandes volúmenes de información en la actualidad. El desarrollo de una agenda distribuida como "Diagenda" en una red Chord con replicación 1 a 1, tolerancia de fallas y técnicas para la consistencia de datos, es un ejemplo de cómo se pueden utilizar los sistemas distribuidos para mejorar la eficiencia de una base de datos.

En este informe, se describirán las principales características y componentes de la agenda distribuida desarrollada, así como también las técnicas utilizadas para garantizar la consistencia y la tolerancia de fallas en el sistema. Además, se presentará una descripción detallada de la implementación de la agenda distribuida, incluyendo la gestión de base de datos y consultas, y la consola interactiva para la interacción usuario-servidor.


## Componentes de la agenda distribuida

La agenda distribuida desarrollada consta de varios componentes clave para garantizar su eficiencia y estabilidad. Los componentes principales incluyen la red Chord, la replicación, la tolerancia de fallas y las técnicas para la consistencia de datos.

- **<ins> Red Chord </ins>**

    La red Chord es un protocolo de enrutamiento que permite la creación de una red de nodos distribuidos en la cual cada nodo es responsable de un rango de claves (en este caso usamos como llave el username que garantizamos que sea único desde la consola), tiene una estructura de anillo en donde se distribuye la base de datos en varias máquinas. Cada máquina en la red Chord se encarga de una parte específica de la base de datos y se comunica con su sucesor en el anillo para garantizar la coherencia de los datos. La red Chord se utiliza en la agenda distribuida para garantizar que los datos estén disponibles en todas las máquinas de la red y que se puedan buscar y actualizar de manera eficiente. Cada nodo mantiene una tabla de enrutamiento que le permite encontrar el nodo responsable de cualquier clave en la red en tiempo logarítmico. 

- **<ins> Replicación</ins>**
 
    La replicación se utiliza en la agenda distribuida para garantizar que cada dato tenga una copia de respaldo en otra máquina de la red. Esto se hace para garantizar que si una máquina falla, otra pueda tomar su lugar y mantener la disponibilidad de la agenda, los datos todavía estarán disponibles en otra máquina. Además, la replicación también ayuda a mejorar la eficiencia de la base de datos, ya que las consultas se pueden distribuir entre varias máquinas.

- **<ins> Tolerancia a fallos </ins>**

    La tolerancia a fallos es la capacidad del sistema para continuar funcionando incluso si algunos de sus componentes fallan. En nuestro proyecto, implementamos técnicas para garantizar la tolerancia a fallos de la agenda distribuida. 

- **<ins> Consistencia de datos </ins>**

    La consistencia de datos se refiere a la necesidad de que los datos en la base de datos sean consistentes en todo momento. En nuestro proyecto, analizamos varias formas de implementar algunas de las técnicas que garantizan la consistencia de datos en un sistema distribuido, así como, técnicas de sincronización de datos para garantizar que los datos sean consistentes en todos los nodos de la red y mitiguen errores que puedan surgir: incluyen la propagación de actualizaciones en la red y la resolución de conflictos.

- **<ins> SQLite3 </ins>**

    Para la gestión de la base de datos y consultas, utilizamos SQLite3: es una biblioteca de software que proporciona una base de datos relacional incorporada en la aplicación. Es fácil de usar y proporciona una gestión eficiente de la base de datos, lo que lo convierte en una buena opción para nuestros propósitos.

- **<ins> Consola interactiva </ins>**

    Para la interacción usuario-servidor, implementamos una consola interactiva con algunos comandos especiales. Los usuarios pueden interactuar con la agenda distribuida mediante comandos específicos, como agregar eventos personales, grupales, gestionar grupos jerárquicos, etc. La consola interactiva proporciona una forma fácil e intuitiva de interactuar con la agenda distribuida.


## Implementación de la agenda distribuida

 La red Chord se implementó utilizando una clase en Python que representa cada nodo en la red. Cada nodo tiene una dirección IP y un identificador de nodo único que se utiliza para ordenar los nodos en el anillo.Este identificador es el resultado de hashear su IP usando la función SHA-1, que devuelve un entero unico de 160 bits. Los nodos se comunican entre sí utilizando sockets y se aseguran de que la base de datos esté distribuida en todo el anillo.
- La replicación se implementó creando funciones en Python que se ejecutan en segundo plano en cada nodo de la red. Esta función se encarga de copiar los datos de un nodo a su sucesor cada cierto intervalo de tiempo para garantizar dicha replicación. Además, la función también se encarga de actualizar la base de datos del sucesor cuando se producen actualizaciones.
- La tolerancia de fallas se implementó creando otras funciones en Python que se ejecutan en segundo plano en cada nodo de la red. Para ello en todo momento hay un nodo en la red que asume el cargo de líder. Este utiliza una función en segundo plano que se encarga de enviar un mensaje de comprobación a cada nodo de la red para comprobar si está vivo y mantener actualizada la lista de nodos. Así scuando otro nodo necesite realizar una operación debe solicitar esta lista de nodos al líder para actualizar su Finger Table. En este sentido para garantizar la tolerancia a fallas, cuando un nodo de la red escribe al lider y no recibe respuesta de este en un tiempo determinado, debe comenzar a descubrir los nodos en la red. Si ninguno de los que le responde es lider, entonces toma como lider al nodo que mayor ID tiene. Este a su vez cuando escribe  al resto de los nodos se da cuenta que es el de mayor ID y se comienzan a correr en segundo plano las funciones del lider en este servidor. 
- Para garantizar la consistencia de los datos, se implementó un algoritmo de propagación de actualizaciones en la red Chord. Cuando se realiza una actualización en un nodo, la actualización se propagan al sucesor. 
- Cada nodo en la red Chord tiene su propia copia de la base de datos y se encarga de realizar consultas y actualizaciones en su propia copia.
- Cada nodo en la red Chord tiene su propia copia de la base de datos y se encarga de realizar consultas y actualizaciones en su propia copia. Cuando se realiza una actualización, se propaga al sucesor en la red Chord para garantizar la consistencia de los datos.
- Se implementó una consola interactiva para permitir a los usuarios interactuar con el sistema de manera fácil y efectiva. La consola interactiva permite a los usuarios realizar consultas y actualizaciones en la base de datos distribuida, además también se proporciona información sobre el estado de la red Chord y las máquinas en la red.

 La consola interactiva proporciona una interfaz fácil y efectiva para la interacción usuario-servidor. En general, la implementación de la agenda distribuida demuestra cómo los sistemas distribuidos pueden mejorar la eficiencia y la estabilidad de una base de datos distribuida.
