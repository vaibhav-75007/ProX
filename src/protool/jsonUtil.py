import json
import flashcard_class as flash
import Task as task
import user_class as user
import curriculum
import datetime
import requests

#if there is time create error handling for erroneous json data
#work on curriculums

def stringToDatetime(string):
    splitDate = string.split('/')
    return datetime.datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2][0:2]))

def readAll():
    dictionary = 0
    with open("data.json",'r') as file: #create case if no flashcards, no tasks
        fileContents = file.read()
        dictionary = json.loads(fileContents)

    user.user = user.User(dictionary["name"],dictionary["productivity_score"],dictionary["task_completion_rate"],dictionary["missed_deadline"],dictionary["weekly_productivity_score"],dictionary["weekly_task_completion_rate"],dictionary["weekly_deadlines_missed"],dictionary["id"],dictionary["email"],dictionary["pin"])

    if len(dictionary["tasks"]) == 0:
        task.tasks = []
    else:
        task.tasks = [task.Task(name=tempDict["name"],description=tempDict["description"],deadline=stringToDatetime(tempDict["deadline"])) for tempDict in dictionary["tasks"]]

    if len(dictionary["flashcards"]) == 0:
        flash.flashcards = []
    else:
        flash.flashcards = [flash.FlashCard(tempDict["subject"],tempDict["front_text"],tempDict["back_text"]) for tempDict in dictionary["flashcards"]]

    if len(dictionary["curriculums"]) == 0:
        curriculum.curriculums = []
    else:
        curriculum.curriculums = [curriculum.Curriculum(tempDict["name"],tempDict["subject"],tempDict["topics"]) for tempDict in dictionary["curriculums"]]

def writeAll(user,curriculums,tasks,flashcards): #create case to write null in lists if any of the arrays are empty
    jsonString = toJson(user,curriculums,tasks,flashcards)

    with open("data.json",'wt') as file:
        file.write(json.dumps(jsonString))

    r = requests.put('http://0.0.0.0:54321/' + str(user.id) + '/' + str(user.pin) + '/',json=jsonString)
    print(r.status_code)

def toJson(user,curriculums,tasks,flashcards):
    jsonString = user.__dict__()
    curriculumsString = []
    tasksString = []
    flashcardsString = []

    if len(curriculum.curriculums) != 0:
        curriculumsString = [curriculum.__dict__() for curriculum in curriculums]

    if len(task.tasks) != 0:
        tasksString = [task.__dict__() for task in tasks]

    if len(flash.flashcards) != 0:
        flashcardsString = [flashcard.__dict__() for flashcard in flashcards]

    jsonString["tasks"] = tasksString
    jsonString["flashcards"] = flashcardsString
    jsonString["curriculums"] = curriculumsString

    return jsonString
