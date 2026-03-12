# Teacher-Reviewing-Database
An SQL database using Python containing reviews on college professors that are posted by students. Users are required to login before using the database, and once logged in can do the following:
  1. Add or Delete their own comments.
  2. Sort through reviews based on several conditions:
     -  View their own reviews that they have posted
     -  View the professor with the best or worst reviews in the database
     -  Get the average rating of a specific professors for either a specific class they have taught or for all classes they have taught.
  3.  Get the total numbers of reviews that a user has posted or that a professor has.

Extra information:
  -  Due to time constraints, the database does not have a web application and must be run through a terminal. The database uses Python, Python-SQL connector, and MYSQL Workbench to function properly.
  -  As this project was original made for a class, the database had to meet specific requirements in order to receive full points. Due to these requirements, the database could not be fully optimized in the most efficient way and contains redundant and/or sub-optimal relationships among its entities. These problems may be addressed in a future, more polished version of this project with the following implementations:
     -  Design a web page application for the database
     -  Further optimize the relationships, tables, and entities of the database
     -  Add a seperate 'administrator' user system within the database that is allowed to add and delete data from other tables (professors, universities, classes) instead of relying on manual input into MYSQL Workbench.
     -  Additional options for sorting data among universities, professors, classes, reviews, and users.
     -  A profile/informtion page for enties within the database
