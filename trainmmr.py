import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import csv

def main():
	with open('mmrdata.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		X_load = []
		y_load = []

		for row in csvreader:
			X_load.append(row[:6])
			y_load.append(row[-1])

	X = np.array(X_load, dtype='float32')
	y = np.array(y_load, dtype='float32')

	data_train, data_test, target_train, target_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

	# Random ForestClassifier
	clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
	clf = clf.fit(data_train, target_train)
	print clf.score(data_test, target_test)

	# Multinomial NB
	clf = MultinomialNB()
	clf = clf.fit(data_train, target_train)
	print clf.score(data_test, target_test)

	# SVC
	clf = svm.SVC()
	clf.fit(data_train, target_train)
	print clf.score(data_test, target_test)

if __name__ == "__main__":
    main()