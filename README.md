# Web-Search-Field-Study-Toolkit

### This tool is used to collect behavioral data on Bing search

### Installation

#### 1. Set up python environment

- download and install miniconda https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

- open Anaconda Prompt (miniconda 3), run this commend to install the virtual environment named "web"

  ```bash
  conda create -n web python=3.8.16 -y
  ```

- after installing the virtual environment, run this commend to activate the environment and install the package Django

  ```bash
  conda activate web
  conda install -c anaconda django -y
  ```

#### 2. Set up the tool

- under the web virtual environment, run these commends to direct to the study tool folder and then the folder where the file manage.py is located:

  ```bash
  cd "{path to the study tool folder}"
  cd OUHCIR_annotation_platform
  ```

- run these commends to initialize the database:

  ```bash
  python manage.py makemigrations user_system
  python manage.py makemigrations task_manager
  python manage.py migrate
  ```

- run this commend to launch the server

  ```bash
  python manage.py runserver 127.0.0.1:8000
  ```

#### 3. Install the extension in Chrome

- open chrome, click the three-dot button at the upper-right corner of the browser window, go to Extensions - Manage extensions
- enable the Developer mode at the upper-right corner of the extension page, then click "Load unpacked" button at the upper-left corner of the extension page
- directed to the "OUHCIRChromeExtension" folder and click "Select Folder", then you will see the tool extension is added in Chrome

#### 4. Sign up and login (for each user)

- go to http://127.0.0.1:8000/, click "Create a new account", input username and password (minimum length six numbers or characters)
- log in with the account on both the web page and the **extension**

#### 5. Ready to use!

- go to bing.com and start to search, the page html, query, click, mouse movement will be collected
- to review the collected data (require DB browser installed, https://download.sqlitebrowser.org/DB.Browser.for.SQLite-3.12.2-win64.msi), open the db file in the OUHCIR_annotation_platform folder, the task_manager_pagelog table contains the data for this study



### Limitations

1. This tool only works on Bing search, it will be better to set Bing as the default search engine
2. The pagelog data will be stored only when the page is closed, please notify users to close each page before closing Chrome
3. The clicked results belongs to the current query and SERP, searching with multiple queries without closing the previous SERP will lead to incorrect query-result connections



## Acknowledgement
This toolkit is modified from the original work: https://github.com/xuanyuan14/Web-Search-Field-Study-Toolkit
