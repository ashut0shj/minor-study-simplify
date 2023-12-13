dic = {}

def pdfgen(dic):
    file = open(r"flashes.txt","w+")

    for topic in dic:
        file.write("\n"+topic+"\n")
        for line in dic[topic]:
            file.write("    --> "  + line+"\n")
       
    file.close()