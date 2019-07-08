# Natural-Language-DB-Query
Querying a database structure using natural language questions and answer - QA - system. 

Examples: 

Question: "What was the average score for assignment 1?"

Answer: "Average score for assignment 1 is 78,1."

Question: "From those who scored more than 80% on exam 1, what is the average score?"

Answer: "The average score for those who scored more than 80% on exam 1 is 90.95".

## System Design
How to translate natural language question into a structured database query and retrieve the proper results?

"From those who scored more than 80% on exam 1" - Condition is exam1 > 80%

"what is the average score?" - Calculation is average

The solution we found is:

1. Build the Database with certain structure

2. Question Parsing depend on the query pattern and transfer into SQL query

3. Data retrieving: finding and calculating with SQL query

4. Answer generation which feed back a certain number  (Ideally it should feed back with a full sentence and this step will be improved)

## The core NLP design of this project

### NLP Techniques in this project 

#### 1. Stanford Dependency Parser: 
Powered by a neural network, the parser outputs typed dependencies between words on a sentence.
![alt text](https://github.com/JKYang01/Natural-Language-DB-Query/blob/master/pictures/DEPEENCY_PARSER.png)

##### 2. Synonyms Substitution: 
users may refer to the same concept using different words or expressions. Synonym substitution should process the question to extract meaning from groups of words (bigrams, trigrams) and transform them to make it easier for the system to understand them.

What is the average score on assignment 1 / What is the mean for assignment 1? average = mean
What is Julie's score for assignments 1 and 2? / What is Julie's score for the first two assignments?
assignments 1 and 2 = first two assignments = assignment1 assignment2

#### 3. NLTK Chunk Package: 
A processing interface to identify non-overlapping groups in unrestricted text. 
Typically, chunk parsers are used to find base syntactic constituents, such as base noun phrases.
![alt text](https://github.com/JKYang01/Natural-Language-DB-Query/blob/master/pictures/NLP_CHUNKER1.png)

##### 4. StanfordCoreNLP Constituency  Parser:  
Provides full syntactic analysis, minimally a constituency parse of sentences.
Indicate the sub-sentence of a matrix sentence or phrase with the tag of “SBAR” .
It helps to identify the character of PrepositonPhrase_Clause and WHQuery_Clause.
![alt_text](https://github.com/JKYang01/Natural-Language-DB-Query/blob/master/pictures/constituency%20parser.png)

### The modules of natural language processing in this system
We use the NLP techneques above to do the preprocessing of sentence and extract the keywords and generate the SQL query
according to sentence structure and the key words.

#### 1. Sentence Parser 
The sentence parser include two steps:
1. Sentence detector: find the complex sentence 
2. Sentence spliter: split the complex sentence into simple ones and send to the next step

##### Example Code for sentence parser

###### Complex Sentence detecor:
```ruby
def detect_p(self,tree): # detect the complex preposition clause
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='PP') and ('SBAR' in child_nodes)
     
    def detect_s(self,tree): # detect the complex sentence sturcture
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='SBARQ') and ('SBAR' in child_nodes)
        
    def detect_conj(self,tree): #detect the conjunction
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='SBARQ') and ('CC' in child_nodes)

    def extract_sbar(self,tree):# extract the subsentence 
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
    #if (tree.label() == 'SBARQ') and ('WHPP' in child_nodes):
        return (tree.label()=='SBAR') and ('S'in child_nodes)

```
###### Sentence Parser:
```ruby
def split_pp(self,tags):   # ertract the matix PP 
        grammar = r"""P_CLAUSE:{<IN><DT>?<NN.*|PRP>?<W.*|NN.*><VB.*><JJ.*>?<IN|TO>?<NN.*|PRP|CD>?<IN|TO>?<NN.*|PRP|CD>?}
                  PP:{<IN|TO><NN.*|PRP|CD>}
                  CLAUSE:{<W.*><VB.*><DT|PRP$>?<JJ.*>?<NN.*|PRP|CD>+<PP>?}"""
        cp = nltk.RegexpParser(grammar)
        p = cp.parse(tags)
        chunks = []
        for subtree in p.subtrees(filter=lambda t: t.label() == 'P_CLAUSE'):
            chunk = ""
            for leave in subtree.leaves():
                chunk += leave[0] + ' '
                chunks.append(chunk.strip())
        return chunks[-1]


    def split_s(self,tags):  # extract the matix wh_clause
        grammar = r"""P_CLAUSE:{<IN><DT>?<NN.*|PRP>?<W.*|NN.*><VB.*><JJ.*>?<IN|TO><NN.*|PRP|CD><IN|TO>?<NN.*|PRP|CD>?}
                PP:{<IN|TO><NN.*|PRP|CD>}
                CLAUSE:{<W.*><VB.*><DT>?<JJ.*>?<NN.*|PRP|CD>+<PP>+}"""
        cp = nltk.RegexpParser(grammar)
        p = cp.parse(tags)
        chunks = []
        for subtree in p.subtrees(filter=lambda t: t.label() == 'CLAUSE'):
            chunk = ""
            for leave in subtree.leaves():
                chunk += leave[0] + ' '
                chunks.append(chunk.strip())
        return chunks[-1]
```
#### 2. Translater 
Using the dependency paser and generate SQL query by the corrdination of SQL command and grammatical component
1. preprosess the key words in sentence with synonym subsititution
2. using dependet paser and transfer into SQL query

##### Example code

###### Synonym Substitution:
```ruby
syn_01.append(['average', ['mean', 'avg']])
syn_01.append(['max', ['top', 'best', 'highest', 'maximum']])
syn_01.append(['min', ['worst', 'lowest', 'minimum']])
syn_01.append(['lastname', ['last name']])
syn_01.append(['firstname', ['first name']])
syn_01.append(['exam1', ['exam 1', 'exam one', 'first exam', '1 exam', '1st exam']])
syn_01.append(['exam2', ['exam 2', 'exam two', 'second exam', '2 exam', '2nd exam']])
syn_01.append(['exam1 exam2', ['both exams', 'all exams', 'exams 1 and 2', '2 exams', 'two exams']])
......
```
###### Translate to SQL query  
```ruby
def extract_calc(question):
    dbcols = ['assignment1', 'assignment2', 'assignment3', 'assignment4','assignment5', 'exam1', 'exam2', 'firstname', 'lastname']
    coreword = ''
    question = pre_process_question(question)
    qtokens = nltk.word_tokenize(question)
    
    # Dependencies
    dep_01 = dependency_parser.raw_parse(question)
    dep_01 = dep_01.__next__()
    deplist = list(dep_01.triples())      
    
    # WHAT questions
    if question.find('what') > -1:
        # find what que question is asking about
        for a,b,c in deplist:
            if (a[0] in ['what']) and (b == 'nsubj'):
                coreword = c[0]
        #Find operations
         if coreword != '':
             if coreword in ['average', 'max', 'min', 'sum']:
                 operation = coreword
            else:
                for a,b,c in deplist:
                    if (a[0] == coreword) and (b in ['amod','nmod', 'compound']):
                        ......            
        
        # Find Scope and Fields
            fields = []
            for word in qtokens:
                if word in dbcols[:7]: fields.append(word)   
            if operation == 'none':
                scope = 'for each'                
            else:
               .....
                
```

## Examples of the outcomes of this DB query system
![alt_text](https://github.com/JKYang01/Natural-Language-DB-Query/blob/master/pictures/example1.png)
![alt_text](https://github.com/JKYang01/Natural-Language-DB-Query/blob/master/pictures/example2.png)


