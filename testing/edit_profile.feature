Feature: Edit profile

    As a user, I want to be able to edit my profile

    Scenario: User is on their own profile page
        Given that a user is on their own profile page
        When the user clicks on the Edit profile button
        Then user can see the prefilled profile fields
        And be able to change those profile fields
        When the user clicks on Submit
        And there are no errors
        Then the edits to the profile should be saved
        And the user will be redirected to view profile page with the new edits displayed
