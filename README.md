# A simple RestAPI service using FastAPI


## Requirements:
* Create a RestAPI using python FastAPI.
* User signup with email, login with email, get profile , update profile
* JWT based authentication
* Fields to include for user - firstName, LastName, DoB, age(calculated internally), gender, address (flat no, area, city, state, country, pin code) etc.
* API request / response should be in JSON format
* Additional apis to get list of sports and statistics of each sport , (choose any 5 sports and its basic analytics , use external open source information, store it locally and respond in apis as per request)
* All the api should support asynchronous call
* Write a schema for MySQL for user and sport data storage and retrieval ( no need to actually integrate with mysql)
* API should handle at least 100 concurrent request and response time should be under 200 ms

## Improvements for a real-time RestAPI Service using FastAPI
* Use Hashing for passwords
* Store the secrets securely in a .env file
* Stronger JWT Authentication
* Implement multiple unit test cases
* Use of Enum for gender field
* Proper daatabase integration using SQLAlchemy
* Usage of Repository/Service Pattern 
* Logging and more try catch blocks for exceptions
* Input Validation using ORM
* Automated testing using CI/CD 
* Proper montoring metrics using tools like grafana, telemetry, loki

