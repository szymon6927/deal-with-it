# deal-wtih-it

### Popular "deal with it" meme generator with face detection

![Test output gif](test.gif)

## Getting Started

To start with it follow the instructions bellow

## Prerequisites

Before you begin download and install [CMake](https://cmake.org/download/) e.g from 

```
https://cmake.org/download/
```

It's required for correct install Dlib libary

## Installing

First download or clone the repo

```
https://github.com/szymon6927/deal-with-it.git
```
Go to project directory
```
cd deal-with-it
```
Then install all dependency by PIP
```
pip install -r requirements.txt
```

## Run
To run a application
```
python main.py -image your_image_path.jpg -output your_gif_name.gif
```
If your image is too big, don't worry app take care of resize image.
And if your image contains many faces, don't worry app probably detect them.

Enjoy!


## Running the tests

TODO(implement the tests)

### License

This project is licensed under the MIT License