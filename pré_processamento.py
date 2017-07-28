# This Python file uses the following encoding: utf-8
import xlrd
import xlwt
import math



###########################Calculos definidos com base no documento ################################


def Oxigenio_Dissolvido(tmp, ccl, OD):


    #### calcula a concentração de saturação de oxigênio #####################

    
    Cs = (14.2 * math.exp(-0.0212* tmp) - ( 0.0016 * ccl  * math.exp(-0.0264 * tmp))) * (0.994 - (0.0001042 * altitude))

    ###### porcentagem de oxigênio dissolvido ##############

    POD = ((OD/Cs) * 100)

    print "POD ", POD

   ############### variáveis auxiliares para o calculo do oxigenio dissolvido ###################
    pi = math.pi

    y1 = 0.01396 * POD + 0.0873
    y2 = pi/56 * (POD - 27)
    y3 = pi/85 - (POD -15)
    y4 = (POD - 65)/10
    y5 = (65 - POD)/10
    seny1 = math.sin(y1)
    seny2 = math.sin(y2)
    seny3 = math.sin(y3)
    expr = math.exp(y4) + math.exp(y5)
    powseny1 = math.pow(seny1,2)

     

    if POD <= 100:
       qso = (100 * powseny1) - (( (2.5 + seny2 - (0.018 * POD)) + 6.86) * seny3 ) + 12/expr
    elif POD > 100 and POD <= 140 :
        qso = - 0.00777142857142832 * math.pow(POD,2) + 1.27854285714278 * POD + 49.8817148572
    
    elif POD > 140:
        qso = 47

    print "oxigenio Dissolvido  = ", qso
    print "seny1 ",seny1
    print   "seny12 ",math.pow(seny1,2) 

    print "essa porra mesmo ", math.exp(y4)
    return qso

#################################################################################################################################
################## coliformes Fecais ##############################################


def Coliformes_Fecais(CF):
    
    if CF <= 1000000:
        coliformes_fecais = 98.24034 - 34.7145 * (math.log(CF,10)) + 2.614267 * (math.pow(math.log(CF,10),2)) + 0.107821 * (math.pow(math.log(CF,10),3))
    else:
        coliformes_fecais = 3.0

    print "Coliformes fecais = ", coliformes_fecais
    return coliformes_fecais

#######################################################################################################################
################### PH ###############################################################################################

def PH(PH_var):

    if PH_var <= 2.0:

        PH = 2.0

    else:
        if PH_var > 2.0 and PH_var <= 6.9:

            PH = -37.1085 + (41.91277 * PH_var) - (15.7043*(math.pow(PH_var,2))) + ( 2.417486 * (math.pow(PH_var,3))) - ( 0.091252 * (math.pow(PH_var,4)))
        else:
            if PH_var > 6.9 and PH_var <= 7.1:

               PH =  -4.69365 - (21.4593 * PH_var) - (68.4561 * (math.pow(PH_var,2))) +  (21.638886 * (math.pow(PH_var,3))) - (1.59165 * (math.pow(PH_var,4)))

            else:
                if PH_var > 7.1 and PH_var <= 12.0:

                    PH =  -7698.19 + (3262.031 * PH_var) - (499.494 * math.pow(PH_var,2)) + (33.1551 * math.pow(PH_var,3)) - (0.810613 * math.pow(PH_var,4))

                else:

                    PH = 3.0
    print "PH = ",PH
    return PH


###################################################################################################################################
############################################## DBO ################################################################################

def Demanda_Oxigenio(DBO_var):

    if DBO_var <= 30:

        DBO = 100.9571 - (10.7121 * DBO_var) + (0.49544 * math.pow(DBO_var,2))  - (0.011167 * math.pow(DBO_var,3)) + ( 0.0001 * math.pow(DBO_var,4))

    else:
        DBO = 2.0

    print "DBO = ", DBO
    return DBO

#######################################################################################################################################
############################### Nitrato Total #########################################################################################

def Nitrato_Total(NO):

    if NO <= 10:

        Nitrato = -5.1 * NO + 100.17

    else:
        if NO > 10 and NO <= 60:

            Nitrato = -22.853 * (math.log(NO)) + 101.18

        else:
            if NO > 60 and NO <= 90:

                Nitrato = 10000000000 * (math.pow(NO, -5.1161))

            else:

                Nitrato = 1.0


    print  "nitrato = " , Nitrato
    return Nitrato

def Turbidez(tu):

    if tu <= 100:
        cos = 0.0571 * (tu - 30)
        turbidez = (90.37 * math.exp(-0.0169 * tu)) - (15 * math.cos(cos)* (math.pi/180))+ (10.22 * (math.exp(-0.231*tu))) - 0.8
    else:
        turbidez = 5.0


    print "turbidez = ", turbidez
    return turbidez


def Fosfato(PO):

    if PO <= 10:

       fosfato = (79.7*(math.pow(PO+0.821,-1.15)))
    else:
        fosfato = 5.0

    print fosfato
    return fosfato

def Solidos_Totais(ST):

    if ST <= 500:

       SoT =  (133.17 * math.exp(-0.0027 * ST)) - (53.17 * math.exp( -0.0141 * ST)) + ((-6.2 * math.exp(-0.00462 * ST)) * (math.sin(0.0146 * ST)))

    else:

       SoT = 30.0

    print SoT
    return SoT

def nivel_de_qualidade(IQA_total):

    if IQA_total > 90.0 and IQA_total <= 100.0:

        return "Excelente"
    else:
        if IQA_total > 70.0 and IQA_total <= 90.0:

            return "Bom"
        else:
            if IQA_total > 50 and IQA_total <= 70:

                return"Medio"
            else:
                if IQA_total > 25 and IQA_total <= 50:

                    return "Ruim"
                else:
                    if IQA_total > 0 and IQA_total <= 25:

                        return "Pessimo"





workbook = xlrd.open_workbook('2017.xls')#dados necessários para o pré processamento, para o rio grande o processo é o mesmo
worksheet = workbook.sheet_by_index(0)#primeira página do arquivo

IQA_tmp = str(92)#o IQA para a agua é constante
var_tem = 92
for row_num in xrange(worksheet.nrows):

    if row_num == 0:
        continue
    row = worksheet.row_values(row_num)

    
    tmpD.write(IQA_tmp + "\n")#escreve o IQA da agua no arquivo .txt

    ##  1  ####### Oxigenio Dissolvido #########

    altitude = row[7]
    Ccl = row[8] 
    print "cloreto",Ccl
    print "altitude",altitude
    Tmp = row[9] 
    print "Tmp",Tmp
    OD = row[10]
    print"OD",OD
    oxig = round(Oxigenio_Dissolvido(Tmp,Ccl,OD),2)

    if oxig >= 100:
        oxig = 100

    oxigenio = str(oxig)

    IQA.write( oxigenio + " ")
    
    ##  2  ######## Coliformes Fecais ###########
    CF =row [0]

    coliformes = round(Coliformes_Fecais(CF),2)
    print "coliformes ", CF

    col = str(coliformes)
    
    Cf.write(col + "\n")
    IQA.write(col + " ")



    ##  3  ########PH##############

    PH_var = row[1]
    print "ph", PH_var
    p_H = round(PH(PH_var),2)

    pH = str(p_H)

    ph.write(pH + "\n")
    IQA.write( pH + " ") 

    
    ##  4  ###### demanda bioquimica de oxigenio #########
    
    DBO_var = row[2]

    d_b_o = round(Demanda_Oxigenio(DBO_var),2)
    print "dbo", DBO_var
    db_o = str(d_b_o)

    dbo.write(db_o + "\n")
    IQA.write(db_o + " ")

   

    ##  5 ####Nitrato total##########

    NO = row[3]
    print "NO ", NO
    nit = round(Nitrato_Total(NO),2)
    ni = str(nit)

    nitrato.write(ni + "\n")
    IQA.write(ni + " ")

    

    ## 6 ######## Turbidez##################

    tu = row[4]
    print "turbidez ", tu
    turbi = round(Turbidez(tu),2)
    turb = str(turbi)
    tur.write(turb + "\n")
    IQA.write(  turb + " ")

    ##  7 ##################fosfato################

    PO = row[5] 

    print "fosfato ", PO
    fosfa = round(Fosfato(PO),2)
    fosf = str(fosfa)

    fos.write(fosf + "\n")
    IQA.write( fosf + " ")



    ##  8 ####### Solidos totais ##########

    ST = row[6]

    slt = round(Solidos_Totais(ST),2)
    solt = str(slt)


    st.write(solt + "\n")
    IQA.write( solt + " " + IQA_tmp + " ")

    IQA_total =  round((coliformes * 0.15) + (p_H * 0.12) + (d_b_o * 0.10)+ (nit * 0.10) + (turbi * 0.08) + (fosfa * 0.10) + (slt * 0.08) + (var_tem * 0.10),2)

    IQA_res = str(IQA_total)

    iqa.write(IQA_res + "\n")
    IQA.write(IQA_res + "\n")

    qualidade.write(nivel_de_qualidade(IQA_total) + "\n")


