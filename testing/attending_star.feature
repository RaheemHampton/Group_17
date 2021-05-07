Feature: Attending star

    As a user, I want a star to appear next to events that I have RSVP'd to or have created

    Scenario: User is on the homepage
        Given that a user is on the homepage
        When the user RSVP's to and creates events
        Then the user should see a star next to the events they have created or RSVP'd to