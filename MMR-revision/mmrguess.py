input=open("data.csv",'r')
#output=open("",w)
for line in input:
    y=line.split(',')
    if((int)(y[9])==2):
        if((((float)(y[0])*2/2.75)+((float)(y[1])/449)+((float)(y[2])/453)+(float)(y[3])/12159)>5):
            print(5)
        else:
            print (4)
    elif((int)(y[9])==1):
        if((((float)(y[0])*2/2.66)+((float)(y[1])/426)+((float)(y[2])/420)+(float)(y[3])/11064)>5):
            print (3)
        else:
            print(2)
    else:
        if((((float)(y[0])*2/2.48)+((float)(y[1])/413)+((float)(y[2])/364)+(float)(y[3])/9080)>5):
            print(1)
        else:
            print(0)
