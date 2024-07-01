Note
By default, I have stopped the table migration from manage.py because I have already created a database and its tables. After running Docker, you need to go inside the MySQL Docker container and execute the queries from the provided queries file. Once this is done, you can use the APIs as intended.

To turn on migrations using Django commands, modify the Meta class of the model by setting the managed attribute to True.

python3
class YourModel(models.Model):
    # my models
    
    class Meta:
        managed = True  # Change this to True to enable migrations
