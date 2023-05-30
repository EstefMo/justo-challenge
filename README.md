# justo-challenge
Evaluation project for the position of backend developer at Jüsto

Project Name: Spy Agency Assignment System

Overview:
We are building a simple tool for an international spy agency to manage assignments for their hitmen. The agency conducts planned assassinations and needs a new system to assign and track hits. The system will have multiple user roles, including hitmen, managers, and a boss. Hitmen can be assigned hits and view their upcoming work. Managers can create and assign hits to the hitmen they manage, while the boss has the authority to assign hits to anyone in the system, including managers. The system should also handle cases where hits fail or targets are no longer accessible due to security measures.

Technology stack: 

        python 3.8.10 django 3.2.16 postgres docker
    
Installation:
  To be able to use the project, it will be necessary to raise the docker, which is done from the command console, once located inside the root folder of the project and typing the following line:
  
        docker-compose up
        
Subsequently accessing in the browser to the address: 

        http://localhost:8000
    
In the same way this command generates the database where the following are already registered:
    -A user of type: big boss 
     Whose login credentials are: 
            
        email: bigboss@example.com
        password: admin123

In addition we have three Manager type users who identify themselves with the emails 'hitman' (followed by the user number) '@example.com' for example:
( hitman2@example.com). The user numbers of these managers are 2, 3, 4 respectively. and their password is 'password'.
and finally 6 hitman type users in the same way these contain an email with the same structure as the managers and the user numbers are from 5 to 11 respectively, and their password is also 'password'.
 
Features:
The following features can be used within the system, obviously this will depend on the user's role and permissions.

        List of Hits: Displays a list of hits based on the user's role and assigned responsibilities.
        Hit Detail: Provides detailed information about a specific hit, including the assignee, description, target name, and status.
        Create Hit: Allows managers and the boss to create new hits, assigning them to specific users based on their roles.
        List of Hitmen: Displays a list of hitmen based on the user's role, showing the hitmen they manage.
        User Detail: Provides detailed information about an individual hitman, including their name, email, description, and state (active or inactive).
 
 

