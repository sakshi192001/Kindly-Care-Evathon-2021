import numpy as np
import pandas as pd

df = pd.read_csv('ICU.csv')


df.loc[(df.ChronicDisease == 'Arthritis'), ['ChronicDisease']] = 1
df.loc[(df.ChronicDisease == 'Stroke'), ['ChronicDisease']] = 2
df.loc[(df.ChronicDisease == 'Obesity'), ['ChronicDisease']] = 3

df.loc[(df.respiratory == 'Asthama'), ['respiratory']] = 1
df.loc[(df.respiratory == 'Bronchitis'), ['respiratory']] = 2

df.loc[(df.gastrointestinal == 'Constipation'), ['gastrointestinal']] = 1
df.loc[(df.gastrointestinal == 'Gallstone'), ['gastrointestinal']] = 2
df.loc[(df.gastrointestinal == 'Peptic_ulcer'), ['gastrointestinal']] = 3

df.loc[(df.kidney == 'kidneystone'), ['kidney']] = 1
df.loc[(df.kidney == 'kidneyfailure'), ['kidney']] = 2
df.loc[(df.kidney == 'polycystic'), ['kidney']] = 3

df.loc[(df.diabetes == 'Low'), ['diabetes']] = 1
df.loc[(df.diabetes == 'Normal'), ['diabetes']] = 2
df.loc[(df.diabetes == 'High'), ['diabetes']] = 3

df.loc[(df.neuro == 'Parkinson'), ['neuro']] = 1
df.loc[(df.neuro == 'Alzheimer'), ['neuro']] = 2

df.loc[(df.hypertension == 'Heart_attack'), ['hypertension']] = 1
df.loc[(df.hypertension == 'Stroke'), ['hypertension']] = 2

df.loc[(df.ortho == 'Tennis_elbow'), ['ortho']] = 1
df.loc[(df.ortho == 'Baseball_elbow'), ['ortho']] = 2
df.loc[(df.ortho == 'Torn_meniscus'), ['ortho']] = 3

df.loc[(df.blood == 'Leukemia'), ['blood']] = 1
df.loc[(df.blood == 'Lymphoma'), ['blood']] = 2
df.loc[(df.blood == 'Myeloma'), ['blood']] = 3

df.loc[(df.Prostate == 'Prostatis'), ['Prostate']] = 1
df.loc[(df.Prostate == 'BPH'), ['Prostate']] = 2
df.loc[(df.Prostate == 'Prostate_Cancer'), ['Prostate']] = 3


X = df.iloc[:,:-1]
y = df.iloc[:,-1]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)

from sklearn.metrics import accuracy_score
import random
X_train = pd.DataFrame(X_train)
X_test = pd.DataFrame(X_test)
#defining various steps required for the genetic algorithm
def initilization_of_population(size,n_feat):
    population = []
    for i in range(size):
        chromosome = np.ones(n_feat,dtype=np.bool)
        chromosome[:int(0.3*n_feat)]=False
        np.random.shuffle(chromosome)
        population.append(chromosome)
    return population

def fitness_score(population):
    scores = []
    for chromosome in population:
        classifier.fit(pd.DataFrame(X_train.iloc[:,chromosome]),y_train)
        predictions = classifier.predict(X_test.iloc[:,chromosome])
        scores.append(accuracy_score(y_test,predictions))
    scores, population = np.array(scores), np.array(population) 
    inds = np.argsort(scores)
    return list(scores[inds][::-1]), list(population[inds,:][::-1])

def selection(pop_after_fit,n_parents):
    population_nextgen = []
    for i in range(n_parents):
        population_nextgen.append(pop_after_fit[i])
    return population_nextgen

def crossover(pop_after_sel):
    population_nextgen=pop_after_sel
    for i in range(len(pop_after_sel)):
        child=pop_after_sel[i]
        child[3:7]=pop_after_sel[(i+1)%len(pop_after_sel)][3:7]
        population_nextgen.append(child)
    return population_nextgen

def mutation(pop_after_cross,mutation_rate):
    population_nextgen = []
    for i in range(0,len(pop_after_cross)):
        chromosome = pop_after_cross[i]
        for j in range(len(chromosome)):
            if random.random() < mutation_rate:
                chromosome[j]= not chromosome[j]
        population_nextgen.append(chromosome)
    #print(population_nextgen)
    return population_nextgen

def generations(size,n_feat,n_parents,mutation_rate,n_gen,X_train,
                                   X_test, y_train, y_test):
    best_chromo= []
    best_score= []
    population_nextgen=initilization_of_population(size,n_feat)
    for i in range(n_gen):
        scores, pop_after_fit = fitness_score(population_nextgen)
        print(scores[:2])
        pop_after_sel = selection(pop_after_fit,n_parents)
        pop_after_cross = crossover(pop_after_sel)
        population_nextgen = mutation(pop_after_cross,mutation_rate)
        best_chromo.append(pop_after_fit[0])
        best_score.append(scores[0])
    return best_chromo,best_score

chromo,score=generations(size=100,n_feat=16,n_parents=100,mutation_rate=0.10,
                     n_gen=38,X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test)
classifier.fit(X_train.iloc[:,chromo[-1]],y_train)
predictions = classifier.predict(X_test.iloc[:,chromo[-1]])
print("Accuracy score after genetic algorithm is= "+str(accuracy_score(y_test,predictions)))


from sklearn.metrics import *
mcc = make_scorer(matthews_corrcoef)
estimator = LogisticRegression(solver = "liblinear", C = 6, tol = 1, fit_intercept = True)
from genetic_selection import GeneticSelectionCV
from sklearn.model_selection import *
report = pd.DataFrame()
X = pd.DataFrame(X)
nofeats = [] 
chosen_feats = [] 
cvscore = [] 
rkf = RepeatedStratifiedKFold(n_repeats = 2, n_splits = 10)
for i in range(2,15):
  
  selector = GeneticSelectionCV(estimator,
                                cv = rkf,
                                verbose = 0,
                                scoring = mcc,
                                max_features = i,
                                n_population = 10,
                                crossover_proba = 0.5,
                                mutation_proba = 0.2,
                                n_generations = 10,
                                crossover_independent_proba=0.5,
                                mutation_independent_proba=0.05,
                                n_gen_no_change=10,
                                caching=True,
                                n_jobs=-1)
  selector = selector.fit(X, y)
  genfeats = X.columns[selector.support_]
  genfeats = list(genfeats)
  print("Chosen Feats:  ", genfeats)
  cv_score = selector.generation_scores_[-1]
  nofeats.append(len(genfeats)) 
  chosen_feats.append(genfeats) 
  cvscore.append(cv_score)
report["No of Feats"] = nofeats
report["Chosen Feats"] = chosen_feats
report["Scores"] = cvscore


import pickle
pickle.dump(classifier,open('genetic.pkl','wb'))

