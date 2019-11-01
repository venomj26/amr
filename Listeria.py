#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:39:20 2019

@author: jha
"""





#%%
import csv
import mysql.connector as mariadb
from tabulate import tabulate
import pandas as pd

amrdb= mariadb.connect(
        host="localhost",
        user="root",
        passwd="Sukhoi@90",
        database ="myamr"
        )
cursor = amrdb.cursor(buffered=True) # else it fetches one row for everytime it is executed 
print("We are at line 31 we have connection, lets begin")

#%%


    
    
    



#creating a table where all AST_phenotypes have values 
#%%
new_table= cursor.execute("CREATE TABLE IF NOT EXISTS LSTRast AS SELECT * FROM LSTR WHERE AST_phenotypes LIKE '%=%'")
print("Selected %s rows" %new_table)
print("Selected %s rows " %cursor.rowcount)
#rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))

#%%



#get the data from the ast table to make the dataframe 
#%%
import pandas as pd
numrows= cursor.execute("SELECT AST_phenotypes FROM LSTRast ")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
#print(tabulate(rows, headers=['AST_phenotype'], tablefmt='psql'))
#%%


#splitting the AST_phenotype column values into separate columns of the table 
#%%
df = pd.DataFrame(rows)
#print ("the pandas dataframe ",df
       
df.columns=["AST_phenotypes"]
df.head()
split_df= df['AST_phenotypes'].str.split(',', expand= True)
split_df.head()
#split_df = split_df.drop(split_df.columns[[23]], axis=1) 

#%%
#we are making the column names for the AST dataframes 
#%%
split_df_list=[]
split_df_list = split_df.values.tolist()
flat_list_sd = []
for sublist in split_df_list:
    for item in sublist:
        flat_list_sd.append(item)

#print ("ATline {0} in code split_df has been converted to a list{1}".format(lineno(),flat_list_sd))
split_flsd=[]
for element in flat_list_sd:
    if element != None:
        split_flsd.append(element.split('=', 1)[0]) 
#print ("ATline {0} in code split_df has been converted to a list".format(lineno()))
print("the list of all elements in split_df", split_flsd)
header_set=set(split_flsd)
header_list_AST=list(header_set)

print("at line 87 in code the list of header values are ")


#%%

##%%
#
##df_AST= pd.DataFrame(columns = header_list_AST)
#import re
#for name in header_list_AST:
#    print(name)
#    #name=[]
#    for item in flat_list_sd:
#        if item is not None and name in item:
#            print("the code is at line 125")
##                    print ("the column name at line 124 of code is", item,name1)
#            name.append(item)
##                    print ("at line 121 in code \n", "writing the table into AST dataframe ")
##                    #print("at line 127 in code the item name is ", item)
##                    #var = var+1
##        
#            print("at line 132",item)
#
##%%

#the list of antibiotics is populated by the R and S values forming an array. (the result is a list of lists called
#list_list_AST)
#%%
            
def extractDigits(lst): 
    return list(map(lambda el:[el], lst)) 
list_list_AST= extractDigits(header_list_AST)
for x in list_list_AST:
    print(x)
    for item in flat_list_sd:
        if item is not None and x[0] in item:
            x.append(item)
            #print("printing if equal",x)
        #print("printing table item",item)
    #print ("printing x",x)   
        
        
#%%



#we are using regex to remove the anitibiotic name(ex: ampicillin=R and retain the "R" for each column= DONE)
#%%
for col in list_list_AST:
   # print ("col",col)
    for row in col:
        print("the row is",row)
        if "=" in row:
            #print("row", row)
            loc=col.index(row)
            row1=row.split("=")[-1]
            col.remove(row)
            col.insert(loc,row1)
            print ("the row has been split to ",row)
            








#%%

#%%
df_AST= pd.DataFrame(list_list_AST)       
df_ASTT=df_AST.T

         
            
#%%

#%%
df_ASTT.columns = df_ASTT.iloc[0] #grab the first row for the header

df_ASTT=df_ASTT.drop([0])# drops the first row which is a header row from dataframe but this also changes the index of the dataframe
df_ASTT=df_ASTT.reset_index()# the change of index in the previous command causes error in the concatenation of the other dataframe
df_ASTT= df_ASTT.drop(columns=['index'])# so reset is used to create a new index and the old index is deleted 
df_ASTT = pd.concat([df,df_ASTT], axis=1, join_axes=[df.index]) 


#%%


#%%
from sqlalchemy import create_engine

cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
#df3.to_sql(name='salall', con=cnx, if_exists = 'replace', index=False)
df_sal_ast= pd.read_sql('LSTRast',cnx)

#%%


#run this code only once to create the astt table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_ASTT.to_sql(name='LSTRastt', con=cnx, if_exists = 'replace', index=False)
print("we are at line 186 in code")

#%%

#%%

numrows= cursor.execute("SELECT * FROM LSTRastt LEFT JOIN LSTRast ON LSTRastt.AST_phenotypes=LSTRast.AST_phenotypes  UNION SELECT * FROM LSTRastt RIGHT JOIN LSTRast ON LSTRastt.AST_phenotypes=LSTRast.AST_phenotypes")
print("Selected %s rows" %numrows)
print("Selected %s rows " %cursor.rowcount)
rows =cursor.fetchall()#fetch all rows at once
print(tabulate(rows, headers=['strain','AST_phenotype', 'AMR_genotype'], tablefmt='psql'))    
dffinal = pd.DataFrame(rows) 

#%%



#%%
header_astt=[]
header_astt= list(df_ASTT.columns)
header_sal_ast=[]
header_sal_ast= list(df_sal_ast.columns)
header_final=[]
header_final=header_astt+header_sal_ast
dffinal.columns=header_final
dffinal=dffinal.drop(dffinal.columns[[0]], axis=1)







#%%



#run this code snippet just once to create the final table
#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
dffinal.to_sql(name='LSTRfinal', con=cnx, if_exists = 'replace', index=False)
print("we are at line 244 in code")



#%%



#%%
df_AB=df_AST
df_AB= df_AB.T
df_AB.columns= df_AB.iloc[0]
df_AB=df_AB.drop([0])
df_AB=df_AB.reset_index()
df_AB=df_AB.drop(columns=["index"])

#%%





##%%
#count=0
#for row in df_AB:
#    try:
#        sql_insert = 'SELECT count('+ row +') FROM salfinal WHERE ' +row +'= "S" ;'
#        print (sql_insert)
#        numrows= cursor.execute(sql_insert)
#        rows =cursor.fetchall()#fetch all rows at once
#        print(tabulate(rows, headers=['count'], tablefmt='psql'))    
#    #dffinal = pd.DataFrame(rows) 
#    except:
#        pass
#    
#    
#
#
##%%


#%%
chunk=[]
chunk1=[]
for row in df_AB.columns:
    try:
        print(row)
        #print(df_AB[row].value_counts().index.to_list())
        #df_plot=(df_AB[row].value_counts().index.to_list())
        
        #df_plot=pd.merge((df_AB[row].value_counts().to_frame()), on )
        #print(df_AB[row].value_counts().to_frame())
        #df_plot= df.append(df_AB[row].value_counts(), ignore_index=True)
        #print("line 312")
        
        print(df_AB[row].value_counts().reset_index())
        df5=df_AB[row].value_counts().reset_index()
        val=df5.loc[df5['index'] != "S"]
        val=val.T
        val=val.reset_index()
        val=val.drop([0])
        print("before saving to list)")
        chunk1.append(val.values.tolist())
        #val.columns=['antibiotic','number_of_S']
        
        
        
        
        
        #df=pd.DataFrame('antibiotics': val[])
    #    print("yes",val)
        #chunk= [df5.columns.values.tolist()] + df5.values.tolist()
    #    df_plot_C=pd.concat(series5)
    except:
        pass
    

    
#%%


    
#%%
list_chunk=[]       
for x in chunk1:
            print(x)
            for y in x:
                print(y)
                list_chunk.append(y)    
    
    
#%%        


                
        
#%%
        
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
df_plotLNS= pd.DataFrame(list_chunk)

df_plotLNS.columns=["antibiotics","R","I","ND"]
df_plotLNS["non_susceptible"]=df_plotLNS.fillna(0)["R"]+df_plotLNS.fillna(0)["I"] # this line is needed to make non susceptible column by adding R and I columns 
#df_plot.columns=['antibiotics','number_of_S']
#df_plotLNS['percent_nonS'] = ((df_plotLNS['non_susceptible']/118)*100) 
#df_plotLNS.percent_nonS=df_plotLNS.percent_nonS.round(2)
#                           
##print()
#%%                

#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotLNS.to_sql(name='LNS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%



                

#%%
#df_plotLNS_sorted=df_plotLNS.sort_values('percent_nonS',ascending=False)
#ax = df_plotLNS_sorted.plot.bar(x='antibiotics', y='percent_nonS', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotLNS_sorted['percent_nonS']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of listeria samples found non Susceptible to antibiotics (118 samples)")
#plt.ylabel("percentage of nonS")
#plt.plot(x,y)
#plt.show()




#%%                
                
                
                



#for graphing the susceptible microbes
#%%
        
chunk2=[]
chunk3=[]
for row in df_AB.columns:
    try:
        print(row)
        #print(df_AB[row].value_counts().index.to_list())
        #df_plot=(df_AB[row].value_counts().index.to_list())
        
        #df_plot=pd.merge((df_AB[row].value_counts().to_frame()), on )
        #print(df_AB[row].value_counts().to_frame())
        #df_plot= df.append(df_AB[row].value_counts(), ignore_index=True)
        #print("line 312")
        
        print(df_AB[row].value_counts().reset_index())
        df6=df_AB[row].value_counts().reset_index()
        val=df6.loc[df6['index'] == "S"]
        val=val.T
        val=val.reset_index()
        val=val.drop([0])
        print("before saving to list)")
        chunk3.append(val.values.tolist())
        #val.columns=['antibiotic','number_of_S']
        
        
        
        
        
        #df=pd.DataFrame('antibiotics': val[])
    #    print("yes",val)
        #chunk= [df5.columns.values.tolist()] + df5.values.tolist()
    #    df_plot_C=pd.concat(series5)
    except:
        pass   
    
    
    
    
    
    
#%%
    
    

    
#%%
list_chunkS=[]       
for x in chunk3:
            print(x)
            for y in x:
                print(y)
                list_chunkS.append(y)    
    
    
#%%
        
#%%
        
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np
df_plotLS= pd.DataFrame(list_chunkS)

df_plotLS.columns=["antibiotics","Susceptible"]
#df_plotLS['percent_S'] = ((df_plotLS['Susceptible']/118)*100) 
#df_plotLS.percent_S=df_plotLS.percent_S.round(2)
##                           
##print()
#%%


#%%

#df_plotLS_sorted=df_plotLS.sort_values('percent_S',ascending=False)
#ax = df_plotLS_sorted.plot.bar(x='antibiotics', y='percent_S', rot=90,legend=False,    # Turn the Legend off
#        width=0.75,      # Set bar width as 75% of space available
#        figsize=(15,6),  # Set size of plot in inches
#        colormap='summer')
#for index,data in enumerate(df_plotLS_sorted['percent_S']):
#    plt.text(x=index , y =data , s=f"{data}",fontdict=dict(fontsize=8) )
#plt.title("Percentage of Listeria samples found Susceptible to antibiotics (118 samples)")
#plt.ylabel("percentage of S")
#plt.plot(x,y)
#plt.show()





#%%


#making the table with each percentage non-susceptible is non-susceptible/(susceptible+non_susceptible) same for susceptible

#%%

df_plotLS_dict=df_plotLS.set_index('antibiotics')['Susceptible'].to_dict()

df_plotLNS['Susceptible'] = df_plotLNS['antibiotics'].map(df_plotLS_dict)
df_plotLNS["Total_Samples"]=df_plotLNS.fillna(0)["Susceptible"]+ df_plotLNS.fillna(0)["non_susceptible"]

df_plotLNS['percent_S'] = ((df_plotLNS['Susceptible']/df_plotLNS["Total_Samples"])*100) 


df_plotLNS['percent_nonS'] = ((df_plotLNS['non_susceptible']/df_plotLNS["Total_Samples"])*100) 





#%%


#%%
df_plotLNS_sorted=df_plotLNS.sort_values('percent_S',ascending=False)
df_plotLNS_sorted.percent_nonS=df_plotLNS.percent_S.round(0)
df_plotLNS_sorted.percent_nonS=df_plotLNS.percent_nonS.round(0)


#%%





#%%

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import matplotlib.patches as mpatches
r=[]
r= list(df_plotLNS_sorted["antibiotics"])
bars1=[]

bars1= list(df_plotLNS_sorted.fillna(0)["percent_nonS"])

bars2=[]

bars2=list(df_plotLNS_sorted.fillna(0)["percent_S"])
p1=plt.bar(r, bars1, color='#b5ffb9', edgecolor='white', width=1,label="Susceptible")
# Create green bars (middle), on top of the firs ones
p2=plt.bar(r, bars2, bottom=bars1, color='#f9bc86', edgecolor='white', width=1,label="non-Susceptible")
plt.xticks(r,rotation=90)
plt.xlabel("antibiotics")
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
plt.title("Percentage of Listeria samples tested ( samples)")
plt.ylabel("percentage")

rects1 = p1.patches
labels1 = ["%d" % i for i in (df_plotLNS_sorted.fillna(0)["Susceptible"])]
for rect, label in zip(rects1, labels1):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="black", fontsize=8,fontweight="bold")


rects2 = p2.patches
labels2 = ["%d" % i for i in df_plotLNS_sorted.fillna(0)["non_susceptible"]]
for rect, label in zip(rects2, labels2):
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2., 100-height, label,ha='center', va='top',color="blue", fontsize=8,fontweight="bold")


rects1 = p1.patches
labels3 = ["%d" % i for i in df_plotLNS_sorted.fillna(0)["Total_Samples"]]
for rect, label in zip(rects2, labels3):
    height=45
    plt.text(rect.get_x() + rect.get_width() / 2., height, label,ha='center', va='bottom',color="maroon", fontsize=8,fontweight="bold")


plt.show()





#%%





#%%
from sqlalchemy import create_engine
cnx = create_engine('mysql+pymysql://root:Sukhoi@90@localhost/myamr')
df_plotLS.to_sql(name='LS', con=cnx, if_exists = 'replace', index=False)
print("we are at line 356 in code")



#%%