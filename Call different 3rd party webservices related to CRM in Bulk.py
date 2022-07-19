import requests
import json
import datetime
from random import randint
import csv
import base64
import pandas
import time
import sys
from time import sleep


wll_serviceType = '15'
mci_serviceType = '2'

#Request ID IOT starts with 0111 and production starts with 0110
def createRequestID():
    production_pre='0110'
    IOT_pre='0111'
    time_Now = datetime.datetime.now()
    rand = randint(100000,999999)
    request_ID = production_pre+time_Now.strftime("%Y%m%d%H%M%S")+str(rand)
    return request_ID

def result2CSV(ServiceNumber,get,fileCSV):
    data = json.loads(get.text)
    #print(data)
    for s in ("identificationType","identificationNo","classifier","creationDate","deleteStatus","providerName","id","result"):
        try:
            data[s]
        except:
            data[s] = '0'

    fileCSV.writerow([ServiceNumber,
                          data["response"],
                          data["requestId"],
                          data["id"],
                          data["result"],
                          data["comment"],
                          data["identificationType"],
                          data["identificationNo"],
                          data["classifier"],
                          data["creationDate"],
                          data["deleteStatus"],
                          data["providerName"]])

def result2CSV4APN(nationalID,p_APN,get,fileCSV):
    data = json.loads(get.text)
    #print(data)
    for s in ("identificationType","identificationNo","classifier","creationDate","deleteStatus","providerName","id","APN"):
        try:
            data[s]
        except:
            data[s] = '0'

    fileCSV.writerow([nationalID,
                          data["response"],
                          data["requestId"],
                          data["id"],
                          data["result"],
                          data["comment"],
                          data["identificationType"],
                          data["identificationNo"],
                          data["classifier"],
                          data["creationDate"],
                          data["deleteStatus"],
                          data["providerName"],
                          p_APN])


def QueryCRA():
    Production_userpass='***'
    url='***/classifier-enquiry'
    IOT="***"
    Production="***"
    header={"Content-Type":"application/json","Authorization":Production}
    wll_serviceType='15'
    mci_serviceType='2'
    numbersFile = open("c:\\CRA\\cra.txt", "r")
    fileCSV = csv.writer(open("c:\\CRA\\resultsCRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
        "classifier", "creationDate"])

    for line in numbersFile:
        #time.sleep(2)
        myReq = {"serviceType": mci_serviceType, "serviceNumber":"0"+line[0:10], "requestId": createRequestID()}  # python object (dict)
        #beacuse Line has \n I added line[0:10]
        get = requests.post(url, headers=header, data=json.dumps(myReq))
        #print(get)
        print(myReq)
        print(get.content.decode("utf-8"))
        serviceNumber= line
        result2CSV(serviceNumber,get,fileCSV)
    numbersFile.close()

def DeleteCRA():
    QueryCRA()
    url='***/update'
    header={"Content-Type":"application/json","Authorization":"***"}

    fileCSV = csv.writer(open("c:\\CRA\\results_DeleteCRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType",
         "identificationNo",
         "classifier", "creationDate"])
    with open('c:\\CRA\\resultsCRA.csv', mode='r') as queriedCRA:
        csv_reader = csv.DictReader(queriedCRA)
        for line in csv_reader:
            #time.sleep(3)
            if {line["response"]}  == {'200'}: #if respone of queryCRA == 200
                craID = f'{line["classifier"]}'
                serviceNumber= f'{line["ServiceNumber"]}'
                myReq = {"requestId": createRequestID(),"id":craID,"resellerCode": "11111", "serviceNumber":"0"+serviceNumber,"close":1 } #"0"+
                print(myReq)
                resp_deleteCRA = requests.post(url, headers=header, data=json.dumps(myReq))
                print(resp_deleteCRA.content.decode("utf-8"))  #badan check kon bebin khorojie in chia hast shayad az fieldash beshe estefade kard.


                result2CSV(serviceNumber, resp_deleteCRA, fileCSV)
                print("Deleted Succussfully")


def AddB2BCRA():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    service_number = '09166471160'
    IMSI='432113937317099'
    myReq = {"identificationNo": "10861231427",
             "identificationType": "5",  #nationalID = 5, identityCard=6
             "companyName": "كشت و صنعت گلستان دزفول",
             "registrationDate": "13721208",
             "agentFirstName": "علی",
             "agentLastName": "خواجوی",
             "agentFatherName": "غلامحسین",
             "agentIdentificationNo": "2003287231",
             "agentIdentificationType": "0",
             "agentBirthDate": "13670830",
             "agentBirthCertificateNo": "4140",
             "iranian": "1",  #Iranian for sefarat ha bayad 0 bashe
             "person": "0",
             "service": {"type": "2",
                         "mobileNumber": service_number,
                         "serial": IMSI,
                         "mobileType": "1",  # 15 ٌ WLL , #1 normal
                         "sms": "1",
                         "gprs": "1",
                         "mms": "1",
                         "wap": "1",
                         "threeG": "1",
                         "fourG": "1",
                         "videoCall": "1",
                         "resellerCode": "111111"},
             "requestId": createRequestID()}
    resp_addB2B = requests.post(url, headers=header, data=json.dumps(myReq))
    print (resp_addB2B.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\CRA\\resultsAdd_B2B_CRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    result2CSV(service_number, resp_addB2B, fileCSV)

def AddB2CCRA():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    service_number='09119110067'
    myReq =  {
        "name": "کبری",
        "family": "خادمیان نژاد امیری",
        "fatherName": "غلامرضا",
        "certificateNo": "2063221545",
        "birthDate": "13430101",
        "gender": "1",
        "identificationNo": "2063221545",
        "identificationType": "0",
        "iranian": "1",
        "person": "1",
            "address": {
            "address": "بابل ، شهرک بهزاد، فارابی 4",
            "postalCode": "1111111111"
            },
        "service": {
            "type": "2",
            "mobileNumber": service_number,
            "serial": "432111104505965",
            "mobileType": "2",
            "sms": "1",
            "gprs": "0",
            "mms": "0",
            "wap": "0",
            "threeG": "0",
            "fourG": "0",
            "videoCall": "1",
            "resellerCode": "111111"
            },
        "requestId": createRequestID()}
    resp_addB2C = requests.post(url, headers=header, data=json.dumps(myReq))
    print (resp_addB2C.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\CRA\\resultsAdd_B2C_CRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    result2CSV(service_number, resp_addB2C, fileCSV)

def MobileCount():
    url = '***/mobileCount'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    nationalID = '2050210086'

    myReq = {"requestId": createRequestID(),
             "identificationType": "0",#nationalID -> 0   1:passport
             "identificationNo": nationalID,
             }
    resp_MobileCount = requests.post(url, headers=header, data=json.dumps(myReq))
    print (resp_MobileCount.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\CRA\\resultsMobileCount.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    result2CSV(nationalID, resp_MobileCount, fileCSV)
def NOCR():
    url = '***/mobileCount'
    header = {"Content-Type": "application/json", "Authorization": "***"}

def ProviderQuery():
    QueryCRA()
    url='***/provider-enquiry'
    header={"Content-Type":"application/json","Authorization":"***"}

    fileCSV = csv.writer(open("c:\\CRA\\results_Provider.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType",
         "identificationNo",
         "classifier", "creationDate"])
    with open('c:\\CRA\\resultsCRA.csv', mode='r') as queriedCRA:
        csv_reader = csv.DictReader(queriedCRA)
        for line in csv_reader:
            if {line["response"]}  == {'316'}: #if respone of queryCRA == 316
                craID = f'{line["classifier"]}'
                serviceNumber= f'{line["ServiceNumber"]}'
                myReq = {"serviceType": mci_serviceType, "serviceNumber": "0" + serviceNumber[0:10],"requestId": createRequestID()}  # python object (dict)
                print(myReq)
                resp_Provider = requests.post(url, headers=header, data=json.dumps(myReq))
                print(resp_Provider.content.decode("utf-8"))  #badan check kon bebin khorojie in chia hast shayad az fieldash beshe estefade kard.


                result2CSV(serviceNumber, resp_Provider, fileCSV)
                print("Provider Queried Succussfully")


def AddB2B_CRA_Batch():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}

    fileCSV = csv.writer(open("c:\\CRA\\resultsAdd_B2B_CRA_Batch.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    df = pandas.read_csv('c:\\CRA\\Batch_Add_B2B.csv')

    row_column=df.shape #number of rows and columns
    print(row_column[0]) #number of rows

    for i in range(0,row_column[0]):
        time_Now = datetime.datetime.now()
        time.sleep(2)
        service_number = "0"+str(df['SERVICE_NUMBER'][i])
        IMSI = str(df['IMSI'][i])
        #Sefarat Request

        myReq = {
                              "identificationNo":"1444785",
                              "identificationType":"6",
                              "companyName":"سفارت دانمارک",
                              "registrationDate":"19790211",
                              "agentFirstName":"محمود",
                              "agentLastName":"شیخعلی زاده عمرانی",
                              "agentFatherName":"یداله",
                              "agentIdentificationNo":"5689852635",
                              "agentIdentificationType":"0",
                              "agentBirthDate":"13370101",
                              "agentBirthCertificateNo":"1",
                              "iranian":"0",
                              "person":"0",
                              "address": {
                 "address":"شریعتی بالاتر از پل صدر کوچه هدایت کوچه دشتی پلاک 10",
                 "postalCode":"1914861144",
                 "tel":"9121485603"
             },
                              "nationality": "DNK",
                                             "service":{
                                             "type":"2",
                                             "mobileNumber":service_number,
                                             "serial":IMSI,
                                             "mobileType":"1",
                                             "sms":"1",
                                             "gprs":"1",
                                             "mms":"1",
                                             "wap":"1",
                                             "threeG":"1",
                                             "fourG":"1",
                                             "videoCall":"1",
                                             "resellerCode":"111111"},
            "requestId": createRequestID()}
        '''
        #Normal Request:
        myReq = {"identificationNo": "10103647290",
             "identificationType": "5",  #nationalID = 5, identityCard=6
             "companyName": "مخابرات ایران",
             #"registrationNo":"956/500/د",
             "registrationDate": "13870403",
             "agentFirstName":"محمدرضا",
            "agentLastName":"عرب علی دوستی",
             "agentFatherName":"محمود",
             "agentIdentificationNo":"0042944910",
            "agentIdentificationType":"0",
             "agentBirthDate":"13451111",
              "agentBirthCertificateNo":"3122",
             "iranian": "1",  #Iranian for sefarat ha bayad 0 bashe
             "person": "0",
             "address": {
                 "address":"سهروردی شمالی خ توپچی پلاک 3 دفتر روابط عمومی	",
                 "postalCode":"1558919111",
                 "tel":"9128359301"
             },
             "service": {"type": "2",
                         "mobileNumber": service_number,
                          "serial": IMSI,
                         "mobileType": "1",  # 15 ٌ WLL , #1 normal
                         "sms": "1",
                         "gprs": "1",
                         "mms": "1",
                         "wap": "1",
                         "threeG": "1",
                         "fourG": "1",
                         "videoCall": "1",
                         "resellerCode": "111111"},
             "requestId": createRequestID()}
        '''
        print(myReq)
        resp_addB2B = requests.post(url, headers=header, data=json.dumps(myReq))
        print (time_Now.strftime("%Y%m%d%H%M%S") + resp_addB2B.content.decode("utf-8"))
        result2CSV(service_number, resp_addB2B, fileCSV)

def Query_Shops():
    Production_userpass='***'
    url='***/classifier-enquiry'
    header={"Content-Type":"application/json","Authorization":"***"}
    wll_serviceType='15'
    mci_serviceType='2'
    shop_serviceType = '30'
    numbersFile = open("c:\\CRA\\cra.txt", "r")
    fileCSV = csv.writer(open("c:\\CRA\\resultsCRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
        "classifier", "creationDate"])

    for line in numbersFile:
        myReq = {"serviceType": shop_serviceType, "serviceNumber":line[0:10], "requestId": createRequestID()}  # python object (dict)
        #beacuse Line has \n I added line[0:10]
        get = requests.post(url, headers=header, data=json.dumps(myReq))
        #print(get)
        print(myReq)
        print(get.content.decode("utf-8"))
        serviceNumber= line
        result2CSV(serviceNumber,get,fileCSV)
    numbersFile.close()


def Add_Shop_CRA():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    print('Please make sure you have the CSV File with this name in below path: \nc:\CRA\Batch_Add_CRA_Shop.csv \n\nPress Enter to Continue...')
    input()
    fileCSV = csv.writer(open("c:\\CRA\\resultsAdd_CRA_Shop_Batch.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    df = pandas.read_csv('c:\\CRA\\Batch_Add_CRA_Shop.csv', converters={'province': lambda x: str(x)})

    row_column = df.shape  # number of rows and columns
    print('Total Numbers of Shops : ', row_column[0])  # number of rows

    for i in range(0, row_column[0]):
        time_Now = datetime.datetime.now()
        time.sleep(4)
        try:
            name = str(df['name'][i])
            family = str(df['family'][i])
            fatherName = str(df['fatherName'][i])
            certificateNo = str(df['certificateNo'][i])
            birthDate = str(df['birthDate'][i])
            birthPlace = str(df['birthPlace'][i])
            gender = str(df['gender'][i])
            identificationNo = str(df['identificationNo'][i])
            iranian = str(df['iranian'][i])
            address = str(df['address'][i])
            postalCode = str(df['postalCode'][i])
            resellerCode = str(df['resellerCode'][i])
            province = str(df['province'][i])
        except:
                print('The CSV File has problem! Please check and try again. \n\nPress Enter to Exit...')
                #time.sleep(5)
                input()
                sys.exit()
        myReq = {"name": name,
                 "family": family,
                 "fatherName": fatherName,
                 "certificateNo": certificateNo,
                 "birthDate": birthDate,
                 "birthPlace": birthPlace,
                 "gender": gender, #2 woman - 1 man maybe
                 "identificationNo": identificationNo,
                 "identificationType": "0",
                 "iranian": iranian,
                 "person": "1",
                 "address": {"address": address,
                             "postalCode": postalCode},
                 "service": {"type": 30,
                             "resellerCode": resellerCode,
                             "province": '0'+province},
                 "requestId": createRequestID()}
        print(myReq)
        try:
            resp_addShop = requests.post(url, headers=header, data=json.dumps(myReq))
        except:
            print('Network has problem! Please make sure Keyhan is connected! \nYou can check the result path to see is there any results or not.\n\nPress Enter to Exit...')
            # time.sleep(5)
            input()
            sys.exit()
        print(time_Now.strftime("%Y%m%d%H%M%S") + resp_addShop.content.decode("utf-8"))
        result2CSV(resellerCode, resp_addShop, fileCSV)
    print('Finished Successfully! \nPlease go to this path to see the results: C:\CRA\\resultsAdd_CRA_Shop_Batch \n\nPress any key to Exit!')
    #time.sleep(5)
    input()

def AddAPNCRA():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    p_identificationNo = "10861532334"
    myReq = {"identificationNo": "10861532334",
             "identificationType": "5",  # nationalID = 5, identityCard=6
             "companyName": "کارت اعتباری ایران کیش",
             "registrationDate": "13820123",
             "agentFirstName": "آذر",
             "agentLastName": "رسولی",
             "agentFatherName": "محمد",
             "agentIdentificationNo": "4132445674",
             "agentIdentificationType": "0",
             "agentBirthDate": "13520625",
             "agentBirthCertificateNo": "239",
             "iranian": "1",  # Iranian for sefarat ha bayad 0 bashe
             "person": "0",
             "address": {
                            "postalCode": "1111111111"
            },
             "service": {"type": "31",
                         "apn": "139",
                         "province": "076"
                         },
             "resellerCode": "111111",
             "requestId": createRequestID()
            }
    print(myReq)
    resp_addB2B = requests.post(url, headers=header, data=json.dumps(myReq))
    print(resp_addB2B.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\CRA\\results_Add_APN_CRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
       ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
       "classifier", "creationDate"])
    result2CSV(p_identificationNo, resp_addB2B, fileCSV)

def queryAPNCRA():
    url = '***/provider-enquiry'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    p_APN_serviceType = '31'
    fileCSV = csv.writer(open("c:\\CRA\\results_Query_APN_CRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
    [ "companyName","APN_ServiceNumber", "response", "requestId", "id", "result", "comment","classifier", "providerName"])
    df = pandas.read_csv('c:\\CRA\\Query_APN.csv')

    row_column = df.shape  # number of rows and columns
    print(row_column[0])  # number of rows

    for i in range(0, row_column[0]):
        time_Now = datetime.datetime.now()

        p_APN_No = str(df['APN'][i])
        p_companyName = str(df['companyName'][i])

        myReq = {"serviceType": p_APN_serviceType, "serviceNumber": p_APN_No,
                         "requestId": createRequestID()}
        print(myReq)
        resp_queryAPN = requests.post(url, headers=header, data=json.dumps(myReq))
        print(resp_queryAPN.content.decode("utf-8"))  # badan check kon bebin khorojie in chia hast shayad az fieldash beshe estefade kard.

        result2CSV4APN(p_companyName,p_APN_No, resp_queryAPN, fileCSV)
        print("APN Queried Succussfully")

def AddAPNCRA_Batch():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}

    fileCSV = csv.writer(open("c:\\CRA\\results_Batch_Add_APN_CRA.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    df = pandas.read_csv('c:\\CRA\\Batch_Add_APN.csv')

    row_column = df.shape  # number of rows and columns
    print(row_column[0])  # number of rows

    for i in range(0, row_column[0]):
        time_Now = datetime.datetime.now()
        time.sleep(3)
        #service_number = "0" + str(df['ServiceNumber'][i])
        #IMSI = str(df['IMSI'][i])
        p_identificationNo = str(df['IDENTIFICATIONNO'][i])
        p_identificationType = str(df['IDENTIFICATIONTYPE'][i])
        p_companyName = str(df['COMPANYNAME'][i])
        p_registrationDate = str(df['REGISTRATIONDATE'][i])
        p_agentFirstName = str(df['AGENTFIRSTNAME'][i])
        p_agentLastName = str(df['AGENTLASTNAME'][i])
        p_agentFatherName = str(df['AGENTFATHERNAME'][i])
        p_agentIdentificationNo = str(df['AGENTIDENTIFICATIONNO'][i])
        p_agentIdentificationType = str(df['AGENTIDENTIFICATIONTYPE'][i])
        p_agentBirthDate = str(df['AGENTBIRTHDATE'][i])
        p_agentBirthCertificateNo = str(df['AGENTBIRTHCERTIFICATENO'][i])
        p_iranian = str(df['IRANIAN'][i])
        p_person = str(df['PERSON'][i])
        p_postalCode = str(df['POSTAL_CODE'][i])
        p_apn = str(df['APN_TPLID'][i])
        p_province = "0" +str(df['PROVINCE'][i])
        p_resellerCode = str(df['RESELLERCODE'][i])

        myReq = {"identificationNo": p_identificationNo,
                 "identificationType": p_identificationType,  # nationalID = 5, identityCard=6
                 "companyName": p_companyName,
                 "registrationDate": p_registrationDate,
                 "agentFirstName": p_agentFirstName,
                 "agentLastName": p_agentLastName,
                 "agentFatherName": p_agentFatherName,
                 "agentIdentificationNo": p_agentIdentificationNo,
                 "agentIdentificationType": p_agentIdentificationType,
                 "agentBirthDate": p_agentBirthDate,
                 "agentBirthCertificateNo": p_agentBirthCertificateNo,
                 "iranian": p_iranian,  # Iranian for sefarat ha bayad 0 bashe
                 "person": p_person,
                 "address": {
                     "postalCode": p_postalCode
                 },
                 "service": {"type": "31",
                             "apn": p_apn,
                             "province": p_province
                             },
                 "resellerCode": p_resellerCode,
                 "requestId": createRequestID()
                 }

        print(myReq)
        resp_addAPN = requests.post(url, headers=header, data=json.dumps(myReq))
        print(time_Now.strftime("%Y%m%d%H%M%S") + resp_addAPN.content.decode("utf-8"))
        result2CSV4APN(p_identificationNo,p_apn, resp_addAPN, fileCSV)


def Add_Shop_CRA_single():
    url = '***/put'
    header = {"Content-Type": "application/json", "Authorization": "***"}
    print('Please make sure you have the CSV File with this name in below path: \nc:\CRA\Batch_Add_CRA_Shop.csv \n\nPress Enter to Continue...')
    input()
    fileCSV = csv.writer(open("c:\\CRA\\resultsAdd_CRA_Shop_Batch.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["ServiceNumber", "response", "requestId", "id", "result", "comment", "identificationType", "identificationNo",
         "classifier", "creationDate"])
    df = pandas.read_csv('c:\\CRA\\3.csv', converters={'province': lambda x: str(x)})

    row_column = df.shape  # number of rows and columns
    print('Total Numbers of Shops : ', row_column[0])  # number of rows

    for i in range(0, row_column[0]):
        time_Now = datetime.datetime.now()
        time.sleep(4)

        myReq = {"name": 'حامد',
                 "family": 'علي اکبري',
                 "fatherName": 'حسن',
                 "certificateNo": '486',
                 "birthDate": '13530601',
                 "birthPlace":'شهرري',
                 "gender": '1', #2 woman - 1 man maybe
                 "identificationNo": '491481616',
                 "identificationType": "0",
                 "iranian": '1',
                 "person": "1",
                 "address": {"address": 'ميدان شهرري-خيابان قم-روبروي مخابرات شهيد منتظري-پلاک 242',
                             "postalCode":'1876774331'},
                 "service": {"type": "30",
                             "resellerCode":'2101403000',
                             "province":'21'},
                 "requestId": createRequestID()}
        print(myReq)
        try:
            resp_addShop = requests.post(url, headers=header, data=json.dumps(myReq))
        except:
            print('Network has problem! Please make sure Keyhan is connected! \nYou can check the result path to see is there any results or not.\n\nPress Enter to Exit...')
            # time.sleep(5)
            input()
            sys.exit()
        print(time_Now.strftime("%Y%m%d%H%M%S") + resp_addShop.content.decode("utf-8"))
        result2CSV(resellerCode, resp_addShop, fileCSV)
    print('Finished Successfully! \nPlease go to this path to see the results: C:\CRA\\resultsAdd_CRA_Shop_Batch \n\nPress any key to Exit!')
    #time.sleep(5)
    input()

#QueryCRA()
DeleteCRA()
#AddB2BCRA()
#AddB2CCRA()
#MobileCount()
#ProviderQuery()
#AddB2BBBBBBCRA()
#AddB2B_CRA_Batch()
#Query_Shops()
#Add_Shop_CRA()
#AddAPNCRA()
#AddAPNCRA_Batch()
#queryAPNCRA()
#Add_Shop_CRA_single()
