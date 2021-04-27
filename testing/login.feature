Feature: Login

    As a user, I want to be to sign in to my account

    Scenario: User is on login page
        Given there are no other accounts logged in
        And a user is on the login page
        When the user enters their username and password
        And there are no errors
        Then the user should be redirected to the homepage
