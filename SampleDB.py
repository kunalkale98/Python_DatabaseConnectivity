'''
Author: Kunal Kale
Date: 15-04-2021
Description: Program to connect to MySQL database and Perform CRUD operation on it
'''

import mysql.connector
import logs

#Function to Connect to the database
def mysqlconnect():
    try:
        mysqldb=mysql.connector.connect(host="localhost",user="root",password="kunal@123",database="payroll_service")
        logger.info("Database Successfully Connected")
    except Exception:
        logger.error("Can't Connect")
    else:
        return mysqldb
        
#Function to Display Table
def display():
    mysqldb = mysqlconnect()
    mycursor=mysqldb.cursor()
    sql_query = "SELECT * FROM employee_payroll"
    try:  
        mycursor.execute(sql_query)
        result=mycursor.fetchall()   
        for i in result:    
            emp_id=i[0]  
            name=i[1]  
            salary=i[2]
            start_date=i[3]
            gender=i[4]  
            logger.info(f"id:{emp_id},name:{name},salary:{salary},start_date:{start_date},gender:{gender}")  
    except Exception:   
        logger.error('Error:Unable to fetch data.')  
    mysqldb.close()

#Function to Update Data
def updatadata():
    mysqldb = mysqlconnect()
    mycursor=mysqldb.cursor()
    sql_query1 = "UPDATE employee_payroll SET salary=30000 WHERE name='James'"
    sql_query2 = "SELECT * FROM employee_payroll WHERE name='James'" 
    try:  
        mycursor.execute(sql_query1)
        mysqldb.commit()
        logger.info('Record Updated successfully')   
    except Exception: 
        logger.error("Error! unable to update data")    
        mysqldb.rollback()  
    mysqldb.close()

#Function to Delete Data
def deletedata():
    mysqldb = mysqlconnect()
    mycursor = mysqldb.cursor()
    sql_query = "DELETE FROM employee_payroll WHERE name='Olivia'"
    try:   
        mycursor.execute(sql_query)
        mysqldb.commit()
        logger.info('Record Deteted Successfully')  
    except Exception:
        logger.error("Error! unable to update data")  
        mysqldb.rollback()  
    mysqldb.close()

#Driver Function
if __name__=="__main__":
    logger = logs.set_logger()
    display()
    updatadata()
    deletedata()
    display()