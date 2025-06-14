# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
                  host = 'localhost',
                  user = 'root',
                  password = '', #add your password here if youhave one set
                  database = 'books'
        )
        
        self.cur = self.conn.cursor()

        self.cur.execute("""
          Table(
    id int NOT NULL auto_increment  
Price           DECIMAL,    
Description     Text,       
Category        VARCHAR,    
SKU             VARCHAR,    
Stock Quantity  Integer,    
Discount        DECIMAL,    
Tax Rate        DECIMAL,    
Image URL       VARCHAR,    
Review Count    Integer,    
Average Rating  DECIMAL,    
Weight          DECIMAL,    
Dimensions      VARCHAR,    
Brand           VARCHAR,    
Color           VARCHAR,    
Material        VARCHAR,    
Release Date    Date,       
Manufacturer    VARCHAR,    
Shipping Cost   DECIMAL,    
Availability    INTEGER,
   )                                            
     """)                    