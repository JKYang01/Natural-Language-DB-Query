#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from stanfordcorenlp import StanfordCoreNLP

# In[ ]:
# to run the StanfordCoreNLP we should downloade the package first
# from website:
# then run in the terminal with following command:
# # java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# # "*" should be replaced with address of the where the StanfordCoreNLP package 
# # java -mx4g -cp "C:\Users\wangtao\Documents\NLP_project\stanford-corenlp-full-2018-10-05\*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000


# In[ ]:


''' 
Parts of our parse function is based on the following source
Citation: https://www.khalidalnajjar.com/setup-use-stanford-corenlp-server-python/
''' 


# In[ ]:


class Parse:

    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props ={'annotators': 'tokenize,pos,ner,parse,depparse,dcoref,relation',
         'pipelineLanguage': 'en','outputFormat': 'json'}

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)
    
    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def depparse(self, sentence):
        return self.nlp.depparse(sentence)

    def pos_tag(self, sentence):
        return self.nlp.pos_tag(sentence)


if __name__ == '__main__':
    nlp = StanfordCoreNLP()
    text = 'what is the average score on exam1.'
    tree = nlp.parse(text)
    print(tree)

