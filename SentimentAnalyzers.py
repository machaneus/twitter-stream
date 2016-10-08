class AFINNSentimentAnalyzer(object):

    def __init__(self, filename):
        self.scores = self.loadSentimentFile(filename)
   
    def loadSentimentFile(self, filename):
        with open(filename) as sentimentFile:
            scores={}
            for line in sentimentFile:
                term, score = line.split("\t")
                scores[term] = int(score)

        return scores

    def getTextSentiment(self,text):
        score = 0
        words = text.split(' ')
        for word in words:
            if word in self.scores:
                score+=self.scores[word]
        return score
