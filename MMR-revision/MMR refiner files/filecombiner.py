f=open("lmmr.csv","r")
g=open("mmmr.csv","r")
h=open("hmmr.csv","r")
i=open("rmmr.csv","w")
for line in f:
    i.write(line)
for line in g:
    i.write(line)
for line in h:
    i.write(line)
