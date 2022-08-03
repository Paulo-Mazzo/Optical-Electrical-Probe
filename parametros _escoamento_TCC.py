# import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import sys


# sys.path.insert(0, "C:/Users/Paulo Mazzo/PycharmProjects/TCC/MicronOpt-Python-master")
# from micronopt import Interrogator, Sensor

def monitorar_escoamento():
    # start = time.time()

    tempo = []  # lista de tempo
    y1 = []  # lista de dados do sensor1
    y2 = []  # lista de dados do sensor2

    a = 0  # quantidade de elementos nas listas (pontos no gráfico)

    # Utilizando a função 'test_cotinuous' (micronOpt-Python-master/test.py)
    # interr = Interrogator()
    # interr.connect()
    # interr.create_sensors_from_file(
    #     "C:/Users/Paulo Mazzo/PycharmProjects/TCC/MicronOpt-Python-master/test/fbg_properties.json")
    # interr.set_trigger_defaults(False)
    # data = interr.data
    # interr.setup_append_data()
    # interr.data_interleave = 2
    # interr.set_num_averages = 2
    # t0 = time.time()

    # Ajustar tamanho da tela para mais gráficos
    figure1 = plt.figure(figsize=[11, 6.8], constrained_layout=False)

    canvas = FigureCanvasTkAgg(figure1, janela_parametros)
    canvas.draw()
    canvas.get_tk_widget().place(relheight=0.85, relwidth=0.7, relx=0, rely=0)

    toolbar = NavigationToolbar2Tk(canvas, janela_parametros)
    toolbar.update()

    canvas.get_tk_widget().place(relheight=0.85, relwidth=0.7, relx=0, rely=0)

    # Início da captura de dados do sensor
    while True:
        #     interr.get_data()
        #     interr.sleep()
        #     ya = data[interr.sensors[0].name + "_wavelength"][-1]  # alterar 'sensors[x] para selecionar outro canal do interrogador
        #     y1.append(ya)
        #
        #     interr.get_data()
        #     interr.sleep()
        #     ya = data[interr.sensors[1].name + "_wavelength"][-1]  # alterar 'sensors[x] para selecionar outro canal do interrogador
        #     y2.append(ya)
        #
        #     x = round((time.time() - start), 2)
        #     tempo.append(x)
        #
        #     # Definindo o número máximo de pontos mostrado no gráfico (a)
        #     # Adicionar 'del (y...[0])' para outros gráficos
        #     a = a + 1
        #     if a >= 160:
        #         del (y1[0])
        #         del (y2[0])
        #         del (tempo[0])
        #
        #     # Plot do gráfico
        #     # Ajustar 'axes' para colocar mais gráficos
        #
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


# Criando Janela
janela_parametros = Tk()
janela_parametros.title("Parâmetros do escoamento")

frame1 = Frame(janela_parametros, bg="#B5DDE7")
frame1.place(relheight=0.05, relwidth=0.3, relx=0.7, rely=0.05)
text1 = Label(frame1, text="Tamanho médio das bolhas (L_b)", font=30)
text1.place(relheight=0.85, relwidth=0.6, relx=0, rely=0.075)
L_b = Label(frame1, text="")
L_b.place(relheight=0.85, relwidth=0.3, relx=0.65, rely=0.075)

frame2 = Frame(janela_parametros, bg="#B5DDE7")
frame2.place(relheight=0.05, relwidth=0.3, relx=0.7, rely=0.15)
text2 = Label(frame2, text="Tamanho médio do pistão de líq. (L_p)", font=30)
text2.place(relheight=0.85, relwidth=0.6, relx=0, rely=0.075)
L_p = Label(frame2, text="")
L_p.place(relheight=0.85, relwidth=0.3, relx=0.65, rely=0.075)

frame3 = Frame(janela_parametros, bg="#B5DDE7")
frame3.place(relheight=0.05, relwidth=0.3, relx=0.7, rely=0.25)
text3 = Label(frame3, text="Tamanho médio unitário (L_u)", font=30)
text3.place(relheight=0.85, relwidth=0.6, relx=0, rely=0.075)
L_u = Label(frame3, text="")
L_u.place(relheight=0.85, relwidth=0.3, relx=0.65, rely=0.075)

frame4 = Frame(janela_parametros, bg="#B5DDE7")
frame4.place(relheight=0.05, relwidth=0.3, relx=0.7, rely=0.35)
text4 = Label(frame4, text="Velocidade média da bolha (V_b)", font=30)
text4.place(relheight=0.85, relwidth=0.6, relx=0, rely=0.075)
V_b = Label(frame4, text="")
V_b.place(relheight=0.85, relwidth=0.3, relx=0.65, rely=0.075)

frame5 = Frame(janela_parametros, bg="#B5DDE7")
frame5.place(relheight=0.05, relwidth=0.3, relx=0.7, rely=0.45)
text5 = Label(frame5, text="Frequencia média das bolhas (f_b)\n(Tempo de monitoramento de 1 min)", font=30)
text5.place(relheight=0.95, relwidth=0.6, relx=0, rely=0.025)
f_b = Label(frame5, text="")
f_b.place(relheight=0.85, relwidth=0.3, relx=0.65, rely=0.075)

b_start = Button(janela_parametros, text="Iniciar", font=28, bg="#B5DDE7", command=monitorar_escoamento)
b_start.place(relheight=0.06, relwidth=0.1, relx=0.45, rely=0.875)

janela_parametros.mainloop()
