#!/usr/bin/env python
# coding: utf-8


# In[2]:


from google.cloud.sql.connector import Connector
import sqlalchemy


# In[3]:


connector = Connector()

project_id = "ds561-wyc-5304"
region = "us-east1"
instance_name = "hw5--db"

# initialize parameters
INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = "454604"
DB_NAME = "hw5"


# In[4]:


def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


# In[5]:


def getColumnOfAllData(category: str):
    try:
        with pool.connect() as db_conn:
            results = db_conn.execute(sqlalchemy.text("SELECT {} FROM Request".format(category))).fetchall()
        return results
    except:
        return None


# In[23]:


from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import numpy as np

ip_X = np.array(getColumnOfAllData("client_ip"))
ip_X = np.char.split(ip_X, sep=".").tolist()
ip_X = np.array(ip_X, dtype=int).flatten()
ip_X = np.reshape(ip_X, (-1, 4))
ip_X = ip_X[:,:3]

country_y = np.array(getColumnOfAllData("country"))
le = LabelEncoder()
le.fit(country_y.flatten())
country_index_y = le.transform(country_y.flatten())
num_unique_country = max(country_index_y) + 1

ip_X_train, ip_X_test, country_index_y_train, country_index_y_test = train_test_split(ip_X, country_index_y ,test_size=0.35, shuffle=True)
ip_X_train, ip_X_test, country_y_train, country_y_test = train_test_split(ip_X, country_y ,test_size=0.35, shuffle=True)


# In[15]:


## MODEL

# country_index_y
# model = KMeans(n_clusters=num_unique_country, n_init=100, max_iter=300, init='k-means++').fit(ip_X.reshape(-1,1))

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

clf = SVC(kernel="rbf", C=200)
clf.fit(ip_X_train,country_y_train)


# In[16]:


y_pred = clf.predict(ip_X_test)
print("Country prediction accuracy: ", accuracy_score(country_y_test,y_pred))


# In[24]:


def predictCountry(ip):
    inp = np.char.split(ip, sep=".").tolist()
    inp = np.array(inp, dtype=int).flatten().reshape((-1, 4))
    inp = inp[:,:3]
    return clf.predict(inp)


# In[25]:


X_income = np.array(getColumnOfAllData("age, gender, country"))
y_income = np.array(getColumnOfAllData("income"))


# In[26]:


age_enc = LabelEncoder()
age_enc.fit(X_income[:,0])
gender_enc = LabelEncoder()
gender_enc.fit(X_income[:,1])
country_enc = LabelEncoder()
country_enc.fit(X_income[:,2])
income_enc = LabelEncoder()
income_enc.fit(y_income)


# In[29]:


X_income_processed = np.array([age_enc.transform(X_income[:,0]), gender_enc.transform(X_income[:,1]), country_enc.transform(X_income[:,2])])
X_income_processed = X_income_processed.T

y_income_processed = income_enc.transform(y_income)


# In[151]:


X_train, X_test, y_train, y_test = train_test_split(X_income_processed, y_income_processed ,test_size=0.1, shuffle=True)


# In[172]:


from sklearn.ensemble import RandomForestClassifier

# pipe = 

income_regressor = RandomForestClassifier(n_estimators=500, max_depth=1000)
income_regressor.fit(X_train, y_train)


# In[175]:


y_income_pred = income_regressor.predict(X_test)

print("income prediction accuracy: ", accuracy_score(y_test,y_income_pred))

# print(y_income_pred)
# print()
# print(y_test)
