# msy-dashboard

The dashboard’s purpose and key insights:
The purpose of the dashboard is to provide Mai Shan Yun with a clear, data-driven overview of their restaurant operations by integrating ingredient usage, inventory supply, and sales performance data. It allows the owner to monitor trends, detect inefficiencies, and make informed business decisions. By visualizing how ingredients, especially meats, are used across menu items and analyzing October sales performance, the dashboard helps identify surpluses or shortages in meat inventory, optimize purchasing decisions, and project future profitability and scaling potential. Overall, the dashboard serves as a powerful tool for operational insight and strategic restaurant management.


Datasets used and how they were integrated:
For the meat variance calculations, the count of each menu item involving meat was added together from the October dataset. The percentage of meat sold is chosen by the user, and the count of each meal, depending on the type of meat, is calculated. The grams of beef, chicken, and pork used in each meal are taken from the ingredients dataset. The amount of these meats sold in lbs is then calculated using these values. The amount of chicken and beef purchased by the restaurant is taken from the shipments dataset. The amount of chicken and beef purchased monthly is then calculated.
We used the MSY ingredient dataset to create two plots, where one shows the frequency usage of ingredients across menu items, and the other shows the total amount of usage for each ingredient across the menu items.


Setup and run instructions:
Use the command “git clone https://github.com/bunnyirl/msy-dashboard” in the command prompt in a suitable file location
If it doesn’t work, please go to the repository, click “< > Code,” and then download the zip file
Once downloaded, extract the zip file
Please turn up the audio
Before opening files, download the following in the Command Prompt:
py -m pip install dash pandas plotly
Open the “app.py” file 
Run “python app.py” in the directory the file is in
Wait until terminal outputs: “Dash is running on http://127.0.0.1:8050/”
Click on “http://127.0.0.1:8050/” to view the dashboard
If you face an error while running the file, make sure you have done the following:
dash, pandas, and plotly downloaded.
All the files are in the same directory

Example insights or use cases:
Depending on the amount of meat purchased by the customers, there is usually a surplus of beef and chicken purchased by the restaurant.
Mai Shan Yun can project potential future scaling and profits based on the current fiscal year.

