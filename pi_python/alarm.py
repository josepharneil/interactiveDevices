#!/usr/bin/env python

import schedule
import subprocess
import time
import simpleaudio as sa
import sqlite3 as sql

### database connection ###
con = sql.connect("alarms_database.db")
cur = con.cursor()
#############################

onBed = True

alarm_wave_obj = sa.WaveObject.from_wave_file("/home/pi/alarm.wav")
alarm_play_obj = alarm_wave_obj.play()
alarm_play_obj.stop()

def job():
    #if(onBed):
    alarm_play_obj = alarm_wave_obj.play()
    
    #while (currentTime - alarmTime < 30)
    while(True):
        #if onbed
        if(onBed):
            #play if not playing
            if(not alarm_play_obj.is_playing()):
                alarm_play_obj = alarm_wave_obj.play()
                print("alarm is ringing, please get up NOW")
        #if !onbed
        if(not onBed):
            if(alarm_play_obj.is_playing()):
                #stop
                alarm_play_obj.stop()
                print("alarm has stopped")
            
        #wait 1 second
        time.sleep(1)
    #subprocess.call(['aplay -l0 /home/pi/alarm.wav'], shell=True)

### get value from db ###
#cur.execute("SELECT alarm_time FROM alarm_table")
#time_string = (cur.fetchall())[0][0]
#print(time_string)

def GetDatabaseAlarmTime():
    #check if empty, and if it is return early with a special value
    cur.execute("SELECT alarm_time FROM alarm_table")
    fetched = cur.fetchall()
    if(fetched == []):
        return "empty"
    time_string = fetched[0][0]
    return time_string

#schedule.every().day.at(time_string).do(job)
#schedule.every().day.at('16:41').do(job)

localAlarmTime = ''
databaseAlarmTime = ''
while True:   
    #get database time
    databaseAlarmTime = GetDatabaseAlarmTime()
    
    #Validate database alarm time, and if not valid, dont check / change anything
    #todo
    
    #if its the local alarm time is different from the database alarm time
    if((localAlarmTime != databaseAlarmTime) and (databaseAlarmTime != "empty") ):
        #store database alarm time locally
        localAlarmTime = databaseAlarmTime
        #clear all jobs
        schedule.clear()#clear all jobs
        #create a new schedule at alarm time
        schedule.every().day.at(localAlarmTime).do(job)
        print("alarm set for ",localAlarmTime)

    #run pending schedule
    schedule.run_pending()
    
    #wait 1 second
    time.sleep(1)
    
    
    
    
#def job():
    #while (currentTime - alarmTime < 30)
        #if onbed
            #play if not playing
        #if !onbed
            #stop
        #wait 1 second
