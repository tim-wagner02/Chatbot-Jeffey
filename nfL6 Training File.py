
# coding: utf-8

# In[13]:


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import spacy


# In[14]:


import json

data = json.loads(open('nfL6.json', 'r').read())  # reading through the json file of yahoo questions and answers

train = []                                        # creates an empty array

for k, row in enumerate(data):                    # splits into questiona and answera pairs
    train.append(row['question'])
    train.append(row['answer'])

Bot = ChatBot('Jeffey') 

Trainer = ListTrainer(Bot) 

Trainer.train(train)                             # training bot on json file
Trainer.train("chatterbot.corpus.english")       # standard way to train bot on enlgish per documentation

