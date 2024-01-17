Here i will explain the structure of the code and how to implement it using python and mysql.

1.  create a new database in mysql , 
    you can use workbench for it or you can create a new database from cmd commands.

2.  connect python file to the database using attributes such as 
    user name , 
    host name ,
    password ,
     database name.

3.  import cryptography library from  fernet .

4.  create a function that creates a new table in database.

5.  Generate key using fernet , intialize it and store it into an ecryption_key.key file to 
    refetch the encryption key to decrypt the encrypted_password while retriving the password.

6.  create functions such as add password, get password encrypt and decrypt password using fernet.

7.  in main function generate the key and intialize it and create a switch case for user to choose to 
    add password, get password depending upon users choice.

8.  in add password function: insert the website name,
    username,
    password and encrypt the password using fernet.

9.  in get password function: insert the website name and username,
    to select the row from where to fetch the encrypted code stored in the database,
    after successful fetching the code decrypt it and return the actual password.

10.  and at last close the connection and cursor. 

??