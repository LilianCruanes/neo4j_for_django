### You can find the full documentation on ReadTheDocs [here](https://neo4j-for-django.readthedocs.io/en/latest/).

---

<br/>
<br/>

# Presentation :
<br/>

![transparent logo neo4j_for_django](docs/img/transparent_logo_neo4j_for_django.png)
<br/>
<br/>

The **neo4j_for_django** package extends the **_Django_** framework to make it compatible with the **_Neo4j_** databases.  
Two other solutions already exist, but they each have their own inconveniences :  

| [**neo4django**](https://github.com/scholrly/neo4django) | [**neomodel**](https://github.com/neo4j-contrib/neomodel) |
|:--------------:|:------------:|
| This package is out of date (last update in 2014). His usage is deprecated, cause he runs under very old versions of all its components : _Python 2.X_ / _Django 1.5_ / _Neo4j 1.9_. Furthermore, **neo4django** does not provide support for the Django's sessions nor a complete support for the Django's authentication. | This package is regularly updated, he runs also under last versions of all its components. He provides a very complete adaptation of the Django models, but the philosophy of these contributors is almost to make a 'ready and easy to use' tool, so the user interact only with the highlevel surface . The inconvenience of a such reasoning, it's that under the hood, there are foundations that often ignores primary concepts like separation of writing transactions and reading transactions. This philosophy is perfectly compatible with modest projects, but it conduces to a total remake and to more complex programs the days where we will want to have a finger in the pie, to increase the performance of our project with the establishing of clusters (for example). Furthermore, **neomodel** does not provides support for the Django's sessions nor for the Django's authentication. |

**neo4j_for_django** has a completely different philosophy. It wants to let more responsability to the users of the package, leaving him interact with deeper concepts. First, the database interaction has been developed to let the user use writing queries and reading queries, but also more advanced concepts like make multi-transactions sessions and causal chaining. To reuse the above example (in the neomodel column of table) of clusters, we understand that with **neo4j_for_django**, their implementation and optimisations will not be an heavy task, and even, if you have the reflex to use directly theses concepts in your project, there will be almost nothing to change. But on the other hand, methods have been developed to make easier the use of these concepts. With **neo4j_for_django** you can optimise your queries by doing case by case, but you can also use 'ready to use' writing and reading methods to code faster. 
> NB : The separation of writing and reading queries is the unique condition to set up clusters. So you you could just use these two 'ready to use' methods and get pretty good results.

Then, and to a lesser extent than **neomodel**, we have rewrite the Django's _'models'_ , to make them _'node-models'_. The more basics functionalities have been remade, and especially on the elementary structure of the nodes (to improve clarity), considering that the complex requests works must be done by the developers theirself to increase a lot performance of each query.

Finally, the Django's sessions and authentication packages, have been completely remodeled to make them compatible with Neo4j. Maybe later, we will rewrite the Django's administration (Any volunteer ?).

To conclude, if you search a very complete adapation of the Django's models for Neo4j and if you don't need to set authentication and sessions in your project, nor use advanced  graph databases' concepts, you should use [**neomodel**](https://github.com/neo4j-contrib/neomodel), but if you need all of this and more flexibility, check the following documentation. 
<br/>
<br/>
<br/>

---

# Installation :
<br/>

1. First, open a terminal.
<br/>
<br/>

2. Then, go into your Django project or start your virtual environment if you have one :

    Example :
```
> cd my_projects/my_django_project
```
<br/>
<br/>

3. Finally, execute :
```
> pip install neo4j_for_django
```
or if it doesn't work :
```
> python -m pip install neo4j_for_django
```
<br/>
<br/>

4. To check if all works fine, you can execute this in the terminal :
```
> neo4j_for_django -v
```
   If no error message appears, that's good.  
   (You could also try to import the **neo4j_for_django** package in a file of your project.
<br/>
<br/>
<br/>

---

# Getting started :
<br/>

## Introducing

The **neo4j_for_django package** is very fast to setup. Just **2 steps** are needed to execute yours first cypher requests.

>> If you don't have already install the package, please see the [installation](https://neo4j-for-django.readthedocs.io/en/latest/installation/) page.  
<br/>
<br/>


## 1. Set the neo4j_for_django settings to your project 

A very simple step, just import the **`set_neo4j_for_django_settings_on()`** in the settings.py file of your Django project :

> <small>_settings.py_</small>
```python
from neo4j_for_django import set_neo4j_for_django_settings_on
```
<br/>
<br/>

Then, use this method on all the datas contained in your settings.py file. The **`locals()`** function return a dictionary that contains all of these datas.
So just put this **at the bottom** of your settings.py file :

> <small>_settings.py_</small>
```python
set_neo4j_for_django_settings_on(locals())
```
<br/>
<br/>

Finally, and always in the same file (**just below the method** that we have previously set), configure yours Neo4j credentials with the 3 parameters :  
    - **`N4D_DATABASE_URI`**,  
    - **`N4D_DATABASE_ID`**,  
    - and **`N4D_DATABASE_PASSWORD`**.

**`N4D_DATABASE_URI`** is the bolt address of your database. Generally on a local server, the bolt address is '**bolt://localhost:7687**'. But you can find more details in the parameters of your Neo4j database and on the official [documentation](https://neo4j.com/docs/driver-manual/1.7/client-applications/#driver-connection-uris).

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

##### **You're project is now configured to work with `neo4j_for_django` !**

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


## 2. Run a first cypher query

**neo4j_for_django** can be used in all the files of your project. So in one of these files, import the **`gdbh`** object.

> <small>views.py</small>
```python
from neo4j_for_django.db import gdbh
```
<br/>
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
<br/>

---

### You can find the full documentation on ReadTheDocs [here](https://neo4j-for-django.readthedocs.io/en/latest/).