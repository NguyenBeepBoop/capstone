# capstone-project-3900-t11b-3-5
# Table of Contents
1. [Pre-Installation Checklist](#checklist)
	1. [Linux python install](#linux)
	2. [Windows python install](#windows)
2. [Setup](#setup)
3. [Virtual Environment Errors and How To Fix](#errors)
4. [Using the App (Workflow and Use Cases)](#using-app)
	1. [Login and Register](#login-register)
	2. [Forgot your password?](#forgot-pass)
	3. [Your Profile](#login-register)
	4. [The Dashboard](#login-register)
	5. [Login and Register](#login-register)
	6. [Login and Register](#login-register)

## Pre-Installation Checklist <a name="checklist"></a>

|         Requirement       |Description                                                          |
|---------------------------|---------------------------------------------------------------------|
|Python                     |3.8.10, (versions 3.9.X+ is recommended)                             |
|Python3-venv               |same version as your Python                                          |
	> **Note**:  We have not tested on Python 3.10+

### If you do not have python 3.9.X, I recommend following these:

**For Linux systems:**  <a name="linux"></a>

[How To Install Python 3.9](https://tecadmin.net/how-to-install-python-3-9-on-ubuntu-18-04/)

**For Windows or Mac:** <a name="windows"></a>

> **Note**: Use the respective download links for your operating system.

[Download Python 3.9](https://www.python.org/downloads/release/python-390/)
## Setup <a name="setup"></a>

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
Once `**pip3**` has finished installing, setup the app database and run the server:
```console
(.env) $ python3 manage.py migrate
(.env) $ python3 manage.py loaddata fixtures/tags.json 
(.env) $ python3 manage.py runserver 
```
You should be able to access the app now on:
* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Virtual Environment Errors and How To Fix  <a name="errors"></a>
### If you encounter the following error with "ensurepip":
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
### If you encounter "No such file or directory:" when trying to run "python3 -m venv .env ":

 1. Kill the current console instance.
 2. cd back to the project directory.
```console
$ cd capstone-project-3900-t11b-3-5/task_planner_app/
```
3. Try to create the virtual environment and activate it again.	
```console
$ python3 -m venv .env
$ source .env/bin/activate
```
## Using the App (Workflow and Use Cases) <a name="using-app"></a>
### Register and Login <a name="login-register"></a>
#### Overview
Firstly, create an account to access the app:
* http://127.0.0.1:8000/accounts/register/
* Here you are required to enter in an email, username, first name, last name and password. 
* Your date of birth is completely optional and you may update this once logged into the system.
* Upon successful registration you will be logged into the app.

You may also access the app via the login page:
* http://127.0.0.1:8000/accounts/login/
* Enter your email and password to access the app.

### Forgot your password? <a name="forgot-pass"></a>
#### Overview
In the event that you have forgotten your password, it can be recovered through our password recovery:
* http://127.0.0.1:8000/accounts/reset_password/
* Enter your email into the form and submit a password reset request.
* You will then receive an email from our team within a couple of minutes.
	> **Note**: Please check your spam and junk email folders for the password recovery link.
	
* You may now reset the password via the link generated in the email.

### Your Profile  <a name="profile"></a>
#### Overview
 * http://127.0.0.1:8000/accounts/profile/
 * In your profile you may view and manage the details that you have provided about yourself. 
 * Here you will additionally see your assigned Proficiencies (skills), Workload, Capacity, and Profile Picture which has been generated by the system.
	#### Editing your profile
	* http://127.0.0.1:8000/accounts/profile_edit/
	
	You may edit details about yourself including:
	 * Email
	 * Username
	 * First Name
	 * Last Name
	 * Capacity (amount of workload you are willing to take)
	 * Proficiencies
	 * Profile Picture

### Notifications <a name="notifications"></a>
#### Overview
Notifications have been created for users to easily access and respond to relevant notifications from both Users and TaskGroups. You can access and manage your notifications via the bell icon on the top right of the navbar.
Some core functionalities in our app that leverages this system includes:
1. Task Group Notification Broadcasts
2. Task Group Membership Notifications
	* Invitations of Members to Task Groups
	* Promotion of Members
	* Demotion of Members
	* Kicking of Members
3. User connections invitations

### The Dashboard <a name="dashboard"></a>
#### Overview
The Dashboard has been designed with purpose to maximise your productivity only showing relevant information such as your assigned Task(s) and TaskGroup(s). You will find core features and functionalities required for tasking including:
1. Task List View (Including filters and sorting.)
2. Integrated Task Support System
3. Dependent Workflows (Task Dependencies and Links.)
4. Task Reporting Generation
5. Task Group List View (Including filters and sorting.)
6. Task Group Creation, Deletion and Access

#### Viewing Tasks in the Dashboard
* http://127.0.0.1:8000/dashboard/
	> **Note**:  See [How to Create a Task](task-create) to create a task.

Your assigned tasks can be easily viewed and accessed via the "My Tasks" tab on the Dashboard view of our app. Here you will be able to see core information about your assigned tasks including:
* Name
	* Tasks that have links will show a chain icon in front of the task name.
* Task Group
* Task List (The list in which the task is grouped under in a group.)
* Due Date
* Priority 
* Status
	> **Note**:  You may also edit your tasks details by clicking on the pen icon in the action column of the table. 
	
To see a more detailed view of your task click on the task in the table. This will open a pop up window which displays more details about your task including:
* Task Estimation Points
* Task Description
* Links Related Tasks:
	* Parent Tasks
	* Child Tasks
* Task Comments
* Task Help Results 
#### Viewing Groups in the Dashboard
* http://127.0.0.1:8000/groups/

### How to Create a Task <a name="task-create"></a>
To create a task, you would firstly need to 
