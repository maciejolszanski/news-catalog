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

## Project structure
```
└── news-catalog
  ├── .config 
  ├── build 
  ├── dep
  ├── doc
  ├── res
  ├── src
  ├── test
  ├── tools
  ├── README.md
  └── LICENSE
```
`.config` - local configuration related to setup on local machine

`build` - scripts related to build process (Powershell, Docker compose, ...)

`dep` - dependecies

`doc` - documentation

`res` - static resources (images etc.)

`tools` - scripts to automate tasks in the project - build scripts, rename scripts

`src` - source code

`test` - unit tests, integration tests

   
