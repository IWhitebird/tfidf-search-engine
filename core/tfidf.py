import os
from uuid import uuid4
from math import log

class Document:
    def __init__(self, id, title, content, path):
        self.id = id
        self.title = title
        self.content = content
        self.path = path

class Tfidf:
    def __init__(self):
        self.curPath = os.getcwd() 
        self.path = os.path.join(self.curPath,'core', 'news_k50')
        self.documents = []
        # Read and save all documents in the Database
        for filename in os.listdir(self.path):
            if(filename == '.DS_Store'):
                continue
            with open(os.path.join(self.path, filename), 'r' , encoding='utf-8') as file:
                fileString = file.read().lower()
                i = fileString.find('\n')
                title = fileString[:i]
                content = fileString[i + 1:]
                self.documents.append(Document(uuid4(), title, content, os.path.join(self.path, filename)))
                
        # Term Frequency {"doc_id" -> {"string" -> int} }
        self.tf = {}
        # How many documents contain a term {"string" -> set()}
        self.term_occurrences = {}
        # Term Frequency Calculation
        for doc in self.documents:
            self.tf[doc.id] = {}
            for word in doc.title.split():
                self.tf[doc.id][word] = self.tf[doc.id].get(word, 0) + 3
                if word in self.term_occurrences:
                    self.term_occurrences[word].add(doc.id)
                else:
                    self.term_occurrences[word] = {doc.id}
            for word in doc.content.split():
                self.tf[doc.id][word] = self.tf[doc.id].get(word, 0) + 1
                if word in self.term_occurrences:
                    self.term_occurrences[word].add(doc.id)
                else:
                    self.term_occurrences[word] = {doc.id}
    
        # Inverse Document Frequency {"string" -> float}
        self.idf = {}
        # Calculate Inverse Document Frequency
        for word in self.term_occurrences:
            self.idf[word] = log(1 + len(self.documents) / 1 + (len(self.term_occurrences[word])))

    def get_tfidf(self, sentence):
        #Pair <Float , id>
        document_ranking = []
        #Calculating TFIDF for a word in all documents
        words = sentence.split()
        words = [word.lower() for word in words]
        for doc_id in self.tf:
            tfidf = 0
            wordCount = 0
            for word in words:
                if word in self.tf[doc_id]:
                    wordCount += 1
            for word in words:
                if word in self.tf[doc_id]:
                        tfidf += wordCount * (self.tf[doc_id][word] * self.idf[word])
                        print((self.tf[doc_id][word] * self.idf[word]))         
                    
            document_ranking.append((tfidf, doc_id))
        #Sort by TFIDF
        document_ranking.sort(reverse=True)

        fetched_documents = []
        for doc in document_ranking:
            for document in self.documents:
                if document.id == doc[1]:
                    document.rank = doc[0]
                    document.path = document.path.split('/')[-1]
                    fetched_documents.append(document)
                    break
        return fetched_documents[:5]