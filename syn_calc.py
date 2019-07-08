
# coding: utf-8

# In[2]:


import nltk
import re
from nltk.corpus import wordnet
from nltk import stanford


# In[3]:


#Loading Stanford parser
from nltk.parse.stanford import StanfordDependencyParser

#path_to_jar = '/Users/fernandogranato/Documents/Mestrado/IST664 - NLP/Stanford Parser/stanford-parser-full-2018-10-17/stanford-parser.jar'
#path_to_models_jar = '/Users/fernandogranato/Documents/Mestrado/IST664 - NLP/Stanford Parser/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'
path_to_jar = r'C:/Users/wangtao/Documents/NLP_project/stanford-parser-full-2018-10-17/stanford-parser.jar'
path_to_models_jar = r'C:/Users/wangtao/Documents/NLP_project/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'

dependency_parser = StanfordDependencyParser(path_to_jar = path_to_jar, path_to_models_jar = path_to_models_jar)


# In[6]:


# Synonyms
# to Fernando: Should I output this into a .txt file?
syn_01 = []
syn_01.append(['average', ['mean', 'avg']])
syn_01.append(['max', ['top', 'best', 'highest', 'maximum']])
syn_01.append(['min', ['worst', 'lowest', 'minimum']])
syn_01.append(['lastname', ['last name']])
syn_01.append(['firstname', ['first name']])
syn_01.append(['exam1', ['exam 1', 'exam one', 'first exam', '1 exam', '1st exam']])
syn_01.append(['exam2', ['exam 2', 'exam two', 'second exam', '2 exam', '2nd exam']])
syn_01.append(['exam1 exam2', ['both exams', 'all exams', 'exams 1 and 2', '2 exams', 'two exams']])
syn_01.append(['assignment1', ['assignment 1', 'assignment one', 'first assignment', '1st assignment']])
syn_01.append(['assignment2', ['assignment 2', 'assignment two', 'second assignment', '2nd assignment']])
syn_01.append(['assignment3', ['assignment 3', 'assignment three', 'third assignment', '3rd assignment']])
syn_01.append(['assignment4', ['assignment 4', 'assignment four', 'fourth assignment', '4th assignment']])
syn_01.append(['assignment5', ['assignment 5', 'assignment five', 'fifth assignment', '5th assignment']])
syn_01.append(['assignment1 assignment2', ['assignments 1 and 2', 'assignments 1 to 2', 'assignments 1-2', 'first two assignments', 'first 2 assignments']])
syn_01.append(['assignment1 assignment3', ['assignments 1 and 3', 'first and third assignments']])
syn_01.append(['assignment1 assignment2 assignment3', ['assignments 1 to 3', 'assignments 1-3', 'first three assignments', 'first 3 assignments']])
syn_01.append(['assignment2 assignment3', ['assignments 2 and 3', 'assignments 2 to 3', 'assignments 2-3', 'assignments two to three']])
syn_01.append(['assignment1 assignment2 assignment3 assignment4', ['assignments 1 to 4', 'assignments 1-4', 'first four assignments', 'first 4 assignments']])
syn_01.append(['assignment1 assignment2 assignment 3 assignment5', ['assignments 1 to 5', 'assignments 1-5', 'all assignments', '5 assignments', 'five assignments']])


# In[7]:


# Synonyms Substitution
def pre_process_question(question):
    sub_words = question.lower()
    for a, b in syn_01:
        for c in b:
            if sub_words.find(c) > -1:
                sub_words = re.sub(c, a, sub_words)
    return(sub_words)


# In[1]:


#Function extract_calc will parse the question and identify dependecies to understand what the user is asking about
#After parsing the calculation method and parameters should be extracted from the question
#4 types of questions: what, who, how many and which(?)
#What questions reasoning:
    #Find coreword from 'what' - nsubj - what is the user asking about
    #Look for operations on the dependencies of coreword
        #If operation is found, set operation as it is
        #If operation not found, set operation as 'none'
    #If operation was found, look for fields and scope
        #look up for fied names on question and add them to a list
        #if operation = 'none', scope = 'for each'
        #otherwise
            #if length of fields list = 1, scope = 'for all'
            #if length of fields list > 1, scope = 'for each'

def extract_calc(question):
    dbcols = ['assignment1', 'assignment2', 'assignment3', 'assignment4','assignment5', 'exam1', 'exam2', 'firstname', 'lastname']
    coreword = ''
    question = pre_process_question(question)
    #print(question)
    qtokens = nltk.word_tokenize(question)
    
    #Dependencies
    dep_01 = dependency_parser.raw_parse(question)
    dep_01 = dep_01.__next__()
    deplist = list(dep_01.triples())
    
    #print(deplist) #debug
    
    #WHAT questions
    if question.find('what') > -1:
        
        #print('What question.') #debug
        
        #find what que question is asking about
        for a,b,c in deplist:
            if (a[0] in ['what']) and (b == 'nsubj'):
                coreword = c[0]
                
                #print('Coreword is ',coreword) #debug
                
                break
            else:
                continue
        
        #Find operations
        if coreword != '':
            if coreword in ['average', 'max', 'min', 'sum']:
                operation = coreword
            else:
                for a,b,c in deplist:
                    if (a[0] == coreword) and (b in ['amod','nmod', 'compound']):
                        if c[0] in ['average', 'max', 'min', 'sum']:
                            operation = c[0]
                            break
                    else:
                        operation = 'none'
            
        #Find Scope and Fields
            fields = []
            for word in qtokens:
                if word in dbcols[:7]: fields.append(word)
            
            if operation == 'none':
                scope = 'for each'
                
            else:
                if (len(fields) > 1): scope = 'for each'
                if (len(fields) == 1): scope = 'for all'
                if (len(fields) == 0):
                    fields.append('courseaverage') #find the correct name
                    scope = 'for all'
                    
        else:
            #print('Error. I did not understand the question.')
            return('Error. I did not understand the question.')
            
        #print('Operation: ',operation) #debug
        #print('Scope: ',scope) #debug
        #print('Fields: ', fields) #debug
            

    #WHO questions
    if question.find('who') > -1:
        
        #print('who question') #debug
        
        fields = ['firstname', 'lastname']
        scope = 'for each'
        
        for op in ['average', 'max', 'min', 'sum']:
            if question.find(op) > -1: 
                operation = op
                break
            else:
                operation = 'none'
                continue
            
            #Fields:
        for word in qtokens:
            if word in dbcols[:7]: fields.append(word)
        
        if len(fields) < 3: fields.append('courseaverage')
        
        #print('Operation: ', operation) #debug
        #print('Scope: ', scope) #debug
        #print('Fields: ', fields) #debug
    
    
    #HOW MANY questions
    if question.find('how many') > -1:
        
        #print('how many question') #debug
        
        operation = 'none'
        fields = []
        scope = ''
        
        #print('Operation: ', operation) #debug
        #print('Scope: ', scope) #debug
        #print('Fields: ', fields) #debug

    #    if sub_words.find('which') > -1:
    
    try:
        return(operation, scope, fields)
    except:
        return('Error.')
            

