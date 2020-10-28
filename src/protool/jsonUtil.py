import json
import flashcard_class as flash
import Task as task
import user_class as user

#must read in all of the json
#must read in all tasks
#if there is time create error handling for erroneous json data
#create window to initialise new user
#work on curriculums

def stringToDatetime(string):
    splitDate = string.split('/')
    return datetime.datetime(splitDate[0],splitDate[1],splitDate[2])

def readAll():
    with open("data.json",'r') as file: #create case if no flashcards, no tasks
        dictionary = json.loads(file)
    user.user = user.User(dictionary["name"],dictionary["productivity_score"],dictionary["task_completion_rate"],dictionary["deadlines_missed"],dictionary["week_productivity_score"],dictionary["week_task_completion_rate"],dictionary["week_deadlines_missed"])
    task.tasks = [task.Task(tempDict["name"],tempDict["description"],stringToDate(tempDict["deadline"])]) for tempDict in dictionary["tasks"]]
    flash.flashcards = [flash.Flashcard(tempDict["subject"],tempDcit["front_text"],tempDict["back_text"]) for tempDict in dictionary["flashcards"]]

def writeAll(user,curriculums,tassk,flashcards):
    jsonString = dict(user)
    curriculumsString = dict(curriculums)
    tasksString = dict(tasks)
    flashcardsString = dict(flashcards)
    jsonString["tassk"] = tasksString
    jsonString["flashcards"] = flashcardsString
    jsonString["curriculums"] = curriculumsString

    with open("data.json",'wt') as file:
        file.write(json.dumps(jsonString))
