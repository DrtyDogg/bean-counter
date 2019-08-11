Budget
============

Description
------------

This is used for our home budgeting needs.  I created it because most budgeting applications are overly automated.  While using them I find myself not paying much attention because they handle almost everything for me.  So this was created to allow us to track the spending categories that I care about.  Manually entering in the data forces me to interact with the tool and is keeping me engaged in my budget.

Requirments
-------------

- Keep track of our spending
- Support multiple categories
- Easily add new transactions
- Allow for secure login
- Pretty graphs
- Email alerts

Requirements
------------

- Python 3.7

Getting started
------------

```` bash
git clone https://github.com/DrtyDogg/bean-counter.git
cd bean-counter
python -m venv venv
source venv/bin/activate
pip -r requirments.txt
flask run
````
The virtual environment isn't required but strongly suggested

Environment Variables
------------
- ADMIN_USERNAME *optional* The username for the administrator account.  Default: **admin**
- ADMIN_PASSWORD *optional*The password for the administrator account. Default: **admin1234**
- ADMIN_EMAIL *optional* The email address for the administrator account. Default: **admin@admin.adm**
- LOG_DIR *optional* The log directory Default: **logs**
- CONTEXT_ROUTE *optional* If you host proxy the site behind a context route specify that route here.
- DATABASE_URL *optional* Where the database is located.  Default: **app.db**
- SECRET_KEY *change this* The key used for password hashing. Default: **My-default-key**

Releases
------------
v1.0 7/19/2019
