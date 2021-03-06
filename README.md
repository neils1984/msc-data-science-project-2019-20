# msc-data-science-project-2019-20-files-nscriv01
msc-data-science-project-2019-20-files-nscriv01 created by GitHub Classroom

#### Data
The MySQL database dump and images used in this project are too large to upload to GitHub. They are hosted separately on Google Drive here:
https://drive.google.com/file/d/1u5eNmx_OlObpPYuROsHjc_GrjkuLQs4E/view?usp=sharing

Note:
The database contains the raw data in separate tables as well already merged results of running `merge_data.py` in the `train_data` and `test_data` tables
and the cleaned data after `exploration_cleaning.py` has been run (`train_cleaned` and `test_cleaned` tables).
The images are returned by `get_map-images.py`

#### Config
The notebooks and py scripts use a SQLAlchemy engine that is created in the file config.py - this file is not present in the repository as it contains usernames
and passwords. Once the data has been loaded to a MySQL database you will need to create a config.py that instantiates a SQLAlchemy engine (or other SQL connection
that is compatible with the Pandas API) to connect to your MySQL database with your own login credentials.

#### Notebooks
Some of the notebooks require data and files such as `.pkl` files that are produced by other notebooks. The files were intended to run in the following order:
1. (`get_map_images.py`) (see note in *Data* section)
1. (`merge_data.py`) (see note in *Data* section)
1. (`exploration_cleaning.ipynb`) (see note in *Data* section)
1. `baseline_models.ipynb`
1. (`resize_images.py`)*
1. `image_data_prepration.ipynb`
1. `features_model_selection.ipynb`
1. `final_models.ipynb`

\*The 600 x 600 pixel images are hosted on Google Drive. During training the images needed to be resized to 128 x 128 pixels. This can be done at any point before
`image_data_preparation.ipynb` is run.

#### Paths
Note that paths will likely need updating to save and read the files the notebooks produce.
