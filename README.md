# Django Twitter Clone by Redian Marku

Fully functional Django App that looks ecxatly like real Twitter.

Demo Image:
![](TwitterDemo.png)

## Installation

1. Clone this repository to your local machine:

   
bash
   git clone https://github.com/reza72rg/Twitter
   
2. Install the required dependencies:

   
bash
   pip install -r requirements.txt
   
3. Set up the database by running migrations:

   
bash
   python manage.py migrate
   
4. Start the development server:

   
bash
   python manage.py runserver
   
5. Open the program in your web browser at `http://127.0.0.1:8000`.

## API Documentation

The API documentation can be found at `http://127.0.0.1:8000/api/v1/` and `http://127.0.0.1:8000/accounts/api/v1/`, providing details on how to interact with the REST API endpoints.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Special thanks to [Ali Bigdali] for their assistance and feedback during the development of this project.

## Performance Testing

Using Locust, the API tolerance threshold is created and its performance is checked by generating artificial traffic on the site. It can be tested at the address `http://127.0.0.1:8089/`.

### Features
- Django LTS
- Function Based View
- Django RestFramework
- User authentication
- Black
- Flake8
- Responsive Design
- Bootstrap5



### Setup
To get this repository, run the following command inside your git enabled terminal
```bash
git clone https://github.com/alibigdeli/Django-FBV-DRF-TodoApp
```

### Getting ready
Create an enviroment in order to keep the repo dependencies seperated from your local machine.
```bash
python -m venv venv
```

Make sure to install the dependencies of the project through the requirements.txt file.
```bash
pip install -r requirements.txt
```

Once you have installed django and other packages, go to the cloned repo directory and run the following command

```bash
python manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
python manage.py migrate
```

### options
Project it self has the user creation form but still in order to use the admin you need to create a super user.you can use the createsuperuser option to make a super user.
```bash
python manage.py createsuperuser
```

And lastly let's make the App run. We just need to start the server now and then we can start using our simple todo App. Start the server by following command

```bash
python manage.py runserver
```

Once the server is up and running, head over to http://127.0.0.1:8000 for the App.

### Reformat and check
If you want your code to be check by pep8 and all the guide lines, there are two packages added to requirements in order to check and reformat code.
you can use it by this command:
```bash
black -l 79 . && flake8
```
### Database schema
A simple view of the project model schema.
<p align="center">
<img src="https://user-images.githubusercontent.com/29748439/134964183-595bd7cf-df01-4089-8d22-bfb765d62c18.png" alt="database schema" width="300"/>
</p>

### Todo
- [ ] refactor javascript codes in list.html
- [ ] leave comments for codes
- [ ] add unit tests
- [ ] add heroku config files
- [ ] complete the documentation
- [ ] create a video tutorial

### Bugs or Opinion
Feel free to let me know if there are any problems or any request you have for this repo.
