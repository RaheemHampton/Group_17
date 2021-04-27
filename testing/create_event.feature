Feature: Create event

    As a user, I want to be able to create an event.

    Scenario: User is on homepage
        Given that a user is on the homepage
        When a user clicks on the Create Event button
        Then the user should be redirected to separate page to enter event information
        When a user clicks on Submit
        And there are no errors
        Then the created event should be saved
        And the user redirected to homepage to see new event in table
