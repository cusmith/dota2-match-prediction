
#f=open("data.csv","r")
#g=open("lowElo.csv","r")
#h=open("midElo.csv","r")
i=open("highElo.csv","r")
j=open("hmmr.csv","w")
#k=open("hlmmr.csv","w")
x=0
z=0
for line in i:
    x=0
    y=line.split(',')
    x=((float)(y[0])*2/2.75)+((float)(y[1])/449)+((float)(y[2])/453)+((float)(y[3])/12159)
    #j.write(line)
    if(x>5):
        y[8]=5
    else:
        y[8]=4
        
    j.write((str)(y[0])+","+(str)(y[1])+","+(str)(y[2])+","+(str)(y[3])+","+(str)(y[4])+","+(str)(y[5])+","+(str)(y[6])+","+(str)(y[7])+","+(str)(y[8])+","+(str)(y[0])+"\n")

    #x=x+(float)(y[6])
    """if(float(y[9][0])==0):
        g.write(line)
    elif(int(y[9][0])==1):
        h.write(line)
    else:
        i.write(line)"""
#print (x/z)
