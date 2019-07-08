import nltk
from nltk.tree import Tree
# the file that run the stanfordcoreNLP 
from Stanford_Parse import Parse

#nlp = StanfordCoreNLP(r'C:\Users\wangtao\Documents\NLP_project\stanford-corenlp-full-2018-10-05')
#tree = Tree.fromstring(str(nlp.parse(sentence)))
#tags = nlp.pos_tag(sentence)
nlp = Parse()
#tags = nlp.pos_tag(sentence)
#tree = Tree.formstring(str(nlp.parser(sentence))
class detect:
    def __init__(self,sentence):
        self.sentence = sentence
        self.tree = Tree.fromstring(str(nlp.parse(sentence)))
        self.tags = nlp.pos_tag(sentence)
     
    def detect_p(self,tree):
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='PP') and ('SBAR' in child_nodes)
     
    def detect_s(self,tree): # detect the sentence sturcture
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='SBARQ') and ('SBAR' in child_nodes)
        
    def detect_conj(self,tree): #detect the conjunction
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
        return (tree.label()=='SBARQ') and ('CC' in child_nodes)
# extract the subsentence
    def extract_sbar(self,tree):# extract the subsentence 
        child_nodes = [child.label() for child in tree.subtrees() if isinstance(child, nltk.Tree)]
    #if (tree.label() == 'SBARQ') and ('WHPP' in child_nodes):
        return (tree.label()=='SBAR') and ('S'in child_nodes)

# # split sentence using nltk.chunker the RegexParser

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


    def split_s(self,tags): # extract the matix clause
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


if __name__ == '__main__':
    text = 'what is the average score on exam1.'
    tree = nlp.parse(text)
    print(tree)
    print(detect(text).split_s)









