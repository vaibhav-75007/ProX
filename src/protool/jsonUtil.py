'''
This file is part of ProX.

ProX is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ProX is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ProX.  If not, see <https://www.gnu.org/licenses/>
'''

import json
import flashcard_class as flash
import Task as task
import user_class as user
import curriculum
import datetime
import requests
import copy

def stringToDatetime(string):
    splitDate = string.split('/')
    return datetime.datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2][0:2]))

def readAll():
    dictionary = 0
    with open("data.json",'r') as file: #create case if no flashcards, no tasks
        fileContents = file.read()
        listItem = json.loads(fileContents)
    dictionary = listItem[0]
    dictionary1 = listItem[1]

    user.user = user.User(dictionary["name"],dictionary["productivity_score"],dictionary["task_completion_rate"],dictionary["missed_deadline"],dictionary["weekly_productivity_score"],dictionary["weekly_task_completion_rate"],dictionary["weekly_deadlines_missed"],dictionary["id"],dictionary["email"],dictionary["pin"])
    user.offlineUser = user.User(dictionary1["name"],dictionary1["productivity_score"],dictionary1["task_completion_rate"],dictionary1["missed_deadline"],dictionary1["weekly_productivity_score"],dictionary1["weekly_task_completion_rate"],dictionary1["weekly_deadlines_missed"],dictionary1["id"],dictionary1["email"],dictionary1["pin"])

    if len(dictionary["tasks"]) == 0:
        task.tasks = []
    if len(dictionary1["tasks"]) == 0:
        task.offlineTasks = []
    else:
        task.tasks = [task.Task(name=tempDict["name"],description=tempDict["description"],deadline=stringToDatetime(tempDict["deadline"])) for tempDict in dictionary["tasks"]]
        task.offlineTasks = [task.Task(name=tempDict["name"],description=tempDict["description"],deadline=stringToDatetime(tempDict["deadline"])) for tempDict in dictionary1["tasks"]]

    if len(dictionary["flashcards"]) == 0:
        flash.flashcards = []
    if len(dictionary1["flashcards"]) == 0:
        flash.offlineFlashcards = []
    else:
        flash.flashcards = [flash.FlashCard(tempDict["subject"],tempDict["front_text"],tempDict["back_text"]) for tempDict in dictionary["flashcards"]]
        flash.offlineFlashcards = [flash.FlashCard(tempDict["subject"],tempDict["front_text"],tempDict["back_text"]) for tempDict in dictionary1["flashcards"]]

    if len(dictionary["curriculums"]) == 0:
        curriculum.curriculums = []
    if len(dictionary1["curriculums"]) == 0:
        curriculum.offlineCurriculums = []
    else:
        curriculum.curriculums = [curriculum.Curriculum(tempDict["name"],tempDict["subject"],tempDict["topics"]) for tempDict in dictionary["curriculums"]]
        curriculum.offlineCurriculums = [curriculum.Curriculum(tempDict["name"],tempDict["subject"],tempDict["topics"]) for tempDict in dictionary1["curriculums"]]

def writeAll(user,offlineUser1,curriculums,offlineCurriculums1,tasks,offlineTasks1,flashcards,offlineFlashcards1):
    jsonString = toJson(user,curriculums,tasks,flashcards)
    print(offlineTasks1)
    print(offlineCurriculums1)
    offlineJsonString = toJson(offlineUser1,offlineCurriculums1,offlineTasks1,offlineFlashcards1)

    print(offlineJsonString)

    try:
        if requests.get('http://15.237.110.189:5000/').status_code == 200:
            print("merging")
            mergeChanges(jsonString,offlineJsonString)
        else:
            with open("data.json",'wt') as file:
                file.write(json.dumps([jsonString,offlineJsonString]))

    except requests.exceptions.ConnectionError:
        writeOfflineChanges(jsonString,offlineJsonString)
    
    writeDateLastOn()

def writeOfflineChanges(jsonString,offlineJsonString):
    with open("data.json",'wt') as file:
        file.write(json.dumps([jsonString,offlineJsonString]))


def mergeChanges(jsonString,offlineJsonString):
    r = requests.get('http://15.237.110.189:5000/' + str(jsonString["id"]) + '/' + str(jsonString["pin"]) + '/')
    dbJsonString = r.json()
    print(dbJsonString)
    print("offline curriculums")
    print(offlineJsonString["curriculums"])
    print('\n\n\n')
    #all changes happen to offline user, when a request is made it goes through mergeChanges function rather than writeAll now

    if True:
        score = offlineJsonString["task_completion_rate"] - jsonString["task_completion_rate"]
        missed = offlineJsonString["missed_deadline"] - jsonString["missed_deadline"]

        offlineTasks = offlineJsonString["tasks"]
        offlineFlashcards = offlineJsonString["flashcards"]
        offlineCurriculums = offlineJsonString["curriculums"]
        dbTasks = dbJsonString["tasks"]
        dbFlashcards = dbJsonString["flashcards"]
        dbCurriculums = dbJsonString["curriculums"]
        normalTasks = jsonString["tasks"]
        normalFlashcards = jsonString["flashcards"]
        normalCurriculums = jsonString["curriculums"]

        if True:
            offlineOnlyTasks = []
            offlineOnlyFlashcards = []
            offlineOnlyCurriculums = []

            for task in offlineTasks:
                if task not in normalTasks:
                    offlineOnlyTasks.append(task)

            for flashcard in offlineFlashcards:
                if flashcard not in normalFlashcards:
                    offlineOnlyFlashcards.append(flashcard)

            for curriculum in offlineCurriculums:
                if curriculum not in normalCurriculums:
                    offlineOnlyCurriculums.append(curriculum)



            for task in normalTasks:
                if task not in dbTasks and task not in offlineOnlyTasks:
                    offlineTasks.remove(task)
                    normalTasks.remove(task)

            for flashcard in normalFlashcards:
                if flashcard not in dbFlashcards and flashcard not in offlineOnlyFlashcards:
                    offlineFlashcards.remove(flashcard)
                    normalFlashcards.remove(flashcard)

            for curriculum in normalCurriculums:
                if curriculum not in dbCurriculums and curriculum not in offlineOnlyCurriculums:
                    offlineCurriculums.remove(curriculum)
                    normalCurriculums.remove(curriculum)



            for task in normalTasks:
                if task not in offlineTasks and task in dbTasks:
                    dbTasks.remove(task)
                    normalTasks.remove(task)

            #fix this part
            print(f'offline curriculums: {offlineCurriculums} \n\n\n')
            print(f'db curriculums: {dbCurriculums} \n\n\n')
            print(f'normal curriculums: {normalCurriculums} \n\n\n')

            for flashcard in normalFlashcards:
                if flashcard not in offlineFlashcards and flashcard in dbFlashcards:
                    dbFlashcards.remove(flashcard)
                    normalFlashcards.remove(flashcard)
                    print("db remove")
                    print(flashcard)
                    print("\n\n\n")

            for curriculum in normalCurriculums:
                if curriculum not in offlineCurriculums and curriculum in dbCurriculums:
                    dbCurriculums.remove(curriculum)
                    normalCurriculums.remove(curriculum)
                    print("db remove")
                    print(curriculum)
                    print("\n\n\n")

            #print(f'offline flashcards: {offlineFlashcards} \n\n\n')
            #print(f'db flashcards: {dbFlashcards} \n\n\n')
            #print(f'normal flashcards {normalFlashcards} \n\n\n')
            print(f'offline curriculums: {offlineCurriculums} \n\n\n')
            print(f'db curriculums: {dbCurriculums} \n\n\n')
            print(f'normal curriculums: {normalCurriculums} \n\n\n')

            dbJsonString["task_completion_rate"] += score
            dbJsonString["missed_deadline"] += missed
            
            for task in offlineTasks:
                if task not in normalTasks and task not in dbTasks:
                    dbTasks.append(task)
                    normalTasks.append(task)
                elif task not in dbTasks:
                    dbTasks.append(task)

            for curriculum in offlineCurriculums:
                if curriculum not in normalCurriculums and curriculum not in dbCurriculums:
                    dbCurriculums.append(curriculum)
                    normalCurriculums.append(curriculum)
                elif curriculum not in dbCurriculums:
                    dbCurriculums.append(curriculum)

            for flashcard in offlineFlashcards:
                if flashcard not in normalFlashcards and flashcard not in dbFlashcards:
                    dbFlashcards.append(flashcard)
                    normalFlashcards.append(flashcard)
                elif flashcard not in dbFlashcards:
                    dbFlashcards.append(flashcard)

            print(f'offline flashcards: {offlineFlashcards} \n\n\n')
            print(f'db flashcards: {dbFlashcards} \n\n\n')
            print(f'offline curriculums: {offlineCurriculums} \n\n\n')
            print(f'db curriculums: {dbCurriculums} \n\n\n')
            print(f'offline tasks: {offlineTasks} \n\n\n')

            jsonString["productivity_score"] = copy.deepcopy(offlineJsonString["productivity_score"])
            jsonString["weekly_productivity_score"] = copy.deepcopy(offlineJsonString["weekly_productivity_score"])
            jsonString["missed_deadline"] = copy.deepcopy(offlineJsonString["missed_deadline"])
            jsonString["weekly_deadlines_missed"] = copy.deepcopy(offlineJsonString["weekly_deadlines_missed"])
            jsonString["task_completion_rate"] = copy.deepcopy(offlineJsonString["task_completion_rate"])
            jsonString["weekly_task_completion_rate"] = copy.deepcopy(offlineJsonString["weekly_task_completion_rate"])
        
        for task in dbTasks:
            if task not in normalTasks:
                normalTasks.append(task)
                offlineTasks.append(task)

        for flashcard in dbFlashcards:
            if flashcard not in normalFlashcards:
                normalFlashcards.append(flashcard)
                offlineFlashcards.append(flashcard)

        for curriculum in dbCurriculums:
            if curriculum not in normalCurriculums:
                normalCurriculums.append(curriculum)
                offlineCurriculums.append(curriculum)

        print(f'offline flashcards: {offlineFlashcards} \n\n\n')
        print(f'offline curriculums: {offlineCurriculums} \n\n\n')
        
        score = dbJsonString["task_completion_rate"] - jsonString["task_completion_rate"]
        missed = dbJsonString["missed_deadline"] - jsonString["missed_deadline"]

        if score > 0:
            jsonString["task_completion_rate"] += score
        else:
            jsonString["task_completion_rate"] += score * -1
        
        if missed > 0:
            jsonString["missed_deadline"] += missed
        else:
            jsonString["missed_deadline"] += missed * -1

        dbJsonString["weekly_task_completion_rate"] = copy.deepcopy(jsonString["weekly_task_completion_rate"])
        dbJsonString["weekly_deadlines_missed"] = copy.deepcopy(jsonString["weekly_deadlines_missed"])
        dbJsonString["weekly_productivity_score"] = copy.deepcopy(jsonString["weekly_productivity_score"])

        print(dbJsonString)
        print(jsonString["id"])
        print(jsonString["pin"])
        dbJsonString.pop("last_get")
        dbJsonString.pop("last_put")

        r = requests.put('http://15.237.110.189:5000/' + str(jsonString["id"]) + '/' + str(jsonString["pin"]) + '/',json=dbJsonString)
        print(r.status_code)
        print("db:")
        print(dbJsonString)
        print("normal:")
        print(jsonString)
        print("offline:")
        print(offlineJsonString)

        with open("data.json",'wt') as file:
            file.write(json.dumps([jsonString,offlineJsonString]))

        readAll()
        print(dbJsonString)
        print(offlineJsonString)
        print(jsonString)

def toJson(user,curriculums,tasks,flashcards): #convert objects to dictionaries for writing to json
    jsonString = user.__dict__()
    curriculumsString = []
    tasksString = []
    flashcardsString = []

    if len(curriculum.offlineCurriculums) != 0:
        curriculumsString = [curriculum.__dict__() for curriculum in curriculums]

    if len(task.offlineTasks) != 0:
        tasksString = [task.__dict__() for task in tasks]

    if len(flash.offlineFlashcards) != 0:
        flashcardsString = [flashcard.__dict__() for flashcard in flashcards]

    jsonString["tasks"] = tasksString
    jsonString["flashcards"] = flashcardsString
    jsonString["curriculums"] = curriculumsString

    return jsonString

def writeDateLastOn(): #write the date the app was last opened
    with open("date.txt",'wt') as file:
        date = datetime.datetime.now()
        file.write(f'{date.year}/{date.month}/{date.day}/{date.weekday()}')

def readDateLastOn(): #check if new week has started to reset weekly productivity metrics
    with open("date.txt",'r') as file:
        now = datetime.datetime.now()
        string = file.read()
        date = string.split('/')
        if int(date[3]) == 0 and int(date[0]) <= now.year and int(date[1]) <= now.month and int(date[2]) < now.day:
            user.user.week_productivity_score = 0
            user.user.week_deadline_missed = 0
            user.user.week_task_completion_rate = 0
            writeAll(user.user,curriculum.curriculums,task.tasks,flash.flashcards)
