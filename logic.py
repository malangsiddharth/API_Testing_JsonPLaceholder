import requests

get_response_users=requests.get("https://jsonplaceholder.typicode.com/users")

get_response_todos=requests.get("https://jsonplaceholder.typicode.com/todos")

print(get_response_users.json())

users=get_response_users.json()
todos=get_response_todos.json()
list_users_id=[]
list_todos=[]
for i in range(len(users)):
    list_users_id.append(get_response_users.json()[i]['id'])

for j in range(len(todos)):
    if(get_response_todos.json()[j]['userId']) not in list_todos:
        list_todos.append(get_response_todos.json()[j]['userId'])

user_count=0
for i in range(len(users)):
    if len(list_users_id)==len(list_todos):
        if(list_users_id[i]) in list_todos:
            user_count+=1
    else:
        print("Few user are missing")

if user_count==len(list_todos):
    print("Users inside are same")
else:
    print("Users are not similar")

'''
 User belongs to the city FanCode
 Fancode City can be identified by lat between ( -40 to 5) and long between ( 5 to 100) in users api
'''
fancode_users_list=[]
for i in range(len(users)):
    lat_value=get_response_users.json()[i]['address']["geo"]["lat"]
    lng_value=get_response_users.json()[i]['address']["geo"]["lng"]

    if (-40<float(lat_value)<5) and (5<float(lng_value)<100):
        print("Fancode Users:----",get_response_users.json()[i]['id'])
        fancode_users_list.append(get_response_users.json()[i]['id'])
    else:
        print("Not fancode users for user:----",get_response_users.json()[i]['id'])


for i in range(len(fancode_users_list)):
   print(fancode_users_list[i])
   users_task=requests.get("https://jsonplaceholder.typicode.com/todos",params={"userId":fancode_users_list[i]})
   print(users_task.json())
   users_task_response=users_task.json()
   count_task_completed=0
   for j in range(len(users_task_response)):
       if users_task_response[j]["completed"]==True:
           count_task_completed+=1

   if ((count_task_completed / len(users_task_response))*100)>50:
       print("Fancode user completed the task:----",fancode_users_list[i])
   else:
        print("Fancode user not completed the task:----", fancode_users_list[i])
