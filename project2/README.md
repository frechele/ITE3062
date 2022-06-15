# HCI project2

## Environment

This program was tested in the following environment.

- Ubuntu 20.04 LTS
- Intel(R) Core(TM) i9-10940X CPU @ 3.30GHz
- DDR4 32GBx4 (128GB)
- Python 3.8.8
- Streamlit 1.7.0
- Pandas 1.2.4
- NumPy 1.20.1
- Node 16.15.0
- MySQL 8.0.29-0ubuntu0.20.04.3

## How to run

First of all, you need to install the libraries.
```bash
pip3 install streamlit==1.7.0
pip3 install pandas==1.2.4
pip3 install numpy==1.20.1
pip3 install matplotlib==3.3.4
```

After the library installation, you need to configure the api server settings.
(cf. your db manager name should be "db_admin")
```bash
export HCI_MYSQL_HOST="<your mysql server host>"
export HCI_MYSQL_PASSWORD="<your mysql admin password>"
```

Before the server run, you need to create database named as `hci`.
```sql
mysql> CREATE DATABASE hci;
```

And then, run the api server as follow command.
```bash
cd api
node index.js
```

Finally, run the main server as follow command.
```bash
streamlit run main.py
```
