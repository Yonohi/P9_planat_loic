# P9_planat_loic

## Description

Project Django whose purpose is to create a website where users can post requests or reviews on books they want to share. 

Users can subscribe or be followed by other users. It can be a nice platform for exchanging around books and perhaps allowing the discovery of new books.

***
## Requirements
Python 3 : https://www.python.org/downloads/
## Installation

In the terminal, move to the directory where you want to install the repository with the command line:
```
cd <pathdirectory>
```
Clone the remote repository:
```
git clone https://github.com/Yonohi/P9_planat_loic.git
```
Go into the new folder:
```
cd P9_planat_loic
```
Create the environment:
```
python3 -m venv env
```
Activate the environment:
On Unix and macOS:
```
source env/bin/activate
```
On Windows:
```
env\Scripts\activate.bat
```
Now, install packages from requirements.txt
```
pip install -r requirements.txt
```
Go into the folder named LITReview
```
cd LITReview
```
Run in local
```
python3 manage.py runserver
```
Now you can go to the address
```
http://127.0.0.1:8000/
```
## How it works
At this address you can register or log in. After that you access to the flux page where you see your posts, and the posts from users you follow. There are two buttons which allow respectively to create a ticket or a ticket and its review.  You can go to the post page where you will find your posts which can be modified or delete if you want it. There is also a page named 'abonnements' allowing to subscribe to the user you want and unsubscribe to users you want to stop following. You can log out at any time.
## Need a superuser?
You have to go to the project folder and type
```
python3 manage.py createsuperuser
```
Now give your username, mail and password, and it's done. The admin page is reachable.
```
http://127.0.0.1:8000/admin/
```
## Information about database
Go to the folder where you have your database and type
```
sqlite3 db.sqlite3
```
You can see all the tables with
```
.tables
```
To see the content of a table.
```
select * from <nametable>;
```
## Conclusion
It was an interesting project which make me think differently. I hope you will enjoy this creation.
## Author
Loïc Planat
