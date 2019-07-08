class Condition:
    """
    The Condition class is to help select which students
    in the database will be included in following calculations.
    This is done by comparison operators (==, !=, <, <=, >, >=)
    on an existing field (database header). When using these operators,
    the operands MUST be in the order of [<field>, <threshold>].
    For example, c1 = Condition('>=', ['exam1', 80]) would be a condition
    that selects all student who scored higher or equal to 80 on exam1.

    This class also supports Boolean operations (and, or, not).
    The operands for these must be instances of the Condition class,
    and obviously "not" should have one operand, while "and" and "or" have two.

    TO DO: write the validate function used to check that a condition is valid.
    """

    # initialization, needs operator and operands
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    # evaluate condition based on student information, returns True or False
    def evaluate(self, student):
        if self.operator in ['and', 'And', 'AND', '&', '&&']:
            return self.operands[0].evaluate(student) and self.operands[1].evaluate(student)
        elif self.operator in ['or', 'Or', 'OR', '||']:
            return self.operands[0].evaluate(student) or self.operands[1].evaluate(student)
        elif self.operator in ['not', 'Not', 'NOT']:
            return not self.operands[0].evaluate(student)
        elif self.operator == '==':
            return student[self.operands[0]] == self.operands[1]
        elif self.operator in ['!=', '~=', '<>']:
            return student[self.operands[0]] != self.operands[1]
        elif self.operator == '>':
            return student[self.operands[0]] > self.operands[1]
        elif self.operator == '>=':
            return student[self.operands[0]] >= self.operands[1]
        elif self.operator == '<':
            return student[self.operands[0]] < self.operands[1]
        elif self.operator == '<=':
            return student[self.operands[0]] <= self.operands[1]
        else:  # return None if operator is not found, shouldn't happen if validated
            return None

    # validates the condition, check fields do exist in database header, etc
    def validate(self, headers):
        pass

    # gives string representation of condition, can now use print(<Condition>)
    def __str__(self):
        if self.operator in ['not', 'Not', 'NOT']:
            return 'not (' + str(self.operands[0]) + ')'
        else:
            return '(' + str(self.operands[0]) + ') ' + self.operator + \
                    ' (' + str(self.operands[1]) + ')'

    def __repr__(self):
        return self.__str__()


class Query:
    """
    The Query class contains all the information about what question
    we're trying to ask the database.
    "condition" selects which students, and it should be an instance
    of the Condition class above.

    example: "Of those that pass both exams, who scored highest on assignment 1?"
    should give condition:
    c1 = Condition('>=', ['exam1', 50])
    c2 = Condition('>=', ['exam2', 50])
    c = Condition('and', [c1, c2])
    q.condition = c

    "calculation" gives information on what we're trying to calculate.
    It is a list of length three:
    [operation, 'for each' or 'for all', [fields]]
    "operation" (string) should be one of [max, min, average, weighted average, none]
    'for each' means the operation should be done for each student, while
    'for all' means the operation should be done for all students selected
    ["fields"] is a list of fields that we're asking about

    the same example above should have calculation:
    q.calculation = ['max', 'for all', ['assignment1']]

    "expectedResult" tells me 1. how many? and 2. what? should be returned
    it is a list of length two:
    [how many, [what]]
    "how many" can be 'scalar', 'vector' (or 'list'), or 'table'
    [what] is a list of all fields that is asked for

    the same example above should have expectedResult:
    q.expectedResult = ['scalar', ['firstname', 'lastname']]

    TO DO: finish "validate" function
    """
    def __init__(self):
        self.condition = None
        self.calculation = None
        self.expectedResult = None

    def validate(self, headers):
        return True

