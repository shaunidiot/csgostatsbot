#!/usr/bin/env python3

'''
CSGO_STATS_BOT Source Code
BETA v0.12 7/29/2014
Created by: Quack Lord

How it works:
The bot scrapes HLTV.org for certain entries about various players in
a post or when summoned with +/u/CSGO_STATS_BOT. It then saves the ID
of every post/comment to a text file so it will not comment to the
same one twice, preventing spam. Since HLTV.org doesn't neatly create
a list of players for me, I had to do it myself with update_Playerlist().
The rest of how it works is explained in comments.

I am going to give a brief explanation of what everything does rather
than how I do it because I don't have the time to do that. If you have
any question on HOW or WHY I did something, pm me @ /u/CSGO_STATS_BOT.

Feel free to use/modify this code in anyway you wish except for the
reproducing my bot. (i.e I don't want 2 of my bot running around) If
you come up with a major change, features, etc that you add to this bot
please send me the source code and I will add it in and give you credit
where deserved.
'''

print("test")

import sys
import time
import praw
import requests
from urllib.request import Request, urlopen
from time import gmtime, strftime
from pprint import pprint

print(sys.version_info)

version = "v1.1"

#Creates a list of every player in HLTV.org by going through every ID 1-8410 to
#check if the name is not N/A and they have played more than 1 map. If their name
#is N/A or they haven't played a map, it adds a line N/A in the text file, otherwise
#it adds their name. This will be used later.
def update_Playerlist(): 
    i = file_len("/usr/local/sbin/cronjobs/csgostatsbot/PlayerIDs.txt")
    for b in range (1, 841-int(i/10)):
        with open("PlayerIDs.txt","a") as f:
            for c in range (1, 11):
                i = i+1
                url = "http://www.hltv.org/?pageid=173&playerid="+str(i)+"&eventid=0&gameid=2"
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                text = str(urlopen(req).read())

                text = str(response.read())
                index = text.index("Player stats: ")+14
                name = text[index:].split(" ")[0]
                index = text.index("Maps played")+126
                maps = int(text[index:index+1])
                if name != "N/A" and maps > 0:
                     f.write(name+"\n")
                     print(str(i)+"- " + name+":"+str(maps))
                else:
                    f.write("N/A\n")
                    print(str(i)+"- " +"N/A")


def create_PlayerList(entries):
    with open("/usr/local/sbin/cronjobs/csgostatsbot/PlayerIDs.txt","r+") as f:
        for i in range(len(entries)):
            f.write(entries[i])
            
#Opens the text file created by update_Playerlist() and adds every name to a list,
#the reason I had to have the N/A in the text file was so that here it would keep
#the player's ID associated with them. 
def getPlayers():
    players = []
    with open("/usr/local/sbin/cronjobs/csgostatsbot/PlayerIDs.txt") as f:
        for line in f:
            players.append(line.replace("\n",""))
    return players

#Simply gets the number of lines in a file.
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#Modified bubble sort I used to sort the players by ranking. I had to have 3 arrays:
#Player names: Stored the name of every player
#Player Ratings: Stored the rating of every player
#Indexes: created in the sort to keep track of where every player moved to.
def bubble_sort(arr1,arr2):
    indexes = []
    for i in range(0, len(arr1)):
        indexes.append(i)
    unsorted = True
    while unsorted:
        unsorted = False
        for i in range(1,len(arr1)):
            if arr2[i] > arr2[i-1]:                
                temp = arr2[i]
                arr2[i] = arr2[i-1]
                arr2[i-1] = temp
                
                temp = arr1[i]
                arr1[i] = arr1[i-1]
                arr1[i-1] = temp

                temp = indexes[i]
                indexes[i] = indexes[i-1]
                indexes[i-1] = temp
                
                unsorted = True
    return indexes

#Gets the player infor for every player in list inPost. The data points it gathers
#are K/D ratio, Rounds played, Average Kills, Team, HLTV rating, profile URL, Team URL.
#I used a VERY crude way of scraping the site for the data I needed. I can't go into
#detail without dragging on forever, so PM if you want to know the HOW/WHY behind it.
#Then it starts to put together the response with a lot of formatting and the data found.
#It calls the bubble_sort method to determine the order of the people in the post.
def get_player_info(inPost):
    Reply = "Player Name | Primary Team | Total K/D | K/D Ratio | Kills per round | More\n"+":----------|:------------|:------------|:---------|:---------------|:-----:\n"
    KDs = []
    Rounds = []
    AverageKills = []
    Team = []
    TeamURLs = []
    Ratings = []
    URLs = []
    TotalKills = []
    TotalDeaths = []
        
    for i in range (0, len(inPost)):
        url = "http://www.hltv.org/?pageid=173&playerid="+str(inPost[i].split("|")[0])+"&eventid=0&gameid=2"
        print(url)

        r=requests.get(url)
        r.headers
        {
            'User-Agent': 'Mozilla/5.0'
        }
        text = str(r.text)
               
        URLs.append(url)
            
        index = text.index("K/D Ratio")+124
        index2 = text[index:].index("</div>")
        KDs.append(text[index:index+index2])
            
        index = text.index("Rounds played")+128
        index2 = text[index:].index("</div>")
        Rounds.append(text[index:index+index2])

        index = text.index("Average kills per round")+138
        index2 = text[index:].index("</div>")
        AverageKills.append(text[index:index+index2])

        index = text.index("Rating <a href")+259
        index2 = text[index:].index("</div>")
        Ratings.append(float(text[index:index+index2]))

        index = text.index("Primary team:")+129
        index = index + text[index:].index(">")+1
        index2 = text[index:].index("</a>")
        Team.append(text[index:index+index2])

        index = text.index("Primary team:")+138
        index2 = text[index:].index("\"")
        TeamURLs.append("http://www.hltv.org"+text[index:index+index2].replace("&amp;","&"))
        
        index = text.index("Total kills")+126
        index2 = text[index:].index("</div>")
        TotalKills.append(text[index:index+index2])

        index = text.index("Total deaths")+127
        index2 = text[index:].index("</div>")
        TotalDeaths.append(text[index:index+index2])

        print(text[index:index+index2]);    
    if len(inPost) > 0:
        indexes=bubble_sort(inPost,Ratings)
        for i in range(0, len(inPost)):
           # print(str(Ratings[i]) + " " + inPost[i]) 
            Reply = Reply + inPost[i].split("|")[1] + "(["+str(Ratings[i])+"](http://www.hltv.org/?pageid=242)) | [" + Team[indexes[i]] + "]("+TeamURLs[indexes[i]]+") | " + TotalKills[indexes[i]] + "/" + TotalDeaths[indexes[i]] + " | " + KDs[indexes[i]] + " | " + AverageKills[indexes[i]] + " | [HLTV](" + URLs[indexes[i]] + ")\n"
        Reply = Reply + "^Players ^ordered ^by ^rating ^on ^HLTV.org  \n\n**^DISCLAIMER:** *^Some ^players ^may ^not ^appear ^because ^there ^are ^no ^stats ^for ^them ^on ^HLTV. ^These ^stats ^may ^be ^biased ^due ^to ^factors ^such ^as: ^teams ^played, ^games ^played, ^etc.. ^Please ^do ^more ^research ^before ^you ^bet ^as ^this ^bot ^is ^not ^responsible ^for ^your ^bets.*\n\n ^Questions? ^Comments? ^Improvements? ^Bugs? ^Let ^me ^know [^on ^this ^bot's ^thread!](http://www.reddit.com/r/csgobetting/comments/2byr6w/player_stats_bot_for_this_subreddit/)\n\n *^Current ^Version: ^" + version + "* [^source](http://pastebin.com/RX8z1HCu) ^| [^Bot ^Status ^Google ^Chrome ^extension](http://www.reddit.com/r/csgobetting/comments/2ebf6k/google_chrome_extension_for_csgl_trade_status/)"
        Reply = Reply + "\n\n **^Streamer ^of ^the ^week: ^[tarik](https://twitch.tv/tarik_tv) ^((Team CLG)^)**"
        Reply = Reply + "\n\n *^(Please PM me with who you think should be next week's streamer of the week!)*"
        return Reply
    
#Stores comment ID to a text file so it doesn't double post.
def store_comment_ID(comment):
    with open("/usr/local/sbin/cronjobs/csgostatsbot/CommentIDs.txt", "a") as f:
        f.write(comment.id+"\n")

#Stores post ID to a text file so it doesn't double post. 
def store_submission_ID(submission):
    with open("/usr/local/sbin/cronjobs/csgostatsbot/SubmissionIDs.txt", "a") as f:
        f.write(submission.id+"\n")

#Checks to see if the supplied comment ID has been replied to yet.
def check_comment_ID(cid):
    with open("/usr/local/sbin/cronjobs/csgostatsbot/CommentIDs.txt") as f:
        for line in f:
            if cid in line:
                return False
    return True

#Checks to see if the supplied post ID has been replied to yet.
def check_submission_ID(sid):
    with open("/usr/local/sbin/cronjobs/csgostatsbot/SubmissionIDs.txt") as f:
        for line in f:
            if sid in line:
                return False
    return True   

#returns csgl bot's status
#def bot_status():
  #  url = "http://www.csgolounge.com/status"
  #  r=requests.get(url)
  #  r.headers
   # {
   #      'User-Agent': 'Mozilla/5.0'
  #  }
  #  text = str(r.text)
   # if "BOTS ARE OFFLINE" in text:
   #     return "offline"
   # return "online"
    
#Main method:
#Logs into reddit and gets the newest 20 posts to check through.
#First it will check for posts with the flair 'Match' so that it only
#goes to matches that haven't been finished yet. It checks the selftext
#for names and then saves them to a list and send them up to get_player_info()
#Next it goes to comments, searching any of the newest 20 posts for the
#+/u/CSGO_STATS_BOT summon. Once it finds the summon, it will search the
#same way it does the post. Then both post the replies.

#update_Playerlist() 
r = praw.Reddit('Counter Strike:Global Offensive player stats bot version: ' + version)
r.login("CSGO_STATS_BOT","PasswordHere")
already_done = set()
players = getPlayers()
#create_PlayerList(players)
print ("Bot logged in...")

subreddit = r.get_subreddit('csgobetting')
subs = [];
subs.append(r.get_submission(submission_id="2byr6w"))
for submission in subreddit.get_new(limit=10):
    subs.append(submission)
    
subreddit = r.get_subreddit('CSGOanalyses')
for submission in subreddit.get_new(limit=10):
    subs.append(submission)
    
for submission in subs:
    inPost = []
    #Each Post
    if submission.link_flair_text == "Match" and check_submission_ID(submission.id) and "|" in submission.title:
            text = str(submission.selftext).replace(","," ").encode("utf-8").lower().split()
            for i in range (0, len(players)):
                player = str(players[i]).encode("utf-8").lower()
                if player in text and players[i] != "N/A" and players[i] not in inPost:
                    print("Found "+players[i]+"(#"+str(i+1)+") in the post!")
                    inPost.append(str(i+1)+"|"+players[i])
            try:
                submission.add_comment(get_player_info(inPost))
                store_submission_ID(submission)
            except Exception as e:
                print("Error! not posting(post) " + submission.id)
                print(str(e))
                pass
            
    #Each comment
    submission.replace_more_comments(limit=25, threshold=1)
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:
            inComment = []
            text = comment.body.replace(","," ").lower().split()
            if "+/u/csgo_stats_bot" in text and check_comment_ID(comment.id):
                    for i in range (0, len(players)):
                            player = players[i].lower()
                            if player in text and players[i] != "N/A" and players[i] not in inComment:
                                    print("Found "+players[i]+"(#"+str(i+1)+") in a comment!")
                                    inComment.append(str(i+1)+"|"+players[i])
                    if len(inComment) > 0:
                            comment.reply(get_player_info(inComment))
                            store_comment_ID(comment)
          #  if "bot" in text and "status" in text and check_comment_ID(comment.id):
             #   /comment.reply("The bots are currently " + bot_status() + " as of " + datetime.datetime.now().time() + " EST.")
              #  store_comment_ID(comment)
print("done.")