from behave import *
import requests
from utilities.resources import *
from utilities.configuration import *


@given(u'User has the todo tasks')
def verifytodotasks(context):
    context.userslist=requests.get(url=getConfig()['API']['endpoint'] + ApiResources.users)
    assert context.userslist.status_code == 200
    context.todos=requests.get(url=getConfig()['API']['endpoint']+ApiResources.todos)
    assert context.todos.status_code == 200
    users_json = context.userslist.json()
    todos_json= context.todos.json()
    list_users_id = []
    list_todos = []
    for i in range(len(users_json)):
        list_users_id.append(context.userslist.json()[i]['id'])

    for j in range(len(todos_json)):
        if (context.todos.json()[j]['userId']) not in list_todos:
            list_todos.append(context.todos.json()[j]['userId'])
    user_count = 0
    for i in range(len(users_json)):
        if len(list_users_id) == len(list_todos):
            if (list_users_id[i]) in list_todos:
                user_count += 1

    if user_count == len(list_todos):
        print("All Users has todo list are same")
    else:
        print((len(list_todos)-user_count),":---user missing todo list")


@given(u'User belongs to the city FanCode')
def step_impl(context):
    context.fancode_users_list = []
    for i in range(len(context.userslist.json())):
        context.lat_value = context.userslist.json()[i]['address']["geo"]["lat"]
        context.lng_value = context.userslist.json()[i]['address']["geo"]["lng"]

        if (-40 < float(context.lat_value) < 5) and (5 < float(context.lng_value) < 100):
            print("Fancode User:----", context.userslist.json()[i]['id'])
            context.fancode_users_list.append(context.userslist.json()[i]['id'])
        else:
            print("Not fancode users for user:----", context.userslist.json()[i]['id'])


@then(u'User Completed task percentage should be greater than 50%')
def step_impl(context):
    print("Fancode users list:----",context.fancode_users_list)
    for i in range(len(context.fancode_users_list)):
            context.users_task = requests.get("https://jsonplaceholder.typicode.com/todos",
                                          params={"userId": str(context.fancode_users_list[i])})
            assert context.users_task.status_code == 200
            users_task_response = context.users_task.json()
            count_task_completed = 0
            for j in range(len(users_task_response)):
                if users_task_response[j]["completed"] == True:
                    count_task_completed += 1
            print(context.fancode_users_list[i])
            if ((count_task_completed / len(users_task_response)) * 100) > 50:
                print("Fancode user {} completed the task with percentage {}".format(context.fancode_users_list[i],(count_task_completed / len(users_task_response)) * 100))
            else:
                print("Fancode user {} not completed the task, user managed to completed {} task".format(context.fancode_users_list[i],(count_task_completed / len(users_task_response)) * 100))
