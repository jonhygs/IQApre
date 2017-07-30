
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


workbook = xlrd.open_workbook('Doce.xlsx')
worksheet = workbook.sheet_by_index(0)

dataset = SupervisedDataSet(9,1)
tam = worksheet.nrows

oxi = open('Oxigenio_DissolvidoD.txt', 'r')
Cf = open('CFD.txt', 'r')
ph = open('phD.txt','r')
dbo = open('dboD.txt', 'r')
nitrato = open('nitratoD.txt','r')
tur = open('turbidezD.txt', 'r')
fos = open('fosfatoD.txt','r')
st = open('Solidos_TotaisD.txt','r')
iqa = open('iqaD.txt','r')





for row_num in xrange(tam):

    if row_num == 0:
        continue
    row = worksheet.row_values(row_num)

    IQA_col = float(Cf.readline())
    IQA_Oxi = float(oxi.readline())
    IQA_Temp = float(row[13])
    IQA_Ph = float(ph.readline())
    IQA_dem = float(dbo.readline())
    IQA_Nit = float(nitrato.readline())
    IQA_Turb = float(tur.readline())
    IQA_Fos = float(fos.readline())
    IQA_Sot = float(st.readline())
    IQA_Total = float(iqa.readline())

    IQA_Total = (IQA_Total/100)

    if IQA_Total > 100.0:

        IQA_Total = 0.95


    dataset.addSample([IQA_col,IQA_Oxi,IQA_Temp,IQA_Ph,IQA_dem,IQA_Nit,IQA_Turb,IQA_Fos,IQA_Sot], [IQA_Total])

print dataset

# recupera treinamento da rede neural
fileObject = open ('results','r')
network = pickle.load(fileObject)
fileObject.close()

trainer = BackpropTrainer(network,dataset, learningrate = 0.01, momentum = 0.55)

erro,output,target = trainer.testOnData(dataset, verbose = True,returnOutputsTargets = True)

treina = len(output)

i = 0
total = 0.0
correto = 0.0

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


