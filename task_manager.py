from json.tool import main
import os
import json
from colorama import init 


init(autoreset=True)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


class TaskManager :
    def __init__(self):
        self.task =self.load_tasks()

     
    def load_tasks(self):

        if os.path.exists("task.json"):
            try: 

               with open("task.json","r") as file :
                   tasks= json.load(file)
               
                   for task in tasks:
                    
                       if "status" not in task or not task["status"]:

                           task["status"]="pending"
                        
                   return tasks       

            except Exception as e:
                print(f" {RED}An unexpected errror while loading task !!!!!!{e}{RESET}") 
            return []
        else:
            return []
        
    def save_tasks(self):
        try:

            with open("task.json","w") as file :
            
                 json.dump(self.task,file)

        except Exception as e:
             print(f"{RED}An error occurred while saving tasks!!!!!!!{e}{RESET}")


    def add_task(self,title,description,status):
        
        while not title.strip():
            print(f"{RED}Title cannot be empty! Please enter a valid title.{RESET}")
            title = input(f"{BLUE}Enter the title of the task: {RESET}").strip()
            

        task = {"title":title , "description":description,"status":status}
        self.task.append(task)
        self.save_tasks()

        print(f"{GREEN}***TASK '{title}' ADDED SUCCESSFULLY***{RESET}")
        
        
    def task_details(self,title,):
        for task in self.task:
            if task["title"].lower() == title.lower():
                print(f"{GREEN}\nExisting Task Details:{RESET}")
                print(f"{GREEN}Title: {task['title']} - Description: {task['description']} - Current Status : {task['status']}{RESET}")

                break
         
     
        
    def view_tasks(self):
        if not self.task:
            print(f"{RED}NO TASK TO SHOW!!!!!{RESET}")
        else:
            for i, task in enumerate(self.task, 1):
                #status = task.get("status","Unknown")
                #status = "Completed" if task["completed"] else "Pending"
                print(f"{BLUE}{i}. {task['title']} - {task['description']} - [{task['status']}] {RESET}")
                

        print(f"{RED}{'='*30}{RESET}")
        



    def mark_task_status(self, task_number, status):
        while True:
            
            if 0 < task_number <= len(self.task):
                task = self.task[task_number - 1]  

                if  task["status"].lower() == status.lower():
                    print(f"{RED}TASK {task_number} IS ALREADY MARKED AS {status.upper()}**{RESET}")
                    retry = input(f"{YELLOW}Would you like to try again? (y/n): {RESET}").strip().lower()
                    if  retry == 'y':
                        task_number = int(input(f"{BLUE}Enter the task number to update as{GREEN} {status.upper()}: {RESET}"))
                    else:
                       print(f"{YELLOW}Returning to the main menu.{RESET}")
                       break
                else:
                   task["status"] = status
                   self.save_tasks()
                   print(f"{GREEN}**TASK {task_number} STATUS UPDATED TO {status.upper()}**{RESET}")
                
                   retry = input(f"{YELLOW}Would you like to try again? (y/n): {RESET}").strip().lower()
                   if retry == 'y':
                      task_number = int(input(f"{BLUE}Enter the task number to update: {RESET}"))
                   else:
                      print(f"{YELLOW}Returning to the main menu.{RESET}")
                      break
            else:
                 
                print(f"{RED}INVALID TASK NUMBER! \n {GREEN}Please choose the task number 1 to {len(self.task)}{RESET}")
                retry = input(f"{YELLOW}Would you like to try again? (y/n): {RESET}").strip().lower()
                if retry == 'y':
                   task_number = int(input(f"{BLUE}Enter the task number to update: {RESET}"))
                else:
                   print(f"{YELLOW}Returning to the main menu.{RESET}")
                   break
            
    
#  task["status"] = status
#          self.save_tasks()
#           if task["completed"]:
#                retry =input=(f"{BLUE}Would you like to try again the marking different task?(y/n): {RESET}").strip().lower()
#                if retry =='y':
 #                   task_number =int(input(f"{BLUE}Enter the task number to mark as completed :{RESET}"))
 #                   self.mark_task_completed(task_number)
 #               else:
  #                  print(f"{YELLOW}Returning to the main menu.{RESET}")
 #           else:
  #              task["completed"] = True
  #              self.save_tasks()
  #              print(f"{GREEN}**TASK {task_number} MARKED AS UPDATED {status.upper()}**{RESET}")
  #      else:
#         print(f"{RED}INVALID TASK NUMBER!{RESET}")


    def delete_task(self,task_number):
        if 0 < task_number <= len(self.task):
           del  self.task[task_number -1]
           self.save_tasks()

           print(f"{RED}**TASK {task_number} DELETED SUCCESSFULLY**{RESET}")
                   
        else:
            if len(self.task) == 0:
                print(f"{RED} No tasks available !{RESET}")
                
             
            elif len(self.task) == 1:
                   print(f"{RED}Only one task available. Please enter task number 1.{RESET}")
            else:
                 print(f"{RED} INVALID TASK NUMBER !!!!! Choose the number between 1 to {len(self.task)}{RESET}")
                 

def get_input(prompt):
    return input(f"{BLUE}{prompt}{RESET}")


def main():
        task_manager =TaskManager()


        while True:
            print("\n 1.Add New Task")
            print("\n 2.View Tasks ")
            print("\n 3. Update the Task")
            print("\n 4.Delete Task")
            print("\n 5.Exit")


            choice = input("\nChoose an option (1-5): ")

            if choice=="1" :
                while True:
                    title =input("Enter Title of the Task: ")
                    while not title:
                      print(f"{RED}Title cannot be empty! Please enter a valid title.{RESET}")
                      title = input("Enter Title of the Task: ").strip()

                    if any(task["title"].lower() == title.lower() for task in task_manager.task):
                       print(f"{RED}Task with the title '{title}' already exists! {RESET}")
                       task_manager.task_details(title)
                       
                    else:
                        description = input("Enter the Description: ")
                        status = input("Enter the Current status:")
                        if not status:
                          status = "pending"

                        task_manager.add_task(title,description,status)

                        more = input(f"{BLUE}Do you want to Add another task? (y/n): {RESET}").strip().lower()
                        if more != 'y':
                          print(f"{RED}Invalide Option Exiting the Manager, goodbye!")
                          break  


            elif choice =="2" :

                task_manager.view_tasks()


            elif choice =="3" :
                if not task_manager.task:
                    print(f"{RED}No tasks available to update. Please add tasks first!{RESET}")
                    more = input(f"{YELLOW}Would you like to add a task now? (y/n): {RESET}").strip().lower()
                    if more =='y':
                       while True:
                            title =input("Enter Title of the Task: ")
                            while not title:
                                 print(f"{RED}Title cannot be empty! Please enter a valid title.{RESET}")
                                 title = input("Enter Title of the Task: ").strip()
                            
                            if any(task["title"].lower() == title.lower() for task in task_manager.task):
                               print(f"{RED}Task with the title '{title}' already exists! {RESET}")
                               task_manager.add_task(title,description)

                            else:
                               description = input("Enter the Description: ")
                               status = input("Enter the Current status:")
                               if not status :
                                   status ='Pending'

                               task_manager.add_task(title,description,status)

                            more = input(f"{BLUE}Do you want to Add another task? (y/n): {RESET}").strip().lower()
                            if more != 'y':
                                #print(f"{RED}Invalide Option Exiting the Manager, goodbye!")
                             break  
                                
                else:
                                        
                    while True:

                        task_manager.view_tasks()
                        task_number = int(input(" Enter the Task number you want to update the status:"))
                        if 0 < task_number <= len(task_manager.task):

                           print(f"{BLUE}\nAvailable statuses: Pending, Inprogress, Onhold, Canceled,Completed{RESET}")
                           status = input("Enter the status you want to set: ").strip().lower().title()#.capitalize()
                          #print(f"{BLUE}Status entered: '{status}'{RESET}")

                           if status in ["Pending", "Inprogress","Onhold","Canceled","Completed"]:
                             task_manager.mark_task_status(task_number, status)
                           else:
                             print(f"{RED}INVALID STATUS! Please choose from the available statuses.{RESET}")
                        else:
                          if len(task_manager.task)==1:
                             print(f"{RED}Only one task available. Please enter task number 1.{RESET}")
     
                          else:
                             print(f"{RED}INVALID TASK NUMBER! Please enter a valid task number between 1 to {len(task_manager.task)}.{RESET}")
 
                        more = input(f"{BLUE}Do you want to update another task status? (y/n): {RESET}").strip().lower()
                        if more != 'y':
                                 
                            break
                                    
                             
            elif choice =="4" :
                if not task_manager.task:
                    print(f"{RED}No tasks available to update. Please add tasks first!{RESET}")
                    more = input(f"{YELLOW}Would you like to add a task now? (y/n): {RESET}").strip().lower()
                    if more =='y':
                        while True:
                            title =input("Enter Title of the Task: ")
                            while not title:
                                print(f"{RED}Title cannot be empty! Please enter a valid title.{RESET}")
                                title = input("Enter Title of the Task: ").strip()
                            if any(task["title"].lower() == title.lower() for task in task_manager.task):
                               print(f"{RED}Task with the title '{title}' already exists! {RESET}")
                               task_manager.add_task(title,description)

                            else:
                              description = input("Enter the Description: ")
                              status = input("Enter the Current status:")
                              if not status:
                                  status = 'Pending'

                              task_manager.add_task(title,description,status)

                              more = input(f"{BLUE}Do you want to Add another task? (y/n): {RESET}").strip().lower()
                              if more != 'y':
                                print(f"{RED}Exiting the Manager, goodbye!")
                                break   
                    else:
                        print(f"{YELLOW}Returning to the main menu.{RESET}")
                        break
                        
                else:
                            
                   while True:
                        task_manager.view_tasks()
                        task_number =int(input("Enter the task Number to delete: "))
                        
                        task_manager.delete_task(task_number)
                        
                        
                    
                        more = input(f"{BLUE}Do you want to delete another task? (y/n): {RESET}").strip().lower()
                        if more != 'y':
                            print(f"{RED} Exiting the Manager, goodbye!")
                            break  



            elif choice =="5":
                confirm_exit = get_input(f"{BLUE}Are you sure you want to exit? (y/n): {RESET}").strip().lower()
                if confirm_exit == 'y':
                     print(f"{YELLOW}Exiting the Manager, goodbye!{RESET}")
                else:
                    print(f"{RED}Invalide Option Exiting the Manager, goodbye!")
                    break

            else :
                print(f"{YELLOW}>>>>INVALID OPTION , PLEASE TRY AGAIN >>>>{RESET}")


if __name__== "__main__":

    main()


            





