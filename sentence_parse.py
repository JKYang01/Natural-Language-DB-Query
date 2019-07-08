#import nltk
from nltk.tree import Tree
#from nltk import word_tokenize, pos_tag
#import re 
# is this part should be deleted? because we call the stanford parser from the file Stanford_Parse
#from stanfordcorenlp import StanfordCoreNLP

# import two files that contains the function we need 

# the stanford paser
from Stanford_Parse import Parse
# import the function we need form Sentence_Detector class
from sentence_detector import detect

nlp = Parse()
#detect_s = sentence_detector.detect_s()
#detect_p = sentence_detector.detect_p()
#extract_sbar = sentence_detector.extract_sbar()
#detect_conj = sentence_detector.detect_conj()
#split_s = sentence_detector.split_s()
#split_pp = sentence_detector.split_pp()

# detect the structure of sentence. if it is a complex sentence that contains two clause it will return a list of clauses
# they are [p_wh_cluase and wh_clause] p_cluase is an ajunct which means it offers additonal information to the main clause
# according to our task the information about student will be translated to "condition"  and the other would be cauculation
# thus in the next step, the two clauses are processed seperately to extract informaton for conditon and caculation

class is_complex:
    
    def __init__(self,sentence):
        self.sentence = sentence
        self.tree = Tree.fromstring(str(nlp.parse(sentence)))
        self.tags = nlp.pos_tag(sentence)
        
    def sentence_split(self):
        #tree = Tree.fromstring(str(nlp.parse(sentence)))
        #tags = nlp.pos_tag(sentence)
        wh_list = ["what","which","who","how"]
        in_list = ["for","in","at","on","among","to","above","below","between","after","before"]
        b = [t for t in tree.subtrees(filter = detect.detect_s)]
        a = [t for t in tree.subtrees(filter = detect.detect_p)]
        c = [t for t in tree.subtrees(filter = detect.detect_conj)]
        n = len(a)
        a1 = a[0].leaves()
        b1 = b[0].leaves()

        if a and b:
            if n==2:
                if ',' in b1:
                    ss = sentence.split(',')
                    return ss
                else:
                    if b1[0] in wh_list:
                        b2 = [t.leaves() for t in b[0].subtrees(filter = detect.detect_p)][-1]
                        i = -len(b2)
                        return [' '.join(b1[0:i]),' '.join(b2)]
                    if b1[0] in in_list:
                        b2 = [t.leaves() for t in b[0].subtrees(filter = detect.extract_sbar)][-1]
                        i = -len(b2)
                        return [' '.join(b2),' '.join(b1[0:i-1])]
        
            if n==1 and b1[0] in in_list:
                b2 = [t.leaves() for t in b[0].subtrees(filter = detect.extract_sbar)][0]
                i = -len(b2)
                return [' '.join(b2),' '.join(b1[0:i-1])]
            if n==1 and b1[0]in wh_list:
                b2 = [t.leaves() for t in b[0].subtrees(filter = detect.detect_p)][0]
                i = -len(b2)
                return [' '.join(b1[0:i]),' '.join(b2)]
            
        if b and not a:
            #print("only b")
            if ',' in a1:
                ss = sentence.split(',')
                return ss
            else:
                e = [t.leaves() for t in b[0].subtrees(filter = detect.detect_p)]
                s = detect.split_s(sentence)
                return [s,' '.join(e[0])]  
    
        if a and not b:
            if n==2:
                if ',' in a1:
                    ss = sentence.split(',')
                    return ss
                else:
                    if a1[0] in wh_list:
                        e = [t.leaves() for t in a[0].subtrees(filter = detect.extract_sbar)]
                        p = detect.split_pp(sentence)
                        return [' '.join(e[1]),p]
                    if a1[0] in in_list:
                        e = [t.leaves() for t in a[0].subtrees(filter = detect.detect_p)]
                        s = detect.split_s(sentence)
                        return [s,' '.join(e[-1])]
                
            if n==1 :
                try:
                    e = [t.leaves() for t in tree.subtrees(filter = detect.extract_sbar)]
                    p = detect.split_pp(sentence)
                    return [' '.join(e[-1]),p]
            
                except:
                    e = [t.leaves() for t in a[0].subtrees() if t.label()=="SBAR"]
                    i = -len(e[-1])
                    return [' '.join(e[-1]),' '.join(a1[0:i])] 
        if c:
            p = re.split("\\band\\b",sentence)   
            return p                    
        else:
            return [sentence,'simple']

 


#test sentence:
#sentence = "what is john's average"
#sentence = 'between John Marry Joe what is the average score of them in exam2?'
#sentence = 'of thoes who got hihger than 80  what is the average score ?'
#sentence = 'what is the average score of thoes who got higher than 80?'
#sentence = 'for who got higher than 80 what is the average score?'
#sentence = 'For who got higher than 80 in the exams what is the average score of them in exam2?'
#sentence = 'What is their average score in exam2 of thoes who got higher than 80 in exam1'
#sentence = 'what is the average of exam2 for thoes who got higer than 80 in the exams'
#sentence = 'in exam1, who is the higheset?'
#sentence = 'for those who pass the exams who is the best?'
#sentence = "who is the best for thoes who passed the exams"
#sentence = 'On assignment1 assignment2 assignment3 which has the higheset average score'
#sentence = 'among assignment1 assigment2 assighment3 which has the highest score'
#sentence = 'among all of the assignments which has the highest score'
#sentence = 'for those who pass the exams what is the average of thoes who are higher than 80'
#print (tree)
#print(is_complex(tree))

def main(self, sentence):
    self.sentence=sentence
#    tree = Tree.fromstring(str(nlp.parse(sentence)))
#    tags = nlp.pos_tag(sentence)
    a = self.is_complex(sentence)
    if a == False:
        print ("*********************", sentence)
        print ("It is a simple sentence.")
    else:
        print(a)

is_complex("for who got higher than 80% in exam1 what is their average score in exame2")
        
