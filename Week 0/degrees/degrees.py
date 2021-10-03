import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}



def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" 

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #although lecture checks for goal when a node is popped off the frontier, efficiency of search can be improved
    #by checking for a goal as nodes are ADDED. If goal detected, don't add it to frontier, just return the solution
    #immediately

    #create start point
    start = Node(state = source, parent = None, action = None)
    frontier = QueueFrontier()
    frontier.add(start)

    #create explored set
    explored = set()

    while True:
        #if nothing left in frontier, no path exists
        if frontier.empty():
            return None

        #choose a node from the frontier
        node = frontier.remove()
        #if node is goal, we have solution

        #add neighbors 2 frontier using function THATS ALR THERE DUMMY
        for (movie, star) in neighbors_for_person(node.state):
            newNode = Node(state = star, parent = node, action=movie)
            if not frontier.contains_state(newNode) and newNode.state not in explored:
                if newNode.state == target:
                    #reverse the solution
                    solution = []
                    while newNode.parent is not None:
                        actionTuple = (newNode.action, newNode.state)
                        solution.append(actionTuple)
                        newNode = newNode.parent
                    solution.reverse()
                    return solution
                else: frontier.add(newNode)

        #mark state as explored
        explored.add(node.state)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()








import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    #if len(sys.argv) != 2:
        #sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data("shopping.csv")#sys.argv[1])
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
        #lineCount = 0
        #first save the fields:
        numRow = 0
        next(csvReader)
        for row in csvReader:
            if(row[17] == "FALSE"):
                labelList.append(0)
            else: labelList.append(1)
            #labelList.append(row[17])
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
                    elif row[count] == "Jun":
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
            print(evidence)
        
    print(labelList) 
    print(len(labelList))
    print(len(evidenceList))
    returnTuple = (evidenceList, labelList)

    return returnTuple
    #raise NotImplementedError


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
    #raise NotImplementedError


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
    trueNeg = 0
    for data in range(len(labels)):
        if((predictions[data] == 1) and (predictions[data] == labels[data])):
            truePos+=1
        elif((predictions[data] == 0) and (predictions[data] == labels[data])):
            trueNeg+=1
    sensitivity = truePos/(len(labels) + 1)
    specificity = trueNeg/(len(labels) + 1)
    return (sensitivity, specificity)
        

    #raise NotImplementedError


if __name__ == "__main__":
    main()
