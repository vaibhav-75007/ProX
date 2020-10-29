import json
import flashcard_class as flash
import Task as task
import user_class as user
import datetime

#must read in all of the json
#must read in all tasks
#if there is time create error handling for erroneous json data
#create window to initialise new user
#work on curriculums

def stringToDatetime(string):
    splitDate = string.split('/')
    return datetime.datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2][0:2]))

def readAll():
    dictionary = 0
    with open("data.json",'r') as file: #create case if no flashcards, no tasks
        fileContents = file.read()
        dictionary = json.loads(fileContents)

    print(dictionary)
    user.user = user.User(dictionary["name"],0,dictionary["task_completion_rate"],dictionary["missed_deadline"],dictionary["weekly_productivity_score"],dictionary["weekly_task_completion_rate"],dictionary["weekly_deadlines_missed"],dictionary["id"],dictionary["email"],dictionary["pin"])
    task.tasks = [task.Task(name=tempDict["name"],description=tempDict["description"],deadline=stringToDatetime(tempDict["deadline"])) for tempDict in dictionary["tasks"]]
    flash.flashcards = [flash.FlashCard(tempDict["subject"],tempDict["front_text"],tempDict["back_text"]) for tempDict in dictionary["flashcards"]]

def writeAll(user,curriculums,tasks,flashcards): #create case to write null in lists if any of the arrays are empty
    jsonString = user.__dict__()
    curriculumsString = [curriculum.__dict__() for curriculum in curriculums]
    tasksString = [task.__dict__() for task in tasks]
    flashcardsString = [flashcard.__dict__() for flashcard in flashcards]
    jsonString["tasks"] = tasksString
    jsonString["flashcards"] = flashcardsString
    jsonString["curriculums"] = curriculumsString

    with open("data.json",'wt') as file:
        file.write(json.dumps(jsonString))
