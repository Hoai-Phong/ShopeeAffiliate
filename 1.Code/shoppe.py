import csv

# Đường dẫn tới file CSV
file_path = "ao_nu_hot__ban_chay.csv"
# Đường dẫn tới file TXT để lưu kết quả
output_file = "LinkShoppe/ao_nu_hot__ban_chay.txt"

# Mở và đọc file CSV
with open(file_path, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Mở file TXT để ghi
    with open(output_file, mode="w", encoding="utf-8") as txt_file:
        # Ghi tiêu đề
        txt_file.write("Tên sản phẩm,Link ưu đãi\n")
        
        # Duyệt qua từng dòng và ghi dữ liệu
        for row in csv_reader:
            ten_san_pham = row["Tên sản phẩm"].strip()
            link_uu_dai = row["Link ưu đãi"].strip()
            txt_file.write(f"🎋 {ten_san_pham} {link_uu_dai}\n")

print(f"Dữ liệu đã được lưu vào file {output_file}")



