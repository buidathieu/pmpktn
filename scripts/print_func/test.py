from .make_pdf import make_pdf

data = {
    "name": "Vương Kiến Thanh",
    "age": "20 tuổi",
    "gender": "nam",
    "address": "my example address " * 8,
    "diagnosis": "hen phế quản " * 15,
    "weight": "30",
    "height": "165",
    "linedrugs": [["amoxicillin 500mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                  ["paracetamol 500mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                  ["pectol", "Ngày uống 2 lần, lần 5 ml", "1 chai"],
                  ["carbocystein 200mg", "Ngày uống 3 lần, lần 1 gói", "15 gói"],
                  ["prednison 5mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                  ["duphalac 15mg", "Ngày uống 1 lần, lần 1 gói", "5 gói"]],
    "followup": "tái khám khi có gì lạ" + " x" * 200
}

make_pdf("test.pdf", data)
