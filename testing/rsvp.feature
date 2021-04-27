Feature: RSVP to an event

    As a user, I want to RSVP to an event that I would like to attend

    Scenario: User is on event page for event they would like to attend
        Given that a user is not the creator of an event
        And the user is on a view event page
        When the user clicks on the RSVP button
        Then the RSVP of the user should be saved