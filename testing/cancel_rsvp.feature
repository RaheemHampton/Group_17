Feature: Cancel RSVP

    As a user, I want to be able to cancel an event I RSVP'd to

    Scenario: User is on event page for event they are atteending
        Given that a has already RSVP'd to an event
        And the user is on the event page of that event
        When the user clicks on the Cancel RSVP button
        The RSVP should be deleted from the database
        And the user is directed back to homepage