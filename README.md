# Cyber Security Base 2025 course project

Installation instructions:
1) Clone or download the reposity and change to `cmdb` directory 
2) It should not be necessary to run `pip install -r requirements.txt` if you have attended the course
3) Run `python manage.py makemigrations csbcp` and  `python manage.py migrate` to create database
4) Create admin with `python manage.py createsuperuser` if you want to validate FLAW 4: A5:2017-Broken Access Control 
5) Start the server with `python manage.py runserver`


### FLAW 1: CSRF
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/code/csbcp/templates/main.html

App’s html template `main.html` is using `get` instead of `post` and missing Django CSRF tag `{% csrf_token %}` which makes the application vulnerable to CSRF (Cross-Site Request Forgery) attacks. If a form is not protected from CSRF attack, an malicious website can execute javascript on victims browser. The malicious code can inpersonate as the victim on other site while utilizing victim’s session and send a form that has not been protected from CSRF attack. 
 
You can test this by starting a Django web server on `/csrf html` folder with `python3 -m http.server 9000` and starting web browser on http://localhost:9000/csrf.html . As the implementetion required for flaw 3 is not according to best practices, it is best to start course project server first.

Django has a built in protection against CSRF attacks for forms. Set  `{% csrf_token %}` tag on all forms and make sure that middleware `django.middleware.csrf.CsrfViewMiddleware`
 is included in `MIDDLEWARE` list on  `settings.py`. To fix the vulnerability remove commenting from line 19 of `main.html` and change form method from `get` to `post`  on row 17. You also need to modify views.py, for simplicity this is included in the fix for flaw 2 to keep fixes as simple as possible. 

Screenshot before: 
![flaw-1-before-1.png](/screenshots/flaw-1-before-1.png)
flaw-1-before-1.png, flaw-1-before-2.png

Screenshot after: flaw-1-after-1.png


### FLAW 2: A1:2017-Injection
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/code/csbcp/views.py

Django ORM (and most of sqlite sql operations) sanitate sql inputs automatically. One way to handle form unsecurely when using sqlite, is to use sqlite’s `executescript`
raw sql operation with f-string. When used, the application is vulbnerable to injections, including sql injection, in which the attacker can directly write to the database for example from a form. On the main view, you can make sql injection in the message form, for example with `hi'); INSERT INTO csbcp_message (user_id, content) VALUES (1, 'Injected message.'); --`

To fix implementation issues you need to remove the unhealthy raw sql operation from rows 61 - 75 and to remove commenting from rows 56 -60 on `views.py`  to enable code that utilizes Django ORM.

Screenshot before: flaw-2-before-1.png, flaw-2-before-2.png

Screenshot after: flaw-2-after-1.png


### FLAW 3: A2:2017-Broken Authentication
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/code/csbcp/settings.py#L120

The application uses a custom session engine that sets the session id to be `session-<user id>`. (The implementation using thread local data is not a recommended pattern for production use either.) This vulnerability makes authentication very unsecure as attacker can easily go through possible session ids, starting from attacker’s id and proceeding to one.

Removing `SESSION_ENGINE` setting from line 120 of `settings.py` fixes the vulnerability as it returns Django to use default session engine that handles session id more securely. Also `views.py` would benefit from refactoring by removing the useless import and call for `setUser_id()`  and that the now useless `threadVariable.py` & `userSession.py` could be deleted. 

Screenshot before: flaw-3-before-1.png

Screenshot after: flaw-3-after-1.png

It can also be argued, that the login and signup implementations are insecure. For example signup does not enforce safe password use. Best practice is to use Django default functionalities if you are not very experienced in creating custom login.

### FLAW 4: A5:2017-Broken Access Control
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/code/csbcp/views.py

The admin view is hidden from navigation if the user is not an admin. However user can access it from url `admin/` to see admin view content.

Naive fix for the issue is to redirect non-admin users to another page and not render the admin page for them. Remove commenting in lines 89 - 90 of `views.py` in order to have normal users redirected to `main/` when they try to access `admin/`.

Screenshot before: flaw-4-before-1.png

Screenshot after: flaw-4-after-1.png


### FLAW 5: A6:2017-Security Misconfiguration
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/code/csbcp/settings.py
https://github.com/juhoaj/cybersecuritybasecourseproject/blob/main/.gitignore#L213

There are two key misconfigurations:

**5.1** The first one is that `SECRET_KEY`  is visible on row 11 of `settings.py` . Secrets should never be set on files that are not in `.gitignore`. Otherwise secrets can be pushed to reposity and this creates a new attack vector for leaking secrets, even in the case that the reposity is not public.  

This is fixed by moving the secrets to another file that is not pushed to reposity. The proposed fix is to first remove line 11 with the secret and remove commenting on lines 15 – 19 of `settings.py` which loads the secrets from another file. (`secrets.json` file allready exists.) 

In a real life situation it would be necessary to remove `secrets.json` from reposity and prevent it’s future commits. First by commenting on line 213 of `.gitignore` and running `git rm --cached secrets.json` and `git commit -m "Removed secrets from repo, d'oh!”` to remove `secrets.json` from the current commit and to prevent future commits. After this you would need to run your favourite destructive workflow for deleting previous commits of `secrets.json`, for example with `git-filter-repo`.

screenshot before: flaw-5.1-before-1.png

screenshot after: flaw-5.1-after-1.png

**5.2** Second misconfiguration is on row 21 of `settings.py`. Debug state is left on with `DEBUG = True`. This allows the user to gain insightful information on app’s inner working in the case of errors. It is extremelty useful when exploiting other vulnerabilities. For example making a sql injection (FLAW 1: A1:2017-Injection) becomes much easier as the attacker gets helpful error messages if the attack is not successfull.

This is fixed by either deploying the project or changing settings manually. For review purposes, please do this manually and change `True` to `False` on line 21 of `settings.py.`

screenshot before: flaw-5.2-before-1.png, flaw-5.2-before-2.png

screenshot after: flaw-5.2-after-1.png