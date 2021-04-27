Feature: Edit event

    As a user, I want to be able to edit an event

    Scenario: Creator of event is on view event page
        Given that a user is the creator of an event
        And that user is on the view event page
        When the user clicks on the Edit button
        Then user can see the prefilled event fields
        And be able to change those event fields
        When the user clicks on Submit
        And there are no errors
        Then the edits to the event should be saved
        And the user will be redirected to view event page with edits displayed
