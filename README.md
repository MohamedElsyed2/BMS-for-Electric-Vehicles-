# BMS-for-Electric-Vehicles-

#*******************************************************#

Creating a Docker container on DigitalOcean:
1.	Create a DigitalOcean account: If you haven't already, create an account on DigitalOcean.
2.	Create a droplet: Click on the "Create Droplet" button and select the droplet size, region, and operating system you want to use.
3.	SSH into the droplet: Once the droplet is created, you will receive an email with the IP address, username, and password. Use a tool like PuTTY or the built-in terminal to SSH into the droplet.
4.	Install Docker: Once you are logged into the droplet, install Docker by running the following command:
-	sudo apt-get update
-	sudo apt-get install docker.io
5.	Pull a Docker image: After Docker is installed, you can pull a Docker image by running the following command:   
-	sudo docker pull <ceaf6a38181d  >
6.	Run the Docker container: Finally, run the Docker container by running the following command:  
-	sudo docker run -d -p 80:80 <ceaf6a38181d>
7.	Here, “-d” flag runs the container in the background, “-p” flag maps the port 80 on the droplet to the port 80 on the container, and <CBBMS > is the name of the Docker image you pulled.
  
 #***************************************************************#
 
creating a website on DigitalOcean using flask and HTML, you can follow these steps:

1.	Install Python and Flask: Once you are logged into the droplet, install Python and Flask by running the following command: 
-	sudo apt-get update
-	sudo apt-get install python3 python3-pip
-	sudo pip3 install flask
2.	Write your Flask application: Create a new file called app.py on the server and add your Flask application code. Here's an example Flask application that serves a simple HTML page:
3.	Create your HTML template: Create a new directory called templates on the server and add an HTML file called index.html to it. Here's an example HTML file:
4.	Run the Flask application: Finally, run the Flask application by running the following command:   
-	python3 app.py
5.	Test the website: Finally, test the website by navigating to the IP address < http://142.93.104.90:5000/ > of the server in a web browser.

#************************************************************#
  
  Navigate into a container:

1.	List the running containers on the cloud server using the command:
-	docker ps
2.	to open an interactive shell session within the container, run the command:
- docker exec -it 80012edc87cc /bin/bash 
  
#**************************************************************#
  
Editing configuration files, scripts, and other plain text files in the container, use the following command:
-	nano, for example nano main.py

  #**************************************************************#
  
 Logging  into the MySQL command-line interface:
-	mysql -u root -p


