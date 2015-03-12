# NDW
Tools for recognizing and storing ndw data

This is a Django application for parsing and storing NDW data in database.
First you need to install Django, install South also.
Then configure your database connection in settings.py file.
Use South migration commands to apply existing database migrations and create the actual database schema.
Then enjoy using the ndwparser methods to parse NDW sensor info and measurement files.

PS. Django main feature are apps, so, to create your own functional, that uses existing, create new app near ndw folder and import what you need from ndw.
