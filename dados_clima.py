import csv
import datetime
from statistics import mode
import matplotlib.pyplot as plt

# abrindo o arquivo CSV e lendo os dados
with open('ArquivoDadosProjeto.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    dados = []
    for row in reader:
        # convertendo as strings em tipos apropriados
        row['data'] = datetime.datetime.strptime(row['data'], '%d/%m/%Y')
        row['precip'] = float(row['precip'])
        row['maxima'] = float(row['maxima'])
        row['minima'] = float(row['minima'])
        row['horas_insol'] = float(row['horas_insol'])
        row['temp_media'] = float(row['temp_media'])
        row['um_relativa'] = float(row['um_relativa'])
        row['vel_vento'] = float(row['vel_vento'])
        dados.append(row)

# a) qual é o mês mais chuvoso em todo esse período?
chuva_por_mes = {}
media_horas_sol = {1970: 0, 1980: 0, 1990: 0, 2000: 0, 2010: 0}
for d in dados:
    ano = d['data'].year
    horas_sol = d['horas_insol']
    if ano >= 1970 and ano < 1980:
        media_horas_sol[1970] += horas_sol
    elif ano >= 1981 and ano < 1990:
        media_horas_sol[1980] += horas_sol
    elif ano >= 1991 and ano < 2000:
        media_horas_sol[1990] += horas_sol
    elif ano >= 2001 and ano < 2010:
        media_horas_sol[2000] += horas_sol
    elif ano >= 2011 and ano < 2020:
        media_horas_sol[2010] += horas_sol

for decada in media_horas_sol:
    media_horas_sol[decada] = media_horas_sol[decada] / 10
for decada in media_horas_sol:
    print(f"Média anual de horas de sol na década de {decada}: {media_horas_sol[decada]:.2f} horas")
for d in dados:
    mes = d['data'].month
    if mes not in chuva_por_mes:
        chuva_por_mes[mes] = 0
    chuva_por_mes[mes] += d['precip']

mes_mais_chuvoso = max(chuva_por_mes, key=chuva_por_mes.get)
ano_mais_chuvoso = max(dados, key=lambda d: d['precip'])['data'].strftime('%Y')
print(f"O mês mais chuvoso foi {mes_mais_chuvoso}/{ano_mais_chuvoso}, com {chuva_por_mes[mes_mais_chuvoso]:.2f} mm de chuva.")

# b) Qual a média e a moda da temperatura mínima, umidade do ar e velocidade do vento no mês de agosto (auge do inverno) nos últimos 10 anos (2006 a 2016)?
for ano in range(2006, 2017):
    dados_agosto_ano = [d for d in dados if d['data'].month == 8 and d['data'].year == ano]
    if dados_agosto_ano:
        media_temp = sum(d['minima'] for d in dados_agosto_ano) / len(dados_agosto_ano)
        moda_temp = mode(d['minima'] for d in dados_agosto_ano)
        media_umidade = sum(d['um_relativa'] for d in dados_agosto_ano) / len(dados_agosto_ano)
        moda_umidade = mode(d['um_relativa'] for d in dados_agosto_ano)
        media_vel_vento = sum(d['vel_vento'] for d in dados_agosto_ano) / len(dados_agosto_ano)
        moda_vel_vento = mode(d['vel_vento'] for d in dados_agosto_ano)
        print(f"Agosto/{ano}: temperatura mínima: média = {media_temp:.2f}, moda = {moda_temp:.2f}; umidade do ar: média = {media_umidade:.2f}, moda = {moda_umidade:.2f}; velocidade do vento: média = {media_vel_vento:.2f}, moda = {moda_vel_vento:.2f}")
decadas = ['1970-1980', '1981-1990', '1991-2000', '2001-2010', '2011-2020']
medias = [media_horas_sol[1970], media_horas_sol[1980], media_horas_sol[1990], media_horas_sol[2000], media_horas_sol[2010]]
plt.bar(decadas, medias)
plt.xlabel('Década')
plt.ylabel('Média anual de horas de sol')
plt.title('Média anual por década')
plt.show()



