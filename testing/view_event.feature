Feature: View event

    As a user, I want to be able to view the events I'm attending and events I created

    Scenario: User is on homepage
        Given that a user is on the homepage
        And an event is listed
        When the user clicks on the name of that event
        Then the detailed event information is displayed on a separate page
