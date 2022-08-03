# capstone-project-3900-t11b-3-5
## Pre-Installation Checklist
|         Requirement       |Description                                                          |
|---------------------------|---------------------------------------------------------------------|
|Python                     |3.8.10, (versions 3.9.X+ is recommended)                             |
|Python3-venv               |same version as your Python                                          |
> **Note**:  We have not tested on Python 3.10+
### If you do not have python 3.9.X, I recommend following these:
**For Linux systems:**

[How To Install Python 3.9](https://tecadmin.net/how-to-install-python-3-9-on-ubuntu-18-04/)

**For Windows or Mac:**

> **Note**: Use the respective download links for your operating system.

[Download Python 3.9](https://www.python.org/downloads/release/python-390/)
## Setup

Firstly, clone the repository and change to project directory:
```console
$ git clone git@github.com:unsw-cse-comp3900-9900-22T2/capstone-project-3900-t11b-3-5.git
$ cd capstone-project-3900-t11b-3-5/task_planner_app/
```
Create a virtual environment to install project dependencies and activate it:
> **Note**: Make sure you are in the directory "capstone-project-3900-t11b-3-5/task_planner_app/"

```console
$ python3 -m venv .env 
$ source .env/bin/activate
```
You should now see a **(.env)** in front of your console path e.g.:
```console
(.env) ~/capstone-project-3900-t11b-3-5/task_planner_app$
```
Install the project dependencies:
```console
(.env) $ pip3 install -r requirements/requirements.txt
```
Once **pip3** has finished installing, setup the app database and run the server:
```console
(.env) $ python3 manage.py migrate
(.env) $ python3 manage.py loaddata fixtures/tags.json 
(.env) $ python3 manage.py runserver 
```
You should be able to access the app now on:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Virtual Environment Errors and How To Fix
#### If you encounter the following error with "ensurepip":
```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.9-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: ['/home/nguyen/capstone-project-3900-t11b-3-5/task_planner_app/.env/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']
```
Then run the following:
```console
$ sudo apt install python3.9-venv
```
#### If you encounter an error related to "No such file or directory:" when trying to run "python3 -m venv .env ":

 1. Kill the current console instance.
 2. cd back to the project directory.
```console
$ cd capstone-project-3900-t11b-3-5/task_planner_app/
```
3. Try to create the virtual environment and activate it again.	
```console
$ python3 -m venv .env
$ source .env/bin/activate

