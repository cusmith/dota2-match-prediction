

import pprint


def load_dataset():
	x=[]
	f=open("data.csv","r")
	
	for line in f:
		#print line
		#line.rstrip()		
		y=line.split(',')
		#print (y[4])
		if(float(y[0])>2.66):
			y[0]=01
		else:
			y[0]=00
		if(float(y[1])>433):
			y[1]=11
		else:
			y[1]=10
		if(float(y[2])>423):
			y[2]=21
		else:
			y[2]=20
		if(float(y[3])>11173):
			y[3]=31
		else:
			y[3]=30
		if(float(y[4])>1315):
			y[4]=41
		else:
			y[4]=40
		if(float(y[5])>121):
			y[5]=51
		else:
			y[5]=50
		if(float(y[6])>4.4):
			y[6]=61
		else:
			y[6]=60
		y[9]=int((y[9])[0])
		y.remove(y[8])
		y.remove(y[7])
		#print (y)
		x.append(y)
	""""q=0
	for v in x:
		q=q+float(v[6])
			
	print (q/len(x))
	#print (x)"""
	#exit()
	
	return x

def createC1(dataset):
    # Create a list of candidate item sets of size one.
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    # frozenset because it will be a ket of a dictionary.
    # Note: forzensets just don't allow the set to be changed.
    return map(frozenset, c1)


def scanD(dataset, candidates, min_support):
    # Returns all candidates that meets a minimum support level
    sscnt = {}

    # Put subsets in a dict, store the # of occurrences 
    for tid in dataset:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1

    num_items = float(len(dataset))
    retlist = []
    support_data = {}

    # Start the reduction - only keep subsets that are >= threshold
    for key in sscnt:
        support = sscnt[key] / num_items
        if support >= min_support:
            retlist.insert(0, key)
        support_data[key] = support

    return retlist, support_data


def aprioriGen(freq_sets, k):
    # Generate the joint transactions from candidate sets
    retList = []
    lenLk = len(freq_sets)

    for i in range(lenLk):
        for j in range(i + 1, lenLk):

            # convert the set to a list, 
            # and only return the list of index 0 to k-2 items
            # Remember that we start with the null set and C1 set already - hence k-2
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                # for sets, | means 'union'
                retList.append(freq_sets[i] | freq_sets[j])
    return retList


def apriori(dataset, minsupport=0.5):
    # Generate a list of candidate item sets

    # returns a frozenset
    C1 = createC1(dataset)
    D = map(set, dataset)

    # Returns retList and support data for first set of candidates
    L1, support_data = scanD(D, C1, minsupport)
    L = [L1]
    k = 2

    # Now we can loop
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)

        # Returns retList and support data
        Lk, supK = scanD(D, Ck, minsupport)
        support_data.update(supK)
        L.append(Lk)
        k += 1

    return L, support_data



def generateRules(L, support_data, min_confidence=0.7):
    """Create the association rules
    L: list of frequent item sets
    support_data: support data for those itemsets
    min_confidence: minimum confidence threshold
    """
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            print ("freqSet", freqSet, 'H1', H1)
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, min_confidence)
    return rules


def calc_confidence(freqSet, H, support_data, rules, min_confidence=0.7):
    "Evaluate the rule generated"
    pruned_H = []
    for conseq in H:
        conf = support_data[freqSet] / support_data[freqSet - conseq]
        if conf >= min_confidence:
            print (freqSet - conseq, '--->', conseq, 'conf:', conf)
            rules.append((freqSet - conseq, conseq, conf))
            pruned_H.append(conseq)
    return pruned_H


def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.7):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)


if __name__ == "__main__":

    min_confidence = 0.85
    min_support = 0.4

    print ("Generating Frequent Sets (sup >= %s)..." % (min_support, ))
    D = load_dataset()
    L, support = apriori(D, minsupport=min_support)

    print ("Frequent Sets:\n")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint((L, support))

    print (40*"-")
    print ("Generating Rules (conf >= %s)... \n" % (min_confidence, ))

    rules = generateRules(L, support, min_confidence=min_confidence)
    pp.pprint(rules)









