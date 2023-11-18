# Expense Tracker

Expense Tracker is a Python-built application that seamlessly integrates with Google Sheets via API, providing users with a streamlined solution for tracking and controlling their monthly expenses. 

The app has a user-friendly interface, real-time data synchronization, and insightful visualizations, empowering individuals to make informed financial decisions while ensuring the security of their sensitive information. By analyzing spending patterns and setting budget goals, Expense Tracker offers a convenient and secure way to manage finances in the digital era.

The app was inspired by the traditional pen-and-paper method and offers a digital solution that leverages the power of technology to streamline expense tracking and financial management.

[Live Website](https://expense-tracker-at-fd85a26ed02d.herokuapp.com/)

[Github Repository](https://github.com/terintealexandrin18/exptrack)

![Image of the welecome/start screen python expense tracker app](assets/mainscreen.png)


## Table of Contents
    - 1 User Experience
        - Project Goal
        - User Stories
    - 2 Design
        - Page Layout
        - Color Scheme
        - Flowchart
    - 3 Features
        - Existing Features
        - Future Features
    - 4 Technologies
        - Languages Used
        - Frameworks, Libraries and Programs Used
    - 5 Testing
        - Bugs
            - Fixed Bugs
            - Unfixed Bugs
        - Code Validation
        - Compatibility
        - Manual Testing
    - 6 Deployment
    - 7 Finished Product
    - 8 Credit
    - 9 Acknowledgments


## User Experience

### Project Goal
 - To build an app that is user-friendly and requires minimal instructions.
 - To ensure easy navigation throughout the app.
 - To implement a database that can store user input.
 - To incorporate input validation to prevent incorrect data entry
 - The program should run continuously until the user decides to stop it.

### User Stories
- As a user, I want to understand the process of the app.
- As a user, I want to be able to view the expenses that have been added.
- As a user, I want the ability to add more expenses without having to open the app every time.
- As a user, I want to be able to enter only valid data.


## Design

### Page Layout
 - The Expense Tracker app boasts a well-structured command-line interface, featuring clear user prompts, engaging ASCII art, and a logical menu structure, providing users with an intuitive and visually coherent platform for effective expense tracking and financial management.

 ### Color Scheme
- The app's color scheme enhances both its visual appeal and functionality by using consistent color-coding for different types of messages. This provides clear visual cues and improves the user experience.
 - Color BLUE - represents user input.
 - Color GREEN - represents success, invalid input or errors, guiding the user to provide the correct type of information.
 - Color RED - represents a warning message, and this helps to draw attention to a potential budget deficit. 
 - Color WHITE - represents default text color.

![color scheme example](assets/images/colors.png)

### Flowchart

to be add.


## Features

### Existing Features

Google Sheet:
 - User expenses are stored in a Google Sheet. Currently, the app does not support multiple user logins and passwords, so the data is cleared each time the app is run.

![google sheet](assets/images/googlesheet.png)

Title:
 - The Expense Tracker application starts with an eye-catching tile created with ASCII art. This introduction is not only visually appealing but also serves to explain the purpose of the app, enhancing the user experience. It creates a positive and engaging environment for expense tracking, making it more enjoyable for the user.

![tilte of the app Expense Tracker](assets/images/title.png)

Expense Category Selection:
 - Simplifies expense entry by providing predefined categories with emoji icons, making it faster and more user-friendly. Emoji icons also improve accessibility for users who prefer symbols over text.
 
 ![category  of the expenses](assets/images/category.png)

 View Expenses by Category:
 - By analyzing spending in specific categories, users can better manage their expenses and budgets and track where their money is going.

 ![expenses by category](assets/images/viewexpensesbycategory.png)

 Total Expenses by Category:
 - Offers users insights into their spending patterns by displaying total expenses in different categories, facilitating better financial awareness.

 ![total expenses by category](assets/images/totelexpensesbycategory.png)

 View Total Amount Spent This Month:
 - The feature provides users with a comprehensive overview of their monthly spending, promotes financial awareness, and facilitates informed and timely decision-making.

![monthly spent](assets/images/totalspent.png)


 Set up Monthly Budget:
 - Users can set up a monthly budget for their expenses, contributing to financial planning, spending limits and tracking.

 ![set up monthly budget](assets/images/monthlybudget.png)


 View Monthly Budget Status:
 - The application calculates and displays the monthly budget left, total amount spent, and daily budget. It provides warnings for budget deficits and encourages users to stay within their budget.

 - Budget > Total Expenses

   ![budget higher than total expenses](assets/images/highbudgetstatus.png)

 - Budget < Total Expenses

   ![budget lower than total expenses](assets/images/lowbudgetstatus.png)


### Future Features

- Create an interactive budget planning tool that helps users allocate funds to various categories based on their priorities and financial goals.
- Allow multiple users (e.g., family members or partners) to collaborate on a shared budget. This can be particularly useful for households managing finances together.
- Set up alerts and notifications to inform users when they are approaching or exceeding budget limits. This proactive approach helps users stay on track with their financial goals.
- Provide visual analytics and insights into spending patterns over time. Graphs, charts, and reports can help users understand trends and make more informed financial decisions.
- Enable users to create custom budget categories based on their specific needs. This allows for a more personalized budgeting experience.


## Technologies

### Languages Used

 - [Python3](https://en.wikipedia.org/wiki/Python_(programming_language)) - Used for writing the Expense Tracker code.


### Frameworks, Libraries and Programs Used

- Libraries:
    - gspread - This library is used for accessing Google Sheets API. It allows you to interact with Google Sheets and perform operations such as reading and writing data.
    - calendar - This is a standard Python library for working with dates and calendars. Used in the app to get the number of days in the current month.
    - datetime - This is a standard Python library used for working with dates and times. Used in the app to get the current date and time.
    - google.oauth2.service_account - This library provides tools for working with Google service accounts. Used in the app to load Google Sheets credentials from a service account file.

- [CODEANYWHERE](https://codeanywhere.com/) - Used for writing the code, committing and push it to GitHub.
- [GITHUB](https://github.com/) - Used to store the project after finishing writing in Codeanywhere.
- [HEROKU](https://dashboard.heroku.com/) - Used to deploy the app.
- [ASCII ART](https://www.asciiart.eu/text-to-ascii-art) - Used to generate the title of the app "Expense Tracker"
- [LUCIDCHART](https://www.lucidchart.com/pages/) - Used the create the flowchart.
- SNIPPING TOOL - Used for screenshot and snipping.
- PAINT - Used to combine the snipped images   