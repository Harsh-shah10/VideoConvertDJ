Note : By default, I have stopped the table migration from manage.py because I have already created a database and its tables. After running Docker, you need to go inside the MySQL Docker container and execute the queries from the provided queries file. Once this is done, you can use the APIs as intended. To turn off automatic migrations and use normal migrations, modify the Meta class of the model by setting the managed attribute to False.

