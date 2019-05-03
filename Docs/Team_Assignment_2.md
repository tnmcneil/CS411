# CS411 Group 4 - Section A3 : Team Assignment 2 user Stories
### Team Members

* Yahia Bakour
* Michael Hendrick
* Theresa Mcneil
* Zhipeng (Eric) Wang 

### Idea we chose

#### WhereWeGoin.io

**Description:** A user tells us a City they plan on traveling to.  We then use this information to help recommend attractions and things to do for the user on their preferences. We will need to pull in 2 datasets, one for the location/tourist activity data(GooglePlaces, etc…) and Yelp for the reviews.  We will use a database to store user account information and cache past location searches to improve search time.

### User Stories


**User Story 1: User Signup**

The user will first be directed to our site by the URL and then proceed to be asked if they want to login or signup, if they are a first time user and try to login then proceed to user story 2. Once the user clicks the signup button, they will be redirected to signup with an email and password. If they don’t enter either of the fields then nothing will happen but the field will display a message above it saying that it is a required field.Then after they click signup with all the values filled out, they will be asked to fill out a short 5 question form to populate their preferences center (Age, Weather preferences, Hobbies, etc..). They will then be redirected to start user story 3.


**User Story 2: User Login**

The user will first be directed to our site by the URL, and then proceed to be asked if they want to login or signup. If the user enters invalid credentials then we will display a message letting them know that their credentials are invalid and give them a button to start user story 1, if the user forgets to enter one field then it will display a message letting them know the field is required. If it isn’t the users first time logging in, then they can simply click the login button, enter their email and password and click enter to proceed to login. This will cause the page to have an account info button on the top right corner and will allow them to proceed to user story 3.


**User Story 3: Entering Location Info and Displaying Results**

After the Users login (User Story 2) or sign up (User Story 3), they will be asked to input a time of year they want to travel and a location they want to travel to. Then we build a list of results based on their preferences (What weather they like, age , etc,,), the list will show the weather at the location at that time and will also have the option to click on any of the locations to see further details, this will lead them to user story 4. If the user doesn’t click on anything then nothing will happen. If the user clicks on our logo on the top of the page then they will be redirected to the main page where they started the beginning of user story 3. The user will have the ability to change the date/time and location from the top of the list which will reload the list.


**User Story 4: Clicking on a location from the list of locations shown after user story 3.**

The user will have the option to click on any location from the list of locations shown in user story 3. If they click on any of these locations then a sub-list will show up that will inform them of activities and things to do in that area at that time of year. This will also be influenced by their preferences set when they signed up initially. They can also choose to change the date/time and location at the top of the list to reload the list. 
