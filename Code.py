#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import string
import pandas as pd
import io 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize


# In[3]:


#Reading the dataset into a common list

os.chdir("coca")
commonlist=[]
for i in os.listdir():
    
    f = open(i,"r")
    text = f.read()
    
    #splitting on white spaces
    words = text.split() 
    commonlist.append(words)

len(commonlist)


# In[4]:


#replace punction with whitespace

commonlist_no_punct=[]

for sublist in commonlist:
    table = str.maketrans('', '', string.punctuation)
    no_punct = [w.translate(table) for w in sublist]
    commonlist_no_punct.append(no_punct)


# In[5]:


#remove whitespaces

commonlist_no_whitespace = []

for sublist in commonlist_no_punct:
    new_x = [elem for elem in sublist if elem.strip()]
    commonlist_no_whitespace.append(new_x)


# In[6]:


# convert to lower case

commonlist_lcase = []

for sublist in commonlist_no_whitespace:
    x = [word.lower() for word in sublist]
    commonlist_lcase .append(x)           


# In[7]:


#removing stopwords

stop_words = set(stopwords.words('english')) 
commonlist_no_stopwords = []

for sublist in commonlist_lcase:
    output = []
    for x in sublist: 
        if x not in stop_words:
            output.append(x)
    commonlist_no_stopwords.append(output)


# In[8]:


# Get the word count of each word

w_count = dict() 

for sublist in commonlist_no_stopwords:
    for word in sublist:
        if word in w_count:
            w_count[word] = w_count[word] + 1
        else:
            w_count[word] = 1


# In[10]:


w_count


# In[11]:


#Eliminate the words with count less than 10

new_dict = {key : value for (key, value) in w_count.items() if value > 9}


# In[12]:


print (new_dict)


# In[137]:


print(len(new_dict))


# In[138]:


#converting new dictionary to list

new_word_list=list(new_dict.keys())


# In[139]:


with open("coca_dict", "w") as outfile:
    for s in new_word_list:
        outfile.write("%s\n" % s)


# In[42]:





# In[140]:


#Mapping the words with their resprctive indices

list_after_mapping = []

for sublist in commonlist_no_stopwords:
    elem = {k: i for i, k in enumerate(new_word_list)} 
    Output = list(map(elem.get, sublist)) 
    list_after_mapping.append(Output)


# In[141]:


print(len(list_after_mapping))


# In[142]:


#Eliminating None values from the list

final_output = [] 

for sublist in list_after_mapping:
    output = []
    for x in sublist: 
        if x != None :
            output.append(x)
    final_output.append(output)


# In[145]:


# Making the output compatible for MMSG topic model
# ELiminating brackets and commas

string1 = str(final_output)[1:-1] 
string2 = str(string1)[1:-1] 
string3 = ''.join(string2.split(','))
string4 = '\n'.join(string3.split('['))
Final_file = ''.join(string4.split(']'))

#'Final_file' compatible for MMSG topic model


#Saving Final file
with open("input file for MMSG", "w") as output:
    output.write(str(Final_file))


# # Run the Final_file through the MMSG-TM model.

# In[175]:


#Fetching Top 10 words each topic
# Reading the output file generated from the MMSG Topic Model


df_topic=pd.read_csv("MMSGTM_ForTopics.csv")
df_topic.set_index("WORD", inplace = True) 


#Filter top 10 values for all columns (200 Topics) 

new_df1 = df_topic.apply(lambda s, n: pd.Series(s.nlargest(n).index), axis=0, n=10)

#Saving the result in excel file
new_df1.to_excel (r'top10_words.xlsx', index = True, header=True)


# In[188]:


new_df1


# In[ ]:


#Top 3 topics
# Reading the output file generated from the MMSG Topic Model
df_words=pd.read_csv("MMSGTM_ForWords.csv")
df_words.set_index("WORD", inplace = True) 


#Filter top 3 values for every row (11453 words) 

new_df = df.apply(lambda s, n: pd.Series(s.nlargest(n).index), axis=1, n=3)

#Saving the result in excel file
new_df.to_excel (r'top3_topics.xlsx', index = True, header=True)


# In[161]:


df_words

