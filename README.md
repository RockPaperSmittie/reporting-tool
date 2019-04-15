# Logs Analysis Project 

Creating a reporting tool with Python and Postgresql.

## Technologies used

* Postgresql
* Python
* Vagrant
* Linux-based virtual machine


## Reporting tool 

The reporting tool returns answers to the following three questions:

1. What are the three most popular articles?
2. Who are the three most popular authors?
3. On which days did more than 1% of requests lead to errors?

## Quick setup

1. Download and install [vagrant](https://www.vagrantup.com/)
2. Download and install [Virtual Box](https://www.virtualbox.org/)
3. Clone this repository to a directory of your choice.
4. Download the database here [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
5. Move the newsdata.sql into the cloned directory

## Setting up vagrant

1. Open terminal and cd into the working directory. Run `vagrant up`. This will install the Linux-based virtual machine.
2. Run `vagrant ssh` to log into your virtual machine.

## Connecting to the database

1. Load the data into your vagrant directory with the following terminal command `psql -d news -f newsdata.sql`
2. Connect to the database using `psql -d news`

## Views created

Before running the reportingtool.py file, create the following views in your terminal while connected to the database:

```sql
create view daily_requests as
select to_char(time, 'Month DD, YYYY') as date, count(status) as request
from log
group by date
order by date
```

```sql
create view daily_errors as
select to_char(time, 'Month DD, YYYY') as date, count(status) as error
from log
where status like '4%'
group by date
order by date
```

```sql
create view error_percentages as
select daily_requests.date, round(100.00 * error / request, 2) as percentage
from daily_requests, daily_errors
where daily_requests.date = daily_errors.date
```

## Running reporting tool

Finally run reportingtool.py with the following terminal command:

`python reportingtool.py`

The terminal should output three different sets of data answering the three aforementioned questions.











