
# Automate resource uploads


Upload a record into ELG using Python through our Python SDK
(https://gitlab.com/european-language-grid/platform/python-client) but
this is relatively new. This is why it is not yet part of the Python
SDK section of our documentation
(https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/PythonSDK.html). However
this is already useable and I would be happy to work on it more
intensively if you notice some issues with it (or have suggestions for
improvments).

It is working as follows:

```
from elg import Provider

me = Provider()
response = me.upload_xml(“path/to/the/xml/file.xml”) 
# A new item should have be created into “My Grid” if the response’s status code is 2xx
```

To see all the possible parameters (to upload data for example), you can have a look to the source code: https://gitlab.com/european-language-grid/platform/python-client/-/blob/master/elg/provider.py


# Cleanup

delete local docker images and volumes

```
docker system prune -a --volumes
```