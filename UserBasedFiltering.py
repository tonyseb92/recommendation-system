# -*- coding: utf-8 -*-

import math

from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # k: the number of nearest neighbors
    # defaults to 1
    # m: the number of recommedations to return
    # defaults to 10
    
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            
    #################################################
    # pearson correlation similarity
        def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            
    #################################################
    # making recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        #Creating the pearson correlation matrix
        pearsCorrtable = {}
        for name,score in self.usersItemRatings.items():
            namedict = {}
            
            for name2, score2 in self.usersItemRatings.items():
                if name2 != name:
                    pears = self.pearsonFn(score,score2)
                    namedict[name2] = pears
            pearsCorrtable[name] = namedict

        #converting dictionary to list for UserX and sorting
        pearsinner = pearsCorrtable[userX]
        lst = []
        for k,v in pearsinner.items():
            tup = (k,v)
            lst.append(tup)    
                
        sortedlst = sorted(lst, key=itemgetter(1), reverse = True)

        # calculating the weighted average item recommendations for userX from userX's k NNs
        # Creating list of artists and noting the missing ones for UserX
        artistlist = []
        for k2,v2 in self.usersItemRatings.items():
    
            for k3, v3 in v2.items():
                if k3 not in artistlist:
                    artistlist.append(k3)
        
        missingartist = []
        namesclosest = []
        kList = list(range(self.k)) 
        
        # returning sorted list of recommendations (sorted highest to lowest ratings)
        for kvalue in kList:
            namesclosest.append(sortedlst[kvalue][0])

        for artist in artistlist:
            if artist not in self.usersItemRatings[userX].keys():
                missingartist.append(artist)
        
        #modifying the pearson correlation to account for effects of negative correlation values
        pcmod = {}
        for name in namesclosest:
            pcmod[name] =(pearsinner[name]+1)/2

        summodvalue = 0
        for name, pcmodvalue in pcmod.items():
            summodvalue = summodvalue + pcmodvalue
       
        #calculating weights and creating weighted table
        weights = {}
        for name, pcmodvalue in pcmod.items():
            weights[name] = pcmodvalue/summodvalue

        weightedrating = {}
        
        for artist in missingartist:
            artistsum = 0
            for name in namesclosest:
                if artist in self.usersItemRatings[name].keys():
                    artistsum = artistsum + weights[name]*self.usersItemRatings[name][artist]
            weightedrating[artist] = round(artistsum,2)
            
        #creating the final list of tuples
        finallst = []
        for finalk, finalv in weightedrating.items():
            if finalv != 0:
                finaltup = (finalk, finalv)
                finallst.append(finaltup)
        
        sortedfinallst = sorted(finallst, key=itemgetter(1), reverse = True)
        return(sortedfinallst[0:self.m])
       



        
