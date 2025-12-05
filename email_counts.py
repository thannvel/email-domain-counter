# import libraries
import sqlite3
import re

# create a connection to the database (the database will be created if it doesn't already exist)
conn = sqlite3.connect("email_counts.sqlite")
cur = conn.cursor()  # this cursor is our manipulation lever in the database

# create the 'Counts' table within the database
cur.execute('CREATE TABLE IF NOT EXISTS Counts (org TEXT, count INTEGER)')

# open and read the 'mbox.txt' file
with open("mbox.txt", "r") as f:
    for line in f:
        if line.startswith("From "):
            email = re.findall("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+", line)  # use regex pattern to extract email address
            if email:
                domain = email[0].split("@")[1]  # extract domain part of the email
                cur.execute('SELECT count FROM Counts WHERE org = ? ', (domain,))  # check if domain is already in the database
                row = cur.fetchone()
                if row is None:
                    cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (domain,))  # if domain doesn't exist, insert a new row
                else:
                    cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))  # if domain exists, update the count

    conn.commit()  # save all changes made to the database

# display top 10 domains by email count
cur.execute('SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10')
for row in cur:
    print(f"{row[0]}: {row[1]}")

# close database connection
conn.close()
