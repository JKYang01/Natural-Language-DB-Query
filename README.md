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

Build the Database with certain structure

Question Parsing depend on the query pattern and transfer into SQL query

Data retrieving: finding and calculating with SQL query

Answer generation which feed back a certain number 

(Ideally it should feed back with a full sentence and this step will be improved)

### NLP Techniques in this project

Stanford Dependency Parser: Powered by a neural network, the parser outputs typed dependencies between words on a sentence.
![alt text](https://raw.githubusercontent.com/username/projectname/branch/path/to/img.png)

Synonyms Substitution: users may refer to the same concept using different words or expressions. Synonym substitution should process the question to extract meaning from groups of words (bigrams, trigrams) and transform them to make it easier for the system to understand them.

What is the average score on assignment 1 / What is the mean for assignment 1? average = mean

What is Julie's score for assignments 1 and 2? / What is Julie's score for the first two assignments?

assignments 1 and 2 = first two assignments = assignment1 assignment2

NLTK Chunk Package: A processing interface to identify non-overlapping groups in unrestricted text. 
Typically, chunk parsers are used to find base syntactic constituents, such as base noun phrases.
![alt text](https://raw.githubusercontent.com/username/projectname/branch/path/to/img.png)

StanfordCoreNLP Constituency  Parser:  
Provides full syntactic analysis, minimally a constituency parse of sentences.
Indicate the sub-sentence of a matrix sentence or phrase with the tag of “SBAR” .
It helps to identify the character of PP_Clause and WH_Clause. 

