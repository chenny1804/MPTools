def read_param_file(filename):
    f=open(filename,"r")
    read_param_list=[]
    for line in f.readlines():
        read_param_list.append(line)
    f.close()
    return  read_param_list
def write_param(filename,string):
    f=open(filename,"a")
    f.write(string)
    f.flush()
    f.close()
def chang_power_index_format(string):
    # print string
    new_string=""
    for i in range(0,len(string),2):
        # print string[i:i+2]
        new_string=new_string+" "+str(int("0x"+string[i:i+2],16))
    print new_string
    return new_string
def TranslateTheIndex(filename):
    print filename
    read_param_list=read_param_file(filename)
    for line in read_param_list:
        if "TX_POWER" in line:
            new_string_list=line.split(":")[1].split("=")
            print new_string_list
            write_param("Trans_"+filename,"flash set "+new_string_list[0]+chang_power_index_format(new_string_list[1].split("\n")[0])+"\n")
            continue
        string=line.split(":")[1].replace("="," ")
        write_param("Trans_"+filename,"flash set "+string)

if __name__ == '__main__':
    TranslateTheIndex("1.txt")
