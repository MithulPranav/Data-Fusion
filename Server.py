import json
import time
import math
import paho.mqtt.client as mqtt
from datetime import datetime
import mysql.connector

Loc="LAB"
Tempdata=[]
Humdata=[]
m=[]
f=[]

def Fuse(data1,data2):
    print("the whole dataset is ",data1,data2)
    for i in range(len(data1)):
        m1=float(int(data1[i])/sum(data1))
        m.append(m1)
    print(m)
    for i in range(len(data2)):
        f1=float(int(data1[i])/sum(data2))
        f.append(f1)
    print(f)
    sum1=0
    for i in range(len(f)):
       sum1+=f[i]
    mean=float(sum1/7)
    #print (mean)
    sum1=0
    for i in range(len(f)):
      sum1+=math.pow((mean-f[i]),2)
    d=math.sqrt(sum1/7)
    #print (d)

    dmin=10
    dmax=0
    for i in range(len(f)):
        if dmin>f[i]-d:
            dmin=f[i]
        if dmax<f[i]-d:
            dmax=f[i]
    #print (dmin)
    #print (dmax)
    print ("Step 1 completed")

    #step 2
    dls=abs(d-dmin)
    dns=abs(d-dmax)
    dlsns=abs(d-(dmax-dmin)/2)
    #print (dls)
    #print (dns)
    #print (dlsns)
    print ("Step 2 completed")

    #step 3
    mls=dls/(dls+dns+dlsns)
    mns=dns/(dls+dns+dlsns)
    mlsns=dlsns/(dls+dns+dlsns)
    #print (mls)
    #print (mns)
    #print (mlsns)
    #print ("Step 3 Completed")

    #step 4
    fmax=0
    mmax=0
    betls=[]
    for i in range(len(f)):
        if fmax<f[i]:
            fmax=f[i]
        if mmax<m[i]:
            mmax=m[i]

    for i in range(len(f)):
        ai=f[i]/fmax
        mils=ai*mls
        mins=ai*mns
        milsns=ai*mlsns+(1-ai)

        aj=m[i]/mmax
        mjls=aj*mls
        mjns=aj*mns
        mjlsns=aj*mlsns+(1-aj)

        #step 5
        mijls=(mils*mjlsns+milsns*mjls)/(1-(mils*mjns+mins*mjls))
        mijns=(mins*mjlsns+milsns*mjns)/(1-(mils*mjns+mins*mjls))
        mijlsns=(milsns*mjlsns)/(1-(mils*mjns+mins*mjls))
        #print (i)
        #print (mijls)
        #print (mijns)
        #print (mijlsns)

        #step 6
        betls.append(mijls+(mijlsns/2))
    print ("Step 4,5,6 completed")

    # step 7
    maax=0
    pos=0
    print ("betls:")
    print (betls)
    for i in range(len(betls)):
        if maax<betls[i]:
            maax=betls[i]
            pos=i+1
    print (maax)
    print (pos)
    print ("Step 7 completed")
    data={}
    data["Temp"]=data1[pos-1]
    data["Hum"]=data2[pos-1]
    print ("The data ",data["Temp"],data["Hum"]," can be fused to obtain the best fusion result")
    return data

def on_connect(client, userdata, flags, rc):
    if rc==0:
       print("Connected")

def on_subscribe(client, obj, mid, granted_qos):
    print('SUBSCRIBER-1 : interested in [humidity,temperature]')
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, obj, msg):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Topic: ",msg.topic,msg.payload)
    if msg.topic=="THData":
        data=json.loads(msg.payload.decode("utf-8"))
        
        #Fusion
        Res=Fuse(data["Temp"],data["Hum"])
        print ("Fused Result: ",Res)

        #Local Database
        try:
            mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="adminmanager308",
            database="FUSION")
        except:
            print("Error while conn")
        cur=mydb.cursor()
        try:
            DATE = time.strftime('%Y-%m-%d %H:%M:%S')
            TIME = time.strftime('%Y-%m-%d %H:%M:%S')
            sql="INSERT INTO "+data["Loc"]+" (TEMPERATURE,HUMIDITY,DATE,TIME) VALUES (%s,%s,%s,%s)"
            val=(Res["Temp"],Res["Hum"],DATE,TIME)
            cur.execute(sql,val)
            mydb.commit()
        except:
            print("Error while inserting data in database")
            mydb.rollback()
        cur.close()

# Callback
mqttc = mqtt.Client("P2")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Receiving data for 30 Seconds
mqttc.username_pw_set('rnzmvzya', 'XwYSvlxWroVR')
mqttc.connect('m13.cloudmqtt.com',16433 )
mqttc.subscribe("THData",0)
mqttc.loop_forever()
