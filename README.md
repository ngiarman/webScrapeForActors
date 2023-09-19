
# Let's Scrape Actors' Demographics! 

Author: Nick Giarman njgiarman@yahoo.com.
#
A hobby project from Summer 2020. 

This tool scrapes (A site that now asks not to be scraped, as of September 2023). 
It grabs demographic information from a series of defined pages and writes it to Mongo DB. 
#
Requires a text file (default: d/PycharmProjects/actorsSite/people_list.txt) with one name on each line. 
The script will use this text file to know which pages to scrape and in what order. 
Also requires a local Mongo database (default DB:Table: ethnicitydb:actorsMini). 
That has a table with the actors' names (default: name) and a link to each actor's page (default: ethnicityLink).
The script will match the names in the text files to the Mongo DB table. 
# 
Regarding duplicate names:
I try to run doubleChecker on the text file and manually enter data for the rare actors with identical names.  
