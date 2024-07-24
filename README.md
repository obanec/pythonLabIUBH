# Ideal Function Selector
This project uses Python to select ideal functions based on training data, test data, and provided ideal functions. It utilizes a SQLite database to store the data and Bokeh for visualization.

## Project Summary

The goal of this project is to develop a Python program that:
1. Loads training data, test data, and ideal function data from CSV files.
2. Stores the data in a SQLite database.
3. Selects the four best-fit ideal functions for the training data by minimizing the sum of squared deviations (least-squares method).
4. Maps the test data to the selected ideal functions, ensuring that the maximum deviation does not exceed a specified threshold.
5. Visualizes the training data, ideal functions, and test results using Bokeh.

# To work on this project
## Clone the repository and switch to the develop branch
git clone https://github.com/obanec/pythonLabIUBH
cd your_repository_folder
git checkout develop

## Create a new branch for the changes
git checkout -b feature/new-function

## Make changes and commit
git add .
git commit -m "Added new function"

## Push the new branch to the remote repository
git push origin feature/new-function

## Create a Pull Request on GitHub to merge changes into develop

## After the PR is merged, update the local develop branch
git checkout develop
git pull origin develop
