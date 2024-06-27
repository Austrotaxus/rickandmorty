
# Coding Assignment – RickAndMorty Integeration

In this task, you need to implement a simple integration connector for RickAndMorty API using Python. 
You may use any libraries that will make your code cleaner, or better in any way. 
 
## API 
Please create an integration client pulling data from RickAndMorti API:
https://rickandmortyapi.com/

### The application should:

1. Fetch the entire API contents for the objects:
a. Character
b. Location
c. Episode
2. Output all API objects to separate JSON files
3. Each JSON file should contain 3 fields:
a. Id - generated guid
b. Metadata - the name from within the fetched object
c. RawData - The fetched JSON data presented as dictionary.
d. Upon finish, the program should print to the screen:
1. a log a list of names of the episodes aired between 2017 and 2021
and contains more than three characters.
2. a list of characters which appear only on odd episode numbers
(episode 1, 3, 9 (of whatever season) )

 
### General notes 
1. Please note, the client should be treated as industry level production code, it should be
written with performance and clean code approach.
2. The solution should be as simple and clean as possible, avoid over design/engineering
and stick to the requirements .
 
