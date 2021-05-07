Feature: Sign out

    As a user, I want to be able to sign out of my account

    Scenario: User is signed in
        Given that a user is signed in
        And is on any page of the website
        When the user clicks the Sign Out button
        Then the user signed out of the account
        And redirected to the login screen