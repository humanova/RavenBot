import zvz
import sheets
import drive

kills = ["https://albiononline.com/en/killboard/kill/48114601", 
"https://albiononline.com/en/killboard/kill/48182560", 
"https://albiononline.com/en/killboard/kill/48181212", 
"https://albiononline.com/en/killboard/kill/48179882", 
"https://albiononline.com/en/killboard/kill/48179806", 
"https://albiononline.com/en/killboard/kill/48190504", 
"https://albiononline.com/en/killboard/kill/48178231", 
"https://albiononline.com/en/killboard/kill/48176749", 
"https://albiononline.com/en/killboard/kill/48172475", 
"https://albiononline.com/en/killboard/kill/48173650", 
"https://albiononline.com/en/killboard/kill/48165282"]

print("Get player inventory data")
player_data = zvz.GetVictimsInventory(kills)

print("Reorganizing/Counting items")
items_data = zvz.GetTotalItems(player_data)

print("Creating Worksheet")
sheets.CreateZVZSheet('ZVZ#1', items_data, player_data)

print("Uploading Worksheet")
drive.UploadFile("sheets/ZVZ#1.xlsx")