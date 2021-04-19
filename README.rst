##############################
Django Signup To Organizations
##############################

Django-signup-organization is a django app which allows Organizations to be created and gives
users the ability to join to an organization, the app handles sign up and authentication but
can be customised to suit your needs..

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Download the app and move to your django root folder Add "account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'account',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('account/', include('account.urls', namespace='account')),

3. Add AUTH_USER_MODEL = 'account.AccountUser' to settings file and
   set up your EMAIL configuration for sending mails in django. 
   NB: EMAIL_HOST_USER is responsible for sending
   the mail, so it must be set.

4. Add and variable DOMAIN_URL to your settings file Set it to the url of your site,

5. Run ``python manage.py migrate`` to create the account models.

6. Start the development server and visit http://127.0.0.1:8000/ as the prefix followed by
   the respective paths as staated in the remaining part of the readme
   


# Getting Started
- To create an Organization as an admin use the url::
    /account/signup 
this path will take you to a form which can be used to create a workplace as
an admin, an email will be sent to you for email authentication and account activitation.

- To sign in
    /account/login
Use your email and passowrd to sign in.

- To invite users to join your workplace  when logged in use the url path::
    /account/invite/users/<name_of_workplace>

This will display a form for you to input emails of users you want to invite to join
your organization, the emails must be separated by space.

- To join an organization
You can only join an organization when you are invited by email, of which you will click the link
and it will take you to a path with the name of the organization and your email like this::
    /account/signup/<name_of_workplace>/<your_email>
In the form you just need to fill in the requried details and set your password and it will activate
your account and redirect you to the log in page

### Check urls.py to see list of paths and the views to edit to your taste.
