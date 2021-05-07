Feature: Upload a picture to a profile

    As a user, I want to be able to attach a picture to my profile

    Scenario: User is on the registration page
        Given that a user is creating their account
        When the user clicks on the Choose File button
        Then the user sees file explorer window
        And the user can select a picture
        When the user clicks Open
        And the picture is a png/jpg
        Then the picture will be uploaded
        When the user clicks submit
        Then the picture will be saved to profile