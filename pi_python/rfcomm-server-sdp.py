import bluetooth
from bluetooth import *
import sqlite3 as sql

### Database Connection ###
con = sql.connect("alarms_database.db")
cur = con.cursor()

##wipe the db
cur.execute("DELETE FROM alarm_table")
con.commit()
###########################




def ReadAndStore():
    data = client_sock.recv(1024)
    data_string = data.decode('utf-8')
    data_string = data_string[:2] + ":" + data_string[2:]

    ####Database
    ##wipe the db
    cur.execute("DELETE FROM alarm_table")
    ##insert alarm into database ###
    ps = "INSERT INTO alarm_table (alarm_time) VALUES (?)" #prepared statement
    cur.execute(ps,(data_string,))
    con.commit()



###Server
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

#port = bluetooth.get_available_port( bluetooth.RFCOMM )
port = 1
server_sock.bind(("",port))
server_sock.listen(1)
print ("listening on port %d" % port)

uuid = "a60ddd90-0623-11ea-aaef-0800200c9a66"
bluetooth.advertise_service( server_sock, "FooBar Service", service_id=uuid, service_classes = [uuid, SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE] )

client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)
#

while(True):
    ReadAndStore()
#data = client_sock.recv(1024)
#print(data)
#print(data.decode('utf-8'))
#data_string = data.decode('utf-8')
#data_int = int(data_string)
#print(data_int)


####Database
##insert alarm into database ###
#ps = "INSERT INTO alarm_table (alarm_time) VALUES (?)" #prepared statement
#cur.execute(ps,(data_int,))
#con.commit()
################################






#client_sock.close()
#server_sock.close()
