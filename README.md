# myWebDomain (fullstack)

**myWebDomain** - is my personal website which I built by myself with the idea of publishing my projects. After some time I liked this project so much that I decided to turn it into my personal website.

## Features

The website has many interactive elements such as text appearing on the main page, links reacting on mouse hovers, possibility of sending messages to me using the contact form, favicon icon, special tab for the administrator which has the possibility of modifying the content on the visible website for everyone (projects, about). To the website are connected two relational databases with AWS RDS. For me as a developer the coolest feature is the use of CI/CD in this project. Using the code deployment on Github - AWS CodePipeline automatically detects the change and communicates the code deployment to AWS Elastic Beanstalk *(SO COOL!)*. 

## Stack

The website was created using the **Python 3.8.5** programming language (mainly **Flask**), **HTML5** and **CSS**. I used **AWS (Amazon Web Services)** to deploy the website to the web: **Elastic Beanstalk, S3, RDS, EC2, Route 53, CodePipeline, Certificate Manager**. I used **MySQL Workbench 8.0** to create the tables and to check the connection to the server.

## Link

-> [www.mateuszbuziak.com](www.mateuszbuziak.com)

## Roadmap

My plans still include:

- [x] buying domenta (check - [www.mateuszbuziak.com](www.mateuszbuziak.com) has been bought)
    - [x] implementing it (it's live!)
- [x] adding SSL certificate
    - [x] it's working and typing url basic url (http) redirects to https (thanks to EC2)
- [ ] adding more variety to the website (maybe JavaScript?)
- [ ] constantly adding new projects
- [ ] adding mobile version(s)?
- [ ] sending confirmation mail to sender after filling mail form 
- [ ] SEO

## Author

I am the only author of this project - github.com/8uziak.

## Project status

```diff
+ active / in progress 
```