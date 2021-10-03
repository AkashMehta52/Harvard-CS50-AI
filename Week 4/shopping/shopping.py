import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidenceList = []
    labelList = []
    
    with open(filename) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        numRow = 0
        next(csvReader)
        for row in csvReader:
            if(row[17] == "FALSE"):
                labelList.append(0)
            else: labelList.append(1)
            evidence = [None] * 17
            evidenceList.append(evidence)
            for count in range(17):
                if count == 0 or count == 2 or count == 4 or (count >= 11 and count <= 14):
                    evidenceList[numRow][count] = int(row[count])
                elif count == 10:
                    if row[count] == "Jan":
                        evidenceList[numRow][count] = 0
                    elif row[count] == "Feb":
                        evidenceList[numRow][count] = 1
                    elif row[count] == "Mar":
                        evidenceList[numRow][count] = 2
                    elif row[count] == "Apr":
                        evidenceList[numRow][count] = 3
                    elif row[count] == "May":
                        evidenceList[numRow][count] = 4
                    elif row[count] == "June":
                        evidenceList[numRow][count] = 5
                    elif row[count] == "Jul":
                        evidenceList[numRow][count] = 6
                    elif row[count] == "Aug":
                        evidenceList[numRow][count] = 7
                    elif row[count] == "Sep":
                        evidenceList[numRow][count] = 8
                    elif row[count] == "Oct":
                        evidenceList[numRow][count] = 9
                    elif row[count] == "Nov":
                        evidenceList[numRow][count] = 10
                    elif row[count] == "Dec":
                        evidenceList[numRow][count] = 11
                elif count == 15:
                    if row[count] == "Returning_Visitor":
                        evidenceList[numRow][count] = 1
                    else:
                        evidenceList[numRow][count] = 0
                elif count == 16:
                    if row[count] == "TRUE":
                        evidenceList[numRow][count] = 1
                    else:
                        evidenceList[numRow][count] = 0
                else:
                    evidenceList[numRow][count] = float(row[count])
            numRow += 1
        
    returnTuple = (evidenceList, labelList)

    return returnTuple


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    #evidence is all TRAINING data, so we need to fit our classifier
    #to it
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #labels and predictions
    truePos = 0
    pos = 0
    trueNeg = 0
    neg = 0
    for data in range(len(labels)):
        if((predictions[data] == 1)):
            pos+=1
            if((predictions[data] == labels[data])):
                truePos+=1
        elif((predictions[data] == 0)):
            neg+=1
            if((predictions[data] == labels[data])):
                trueNeg+=1
    sensitivity = truePos/pos
    specificity = trueNeg/neg
    return (sensitivity, specificity)
        


if __name__ == "__main__":
    main()
