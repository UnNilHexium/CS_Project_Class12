#   Project by UnNilHexium, TepicKid, WhiteDiger
#                UnNilHexium - Codebase, Debugging
#                TepicKid    - Idea, Synopsis
#                WhiteDiger  - Testing, Pitch
#                Gemini AI   - Teaching/Guidance/Code

import mysql.connector as m
from PIL import Image, ImageDraw, ImageFont

try:
    gamer_data = m.connect(host="localhost", user="root", password="")
except Exception:
    print("There was an error connecting to the database.")
    host = input("Please enter host: ")
    user = input("Please enter user: ")
    password = input("Please enter password: ")
    gamer_data = m.connect(host=host, user=user, password=password)

db_cur = gamer_data.cursor()

try:
    db_cur.execute("USE gamer_data")
except Exception:
    print("DB does not exist. Creating database...")
    db_cur.execute("CREATE DATABASE gamer_data")
    db_cur.execute("USE gamer_data")
  
def Create_Table():
    table = '''CREATE TABLE IF NOT EXISTS general_info (
        gamer_tag VARCHAR(20) PRIMARY KEY,
        Age INT,
        EXP INT,
        G_Perf VARCHAR(50),
        G_Like VARCHAR(50),
        G_Sec VARCHAR(50),
        G_story VARCHAR(50),
        G_Graph VARCHAR(50),
        Social_Discord VARCHAR(50),
        Social_Steam VARCHAR(50),
        Social_Youtube VARCHAR(50),
        Social_Other_Plat VARCHAR(50),
        Social_Other_UName VARCHAR(50)
    )'''
    db_cur.execute(table)



def Commit_to_Table(data):
    try:
        sql = '''INSERT INTO general_info 
                 (gamer_tag, Age, EXP, G_Perf, G_Like, G_Sec, G_story, G_Graph, 
                  Social_Discord, Social_Steam, Social_Youtube, Social_Other_Plat, Social_Other_UName) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        db_cur.execute(sql, data)
        gamer_data.commit()  
        print("Data successfully saved to the database!")
    except Exception as e:
        print("Error saving data: ", e)

def Input_Gamer_Data():
    Create_Table()
    gamer_tag = input("Please enter Your Gamer tag - ")
    Age = int(input("Please enter your current age - "))
    EXP = int(input("How long have you been gaming? "))
    G_Perf = input("Game that you play the best - ")
    G_Like = input("What game do you like the best - ")
    G_Sec = input("What is your \"alt\" game? ")
    G_story = input("What game do you think has the best story? ")
    G_Graph = input("What game do you think has the best graphics? ")
    Social_1 = input("Username on Discord - ")
    Social_2 = input("Username on Steam - ")
    Social_3 = input("Youtube Channel Name - ")
    Social_4_Plat = input("Another platform you are on - ")
    Social_4_UName = input("Username on said Platform - ")
    
    gamer_data_tuple = (
        gamer_tag, Age, EXP, G_Perf, G_Like, G_Sec, 
        G_story, G_Graph, Social_1, Social_2, Social_3, 
        Social_4_Plat, Social_4_UName
    )
    
    Commit_to_Table(gamer_data_tuple)

def Fetch_Game_Tag_Data():
    tag = input("What is the Gamer-Tag that you want to generate for?(cASe SenSiTiVE) ")
    db_cur.execute("select * from general_info where gamer_tag = %s", (tag,))
    result = db_cur.fetchone()
    if result == None:
        print("Tag not found. Exiting....")
        return 1
    return result

def Gen_Card(): 
    data = Fetch_Game_Tag_Data()
    if data == 1:
        return 1
    image = Image.new("RGB", (1920, 1080), (255, 255, 255))
    draw_obj = ImageDraw.Draw(image)

    (gamer_tag, age, exp, g_perf, g_like, g_sec, 
    g_story, g_graph, discord, steam, youtube, o_plat, o_uname) = data

    start_color = (216,236,209)
    end_color = (222, 176, 225)
    for i in range(1080):
        ratio = 1 - (i/1080)
        r=int(start_color[0] + ((end_color[0]-start_color[0])*ratio))
        g=int(start_color[1] + ((end_color[1]-start_color[1])*ratio))
        b=int(start_color[2] + ((end_color[2]-start_color[2])*ratio))
        
        draw_obj.line([(0, i), (1920, i)], fill=(r, g, b))
    
    f_title=ImageFont.truetype("")


    name = "%s Card.png" % data[0]
    image.save(name)
    print("Card successfully generated and saved as %s!" % name)

def Bring_gamer_data():
    db_cur.execute("Select * from general_info")
    print(db_cur.fetchall())


Gen_Card()