# Design

## Main App requirements
1. News-Catalog is a Desktop app (Possibly enhanced to web app)
2. Newses are gathered from many websites
3. Newses are presented in simple way - only text
4. Newses can be filtered be website, author, topic, keywords, date
5. There are tags assigned to newses based on their content
6. Newses can be marked by user as interesting/not interesting
7. Newses probability to be interesting for specific user is evaluated - based on that only possibly interesting newses are recommended to user, but he/she can see all newses

## Development flow
Gitflow will be used. Main branch contains only released code. Develop branch contains code that is being developed currently. Feature branches are merged to develop. There is no need of using release branches.

## Technologies used
Main app language is Python. Data are scraped using scrapy module. Data are stored as MondoDB documents. App UI is created in Python as Desktop app.

## Scrapy with MongoDB - [example](https://realpython.com/web-scraping-with-scrapy-and-mongodb/)
Tasks:
1. Specify Scraped Data Sctructure in `items.py` in `scrapy_project` directory.
2. [DONE] ~~Create Scrapy spider~~
3. Parse scraped data to created Item
4. Set MondoDB database parameters in `setting.py`
5. Create pipeline to connect spider and database

## UI - Streamlit - [example](https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb)
Tasks:
1. Add mongoDB secrets to Streamlit `secrets.toml` and add it to .gitignore
2. Copy app secrets to the cloud
3. Create Streamlit app to display Newses:
   * Filtering newses (date, author, webiste, tags)
   * Possibility to mark news as interesting/not interesting

## Open questions:
1. Maybe there should be not a pipeline that connects spider with mongoDB, but there should be another layer - API that will enale connection with db - it will be easier for Streamlit to read and modify these data?
   