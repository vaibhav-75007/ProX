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
        dictionary = json.loads(file)
    user.user = user.User(dictionary["name"],dictionary["productivity_score"],dictionary["task_completion_rate"],dictionary["deadlines_missed"],dictionary["week_productivity_score"],dictionary["week_task_completion_rate"],dictionary["week_deadline_missed"],dictionary["id"],dictionary["email"],dictionary["pin"])
    task.tasks = [task.Task(tempDict["name"],tempDict["description"],stringToDate(tempDict["deadline"])) for tempDict in dictionary["tasks"]]
    flash.flashcards = [flash.Flashcard(tempDict["subject"],tempDcit["front_text"],tempDict["back_text"]) for tempDict in dictionary["flashcards"]]

def writeAll(user,curriculums,tasks,flashcards): #create case to write null in lists if any of the arrays are empty
    jsonString = user.__dict__()
    curriculumsString = [curriculum.__dict__() for curriculum in curriculums]
    tasksString = [task.__dict__() for task in tasks]
    flashcardsString = [flashcard.__dict__() for flashcard in flashcards]
    jsonString["tassk"] = tasksString
    jsonString["flashcards"] = flashcardsString
    jsonString["curriculums"] = curriculumsString

    with open("data.json",'wt') as file:
        file.write(json.dumps(jsonString))
