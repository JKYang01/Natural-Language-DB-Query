from query import *

class Database:
    """
    The Database class contains the data itself, as well as
    functions to answer queries.
    """
    def __init__(self):
        self.headers = []
        self.scoreheaders = []
        self.students = dict()
        self.numstudents = 0
        self.weights = dict()

    # imports data from given file,
    # note that the weights assume 5 assignments, 2 exams,
    # and a "courseaverage" has been calculated with that assumption
    def import_data(self, filename):
        file = open(filename, mode='r')
        header = file.readline()
        headers = header.strip().split(',')
        self.headers = headers
        self.scoreheaders = headers[3:]
        # print(self.scoreheaders)
        self.set_weights(headers)

        for line in file:
            if len(line) == 0:
                break
            items = line.split(',')
            student = dict()
            for (h, i) in zip(headers, items):
                if h == "firstname" or h == "lastname":
                    student[h] = i
                else:
                    student[h] = int(i)
            student['courseaverage'] = \
                sum([self.weights[field] * student[field]\
                     for field in self.weights])

            self.students[student['studentnumber']] = student
            self.numstudents += 1

        self.scoreheaders.append('courseaverage')
        self.weights['courseaverage'] = 0
        file.close()

    def set_weights(self, headers):
        assert len(headers) == 10
        self.weights['assignment1'] = 0.06
        self.weights['assignment2'] = 0.06
        self.weights['assignment3'] = 0.06
        self.weights['assignment4'] = 0.06
        self.weights['assignment5'] = 0.06
        self.weights['exam1'] = 0.3
        self.weights['exam2'] = 0.4

    def process_query(self, query):
        if not query.validate(self.headers):
            return None

        selected = self.make_selection(query.condition)
        # print(selected)
        if len(selected) == 0:
            return []

        tempresult = self.do_calculation(query.calculation, selected)

        finalresult = self.extract_result(query, tempresult)
        return finalresult

    def make_selection(self, condition):
        if condition is None:
            return self.students.keys()
        else:
            return [x for x in self.students.keys()\
                    if condition.evaluate(self.students[x])]

    def do_calculation(self, calc, sel):
        if calc[0] is None or calc[0] in ["None", "none", "NONE"]:
            return sel
        elif calc[0] in ['max', 'min']:
            return self.find_max(calc, sel)
        elif calc[0] == 'average':
            return self.find_average(calc, sel)


    def extract_result(self, query, tempresult):
        #print(tempresult)
        if query.expectedResult[0] == 'scalar':
            if query.calculation[0] is None or\
               query.calculation[0] in ["None", "none", "NONE"]:
                if len(query.expectedResult[1]) == 0 or query.expectedResult[1][0] == "count":
                    return len(tempresult)
                else:
                    return self.students[tempresult[0]][query.expectedResult[1][0]]
            elif query.calculation[0] in ['max', 'min']:
                (studentnumber, score) = tempresult
                result=[]
                for field in query.expectedResult[1]:
                    if field in self.headers:
                        result.append(self.students[studentnumber][field])
                    elif field == 'score':
                        result.append(score)
                return result
            elif query.calculation[0] == 'average':
                return tempresult

        elif query.expectedResult[0] == 'table':
            if query.calculation[0] is None or \
               query.calculation[0] in ["None", "none", "NONE"]:
                students = tempresult
                result = []
                for s in students:
                    studentresult = [self.students[s][field]\
                                     for field in query.expectedResult[1]]
                    result.append(studentresult)
                return result
            else:
                result = []
                for student, res in tempresult:
                    studentresult = []
                    for field in query.expectedResult[1]:
                        if field in self.headers:
                            studentresult.append(self.students[student][field])
                        elif field in ['score', 'field']:
                            studentresult.append(res)
                    result.append(studentresult)
                return result

    def find_max(self, calc, sel):
        if calc[0] == 'max':
            m = 1
        else:
            m = -1

        if calc[1] == 'for each':
            fields = calc[2]
            results = []
            for s in sel:
                scores = [m * self.students[s][field] for field in fields]
                score, field = max(zip(scores, fields))
                results.append((s, field))
            return results
        elif calc[1] == 'for all':
            if len(calc[2]) == 1:
                field = calc[2][0]
                assert field in self.scoreheaders
                scores = [m * self.students[s][field] for s in sel]
                score, studentnumber = max(zip(scores, sel))
                return studentnumber, score * m
            else:
                scores = []
                for s in sel:
                    student = self.students[s]
                    itemscores = [self.weights[field] * student[field]\
                                  for field in calc[2]]
                    studentscore = sum(itemscores)/sum([self.weights[field]\
                                                        for field in calc[2]])
                    scores.append(m * studentscore)
                score, studentnumber = max(zip(scores, sel))
                return studentnumber, score * m

    def find_average(self, calc, sel):
        fields = calc[2]
        if calc[1] == 'for each':
            results = []
            for s in sel:
                itemscores = [self.weights[field] * self.students[s][field]\
                              for field in fields]
                studentscore = sum(itemscores) / sum([self.weights[field]\
                                                      for field in fields])
                results.append((s, studentscore))
            return results
        elif calc[1] == 'for all':
            tempsum = 0
            for s in sel:
                itemscores = [self.weights[field] * self.students[s][field]\
                              for field in fields]
                studentscore = sum(itemscores) / sum([self.weights[field]\
                                                      for field in fields])
                tempsum += studentscore
            average = tempsum / len(sel)
            return average


if __name__ == "__main__":
    db = Database()
    db.import_data("data.csv")
    print(db.students[1])
    print(db.numstudents)

    c1 = Condition('>=', ['exam1', 50])
    c2 = Condition('>=', ['exam2', 50])
    c = Condition('And', [c1, c2])
    print(c.evaluate(db.students[1]))
    print(c.evaluate(db.students[2]))
    print(c)

    q = Query()
    q.condition = c
    q.calculation = ['max', 'for all', ['assignment1']]
    q.expectedResult = ['scalar', ['firstname', 'lastname']]

    result = db.process_query(q)
    print(result)

