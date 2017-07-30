## This Python file uses the following encoding: utf-8
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer 
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules   import SigmoidLayer
import matplotlib.pyplot as plt
import random
import xlrd
import xlwt
import pickle

dataset = SupervisedDataSet(9,1) #definicação do tamanho dos parâmetros, 9 parâmetros de entrada e 1 de saida

workbook = xlrd.open_workbook('Grande.xlsx') 
worksheet = workbook.sheet_by_index(1)

workbook_doce = xlrd.open_workbook('Doce.xlsx')
worksheet_doce = workbook.sheet_by_index(0)

tamGrande = worksheet.nrows
tamDoce = worksheet_doce.nrows

oxi = open('Oxigenio_Dissolvido.txt', 'r')
Cf = open('CF.txt', 'r')
ph = open('ph.txt','r')
dbo = open('dbo.txt', 'r')
nitrato = open('nitrato.txt','r')
tur = open('turbidez.txt', 'r')
fos = open('fosfato.txt','r')
st = open('Solidos_Totais.txt','r')
iqa = open('iqa.txt','r')

oxiD = open('Oxigenio_DissolvidoD.txt', 'r')
CfD = open('CFD.txt', 'r')
phD = open('phD.txt','r')
dboD = open('dboD.txt', 'r')
nitratoD = open('nitratoD.txt','r')
turD = open('turbidezD.txt', 'r')
fosD = open('fosfatoD.txt','r')
stD = open('Solidos_TotaisD.txt','r')
iqaD = open('iqaD.txt','r')
tmpD = open('tempD.txt','r')



#Pega os dados da base de dados do Rio Grande
for row_num in xrange(tamGrande):

    if row_num == 0:
        continue
    row = worksheet.row_values(row_num)

    IQA_col = float(Cf.readline())
    IQA_Oxi = float(oxi.readline())
    IQA_Temp = float(row[24])
    IQA_Ph = float(ph.readline())
    IQA_dem = float(dbo.readline())
    IQA_Nit = float(nitrato.readline())
    IQA_Turb = float(tur.readline())
    IQA_Fos = float(fos.readline())
    IQA_Sot = float(st.readline())
    IQA_Total = float(iqa.readline())

    IQA_Total = (IQA_Total/100)#Normalização do dado de saída entre 0 e 1 para utilização da função de ativação sigmoidal

    if IQA_Total > 100.0:# Se o dado de Saida passar o valor de 100 ele recebe um valor normalizado abaixo de 1

        IQA_Total = 0.95


    dataset.addSample([IQA_col,IQA_Oxi,IQA_Temp,IQA_Ph,IQA_dem,IQA_Nit,IQA_Turb,IQA_Fos,IQA_Sot], [IQA_Total])#adiciona os paramêtros de treinamento em dataset
#Pega os dados da Base do Rio Doce 
for row_num in xrange(tamDoce):

    if row_num == 0:
        continue
    row = worksheet_doce.row_values(row_num)

    IQA_col = float(CfD.readline())
    IQA_Oxi = float(oxiD.readline())
    IQA_Temp = float(tmpD.readline())
    IQA_Ph = float(phD.readline())
    IQA_dem = float(dboD.readline())
    IQA_Nit = float(nitratoD.readline())
    IQA_Turb = float(turD.readline())
    IQA_Fos = float(fosD.readline())
    IQA_Sot = float(stD.readline())
    IQA_Total = float(iqaD.readline())

    IQA_Total = (IQA_Total/100)

    if IQA_Total > 100.0:

        IQA_Total = 0.95


    dataset.addSample([IQA_col,IQA_Oxi,IQA_Temp,IQA_Ph,IQA_dem,IQA_Nit,IQA_Turb,IQA_Fos,IQA_Sot], [IQA_Total])

treina_dados,testa_dados = dataset.splitWithProportion(0.8) # divide os dados adicionados em dataset em vetores de treinamento e teste

network = buildNetwork(treina_dados.indim,16,16,treina_dados.outdim, bias = True, hiddenclass = SigmoidLayer, outclass = SigmoidLayer)#Função que define a rede, com os dados a ser treinado, função de ativação, bias, e quantidades de neurônios na camada escondidada

trainer = BackpropTrainer(network,treina_dados, learningrate = 0.01, momentum = 0.55)#Define o tipo de treinamento a ser utilizado, a taxa de aprendizado e o momento

print "Treinando ...."
erro_epoca = trainer.trainUntilConvergence(dataset=treina_dados, maxEpochs=3000, verbose=True, continueEpochs=10, validationProportion=0.1)#treina a rede com o metodo backpropagation
#grava os treinamento da rede para ser usado posteriormente no framework de teste
fileObject = open ('results', 'w')
print "Gravando..."
pickle.dump(network, fileObject)   # gravando...
fileObject.close()                 # fecha arquivo

erro_epoca.insert(0,0)#insere 0 no inicio do vetor de erro_epoca para erro_epocas e epocas começarem em 0
epocas = range(3001)#numero de epocas para gerar o grafico
epocas.insert(0,0)
#plota o grafico
plt.plot(epocas,erro_epoca,'-')
plt.show()

erro,output,target = trainer.testOnData(testa_dados, verbose = True,returnOutputsTargets = True)#função de teste, testa os dados separados na função split
                                                                                                #retorna o erro, a saida alcançada e a saida desejada
treina = len(output)#tamanho dos dados para o calculo da porcentagem de acerto

i = 0
total = 0.0
correto = 0.0

#calcula a porcentagem de acerto de acordo com os intervalos definidos para classificação da qualidade da água
print "Calculando a porcentagem de acerto..."
for i in xrange(treina):

    total += 1
    print target[i]
    print output[i]
    if target[i] > [0.9]:
        
        desejavel = "excelente"
        print "desejavel", desejavel

    elif target[i] > [0.7] and target[i] <= [0.9]:

        desejavel = "Otimo"
        print "desejavel",desejavel

    elif target[i] >[0.5] and target[i] <= [0.7]:

        desejavel = "bom"
        print "desejavel", desejavel

    elif target[i] > [0.25] and target[i] <= [0.5]:

        desejavel = "ruim"
        print "desejavel", desejavel

    elif target[i] <= [0.25]:

        desejavel = "Pessimo"
        print "desejavel", desejavel

    if output[i] > [0.9]:
        
        saida = "excelente"
        print "Saida", saida

    elif output[i] > [0.7] and output[i] <= [0.9]:

        saida = "Otimo"
        print "saida", saida

    elif output[i] > [0.5] and output[i] <= [0.7]:

        saida = "bom"
        print "saida", saida

    elif output[i] > [0.25] and output[i] <= [0.5]:

        saida = "ruim"
        print "saida", saida

    elif target[i] <= [0.25]:

        saida = "Pessimo"
        print "saida", saida

    if saida == desejavel:

        correto += 1

print correto
print total
porc_acerto = (correto/total)*100

print "Porcentagem de acerto", porc_acerto


    





