import sqlite3
from uuid import uuid4


class VoteDB:
    def __init__(self):
        self.conn = sqlite3.connect('vote.db', check_same_thread=False)
        # เรียกใช้ function create table
        self.create_table()
    def create_table(self):
        #AUTOINCREMENT คือ add id auto
        create_topic_query = """
        CREATE TABLE IF NOT EXISTS Topics (
         id VARCHAR(64) primary key not null,
         name VARCHAR(50) not null   
        );"""
        create_vote_query = """
        CREATE TABLE IF NOT EXISTS Votes(
            id INT primary key not null AUTOINCREMENT,
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
    
    def get_topic(self,topic_id):
        """
        (
            [
                (vote_id, choice_name, choice_count)
            ]
            topic_name
        )
        """
        topic_name_query = """
        SELECT name FROM Topics
        WHERE Topics.id = ?
        """
        topic_name_result = self.conn.execute(topic_name_query, (topic_id,)).fetchone() # ('topic', ) ##fetchone แปลว่า ต้องการแค่ result เดียว
        topic_name = topic_name_result[0]
        query = """
        SELECT id, choice_name, choice_count
        FROM Votes v
        WHERE v.topic = ?
        """
        result = self.conn.execute(query,(topic_id,))
        ret = []
        for data in result:
            cid, cname, ccount = data
            ret.append((cid, cname, ccount))
        return ret,topic_name
    
    def add_choice(self, choice_name, topic_id):
        query = """
        INSERT INTO Votes (topic, choice_name, choice_count)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (topic_id,choice_name,0))
        self.conn.commit()