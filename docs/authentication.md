### >> Authentication :
[TOC]

<br/>

---

# Introducing
**neo4j_for_django** provides a full Django authentication, compatible with the Neo4j databases.  
So, like in the native Django package, there is node classes : **`User`**, **`Group`** and **`Permission`**.  
Let's see more about that.  
<br/>
<br/>
<br/>

---

# Initialize native permissions
For each node models and like in the native Django authentication, it is recommended to create 4 permissions for each new node models class : 

- "**create_**(class name)",  

- "**view_**(class name)",  

- "**update_**(class name)",  

- "**delete_**(class name)".  
<br/>

**neo4_for_django** provides the **`n4d-init`** command to quickly create in the database, all the native permissions for the **`User`**, **`Group`** and **`Permission`** classes.  
So, you'll just have to run : **```python manage.py n4d-init```** in your terminal.  
<br/>
<br/>
<br/>

---

# Initialize all other permissions

We have just seen how to apply all the **neo4j_for_django** native permissions, so it would be nice if we could do this with all other node models classes developed in a Django project.  
**neo4j_for_django** provides the **`n4d-perms`** command to quickly do that.  
So, you'll just have to run : **```python manage.py n4d-perms```** in your terminal and the CRUD permissions will be created for all your own node models (but not for the natives, which ones are created with the above **`n4d-init`** command).


<br/>
<br/>
<br/>

---

# Permissions
<br/>

 - ## Create permissions

Like in the native Django authentication, permissions are instances of a class named **`Permission`**.
We can find this class into the **`neo4j_for_django.contrib.auth.node_models`** file.  
A Permission instance has 2 parameters :

- **`codename`** (required and unique) : like in the Django native authentication, the **codename** serves to identify the permissions between them. The **codename** has a **unicity** constraint and is **required**.
<br/>
<br/>
- **`description`** (required and unique) : like in the Django native authentication, the **description** is a text, generally not too long, that describes the permission.
<br/>
<br/>

So you can easily create a Permission node, by instantiating the **`Permission`** class :

```python
from neo4j_for_django.contrib.auth.node_models import Permission


Permission(codename="create_post",
           description="The user can create a post into the site.")
```
<br>
> Note that the permission codename should always contain a CRUD element ("create", "view", "update", "delete") +  a cible (optional) + the concerned node models name or the concerned entity name, in lowercase.  
<br/>
Some examples :

- **create_user** (CRUD + **`User`** node model),  
<br/>
- **view_administration_page** (CRUD + a page of the site),  
<br/>
- **update_own_messages** (CRUD + target + **`Message`** node model),  
<br/>
- **delete_post** (CRUD + **`Post`** node model),  
<br/>
etc...  
<br/>
<br/>
<br/>

- ## Work with permissions
<br/>

> - ### Get permissions
The **`Permission`** class' possesses a **`get()`** method. This method has a unique parameter, the **codename** of the permission to retrieve, and returns a **`Permission`** instance :

```python
from neo4j_for_django.contrib.auth.node_models import Permission


Permission.get("can_add_post")


>>> <Permission(codename="can_add_post", description="The user can add a post into the site.")>
```
<br/>
<br/>
<br/>


---

# Groups
<br/>

 - ## Create groups
 
Like in the native Django authentication, groups are instances of a class named **`Group`**.  
We can find this class into the **`neo4j_for_django.contrib.auth.node_models`** file.  
A Group instance has 2 parameters :

- **`uuid`** (do not fill) : Each group has an Universal Unique Identifier. This parameter must not be filled in during the Group instantiation because it is automatically filled in.  
<br/>
- **`name`** (required and unique) : like in the Django native authentication, the **name** parameter is the name of the group.  
<br/>

So you can easily create a Group node, by instantiating the **`Group`** class :

```python
from neo4j_for_django.contrib.auth.node_models import Permission


Group(name="SuperUser")
```  
<br/>
<br/>

- ## Work with groups
<br/>

> - ### Get groups
    
The **`Group`** class possesses a **`get()`** method. This method has a unique parameter, the **name** of the group to retrieve, and returns a **`Group`** instance :

```python
from neo4j_for_django.contrib.auth.node_models import Group


Group.get("Moderator")


>>> <Group(name="Moderator", uuid="dcadfbcb4dc04bd3b8dbeb0df1e1bcd6")>

```
<br/>
<br/>

> - ### Get groups' permissions
    
The **`Group`** instances possesse a **`get_permissions()`** method. This method doesn't have any parameter and returns a set of **`Permission`** instances :
```python
from neo4j_for_django.contrib.auth.node_models import Group


Group.get_permissions()


>>> {<Permission(codename="view_session", description="The user can view Session nodes.")>,
     <Permission(codename="delete_session", description="The user can delete Session nodes.")>}
```
<br/>
<br/>

> - ### Get groups' users
    
The **`Group`** instances possess a **`get_users()`** method. This method doesn't have any parameter, and returns a set of **`User`** instances :
```python
from neo4j_for_django.contrib.auth.node_models import Group


Group.get_users()


>>> {<User(first_name="Joe", last_name="B", uuid="a81a8d8259ab4f239c6e7b12b3a576b3")>,
     <User(first_name="Bruce", last_name="W", uuid="a4dc3e3368864db5a223f153097793e1")>}

```
<br/>
<br/>

> - ### Add groups' permissions
    
The **`Group`** instances possess an **`add_permission()`** method. This method has a unique parameter, the **codename** of the permission to add to the group :

```python
from neo4j_for_django.contrib.auth.node_models import Group


my_group = Group.get("Moderator")


my_group.add_permission("delete_session")
```
<br/>
<br/>
<br/>


---

# Users
<br/>

 - ## Create users
 
Like in the native Django authentication, users are instances of a class named **`User`**.
We can find this class into the **`neo4j_for_django.contrib.auth.node_models`** file.  
A User instance has 8 parameters :  

- **`uuid`** (do not fill) : Each user has an Universal Unique Identifier. This parameter must not be filled in during the User instantiation because it is automatically filled in.  
<br/>
- **`is_super_user`** (optional, default=**False**) : As in the native Django authentication, this parameter can be either True or False. If defined on True, the user possesses full rights, he can do anything.  
<br/>
- **`is_staff_user`** (optional, default=**False**) : As in the native Django authentication, this parameter can be either True or False. If defined on True, the user can access to the administration page of the site.  
<br/>
- **`is_active_user`** (optional, default=**True**) : As in the native Django authentication, this parameter can be either True or False. If defined on True, the user can log into the site. However, if defined on False, the account of the user can be considered as **"deactivated"** : the user can not log into the website.  
<br/>
- **`first_name`** (required) : The first name of the user.  
<br/>
- **`last_name`** (required) : The last name of the user.  
<br/>
- **`email`** (required) : The email of the user.  
<br/>
- **`password`** (required) : The encrypted password of the user.  
<br/>
- **`registration_datetime`** (do not fill, default=**datetime.datetime.now**) : The datetime value at the moment where the user has created this account.  This parameter must not be filled in during the User instantiation because it is automatically filled in.  
<br/>

Before users creation, 2 variables must be defined in your general **settings.py** file and below the the **`set_neo4j_for_django_settings_on()`** method :  

- **`PEPPER_1`** : A string used in the password hashing to strengthen the solidity of the hash. **This string must be secret.**  
<br/>
- **`PEPPER_2`** : (The same thing).  
<br/>

Example :
    
>> <small>settings.py</small>
```python
PEPPER_1 = 'zwHD2UiZgk4ftvp0qxSQ'


PEPPER_2 = 'ApTIqGSLDqE2.!'
```  
<br/>

> Note that you could modify the **`_pepper()`** method in **`neo4j_for_django.contrib.auth.hashers`** to add a personalized peppers management. On the other hand, you must do that before the first password savings, because the **`_pepper()`** method is also used to check passwords during authentication.  
<br/>

There are 2 classmethods to create an user, named **`create()`** and **`create_super_user()`** :  

- The **`create()`** method has the same behaviour as an instantiation of the **`User`** class, except that the raw password provided is automatically hashed before saving in the database.  
<br/>
- The **`create_super_user()`** method, creates a user and a hash like the raw password before saving, but in addition to that, it forces also the **`is_super_user`** and **`is_staff_user`** parameters, on **True**.
<br/>
<br/>

**WARNING** : To create a user, **never use** the simple **instantiation** of the **`User`** class because it doesn't provide an automatic password hashing (same behaviour that the native Django authentication). Store the raw passwords in the database is a very **bad and dangerous practice**.
<br/>

> Note that you will have to name parameters with this method.  
Example : **`User.create(first_name="John", ...)`** and not **`User.create("John", ...)`**.

Demonstration :

```python
from neo4j_for_django.contrib.auth.node_models import User


bob = User.create(first_name="Bob",
                       last_name="C",
                       email="bob@mail.com",
                       password="1234")
                       
                       
# Or to create automatically a super user :
bob = User.create_super_user(first_name="Bob",
                             last_name="C",
                             email="bob@mail.com",
                             password="1234")
                             

# But to do the same thing, you could have done that :
bob = User.create(first_name="Bob",
                  last_name="C",
                  email="bob@mail.com",
                  password="1234",
                  is_super_user=True,
                  is_staff_user=True)
                  

# In the other hand, this, would have raised an error :
bob = User.create_super_user(first_name="Bob",
                             last_name="C",
                             email="bob@mail.com",
                             password="1234",
                             is_super_user=False)

```  
<br/>

> NB : Like in the native Django authentication, you could use the command **`python manage.py createsuperuser`** in your terminal to create a super user. You'll only have to follow the indications.  
<br/>
<br/>

- ## Work with users  
<br/>

> - ### Get users
    
The **`User`** class possesses a **`get()`** method. This method has 2 parameters, the **uuid** of the user to retrieve and/or his **email**, and returns a **`User`** instance :

```python
from neo4j_for_django.contrib.auth.node_models import User


User.get(email="john@mail.com")


>>> <User(first_name="John", last_name="X", uuid="a81a8d8259ab4f239c6e7b12b3a576b3")>

```
<br/>
<br/>

>  - ### Update users' properties

The **`User`** instances possess an **`update()`** method. This method takes 2 parameters : the **property name** and the **new property value**.
```python
from neo4j_for_django.contrib.auth.node_models import User

john = User.get(email="john@mail.com")
print(john)

>>> <User(first_name="John", last_name="X", uuid="a81a8d8259ab4f239c6e7b12b3a576b3")>


john.update("first_name", "Johnny")


print(john)


>>> <User(first_name="Johnny", last_name="X", uuid="a81a8d8259ab4f239c6e7b12b3a576b3")>
```
<br/>
<br/>

> - ### Get users' permissions
    
The **`User`** instances possess a **`get_permissions()`** method that returns a set of all the concerned user's permissions. This method doesn't have any parameter.
```python
from neo4j_for_django.contrib.auth.node_models import User


User.get_permissions()


>>> {<Permission(codename="view_session", description="The user can view Session nodes.")>,
     <Permission(codename="delete_session", description="The user can delete Session nodes.")>}
```
<br/>
<br/>

> - ### Get users' groups
    
The **`User`** instances possess a **`get_groups()`** method that returns a set of all the concerned user's groups. This method doesn't have any parameter.
```python
from neo4j_for_django.contrib.auth.node_models import User


User.get_groups()


>>> {<Group(name="Moderator", uuid="dcadfbcb4dc04bd3b8dbeb0df1e1bcd6")>}
```
<br/>
<br/>

> - ### Get users' sessions
    
The **`User`** instances possess a **`get_sessions()`** method that returns a set of all the concerned user's sessions. This method doesn't have any parameter.
```python
from neo4j_for_django.contrib.auth.node_models import User


User.get_session()


>>> <Session object(session_key="8fu3wz00b7gzxvmzb45onz44d8hsesvm", expire_date="2019-04-12 0
    4:07:32.897744+00:00")>

```
<br/>
<br/>

> - ### Add users' permissions
    
The **`User`** instances possess an **`add_permission()`** method. This method has a unique parameter, the **codename** of the permission to add to the user :

```python
from neo4j_for_django.contrib.auth.node_models import User


an_user = User.get(uuid="a81a8d8259ab4f239c6e7b12b3a576b3")


an_user.add_permission("delete_session")
```
<br/>
<br/>

> - ### Add users' groups
    
The **`User`** instances possess an **`add_group()`** method. This method has a unique parameter, the **name** of the group in which we want to add the user :

```python
from neo4j_for_django.contrib.auth.node_models import User


an_user = User.get(uuid="a81a8d8259ab4f239c6e7b12b3a576b3")


an_user.add_group("Moderator")
```
<br/>
<br/>

> - ### Test users' permissions

The **`User`** instances possess a **`has_perm()`** method that test if an user has a certain permission. This method has a unique parameter, the **codename** of the property to check.
```python
from neo4j_for_django.contrib.auth.node_models import User


an_user = User.get(uuid="a81a8d8259ab4f239c6e7b12b3a576b3")


print(an_user.has_perm('delete_session'))


>>> False

```
<br/>
<br/>
<br/>
