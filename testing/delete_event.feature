Feature: Delete event

    As a user, I want to be able to delete an event

    Scenario: User is the creator of an event
        Given that a user is the creator of an event
        And is on the edit event page
        When the user clicks on Delete Event
        Then the event should be deleted
        And the user redirected to the homepage to notice the deleted event is gone