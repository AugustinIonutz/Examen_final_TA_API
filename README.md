# Automation Testing --> Simple Book API

### Project author: Augustin Balan

### INFO.
The scope of this application is to test the functionalities of the Simple Book API

The documentation can be found [here](https://github.com/vdespa/introduction-to-postman-course/blob/main/simple-books-api.md) 

## INTSTALLATION
In order to use this project you need python (version 3.12), pip to be installed. Also you need the following libraries: requests (version 2.31.0), pytest (version 8.1.1) and pytest-html (version 4.1.1). To install them (libraries), run the Terminal command:

```commandline
pip install -r requirements.txt
```

## RUNNING THE TESTS
You can find the tests in the "tests" folder. To run any test click on the green arrow in the left side of the test function or ctrl+shift+f10 ![pentru readmeFILE](https://github.com/AugustinIonutz/SIMPLE_BOOK_API_AUTOMATION_TESTING/assets/164404789/14319feb-4de9-4dd0-a9ba-a944bc42030f)


## REPORTS

#### pytest-html
pytest-html is a plugin that generates tests report HTML file with a single command, add this to your Pytest run command:

```commandline
python -m pytest --html=./report.html tests/BooksTests.py
```

![final report](https://github.com/AugustinIonutz/SIMPLE_BOOK_API_AUTOMATION_TESTING/assets/164404789/f721eaf3-2fad-4761-af7d-4bb0fd83595f)


