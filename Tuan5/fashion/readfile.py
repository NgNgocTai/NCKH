import json
file_path = 'outfits_info.json'

try:
  with open(file_path,"r") as file: #fileObject
    data = json.load(file)
    print(f"Số lượng object thu được : {len(data)}")
    count = 1
    for item in data:
      title = item["title"]
      numberOfProduct = len(item["detail"])
      print (f"Object thứ {count} có: " )
      print(f"{title}:{numberOfProduct} món hàng")
      count+=1
      print()
      
except FileNotFoundError:
  print("File not found")
except PermissionError:
  print("Permission denied")