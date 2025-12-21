SETUP GUIDE
1. Go to https://console.cloud.google.com/welcome
2. Make a project on the top left corner
3. Click the 3 dashes in the top left corner 
4. Click "APIs & Services" on the side dashes.
5. Click on "Library" on the left side of the screen.
6. Scroll down and click on YouTube Data API v3
7. Click "Enable"
8. Wait for it to finish enabling
9. It should have opened to the service details of the youtube API, if it didnt, click "Manage"
10. Click on "Credentials" on the left side of the screen.
11. Click on the "Create Credentials" button on the center-left middle-top region of the screen.
12. Click "API key" after it drops down from the Creat Credentials button
13. Click "Create" on the Bottom Right corner
14. Copy the created API key
15. Clone the repo using: 

git clone https://github.com/iliketheinternet223/custom-media-player.git
cd custom-media-player

16. Run Main.py, it should create an empty .env file on the root folder(where it was installed)
17. The file should have YOUTUBE_KEY=, if it doesnt, copy it from below

YOUTUBE_KEY=

18. WITHOUT ANY SPACES SEPARATING YOUTUBE_KEY=, paste your Youtube key and press any button on the cmd. Do not worry if you accidentally misclicked, just open it again and it should detect it. Below is an example of how it should look:

YOUTUBE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

19. Run Main.py. It should automatically install any libraries you dont have. If you dont have pip, thats not my problem.
20. That SHOULD be it. Open an issue if you have any problems.
