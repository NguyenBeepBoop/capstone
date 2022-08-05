
# Capstone-Project-3900-t11b-3-5

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
   7. [

## Pre-Installation Checklist <a name="checklist"></a>

| Requirement  | Description                              |
| ------------ | ---------------------------------------- |
| Python       | 3.8.10, (versions 3.9.X+ is recommended) |
| Python3-venv | same version as your Python              |

> **Note**:  We have not tested on Python 3.10+

### If you do not have python 3.9.X, I recommend following these

**For Linux systems:**  <a name="linux"></a>

[How To Install Python 3.9](https://tecadmin.net/how-to-install-python-3-9-on-ubuntu-18-04/)

**For Windows or Mac:** <a name="windows"></a>

[Download Python 3.9](https://www.python.org/downloads/release/python-390/)

> **Note**: Use the respective download links for your operating system.

## Setup <a name="setup"></a>

Firstly, clone the repository and change to project directory:

```bash
git clone git@github.com:unsw-cse-comp3900-9900-22T2/capstone-project-3900-t11b-3-5.git
cd capstone-project-3900-t11b-3-5/task_planner_app/
```

Create a virtual environment to install project dependencies and activate it:
> **Note**: Make sure you are in the directory "capstone-project-3900-t11b-3-5/task_planner_app/"

```bash
python3 -m venv .env 
source .env/bin/activate
```

You should now see a `(.env)` in front of your console path e.g.:

```bash
(.env) ~/capstone-project-3900-t11b-3-5/task_planner_app$
```

Install the project dependencies:

```bash
(.env) $ pip3 install -r requirements/requirements.txt
```

Once `pip3` has finished installing, setup the app database and run the server:

```bash
(.env) $ python3 manage.py migrate
(.env) $ python3 manage.py loaddata fixtures/tags.json 
(.env) $ python3 manage.py runserver 
```

You should be able to access the app now on:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Virtual Environment Errors and How To Fix  <a name="errors"></a>

### If you encounter the following error with "ensurepip"

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

```bash
sudo apt install python3.9-venv
```

### If you encounter "No such file or directory:" when trying to run "python3 -m venv .env "

 1. Kill the current console instance.
 2. cd back to the project directory.

```bash
cd capstone-project-3900-t11b-3-5/task_planner_app/
```

3. Try to create the virtual environment and activate it again.

```bash
python3 -m venv .env
source .env/bin/activate
```

## Using the App (Workflow and Use Cases) <a name="using-app"></a>

### Register and Login <a name="login-register"></a>

Firstly, create an account to access the app:

* <http://127.0.0.1:8000/accounts/register/>
* Here you are required to enter in an email, username, first name, last name and password.
* Your date of birth is completely optional and you may update this once logged into the system.
* Upon successful registration you will be logged into the app.

You may also access the app via the login page:

* <http://127.0.0.1:8000/accounts/login/>
* Enter your email and password to access the app.

#### Register and Sign Up Views

![Register View](images/register.png)
![Login View](images/login.png)

### Forgot your password? <a name="forgot-pass"></a>

In the event that you have forgotten your password, it can be recovered through our password recovery:

* <http://127.0.0.1:8000/accounts/reset_password/>
* Enter your email into the form and submit a password reset request.
* You will then receive an email from our team within a couple of minutes.

 > **Note**: Please check your spam and junk email folders for the password recovery link.

* You may now reset the password via the link generated in the email.

#### Forgot Password View

![Forgot Password View](images/forgot_password.png)

### Your Profile  <a name="profile"></a>

* <http://127.0.0.1:8000/accounts/profile/>
* In your profile you may view and manage the details that you have provided about yourself.
* Here you will additionally see your assigned Proficiencies (skills), Workload, Capacity, and Profile Picture which has been generated by the system.

![Profile View](images/profile.png)
#### Editing your profile

* <http://127.0.0.1:8000/accounts/profile_edit/>

 You may edit details about yourself including:

* Email
* Username
* First Name
* Last Name
* Capacity (amount of workload you are willing to take)
* Proficiencies
* Profile Picture

![Edit Profile](images/edit_profile.png)
### Notifications <a name="notifications"></a>

Notifications have been created for users to easily access and respond to relevant notifications from both Users and TaskGroups. You can access and manage your notifications via the bell icon on the top right of the navbar.
Some core functionalities in our app that leverages this system includes:

1. Task Group Notification Broadcasts'

![Notification Broadcast](images/notification_broadcast.png)

2. Task Group Membership Notifications

* Invitations of Members to Task Groups
* Promotion of Members
* Demotion of Members
* Kicking of Members

![Membership Notification](images/membership_notification.png)

3. User connections invitations

![User Connection Notification](images/user_connection_notification.png)


### The Dashboard <a name="dashboard"></a>

The Dashboard has been designed with purpose to maximise your productivity only showing relevant information such as your assigned Task(s) and TaskGroup(s). You will find core features and functionalities required for tasking including:

1. Task List View (Including filters and sorting.)
2. Integrated Task Support System
3. Dependent Workflows (Task Dependencies and Links.)
4. Task Reporting Generation
5. Task Group List View (Including filters and sorting.)
6. Task Group Creation, Deletion and Access

#### Viewing Tasks in the Dashboard

* <http://127.0.0.1:8000/dashboard/>

 > **Note**:  See [How to Create a Task](#task-create) to create a task.

Your assigned tasks can be easily viewed and accessed via the "My Tasks" tab on the Dashboard view of our app. Here you will be able to see core information about your assigned tasks including:

* Name
  * Tasks that have links will show a chain icon in front of the task name.
* Task Group
* Task List (The list in which the task is grouped under in a group.)
* Due Date
* Priority
* Status

![Dashboard Tasks View](images/dashboard.png)

 > **Note**:  You may also edit your tasks details by clicking on the pen icon in the action column of the table.

To see a more detailed view of your task click on the task in the table. This will open a pop up window which displays more details about your task including:

* Task Estimation Points
* Task Description
* Links Related Tasks:
  * Parent Tasks
  * Child Tasks
* Task Comments
* Task Help Results

![Dashboard Tasks Detailed View](images/task_support_comments_and_dependency.png)

#### Viewing Groups in the Dashboard

* <http://127.0.0.1:8000/groups/>

You can easily access the Task Groups you are a member in via the "My Groups" tab on the Dashboard view of the app.
Here you can view core information about the groups including:
* Group Name
* Group Description
* Date Joined

![Dashboard Groups View](images/dashboard_group_view.png)

> **Note**: You may also view more details of the group, and to delete or leave a group depending on your permissions, through the action column of the table.

### How to Create a Task <a name="task-create"></a>

1. Create a Task Group by navigating to the Dashboard and clicking "Create Group".
    * A modal form will then be presented, where you can enter in a Name(required) and Description for your Task Group.

![Create Group Modal](images/create_group.png)

2. Create a Task List for your Tasks:
    * Enter in details for your Task List.

![Create List](images/create_list.png)

3. Create a Task, providing the following information:
	* Name
	* Description
	* Deadline
	* Status
	* Priority
	* Assignee
	* Task Estimation Points
	* Related Tasks
	* Related Tags

#### How to Edit a Task <a name="task-edit"></a>
Editing a task can be completed by either clicking on the edit button found in the Dashboard - My Tasks page, or by clicking on the existing task in the Tasks page.

On this Edit page, users can edit any field in the task model, whilst also having access to the Assignee Recommendation and Comment sections.

![Edit Task](images/edit_task.png)

### Task Groups
As an owner of a Task Group, you have the ability to manage the roles of other members in the group.

After accessing a particular group, there will be a sidebar which allows users with certain permissions to:
1. <a name="notifications">Broadcast Notifications (Moderators only)</a>
2. Manage Members (Moderators only) 
3. Manage Task List (All Members)
	* View a list of Task Lists in the Task Group.
4. Create Task List (All Members)
5.  Manage Group (Moderators only)
	* Can edit Task Group fields and select which users will remain as members.
6. Leave Group (All Members)
7. Delete Group (Owner only)

![Manage Members](images/member_management.png)

### Friends
#### Sending Friend Requests
Users can access the profile of other users. This will provide the same <a name="profile">profile view</a> illustrated previously, however, will include the ability to send a friend request. If a request is already pending, the button will be replaced to say 'Cancel Friend Request'. 

#### Viewing User Friends
Once a friendship has been established, you are given permission to view which users are friends with the profile you are viewing.
