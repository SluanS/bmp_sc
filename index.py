from openpyxl import load_workbook
import datetime
from io import BytesIO
from openpyxl.utils.datetime import from_excel

class returnObject:
    def __init__(self, new, newTime, transfered, situationUpdate):
        self.new = new
        self.newTime = newTime
        self.transfered = transfered
        self.situationUpdate = situationUpdate

def baterMapa(dia, planilhaHorario, planilhaNeoh):
    wbPre = load_workbook(BytesIO(planilhaHorario.getvalue()))
    dataPre = wbPre[dia]

    wbNeoh = load_workbook(BytesIO(planilhaNeoh.getvalue()))
    dataNeoh = wbNeoh[f"{wbNeoh.sheetnames[0]}"]

    curentGroup = {}
    updatedGroup = {}
    transfered = []
    new = []
    newTime = {}
    situationUpdate = {}


    for data in dataPre:
        if data[3].value != None:
            print(data[0].value)
            if (type(data[1].value) != str):
                curentGroup[f"{data[3].value}"] = [data[1].value, data[0].value]
            elif (type(data[1].value) == str and data[1].value != "Data Cirurgia"):
                try:
                    dateStr = data[1].value.replace("/","-")
                    formatedDate = datetime.datetime.strptime(dateStr, "%d-%m-%Y %H:%M")
                    curentGroup[f"{data[3].value}"] = [formatedDate, data[0].value]
                except ValueError:
                     convertedData = from_excel(float(data[1].value)).strftime("%d/%m/%Y %H:%M").replace("/","-")
                     formatedDate = datetime.datetime.strptime(convertedData, "%d-%m-%Y %H:%M")
                     curentGroup[f"{data[3].value}"] = [formatedDate, data[0].value]

                    
                    
    for data in dataNeoh: 
        if (data[1].value != None and data[0].value != None and data[3].value != None and data[1].value != "Data agendada"):
            dateStr = data[1].value.replace("/","-")
            formatedDate = datetime.datetime.strptime(dateStr, "%d-%m-%Y %H:%M")
            updatedGroup[f"{data[0].value}"] = [formatedDate, data[3].value]

    # Verifica se existe avisos novos
    for k, v in updatedGroup.items():
        if k not in curentGroup:
            new.append(k)


    #Verifica se houveram transfências ou alteração de situação/horário
    for k, v in curentGroup.items():
        print(k, v)
        if k in updatedGroup:
            currentTime = updatedGroup[k][0]
            if (v[0] != currentTime):
                newTime[f"{k}"] = [currentTime,v[0]]
            #Verfica se houvera autorizações
            if (v[1] == "ANÁLISE OPERADORA" or v[1] == "ANALISE OPERADORA"):
                newSituation = updatedGroup[f"{k}"][1]
                if(newSituation != "ANÁLISE OPERADORA" or newSituation != "ANALISE OPERADORA"):
                    print("Autorizado")
                    situationUpdate[f"{k}"] = [v[1], newSituation]
        else:
            transfered.append(k)
    return returnObject(new,newTime,transfered,situationUpdate)