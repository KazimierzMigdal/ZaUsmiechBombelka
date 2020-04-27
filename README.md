# ZaUsmiechBombelka
ZaUsmiechBombekla - contains source files of the authored project written in Django. After creating an account on the portal, 
users can publish pictures of products (in this case children's clothes), browse products published by others and contact each
other to buy/sell them.   

The project also includes a blog section and a user activity tracking system.

## Inicialization:
**ZaUsmiechBombelka** uses Python programming language, its Django framework, RDBMS SQLite3 and remote dictionary server Redis. To run the project locally:

**1.** Install [Python](https://www.python.org/downloads/)

**2.** Install [PIP](https://bootstrap.pypa.io/get-pip.py)

**3.** Install [Redis](https://redis.io/download)

**4.** Clone this repository: 
```
git clone https://github.com/KazimierzMigdal/ZaUsmiechBombelka.git
```

**6.** Create virtual environment, activate it and install install packages from the requirements.txt:
```
pip install -r requirements.txt
```

**7.** Run redis-server on default (6379) port

**8** Go to main directory and run server by typing
```
python manage.py runserver
```
The **ZaUsmiechBombelka** is available at the address http://127.0.0.1

## Superuser:
Super User is already created.

**Login:** admin

**Password:** Adminpassword123
