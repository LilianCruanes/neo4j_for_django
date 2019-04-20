### >> Presentation :
<br/>

![transparent logo neo4j_for_django](../img/transparent_logo_neo4j_for_django.png)
<br/>
<br/>

The **neo4j_for_django** package extends the **_Django_** framework to make it compatible with the **_Neo4j_** databases.  
Two other solutions already exist, but each has its own inconveniences :  

| [**neo4django**](https://github.com/scholrly/neo4django) | [**neomodel**](https://github.com/neo4j-contrib/neomodel) |
|:--------------:|:------------:|
| This package is out of date (last update in 2014). His usage is deprecated, cause he runs under very old versions of all its components : _Python 2.X_ / _Django 1.5_ / _Neo4j 1.9_. Furthermore, **neo4django** does not provide support for the Django's sessions nor a complete support for the Django's authentification. | This package is regularly uptaded, he runs also under last versions of all its components. He provides a very complete adaptation of the Django models, but the philosophy of these contributors is almost to make a 'ready and easy to use' tool, so the user interact only with the highlevel surface . The inconvenience of a such reasonning, it's that under the hood, there are foundations that often ignores primary concepts like separation of writting transactions and reading transactions. This philosophy is perfectly compatible with modest projects, but it conduces to a total remake and to more complex programs the day where we will want to have a finger in the pie, to increase the perfromance of our project with the establishing of clusters (for example). Furthermore, **neomodel** does not provide support for the Django's sessions nor for the Django's authentification. |

**neo4j_for_django** has a completely different philosophy. It wants to let more responsibilities to the users of the package, leaving them interact with deeper concepts. First, the database interaction has been developped to let the user use writing queries and reading queries, but also more advanced concepts like make multi-transactions sessions and causal chaining. To reuse the above example (in the neomodel column of table) of clusters, we understand that with **neo4j_for_django**, their implementation and optimisations will not be an heavy task, and even, if you have the reflex to use directly theses concepts in your project, there will be almost nothing to change. But on the other hand, methods have been developped to make easier the usage of these concepts. With **neo4j_for_django** you can optimise your queries by doing case by case, but you can also use 'ready to use' writing and reading methods to code faster. 
> **NB** : The separation of writing and reading queries is the unique condition to set your program compatible with clusters. So you could just use these two 'ready to use' methods and get pretty good results.

Then, and to a lesser extent than **neomodel**, we have rewrite the Django's _'models'_ , to make them _'node-models'_. The more basics functionnalities have been remade, and especially on the elementary structure of the nodes (to improve clarity), considering that the complex requests work must be done by the developpers theirself, to increase a lot performance of each query.

Finally, the Django's sessions and authentification packages, have been completely remodeled to make them compatible with Neo4j. Maybe later, we will rewrite the Django's administration (Any volonteer ?).

To conclude, if you search a very complete adapation of the Django's models for Neo4j and if you don't need to set authentification and sessions in your project, nor use advandced  graph databases' concepts, you should use [**neomodel**](https://github.com/neo4j-contrib/neomodel), but if you need all of this and more flexibility, check the following documentation. 

###### [>> Installation](https://neo4j-for-django.readthedocs.io/en/latest/installation/)
<br/>
<br/>
<br/>

