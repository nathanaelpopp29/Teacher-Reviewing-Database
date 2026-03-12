import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="B1gB0y#l0l",
    database="CommentSystem"
)
mycursor = db.cursor()
clear = lambda: os.system('cls')

################################# Create Tables Function ###################################
######################################################################################

#Create Tables in database
def Create_Tables_In_Database():
    mycursor.execute("""
        CREATE TABLE User (
            user_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, 
            username VARCHAR(40) NOT NULL, 
            password CHAR(100) NOT NULL, 
            age INTEGER, 
            major VARCHAR(100)
        )""")

    mycursor.execute("""
        CREATE TABLE Class (
            class_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, 
            class_major VARCHAR(100) NOT NULL, 
            class_name VARCHAR(100) NOT NULL, 
            credit_hours INTEGER
        )""")

    mycursor.execute("""
        CREATE TABLE Review (
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES User(user_id) 
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (class_id) REFERENCES Class(class_id) 
                ON UPDATE CASCADE 
                ON DELETE CASCADE,
            rating INTEGER NOT NULL, 
            date_posted DATE NOT NULL, 
            description VARCHAR(500), 
            title VARCHAR(100)
        )""")

    mycursor.execute("""
        CREATE TABLE Professor (
            professor_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, 
            professor_name VARCHAR(50) NOT NULL
    )""")

    mycursor.execute("""
        CREATE TABLE UNIVERSITY (
            university_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, 
            university_name VARCHAR(50) NOT NULL, 
            state CHAR(2), 
            type VARCHAR(100))
        """)

    #Relational tables - Relationships between main tables

    #Students have taken what class
    mycursor.execute("""CREATE TABLE Taken(
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        class_id INTEGER NOT NULL,
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE     # DELETE THIS PROBABLY ???? IF THE CLASS IS DELETED THE STILL TOOK IT
    )""")

    #user posts what reivews (with relation to class)
    mycursor.execute("""CREATE TABLE Posts(
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        class_id INTEGER NOT NULL,
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

    #Professor has what reviews
    mycursor.execute("""CREATE TABLE Has(
        professor_id INTEGER NOT NULL,
        FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

    #Teacher teaches what class
    mycursor.execute("""CREATE TABLE Teaches(
        professor_id INTEGER NOT NULL,
        FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        class_id INTEGER NOT NULL,
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE ###########
    )""")

    #Class is taught at what univesrity
    mycursor.execute("""CREATE TABLE Taught_At(
        class_id INTEGER NOT NULL,
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        university INTEGER NOT NULL,
        FOREIGN KEY (university) REFERENCES UNIVERSITY(university_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")

    #Professor teaches at what university
    mycursor.execute("""CREATE TABLE Teaches_At(
        professor_id INTEGER NOT NULL,
        FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        university_id INTEGER NOT NULL,
        FOREIGN KEY (university_id) REFERENCES UNIVERSITY(university_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )""")



################################# Database Functions ###################################
######################################################################################

#Login to database or create a new user
def login():
    valid = 0
    continue_login = ""
    #Check if its valid
    while valid == 0:
        print("\nPlease select one of the following options: \n1. Quit \n2. Login as existing user \n3. Create a new user")
        option = input("Option: ")
        if option == "1":
            valid = 1
            quit()
        elif option == "2":
            valid = 1
            break
        elif option == "3":
            valid = 1
            break
        else:
            clear()
            print("Invalid option, please try again.\n")
    found = 0
    #loop to continue until person quits, logs in, or creates a new account
    while found != 1:
        found = 0
        #logging in as existing use
        if option == "2":
            #check to see if they wish to continue
            continue_login = input("Logging in as an existing user. Do you wish to continue (y/n): ")
            if continue_login.lower() != 'y':
                clear()
                print("Returning to login options...\n")
                login()
            clear()
            print("Login as existing user:")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            #look for username and password in user table
            mycursor.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password))
            for x in mycursor:
                found = 1
            if found == 1:
                clear()
                print("Login successful! Welcome back, " + username + "!")
                menu(username, password)
            if found == 0:
                clear()
                print("\nLogin failed. Invalid username or password.\n")
        #user is going to create a new account
        elif option == "3":
            clear()
            #check if they wish to continue
            continue_login = input("Creating a new user. Do you wish to continue (y/n): ")
            if continue_login.lower() != 'y':
                clear()
                print("Returning to login options...\n")
                login()
            clear()
            #Add new use to use table with propted variable / information questions
            print("Adding new User:")
            new_username = input("Enter your desired username: ")
            new_password = input("Enter your desired password: ")
            new_age = int(input("Enter your age: "))
            new_major = input("Enter your major (or keep blank): ")
            mycursor.execute("INSERT INTO User (username, password, age, major) VALUES (%s, %s, %s, %s)", (new_username, new_password, new_age, new_major))
            db.commit()
            clear()
            print("\nUser created successfully! Welcome " + new_username + "! You can now login with your new credentials.\n")
            found = 1
            menu(new_username, new_password)

#Show tables in database
def Show_Table():
    print("---------- Showing Tables in Database ----------")
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)
    print("\n----------------------------------------------")
    ok = input ("Press ENTER to Exit...")

#User adds review
#User should write more than one review for the same class taught by the same professor
def Add_Review(username, password):
    found = 0
    while found == 0:
        print("---------- Adding Review ----------\n")
        #Check if there are any viable professors to add reviews to
        mycursor.execute("""Select Professor.professor_name, Class.class_name From Teaches
                            Join Professor On Teaches.professor_id = professor.professor_id
                            Join Class On Teaches.class_id = Class.class_id
                        """)
        results = mycursor.fetchall()
        #Check to see if reviews actually exist, if not exit
        if len(results) == 0:
            print("There are currently no professors in the database.")
            input("Press ENTER to Exit...")
            return
        #if there are then print them out so user can see
        for group in results:
            professor_name, class_name = group
            print("Professor: ", professor_name)
            print("Class:     ", class_name)
            print("\n-----------------------------------")
        #do they truly wish to add this review
        yes_no = input("Adding New Review. Do you wish to continue (y/n): ")
        if yes_no.lower() != 'y':
            clear()
            print("Returning to Main Menu...\n")
            menu(username, password)
        #user need to select the professor to add comment to
        else:
            print("Select one of the following professors to add a review to (as displayed above):")
            professor_name = input("Professor's Full Name: ")
            class_name = input("Class Name: ")
            mycursor.execute ( """
                                SELECT Professor.professor_id, Class.class_id
                                FROM Teaches
                                JOIN Professor ON Teaches.professor_id = Professor.professor_id
                                JOIN Class ON Teaches.class_id = Class.class_id
                                WHERE Professor.professor_name = %s 
                                AND Class.class_name = %s
                                """, (professor_name, class_name))
        #check to see if the professor chosen is a valid option
        for x in mycursor:
            print("Valid Professor and Class Found")
            found = 1
            break
        if found == 0:
            clear()
            print("Invalid Professor or Class Name Entered, Please Try Again.\n")
    clear()
    #Prompt user to give information
    print("----------------------------------------------")
    print("Adding Review for Professor " + professor_name + " for class " + class_name)
    rating = input("Enter rating (0-10): ")
    date_posted = input("Enter date posted (YYYY-MM-DD): ")
    description = input("Enter review description: ")
    title = input("Enter review title: ")
    #Ge professor_id nd class_id from inputed names
    mycursor.execute (""" Select Professor.professor_id, Class.class_id
                            From Teaches
                            Join Professor On Teaches.professor_id = professor.professor_id
                            Join Class On Teaches.class_id = Class.class_id
                            Where Professor.professor_name = %s
                            And Class.class_name = %s
                        """, (professor_name, class_name))
    result = mycursor.fetchone()
    #check to make sure it is a viable match
    if result is None:
        print("No matching professor found!")
    else:
        professor_id, class_id = result
        #print("FOund IDS:", professor_id, class_id)
    #insert into review table
    mycursor.execute (""" INSERT INTO Review (user_id, class_id, rating, date_posted, description, title) VALUES (
                            (SELECT user_id FROM User WHERE username = %s AND password = %s),
                            %s, %s, %s, %s, %s
                        )""", (username, password, class_id, rating, date_posted, description, title))
    #insert into has table
    mycursor.execute(""" INSERT INTO Has (professor_id, user_id)
                        VALUES (%s, (SELECT user_id FROM User WHERE username = %s AND password = %s))
                    """, (professor_id, username, password))
    #insert into posts table
    mycursor.execute(""" INSERT INTO Posts (class_id, user_id)
                        VALUES (%s, (SELECT user_id FROM User WHERE username = %s AND password = %s))
                    """, (class_id, username, password))
    #insert into taken table
    mycursor.execute(""" INSERT INTO Taken (class_id, user_id)
                        VALUES (%s, (SELECT user_id FROM User WHERE username = %s AND password = %s))
                    """, (class_id, username, password))
    db.commit()
    print("\nReview added successfully!")
    okay =  input("Press ENTER to Exit...")

#User can delete one of their reviews
def Delete_Review(username, password):
    choice = ""
    print("---------- Deleting Review ----------")
    print("Date Posted | Class Name | Professor Name | Rating | Title | Description")
    mycursor.execute (""" SELECT Review.date_posted, Class.class_name, Professor.professor_name, Review.rating, Review.title,  Review.description
                            FROM Review
                            JOIN User ON Review.user_id = User.user_id
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE User.username = %s AND User.password = %s
                        """, (username, password))
    reviews = mycursor.fetchall()
    for x in reviews:
        print(x)
    if len(reviews) == 0:
        print("You have not posted any reviews to delete.")
        input("Press ENTER to Exit...")
        return

    print("---------------------------------------------\n")
    choice = input("Deleting Review. Would you like to continue? (y/n): ")
    if choice.lower() != 'y':
        clear()
        print("Returning to Main Menu...\n")
        menu(username, password)
    print("To identify the review to delete, please provide the following details:")
    date_posted = input("Date Posted (YYYY-MM-DD): ")
    class_name = input("Class Name: ")
    professor_name = input("Professor's Full Name: ")
    #FInd the professor_id, user_id, and class_id
    mycursor.execute(""" SELECT Professor.professor_id, User.user_id, Class.class_id
                        FROM Review
                        JOIN User      ON Review.user_id = User.user_id
                        JOIN Class     ON Review.class_id = Class.class_id
                        JOIN Teaches   ON Class.class_id = Teaches.class_id
                        JOIN Professor ON Teaches.professor_id = Professor.professor_id
                        WHERE User.username = %s
                        AND User.password = %s
                        AND Review.date_posted = %s
                        AND Class.class_name = %s
                        AND Professor.professor_name = %s
                        LIMIT 1
                    """, (username, password, date_posted, class_name, professor_name))
    #CHeck if they entered right, if not kick out user
    review = mycursor.fetchone()
    if review is None:
        print("No Matching review found. Please exit and try again.")
        input("Press ENTER to continue...")
        return
    professor_id, user_id, class_id = review
    #delete from review table
    mycursor.execute (""" DELETE Review FROM Review
                            JOIN User ON Review.user_id = User.user_id
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE User.username = %s 
                            AND User.password = %s
                            AND Review.date_posted = %s
                            AND Class.class_name = %s
                            AND Professor.professor_name = %s
                        """, (username, password, date_posted, class_name, professor_name))
    #delete from has table
    mycursor.execute (""" DELETE FROM Has
                          WHERE professor_id = %s 
                          AND user_id = %s
                          LIMIT 1
                       """, (professor_id, user_id))
    #delete from posts table
    mycursor.execute (""" DELETE FROM Posts
                            WHERE user_id = %s
                            AND class_id = %s
                      """, (user_id, class_id))
    #delete from taken table
    mycursor.execute (""" Delete FROM Taken
                            WHERE user_id = %s
                            AND class_id = %s
                      """, (user_id, class_id))
    db.commit()
    print("Review has been deleted successfully.")
    okay =  input("Press ENTER to Exit...")

#Find min and max rating for reviews of professor
def Find_Min_Max_Rating():
    #Print out Professors in database
    print("---------- Please Choose a Professor to Search ----------")
    mycursor.execute ("Select professor_name From Professor")
    for x in mycursor:
        print(x)
    #check to make sure there are professors in database
    if not mycursor:
        print("There are no professors in the database.")
        okay =  input("Press ENTER to Exit...")
        return
    print("--------------------------------------------------------\n")
    #Prompt if thy would like to continue or go back
    choice = input("Finding Min/Max Rating for Reviews. Do you wish to continue? (y/n): ")
    if choice.lower() != 'y':
        clear()
        print("Returning to Main Menu...\n")
        return
    print("\n")
    #Prompt user to enter professors name to search database
    #Sorts the reviews in ascending order and limits to 1 result (min) (if multiple with same rating, shows the one added first))
    professor_name = input("Enter Professor's Full Name to search for their reviews: ")
    print("\n")
    #Check to see if Professor has reviews
    mycursor.execute(""" SELECT COUNT(*)
                            FROM Review
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                    """, (professor_name,))
    count = mycursor.fetchone()[0]
    #check to make sure professor has reviews
    if count == 0:
        print("This Professor has no reviews.")
        okay =  input("Press ENTER to Exit...")
        return
    #Find min and max rated reviews for professor
    print("---------- Finding Min/Max Rating for Reviews -----------")
    print("Rating | Class Name | Review Title | Professor Name | Description")
    print("Worst Rated Review:")
    mycursor.execute (""" SELECT Review.rating, Class.class_name, Review.title, Professor.professor_name, Review.description
                            FROM Review
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                            ORDER BY Review.rating ASC 
                            LIMIT 1
                        """, (professor_name,))
    for x in mycursor:
        print(x)
    #select needed categories/tuples to print out
    print("Best Rated Review")
    mycursor.execute (""" SELECT Review.rating, Class.class_name, Review.title, Professor.professor_name, Review.description
                            FROM Review
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                            ORDER BY Review.rating DESC 
                            LIMIT 1
                        """, (professor_name,))
    for x in mycursor:
        print(x)
    print("--------------------------------------------------------\n")
    print("Min/Max Rating Search Complete.")
    okay =  input("Press ENTER to Exit...")

#Get average Rating of a professor
def Get_Average_Rating():
    #Prompt User if they wish to continue or return
    choice = input("Finding Average Rating of Professor. Do you wish to continue? (y/n): ")
    if choice.lower() != 'y':
        clear()
        print("Returning to Main Menu...\n")
        return
    #prompt user if they wish to find average for all professor's classes or just one
    option = ""
    while option != '1' and option != '2':
        print("Would You Like to Search The Average of All Classes or A Specfic One of a Professor:\n1. All Classes\n2. Specific Class\n")
        option = input("Option: ")
        if option == '1' or option == '2':
            print("Option choice: ", option)
            break
        clear()
        print("Invalid Choice. Please try again\n")
    #Check to see if professors are in database then print them out
    print("---------- Please Choose a Professor to Search ----------")
    mycursor.execute ("Select professor_name From Professor")
    for x in mycursor:
        print(x)
    if not mycursor:
        print("There are no professors in the database.")
        okay =  input("Press ENTER to Exit...")
        return
    print("--------------------------------------------------------\n")
    #Choose professor
    professor_name = input("Please enter the Full Name of the professor to search for their average rating: ")
    #Check to see if Professor has reviews
    mycursor.execute(""" SELECT COUNT(*)
                            FROM Review
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                    """, (professor_name,))
    count = mycursor.fetchone()[0]
    if count == 0:
        print("This Professor has no reviews.")
        okay =  input("Press ENTER to Exit...")
        return
    print("\n")
    #Find Average of all classes
    if option == '1':
        #Find Average Rating of Professor
        print("---------- Finding Average Rating of ", professor_name, " -----------")
        mycursor.execute(""" SELECT AVG(Review.rating)
                            FROM Review
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                        """, (professor_name,))
        avg_rating = mycursor.fetchone()[0]
        print("Average Rating: ", avg_rating)
    
    #Find average of specific class
    if option == '2':
        print("---------- Classes Taught by ", professor_name, " -----------")
        mycursor.execute(""" SELECT Class.class_name
                            FROM Class
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            WHERE Professor.professor_name = %s
                        """, (professor_name,))
        classes = mycursor.fetchall()
        if not classes:
            print("This professor does not teach any classes.")
            input("Press ENTER to Exit...")
            return
        # Print class list
        for c in classes:
            print(c[0])
        print("---------------------------------------------\n")
        # Ask user to pick a specific class
        class_name = input("Enter the class name to find its average rating: ")
        print("\n")
        # Make sure professor teaches this class
        found = 0
        while found == 0:
            mycursor.execute("""SELECT COUNT(*)
                                FROM Class
                                JOIN Teaches ON Class.class_id = Teaches.class_id
                                JOIN Professor ON Teaches.professor_id = Professor.professor_id
                                WHERE Professor.professor_name = %s
                                  AND Class.class_name = %s
                            """, (professor_name, class_name))
            teaches_count = mycursor.fetchone()[0]
            if teaches_count == 0:
                clear()
                print("This professor does not teach that class. Please try again.\n")
            elif teaches_count > 0:
                found += 1
                break
        #print results
        print("---------- Average Rating of", class_name," taught by ", professor_name, "-----------")
        mycursor.execute(""" SELECT AVG(Review.rating)
                                FROM Review
                                JOIN Class ON Review.class_id = Class.class_id
                                JOIN Teaches ON Class.class_id = Teaches.class_id
                                JOIN Professor ON Teaches.professor_id = Professor.professor_id
                                WHERE Professor.professor_name = %s
                                AND Class.class_name = %s
                        """, (professor_name, class_name))
        avg_rating = mycursor.fetchone()[0]
        print("Average Rating:", round(avg_rating, 2))
    
    print("--------------------------------------------------------\n")    
    print("Min/Max Rating Search Complete.")
    input("Press ENTER to Exit...")
    
#Get total number of reveiws for a professor or how many a user has posted??
def Total_Number_of_Reviews(username, password):
    option = ''
    while option != '1' and option != 2:
        print("You are about to look for total number of views. What would you like to do:\n0. Quit\n1. View the total number of reviews a professor has\n2. View the total number of reviews you have")
        option = input("\nOption: ")
        clear()
        if option == '0':
            return
        elif option == '1' or option == '2':
            break
        else:
            print("Invalid answer. Please try again.")
    #find a professors total count of views
    if option == '1': 
        #Check to see if professors are in database then print them out
        print("---------- Please Choose a Professor to Search ----------")
        mycursor.execute ("Select professor_name From Professor")
        for x in mycursor:
            print(x)
        if not mycursor:
            print("There are no professors in the database.")
            okay =  input("Press ENTER to Exit...")
            return
        print("--------------------------------------------------------\n")
        #Choose professor
        professor_name = input("Please enter the Full Name of the professor to search their total: ")
        #Check to see if Professor has reviews
        mycursor.execute(""" SELECT COUNT(*)
                                FROM Review
                                JOIN Class ON Review.class_id = Class.class_id
                                JOIN Teaches ON Class.class_id = Teaches.class_id
                                JOIN Professor ON Teaches.professor_id = Professor.professor_id
                                WHERE Professor.professor_name = %s
                        """, (professor_name,))
        count = mycursor.fetchone()[0]
        if count == 0:
            print("This Professor either has no reviews or doesn't exist.")
            okay =  input("Press ENTER to Exit...")
            clear()
            return
        print("\n")
        print("---------- Total Number of Reviews for", professor_name,"----------")
        print("Count:",count)

    #find the users total number of reviews
    if option == '2':
        mycursor.execute(""" SELECT COUNT(*)
                            FROM Review
                            JOIN User ON Review.user_id = User.user_id
                            WHERE User.username = %s AND User.password = %s
                         """, (username, password))
        count = mycursor.fetchone()[0]
        if count == 0:
            print("This user has no reviews or does not exist.")
            input("Press ENTER to exit...")
            return

        print("\n---------- Total Number of Reviews by", username, "----------")
        print("Total Reviews:", count)
    print("--------------------------------------------------------\n")
    input("Press ENTER to Exit")
    print("\n")

#View Reviews through 4 different sorting/ordings. (all by user, all ever made, all by professor, all by classes)
def View_Reviews(username, password):
    option = ''
    while option != '1' and option != '2':
        print("You are about to go through all of the reviews. What would you like to do:\n0. Quit\n1. View all of the reviews you have posted\n2. View all of the reviews that have been posted in order of being added (not by date)\n3. View all reviews sorted by professor\n4. View all reviews sorted by class")
        option = input("\nOption: ")
        clear()
        if option == '0':
            return
        elif option == '1' or option == '2' or option == '3' or option == '4':
            break
        else:
            print("Invalid answer. Please try again.")
    #print the users reviews
    if option == '1':
        mycursor.execute("""
            SELECT Review.date_posted, Review.rating, Review.title, Review.description, Professor.professor_name, Class.class_name
            FROM Review
            JOIN User ON Review.user_id = User.user_id
            JOIN Class ON Review.class_id = Class.class_id
            JOIN Teaches ON Class.class_id = Teaches.class_id
            JOIN Professor ON Teaches.professor_id = Professor.professor_id
            WHERE User.username = %s AND User.password = %s
        """, (username, password))
        results = mycursor.fetchall()
        #check if they did or did not post any reviews
        if len(results) == 0:
            print("You have not posted any reviews. Exit and go to Option 2 to add some.")
            input("Press ENTER to exit...")
            return
        #print results with better setup than others
        for review in results:
            date_posted, rating, title, desc, prof, classname = review
            print("\n----------------------------------------")
            print("Date Posted: ", date_posted)
            print("Professor:   ", prof)
            print("Class:       ", classname)
            print("Rating:      ", rating)
            print("Title:       ", title)
            print("Description: ", desc)

    #print out all reviews ever posted in order of when they were added to the database (not by date)
    elif option == '2':
        mycursor.execute(""" SELECT Review.date_posted, Review.rating, Review.title, Review.description, Professor.professor_name, Class.class_name, User.username
                                FROM Review
                                JOIN User ON Review.user_id = User.user_id
                                JOIN Class ON Review.class_id = Class.class_id
                                JOIN Teaches ON Class.class_id = Teaches.class_id
                                JOIN Professor ON Teaches.professor_id = Professor.professor_id
                                ORDER BY Review.rating DESC, Review.title
                        """)
        #check to make sure there are reviews in the database
        reviews = mycursor.fetchall()
        if len(reviews) == 0:
            print("No reviews have been added yet.")
            input("Press ENTER to Exit...")
            return
        for review in reviews:
            date_posted, rating, title, description, professor_name, class_name, username = review
            print("\n----------------------------------------")
            print("Date Posted: ", date_posted)
            print("Professor:   ", professor_name)
            print("Class:       ", class_name)
            print("Rating:      ", rating)
            print("Username:    ", username)
            print("Title:       ", title)
            print("Description: ", description)
    #Reviews sorted by professor
    elif option == '3':
        print("\n------- All Reviews Sorted By Professor -------")
        mycursor.execute(""" SELECT Professor.professor_name, Class.class_name, Review.rating, User.username, Review.date_posted, Review.title, Review.description
                            FROM Review
                            JOIN User ON Review.user_id = User.user_id
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            ORDER BY Professor.professor_name DESC, Review.rating DESC
                        """)
        reviews = mycursor.fetchall()
        #check to make sure reviews exists
        if len(reviews) == 0:
            print("No Reviews have been added yet.")
            input("Press ENTER to Exit...")
            return
        #print out reviews
        for object in reviews:
            professor_name, class_name, rating, username, date_posted, title, description,  = object
            print("\n----------------------------------------")
            print("Professor:   ", professor_name)
            print("Class:       ", class_name)
            print("Rating:      ", rating)
            print("Username:    ", username)
            print("Date Posted: ", date_posted)
            print("Title:       ", title)
            print("Description: ", description)

    #Reviews sorted by class
    elif option == '4':
        print("\n------- All Reviews Sorted By Class -------")
        mycursor.execute(""" SELECT Class.class_name, Professor.professor_name, Review.rating, User.username, Review.date_posted, Review.title, Review.description
                            FROM Review
                            JOIN User ON Review.user_id = User.user_id
                            JOIN Class ON Review.class_id = Class.class_id
                            JOIN Teaches ON Class.class_id = Teaches.class_id
                            JOIN Professor ON Teaches.professor_id = Professor.professor_id
                            ORDER BY Class.class_name DESC, Review.rating DESC
                        """)
        #check that there are reviews
        reviews = mycursor.fetchall()
        if len(reviews) == 0:
            print("No Reviews have been added yet.")
            input("Press ENTER to Exit...")
            return
        #print out reviews
        for object in reviews:
            class_name, professor_name, rating, username, date_posted, title, description,  = object
            print("\n----------------------------------------")
            print("Class:       ", class_name)
            print("Professor:   ", professor_name)
            print("Rating:      ", rating)
            print("Username:    ", username)
            print("Date Posted: ", date_posted)
            print("Title:       ", title)
            print("Description: ", description)
    print("----------------------------------------\n")
    input("Press ENTER to Exit...")






def menu(username, password):
    action = 1
    while action != 0:
        #print out username, password, and options available
        print("User: " + username)
        print("Password: " + password)
        print("-------------------- Main Menu --------------------")
        print("Choose one of the following actions:")
        print("1. Show Tables in Database")
        print("2. Add Review")
        print("3. Delete Review")
        print("4. Find Min/Max Rating for Reviews")
        print("5. Get Average Rating")
        print("6. Total Number of Reviews")
        print("7. View Reviews")
        print("8. Quit")
        action = int(input("Option: "))
        #make sure option is valid
        while action < 0 or action > 9:
            print("Invalid Choice Entered. Please Choose From the Menu Below")
            ok = input ("press ENTER")
            action = menu(username, password)
        #choose correct option / function
        match action:
            case 1:
                clear()
                Show_Table()
                clear()
                menu(username, password)
            case 2:
                clear()
                Add_Review(username, password)
                clear()
                menu(username, password)
            case 3:
                clear()
                Delete_Review(username, password)
                clear()
                menu(username, password)
            case 4:
                clear()
                Find_Min_Max_Rating()
                clear()
                menu(username, password)
            case 5:
                clear()
                Get_Average_Rating()
                clear()
                menu(username, password)
            case 6:
                clear()
                Total_Number_of_Reviews(username, password)
                clear()
                menu(username, password)
            case 7:
                clear()
                View_Reviews(username, password)
                clear()
                menu(username, password)
            case 8:
                quit()

def main():
    #Create_Tables_In_Database()
    clear()
    login()
    print("Logging Out...")

if __name__ == "__main__":
    main()    