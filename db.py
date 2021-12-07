import sqlite3
from uuid import uuid4


class VoteDB:
    def __init__(self):
        self.conn = sqlite3.connect('vote.db', check_same_thread=False)
        # เรียกใช้ function create table
        self.create_table()
    def create_table(self):
        create_topic_query = """
        CREATE TABLE IF NOT EXISTS Topics (
         id VARCHAR(64) primary key not null,
         name VARCHAR(50) not null   
        );"""
        create_vote_query = """
        CREATE TABLE IF NOT EXISTS Votes(
            id VARCHAR(64) primary key not null,
            topic VARCHAR(64),
            choice_name VARCHAR(50),
            choice_count INT,
            FOREIGN KEY (topic) REFERENCES Topics(id)
        )
        """
        # สั่งสร้าง TABLE
        self.conn.execute(create_topic_query)
        self.conn.execute(create_vote_query)
        
        # save database
        self.conn.commit()
    # ?, ? ป้องกันการโดน hack หรือ sql injection
    def add_topic(self, topic_name):
        topic_id = str(uuid4())
        query = """
        INSERT INTO Topics (
            id, name
        ) VALUES (
            ?, ? 
        )"""
        self.conn.execute(query,(topic_id,topic_name)) # เอา topic_id,topic_name ไปแทนที่ ?,?
        self.conn.commit()
        
    def get_topic_names(self):
        """
        [
            {
                "topic_id": str,
                "topic_name": str
            }
        ]
        """
        
        query="""
        SELECT * FROM Topics
        """
        result = self.conn.execute(query)
        ret = []
        for data in result:
            print(data)
            ret.append({
                "topic_id": data[0],
                "topic_name": data[1]
            })
        return ret