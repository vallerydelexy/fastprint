# Django test project untuk [fastprint](https://recruitment.fastprint.co.id/tes/programmer)
> made by Rizki Aprita

why i pick django over codeingniter
1. i like python as hobby language, i usually use python for scraping stuff from the internet or doing data processing using `pandas` and `numpy` but i never actually built a website using `python`, because its slow and i usually did that using `php` or `javascript (nodejs)`. so i think this might be a fun to try.
2. i already know `php` and `codeigniter`, no point using tech im familiar with for something like this.
3. the first recommendation are django and postgre, so yeah.

my portfolio: [https://aprita.web.id](https://aprita.web.id)




# Getting started
## 1. Install the Components and clone this repo
```bash
sudo apt update
sudo apt install git python3-pip python3-dev libpq-dev postgresql postgresql-contrib
git clone https://github.com/vallerydelexy/fastprint.git
```
## 2. Create a Database and Database User
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE django;
CREATE USER rizkiaprita WITH PASSWORD 'password';
ALTER ROLE rizkiaprita SET client_encoding TO 'utf8';
ALTER ROLE rizkiaprita SET default_transaction_isolation TO 'read committed';
ALTER ROLE rizkiaprita SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django TO rizkiaprita;
\q
```
## 3. Migrate the model into the database
```bash
cd ~/fastprint
python manage.py makemigrations
python manage.py migrate
```
### if you see this prompt:
>Callable default on unique field model_name.field_name will not generate unique values upon migrating.
> Please choose how to proceed:
> 1) Continue making this migration as the first step in writing a manual migration to generate unique values described here: https://docs.djangoproject.com/en/5.0/howto/writing-migrations/#migrations-that-add-unique-fields.
> 2) Quit and edit field options in models.py.

type `1` on your terminal and then press `enter`

## 4. Run the development server
```python
python manage.py runserver
```
open `http://127.0.0.1:8000/` on your browser to view the project
