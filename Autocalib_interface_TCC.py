import numpy as np
import pandas as pd
import openpyxl as pxl
from tkinter import *


def auto_calibracao():  # LINHA PARA CRIAR A FUNÇÃO DE AUTOCALIBRAÇÃO
    # a = 225 * 10 ** (-6)              0.000225
    # L = 25.4 * 10 ** (-3)             0.0254
    # E = 206 * 10 ** 9                 206000000000
    # R = 225 * 10 ** (-6)              0.000225
    # r = 136.53 * 10 ** (-6)           0.00013653
    # ρ_e = 0.22                        0.22
    # λ_B = 1541.192 * 10 ** (-9)       0.000001541192

    # print("\nInsira os parâmetros da sonda. Utilize valor real.\n")
    a = float(Ea.get())
    L = float(EL.get())
    E = float(EE.get())
    R = float(ER.get())
    r = float(Er.get())
    ρ_e = float(Eρ_e.get())
    λ_B = float(Eλ_B.get())

    S1F1 = float(E1_1.get())
    S1F2 = float(E1_2.get())
    S1F3 = float(E1_3.get())

    S2F1 = float(E2_1.get())
    S2F2 = float(E2_2.get())
    S2F3 = float(E2_3.get())

    S3F1 = float(E3_1.get())
    S3F2 = float(E3_2.get())
    S3F3 = float(E3_3.get())

    S4F1 = float(E4_1.get())
    S4F2 = float(E4_2.get())
    S4F3 = float(E4_3.get())

    S5F1 = float(E5_1.get())
    S5F2 = float(E5_2.get())
    S5F3 = float(E5_3.get())

    sensores_df = pd.DataFrame(data={"Força 1": [S1F1, S2F1, S3F1, S4F1, S5F1],
                                     "Força 2": [S1F2, S2F2, S3F2, S4F2, S5F2],
                                     "Força 3": [S1F3, S2F3, S3F3, S4F3, S5F3]},
                               index=["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4", "Sensor 5"],
                               columns=["Força 1", "Força 2", "Força 3"])

    posicao = []
    for x in np.arange(0, L / 2 + 0.0005, 0.0005):
        x = round(x, 5)
        posicao.append(x)

    forca = []
    for f in np.arange(0.048933, 0.489331, 0.048933):
        forca.append(f)

    deformacao_df = pd.DataFrame([], columns=['Força 1', 'Força 2', 'Força 3', 'Força 4', 'Força 5',
                                              'Força 6', 'Força 7', 'Força 8', 'Força 9', 'Força 10'])

    for x in posicao:
        deformacao = []
        for f in forca:
            e = (a * f * (L - (4 * x))) / (2 * np.pi * E * (R ** 4 - r ** 4)) * (10 ** 6)

            W_L = 1541.192 + (λ_B * e * (1 - ρ_e) * 10 ** 6)

            deformacao.append(W_L)

        df = pd.DataFrame([], columns=['Força 1', 'Força 2', 'Força 3', 'Força 4', 'Força 5',
                                       'Força 6', 'Força 7', 'Força 8', 'Força 9', 'Força 10'])

        to_append = deformacao
        df_length = len(df)
        df.loc[df_length] = to_append

        deformacao_df = pd.concat([deformacao_df, df], ignore_index=True)

    series = pd.Series(np.arange(0, L / 2 + 0.00005, 0.00005))
    series = series.round(5)
    deformacao_df = pd.concat([deformacao_df, series], axis=1)
    deformacao_df = deformacao_df.set_index(0)

    if var.get() == 1:
        sensores_df.to_excel(r'Planilha de C.xlsx', sheet_name="dados sensores")
        excel_book = pxl.load_workbook(r'Planilha de C.xlsx')
        writer = pd.ExcelWriter(r'Planilha de C.xlsx', engine='openpyxl')
        writer.book = excel_book
        deformacao_df.to_excel(writer, sheet_name='dados calibração')
        writer.save()
        writer.close()

    # formato [row, column]
    i = 0  # linha deformcao_df
    # j = 0  # coluna deformacao_df
    # z = 0  # linha excel_df
    # y = 0  # coluna excel_df
    for z in range(0, 5):
        for y in range(0, 3):
            while i < L / 0.0001:
                j = 0
                while j < 10:
                    dif = deformacao_df.iloc[i, j] - sensores_df.iloc[z, y]
                    if abs(dif) <= abs(deformacao_df.iloc[i, j]) * 0.0001:
                        y = y + 1
                        j = 0
                        if y == 3:
                            if z == 0:
                                ac_sensor1["text"] = [f"Posição = {1000 * series[i]} mm.", "\n",
                                                      deformacao_df.loc[series[i]], "\n", sensores_df.iloc[z, :]]
                            if z == 1:
                                ac_sensor2["text"] = [f"Posição = {1000 * series[i]} mm.", "\n",
                                                      deformacao_df.loc[series[i]], "\n", sensores_df.iloc[z, :]]
                            if z == 2:
                                ac_sensor3["text"] = [f"Posição = {1000 * series[i]} mm.", "\n",
                                                      deformacao_df.loc[series[i]], "\n", sensores_df.iloc[z, :]]
                            if z == 3:
                                ac_sensor4["text"] = [f"Posição = {1000 * series[i]} mm.", "\n",
                                                      deformacao_df.loc[series[i]], "\n", sensores_df.iloc[z, :]]
                            if z == 4:
                                ac_sensor5["text"] = [f"Posição = {1000 * series[i]} mm.", "\n",
                                                      deformacao_df.loc[series[i]], "\n", sensores_df.iloc[z, :]]
                            y = 0
                            z = z + 1
                            i = i + 1
                            break
                    j = j + 1
                if z == 3:
                    break
                i = i + 1
            break
        break


# Criando a janela
HEIGHT = 700
WIDTH = 1200

janela = Tk()
janela.title("Auto calibração de sensor FBG")

canvas = Canvas(janela, height=HEIGHT, width=WIDTH)
canvas.pack()

frame1 = Frame(janela)
frame1.place(relheight=0.3, relwidth=0.325, relx=0.025, rely=0.05)

frame2 = Frame(janela)
frame2.place(relheight=0.3, relwidth=0.5875, relx=0.38, rely=0.05)

frame3 = Frame(janela)
frame3.place(relheight=0.08, relwidth=0.2, relx=0.4, rely=0.36)

frame4 = Frame(janela)
frame4.place(relheight=0.5, relwidth=0.15, relx=0.025, rely=0.45)

frame5 = Frame(janela)
frame5.place(relheight=0.5, relwidth=0.15, relx=0.225, rely=0.45)

frame6 = Frame(janela)
frame6.place(relheight=0.5, relwidth=0.15, relx=0.425, rely=0.45)

frame7 = Frame(janela)
frame7.place(relheight=0.5, relwidth=0.15, relx=0.625, rely=0.45)

frame8 = Frame(janela)
frame8.place(relheight=0.5, relwidth=0.15, relx=0.825, rely=0.45)

# Posicionamento no Frame1
instrucao1 = Label(frame1, text="Insira os parâmetros da sonda.", font=2)
instrucao1.place(relheight=0.12, relwidth=1)

a = Label(frame1, text="Distância do deixo central até a fibra externa - a")
a.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.13)
Ea = Entry(frame1)
Ea.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.13)

L = Label(frame1, text="Comprimento do sensor - L")
L.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.255)
EL = Entry(frame1)
EL.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.255)

E = Label(frame1, text="Módulo de elasticidade do conjunto - E")
E.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.380)
EE = Entry(frame1)
EE.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.380)

R = Label(frame1, text="Raio externo do encapsulamento - R")
R.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.505)
ER = Entry(frame1)
ER.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.505)

r = Label(frame1, text="Raio interno do encapsulamento - r")
r.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.630)
Er = Entry(frame1)
Er.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.630)

ρ_e = Label(frame1, text="Constante fotoelástica - ρe")
ρ_e.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.755)
Eρ_e = Entry(frame1)
Eρ_e.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.755)

λ_B = Label(frame1, text="Comprimento de onda de Bragg - λB")
λ_B.place(relheight=0.12, relwidth=0.7, relx=0, rely=0.880)
Eλ_B = Entry(frame1)
Eλ_B.place(relheight=0.12, relwidth=0.25, relx=0.725, rely=0.880)

# Posicionamento no Frame2
instrucao2 = Label(frame2, text="Insira os comprimentos de onda correspondentes (em 'nm').", font=2)
instrucao2.place(relheight=0.12, relwidth=1)

F1 = Label(frame2, text="λ 1", font=2)
F1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.13)
F2 = Label(frame2, text="λ 2", font=2)
F2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.13)
F3 = Label(frame2, text="λ 3", font=2)
F3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.13)

S1 = Label(frame2, text="Sensor 1", font=2)
S1.place(relheight=0.12, relwidth=0.15, relx=0, rely=0.255)
E1_1 = Entry(frame2)
E1_1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.255)
E1_2 = Entry(frame2)
E1_2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.255)
E1_3 = Entry(frame2)
E1_3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.255)

S2 = Label(frame2, text="Sensor 2", font=2)
S2.place(relheight=0.12, relwidth=0.15, relx=0, rely=0.380)
E2_1 = Entry(frame2)
E2_1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.380)
E2_2 = Entry(frame2)
E2_2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.380)
E2_3 = Entry(frame2)
E2_3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.380)

S3 = Label(frame2, text="Sensor 3", font=2)
S3.place(relheight=0.12, relwidth=0.15, relx=0, rely=0.505)
E3_1 = Entry(frame2)
E3_1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.505)
E3_2 = Entry(frame2)
E3_2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.505)
E3_3 = Entry(frame2)
E3_3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.505)

S4 = Label(frame2, text="Sensor 4", font=2)
S4.place(relheight=0.12, relwidth=0.15, relx=0, rely=0.630)
E4_1 = Entry(frame2)
E4_1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.630)
E4_2 = Entry(frame2)
E4_2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.630)
E4_3 = Entry(frame2)
E4_3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.630)

S5 = Label(frame2, text="Sensor 5", font=2)
S5.place(relheight=0.12, relwidth=0.15, relx=0, rely=0.755)
E5_1 = Entry(frame2)
E5_1.place(relheight=0.12, relwidth=0.2, relx=0.195, rely=0.755)
E5_2 = Entry(frame2)
E5_2.place(relheight=0.12, relwidth=0.2, relx=0.4, rely=0.755)
E5_3 = Entry(frame2)
E5_3.place(relheight=0.12, relwidth=0.2, relx=0.605, rely=0.755)

var = IntVar()
check = Checkbutton(frame2, text="Criar um arquivo '.xlsx' com as tabelas de calibração?", font=2, variable=var,
                    onvalue=1, offvalue=0)
check.place(relheight=0.12, relwidth=1, relx=0, rely=0.880)

# Posicionamento no Frame3
botao = Button(frame3, text="Auto calibrar", font=10, command=auto_calibracao)
botao.place(relheight=0.9, relwidth=0.9, relx=0.05, rely=0.05)

# Posicionamento no Frame4
sensor1 = Label(frame4, text="Sensor 1", font=2)
sensor1.place(relheight=0.12, relwidth=1)
ac_sensor1 = Label(frame4, text="")
ac_sensor1.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.15)

# Posicionamento no Frame5
sensor2 = Label(frame5, text="Sensor 2", font=2)
sensor2.place(relheight=0.12, relwidth=1)
ac_sensor2 = Label(frame5, text="")
ac_sensor2.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.15)

# Posicionamento no Frame6
sensor3 = Label(frame6, text="Sensor 3", font=2)
sensor3.place(relheight=0.12, relwidth=1)
ac_sensor3 = Label(frame6, text="")
ac_sensor3.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.15)

# Posicionamento no Frame7
sensor4 = Label(frame7, text="Sensor 4", font=2)
sensor4.place(relheight=0.12, relwidth=1)
ac_sensor4 = Label(frame7, text="")
ac_sensor4.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.15)

# Posicionamento no Frame8
sensor5 = Label(frame8, text="Sensor 5", font=2)
sensor5.place(relheight=0.12, relwidth=1)
ac_sensor5 = Label(frame8, text="")
ac_sensor5.place(relheight=0.85, relwidth=0.9, relx=0.05, rely=0.15)

janela.mainloop()
