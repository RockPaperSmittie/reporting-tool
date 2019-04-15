# !/usr/bin/env python3

# Database code for DB news

import psycopg2

DBNAME = "news"

# Select query for the top 3 most popular articles of all time.

top_articles = """
    SELECT title, count(*) AS views
    FROM articles
    JOIN log ON articles.slug
    LIKE replace(log.path, '/article/', '')
    GROUP BY articles.title
    ORDER BY views DESC LIMIT 3
    """

# Select query for the top 3 most popular authors of all time.

top_authors = """
    SELECT name, count(*) as views
    FROM authors, articles
    JOIN log on articles.slug
    LIKE replace(log.path, '/article/', '')
    WHERE authors.id = articles.author
    GROUP BY authors.id
    ORDER BY views DESC LIMIT 3
    """

# Select query for days where more than 1% of requests lead to errors.
http_errors = """
    SELECT * from error_percentages WHERE percentage > 1
    """


# Connecting, querying and closing connection
def get_posts(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    posts = c.fetchall()
    db.close()
    return (posts)


def report_title(title):
    print(title + '\n')


# Print top three articles
def top_3_articles():
    selection = get_posts(top_articles)
    print("Top 3 Articles of All Time:"+"\n")
    for title, views in selection:
        print("* {0:.<40} {1:,} views".format(title, views))


# Print top 3 authors
def top_3_authors():
    selection = get_posts(top_authors)
    print("\n" + "Top 3 Authors of All Time:"+"\n")
    for author, views in selection:
        print('* {0:.<40} {1:,} views'.format(author, views))


# Print errors greater than 1% of total
def error_days():
    selection = get_posts(http_errors)
    print("\n" + "Greater than '1%' error days :"+"\n")
    for days, percentages in selection:
        print('* '+'{} -- {}% '.format(days, percentages))


if __name__ == '__main__':
    report_title("Generating news data report:")
    top_3_articles()
    top_3_authors()
    error_days()
