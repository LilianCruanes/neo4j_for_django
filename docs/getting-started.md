### >> Getting started :
[TOC]

<br/>

---

# Introducing
The **neo4j_for_django package** is very fast to setup. Just **2 steps** are needed to execute yours first cypher requests.

>> If you don't have already install the package, please see the [installation](https://neo4j-for-django.readthedocs.io/en/latest/installation/) page.  
<br/>
<br/>

--- 

# 1. Set the neo4j_for_django settings to your project 

A very simple step, just import the **`set_neo4j_for_django_settings_on()`** from **`neo4j_for_django`** in the settings.py file of your Django project :

> <small>_settings.py_</small>
```python
from neo4j_for_django import set_neo4j_for_django_settings_on
```
<br/>
<br/>
Then, use this method on all the datas contained in your settings.py file. The **`locals()`** function return a dictionnary that contains all of these datas.
So just put this **at the bottom** of your settings.py file :

> <small>_settings.py_</small>
```python
set_neo4j_for_django_settings_on(locals())
```
<br/>
<br/>
Finally, and always in the same file (**just below the method** that we have previously set), configure yours Neo4j credentials with the 3 parameter variables :  
    - **`N4D_DATABASE_URI`**,  
    - **`N4D_DATABASE_ID`**,  
    - and **`N4D_DATABASE_PASSWORD`**.

**`N4D_DATABASE_URI`** is the bolt adress of your database. Generally on a local server, the bolt adress is '**bolt://localhost:7687**'. But you can find more details in the parameters of your Neo4j database and in the official [documentation](https://neo4j.com/docs/driver-manual/1.7/client-applications/#driver-connection-uris).

**`N4D_DATABASE_ID`** is your Neo4j database **id** or **username**. By default the id is defined on 'neo4j'.

**`N4D_DATABASE_PASSWORD`** is your Neo4j database **password**. By default the password is defined on 'neo4j' too. But normally and if you don't have change the password before, during the first run of the Neo4j database, we will ask you to replace the default password by another. 

Example :

> <small>_settings.py_</small>
```python
N4D_DATABASE_URI = "bolt://localhost:7687"

N4D_DATABASE_ID = 'neo4j'

N4D_DATABASE_PASSWORD = '1234'
```
<br/>
###### **You're project is now configured to work with `neo4j_for_django` !**
<br/>
<br/>

**WARNING** : don't forget to remove the default admin page at the creation of your project, cause the Django administration is'nt already supported by **neo4j_for_django**. Else, a "LookupError: No installed app with label 'admin'." will be raised.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('blog/', include("my_project.urls"))
]
```
<br/>
<br/>

---

# 2. Run a first cypher query
**neo4j_for_django** can be used in all the files of your project. So in one of these files, import the **`gdbh`** object.

> <small>views.py</small>
```python
from neo4j_for_django.db import gdbh
```
<br/>
**g-db-h** means **_Graph Database Handler_** and it is an instance of the **`GraphDatabaseHandler()`** class. This instance will be used all the times where we will want to interact with the Neo4j database.
<br/>
<br/>

Now you can use the **`w_transaction()`** method of the **`gdbh`** object, to send a query to the database :

```python
gdbh.w_transaction("CREATE (:Person) {first_name: 'Adrien', age: 18}")
```
<br/>
>> The **`w_transaction()`** means **writing transaction**, so use it preferably when you want to create or modify datas in the database.  
We also find the **`r_transaction()`** method, which one should be used preferably to retrieve datas from the database.
<br/>
<br/>
For now, if you have any doubt, use the **`w_transaction()`** method.
<br/>
<br/>