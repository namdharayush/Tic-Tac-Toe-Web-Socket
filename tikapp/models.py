from django.db import models

class TicTacToe(models.Model):
    room_code = models.CharField(max_length=20)
    move =  models.CharField(max_length=20)
    total_connection = models.IntegerField()
    create_user = models.CharField(max_length=50)
    join_user = models.CharField(max_length=50)

    
    def __str__(self):
        return self.room_code