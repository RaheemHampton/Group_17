Feature: Register user

    As a user, I want to be able to create a profile so that I can add and view events

    Example: User is on create account page and account exists
        Given that there is no account currently logged in
        And a user is on the create account page
        When user enters in account information
        And clicks Submit
        Then error message 'Email already exists' displays

    Example: User is on create account page and account does not exist
        Given that there is no account currently logged in
        And a user is on the create account page
        When user enters in account information
        And clicks Submit
        And there are no input errors
        Then user is redirected to homepage with list of events

