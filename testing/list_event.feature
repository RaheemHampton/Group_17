Feature: List event

    As a user, I want to see a list of created events

    Scenario: User is on homepage
        Given that a user is on the homepage
        And there have been events that have been created
        Then the user should see a list of created events