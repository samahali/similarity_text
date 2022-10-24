
# Text matching

A small Project used to check the similarity of two statements and if 
the similarity greater than  50 there similarity is high

# Quick start
I used Jaccard coefficient algorithm to check the similarity
it get length of the intersection set between two syntax and divide them by the union of them
after that we will multiply it by 100 to get a percentage degree

you can have a look of jaccard coeffection functions in utility folder

# Used on this project
* Used pandas to read and manipulate with csv file
* unit test
* used coverage
* using also ratelimit to prevent too many requests
 

Running Coverage 
-----------------
Run `coverage run manage.py test appName.testFolder.TestClass.test_func`
* Replace `appName`, `testFolder`, `TestClass` and `test_func` with your corresponding values
Then generate html by Running `coverage html`

Runnig Test
-------------
Run `python manage.py test appName..testFolder.TestClass.test_func`
* Replace `appName`, `testFolder`, `TestClass` and `test_func` with your corresponding values

App Deployed here:
-------

https://agile-brushlands-24112.herokuapp.com/ 
| https://git.heroku.com/agile-brushlands-24112.git
