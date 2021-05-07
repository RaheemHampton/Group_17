Feature: View profile

    As a user, I want to be able to view a profile

    Scenario: User is on homepage
        Given that a user is on the homepage
        And the user's name at the top is clicked
        Or the name of an event creator in the event table is clicked
        Then user is redirected to the profile of the user they clicked on
