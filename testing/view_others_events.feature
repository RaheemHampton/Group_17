Feature: View events that users have created and RSVP'd to on their profile

    As a user, I want to be able to see the events that other users have created and RSVP'd to

    Scenario: User is on a profile of another user who has created events and RSVP'd to events
        Given that a user is on the profile of another user
        And that other user has created and RSVP'd to events
        Then the user will see 2 tables
        And the left table will contain events the viewed user created
        And the right table will contain events the viewed user RSVP'd to and created
