# url-short

A simple URL shortener written in python using the Flask and redis-py libraries.

It looks not too bad. I spent around 1 hour writing the backend, and probably 5 hours working on the front-end, so you can tell where the primary emphasis of this project is.

## depend

Only 2 packages are depended upon.

Get them using `pip install redis Flask`

## configure

Configure how the URL shortener works in `app.py`

Line 8: change host='.' and port=6380 to the host and port of your redis setup

Line 12, 14, 16: Configures how a key is generated, the length of the key, possible characters to choose from when generating a key, and how many tries to generate a key.

Line 18: Site title. You're better off changing this in templates/index.html

Line 79: Debug mode on/off

Line 80: Open to public?

## run

`python app.py`

That's it!
