datas = "23c22926-ac1e-41a7-99f5-3ad44d754633;honeydew;Modi sed amet dolore magnam. Volupt;c1a3d333-f73d-488b-a3d2-a7608fd77ad9;lemon;Magnam neque etincidunt sed;094004fb-03ef-4dc4-a94a-8802b2879c0c;honeydew;Dolore quaerat qua;e68c155-1125-47f2-ab07-5155657a3977;kiwi;Porro non nequ;"

# Memisahkan data berdasarkan ;
data_list = datas.split(';')

# Mengelompokkan data menjadi kelompok dengan tiga elemen
list_data = [data_list[i:i + 3] for i in range(0, len(data_list), 3)]

print(list_data)
