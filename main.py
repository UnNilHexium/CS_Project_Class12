import mysql.connector as m
from PIL import Image, ImageDraw, ImageFont
import textwrap

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

def draw_mixed_text(draw_obj, pos, text, font_main, font_num, fill):
    x, y = pos
    text_str = str(text)
    if not text_str:
        return
    current_chunk = ""
    is_num_chunk = text_str[0].isdigit()
    for char in text_str:
        char_is_num = char.isdigit()
        if char_is_num == is_num_chunk:
            current_chunk += char
        else:
            font = font_num if is_num_chunk else font_main
            draw_obj.text((x, y), current_chunk, fill=fill, font=font)
            bbox = font.getbbox(current_chunk)
            if bbox:
                x += (bbox[2] - bbox[0])
            current_chunk = char
            is_num_chunk = char_is_num
    if current_chunk:
        font = font_num if is_num_chunk else font_main
        draw_obj.text((x, y), current_chunk, fill=fill, font=font)

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
    
    f_title=ImageFont.truetype("/workspaces/CS_Project_Class12/fonts/titlefont.ttf", 60)
    f_body_alt=ImageFont.truetype("/workspaces/CS_Project_Class12/fonts/bodyfont.ttf", 36)
    f_body=ImageFont.truetype("/workspaces/CS_Project_Class12/fonts/bodyalt.ttf",36)
    f_num=ImageFont.truetype("/workspaces/CS_Project_Class12/fonts/numberfont.ttf",36)
    t_color = (0,0,0)

    title_text = "GAMER CARD: %s" % gamer_tag.upper()
    
    bbox = f_title.getbbox(title_text)
    text_width = bbox[2] - bbox[0]
    title_x = (1920 - text_width) // 2
    title_y = 60
    
    draw_obj.text((title_x, title_y), title_text, fill=t_color, font=f_title)

    draw_obj.line([(150, 150), (1770, 150)], fill=t_color, width=4)

    col1_x = 150
    col1_y = 200

    draw_obj.text((col1_x, col1_y), "[ PLAYER STATS & GAMES ]", fill=t_color, font=f_body_alt)
    col1_y += 60

    stats_list = [
        "Age: %s" % age,
        "Gaming EXP: %s years" % exp,
        "Best Game: %s" % g_perf,
        "Favorite Game: %s" % g_like,
        "Secondary Game: %s" % g_sec,
        "Best Story: %s" % g_story,
        "Best Graphics: %s" % g_graph
    ]

    for item in stats_list:
        wrapped_lines = textwrap.wrap(item, width=32)
        for line in wrapped_lines:
            draw_mixed_text(draw_obj, (col1_x, col1_y), line, f_body, f_num, t_color)
            col1_y += 42
        col1_y += 12  

    col2_x = 1050
    col2_y = 200

    draw_obj.text((col2_x, col2_y), "[ SOCIAL PROFILES ]", fill=t_color, font=f_body_alt)
    col2_y += 60

    socials_list = [
        "Discord: %s" % discord,
        "Steam: %s" % steam,
        "YouTube: %s" % youtube
    ]
    
    if o_plat and o_uname:
        extra_social = "%s: %s" % (o_plat, o_uname)
        socials_list.append(extra_social)

    for item in socials_list:
        wrapped_lines = textwrap.wrap(item, width=28)
        for line in wrapped_lines:
            draw_mixed_text(draw_obj, (col2_x, col2_y), line, f_body, f_num, t_color)
            col2_y += 42
        col2_y += 12

    name = "%s Card.png" % data[0]
    image.save(name)
    print("Card successfully generated and saved as %s!" % name)

def Bring_gamer_data():
    db_cur.execute("Select * from general_info")
    print(db_cur.fetchall())
def iteration():
    print("Welcome to CardGen.Co, where you can make yourself a Business Card, But for gamers.")
    print('''You can -
    1. Add an entry of your username to the database(A)
    2. Inspect all entries(I)
    3. Generate your very own Gamer Card(G) ''')
    action = input("What would you like to do? ").lower()
    if action == 'a':
        Input_Gamer_Data()
        return 0
    elif action == 'i':
        Bring_gamer_data()
        return 0
    elif action == 'g':
        Gen_Card()
        return 0
    else: 
        print('please select valid operation')
        return iteration()

def main():
    Again = ''
    while True:
        iteration()
        Again = input("Go again ? (Enter)\nStop? (s)").lower
        if Again == 's':
            break

main()