"""
Programa para plotar os dados capturados pela sonda (gráfico em tempo real)
"""

import time
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "C:/Users/Paulo Mazzo/PycharmProjects/TCC/MicronOpt-Python-master")
from micronopt import Interrogator, Sensor


start = time.time()

tempo = []  # lista de tempo
y1 = []  # lista de dados do sensor1
y2 = []  # lista de dados do sensor2

a = 0  # quantidade de elementos nas listas (pontos no gráfico)


# Utilizando a função 'test_cotinuous' (micronOpt-Python-master/test.py)
interr = Interrogator()
interr.connect()
interr.create_sensors_from_file(
    "C:/Users/Paulo Mazzo/PycharmProjects/TCC/MicronOpt-Python-master/test/fbg_properties.json")
interr.set_trigger_defaults(False)
data = interr.data
interr.setup_append_data()
interr.data_interleave = 2
interr.set_num_averages = 2
t0 = time.time()

# Ajustar tamanho da tela para mais gráficos
plt.figure(figsize=[11, 6.8], constrained_layout=False)

# Início da captura de dados do sensor
while True:
    interr.get_data()
    interr.sleep()
    ya = data[interr.sensors[0].name + "_wavelength"][-1]  # alterar 'sensors[x] para selecionar outro canal do interrogador
    y1.append(ya)

    interr.get_data()
    interr.sleep()
    ya = data[interr.sensors[1].name + "_wavelength"][-1]  # alterar 'sensors[x] para selecionar outro canal do interrogador
    y2.append(ya)

    x = round((time.time() - start), 2)
    tempo.append(x)

    # Definindo o número máximo de pontos mostrado no gráfico (a)
    # Adicionar 'del (y...[0])' para outros gráficos
    a = a + 1
    if a >= 160:
        del (y1[0])
        del (y2[0])
        del (tempo[0])

    # Plot do gráfico
    # Ajustar 'axes' para colocar mais gráficos

    plt.ion()

    plt.axes([.1, .585, .85, .375])
    plt.plot(tempo, y1)
    plt.grid()
    plt.margins(0.03)
    plt.title('FBG par 1')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Comprimento de Onda (nm)')

    plt.axes([.1, .08, .85, .375])
    plt.plot(tempo, y2)
    plt.grid()
    plt.margins(0.03)
    plt.title('FBG par 2')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Comprimento de Onda (nm)')

    plt.pause(0.001)
    plt.cla()
    plt.clf()

    plt.ioff()
