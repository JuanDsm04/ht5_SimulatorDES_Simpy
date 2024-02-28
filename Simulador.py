# Description: Simulador de un sistema operativo con un procesador y memoria RAM
# Autor: Juan Solís
# Version: 1.0

import simpy
import random

# Clase Proceso
class Proceso:
    def __init__(self, id, ram_requerida, cantidad_instrucciones):
        self.id = id
        self.ram_requerida = ram_requerida
        self.cantidad_instrucciones = cantidad_instrucciones
        self.estado = None

# Función que simula la llegada de un proceso al sistema
def llega_proceso_al_sistema(env, ram, cpu, cantidad_procesos):

    # New
    id_proceso = 1
    for _ in range(cantidad_procesos):
        yield env.timeout(random.expovariate( 1.0 /intervalo_exponencial))
        ram_requerida = random.randint(1, 10)  
        cantidad_instrucciones = random.randint(1, 10)

        proceso = Proceso(id_proceso, ram_requerida, cantidad_instrucciones)
        id_proceso += 1

        with ram.get(ram_requerida) as recurso:
            # Ready
            yield recurso
            proceso.estado = 'ready'
            yield env.timeout(1)

        env.process(se_atiende_el_proceso(env, proceso, ram, cpu))

# Función que simula el proceso de atención de un proceso
def se_atiende_el_proceso(env, proceso, ram, cpu):

    #Running
    while True:
        if proceso.cantidad_instrucciones <= 0:
            proceso.estado = 'Terminated'
            ram.put(proceso.ram_requerida)
            break

        with cpu.request() as recurso_cpu:
            yield recurso_cpu
            proceso.estado = 'Running'

            if proceso.cantidad_instrucciones <= 0:
                proceso.estado = 'Terminated'
                ram.put(proceso.ram_requerida)
                print(f"{proceso.id}, {env.now}")

            else:
                proceso.estado = 'Ready'
                numero_aleatorio = random.uniform(1, 2)
                
                if numero_aleatorio <= 1:
                    proceso.estado = 'Waiting'
                    yield env.timeout(2)
                    proceso.estado = 'Ready'
                else:
                    proceso.estado = 'Ready'

# Parámetros de simulación
env = simpy.Environment()
ram = simpy.Container(env, init = 100, capacity = 100)
cpu = simpy.Resource(env, capacity = 1)
random.seed(100)
instrucciones_atendibles = 3
intervalo_exponencial = 10

cantidad_procesos_a_ejecutar = int(input("Cantidad de procesos a ejecutar: "))

env.process(llega_proceso_al_sistema(env, ram, cpu, cantidad_procesos_a_ejecutar))
env.run(until=simpy.core.Infinity)