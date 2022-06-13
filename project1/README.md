# HCI project1

The goal of Project 1 is to explore what areas of automation tools should be automated in order to actually benefit users.
In this study, we provide the automated time table creater to users.
The users can create their time tables with this tool by input their opinions.
And then, the program will create 5 time table candidates automatically.

## Environment

This program was tested in the following environment.

- Ubuntu 20.04 LTS
- Intel(R) Core(TM) i9-10940X CPU @ 3.30GHz
- DDR4 32GBx4 (128GB)
- Python 3.8.8
- Streamlit 1.7.0
- Pandas 1.2.4
- NumPy 1.20.1
- Matplotlib 3.3.4

## How to run

First of all, you need to install the libraries.
```bash
pip3 install streamlit==1.7.0
pip3 install pandas==1.2.4
pip3 install numpy==1.20.1
pip3 install matplotlib==3.3.4
pip3 install streamlit_option_menu
```

After the library installation, run the server as follow command.
```bash
streamlit run main.py
```

Then you can check the program via web browsers.
