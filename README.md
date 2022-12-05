# [been_russia_bot](https://t.me/been_regions_russia_bot)
Telegram bot that allows user to see the map with the regions in Russia he/she has been to and some stats.

* The user gets a series of polls with regions to select for each federal district. Multiple answers are possible.  
* When done with the selection, the user gets the stats and the map with the regions he/she has been to.


![image](https://user-images.githubusercontent.com/104202715/204247374-2c6d4ede-295f-4a29-a687-9adcfc3f4539.png)
![image](https://user-images.githubusercontent.com/104202715/204247921-32c26647-3721-4f97-ba30-233d4725a5c8.png)

In order to deploy with Docker, input your telegram token and telegram id into envs below:
```
docker build -t been_russia_bot .
docker run -d --name been_bot \ 
           -e token='your_token' -e owner_id=your_tg_id \
           -v been_bot:/app/db been_russia_bot
```
