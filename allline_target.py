#allline_target.py
#-*-coding:utf-8 -*-


def main():

    with open("ict/train_lmtd_cp", "r") as fi, open("ict/train_lmtd_ref", "r") as fr:
        nextline = fr.next()

        for line in fi:
            try:
                nextline = fr.next()
            except StopIteration:
                nextline = ""

            if line.startswith("#"):
                target_line = line.rstrip("\n")
                #fo.write(target_line)
                print target_line
            elif line == "\n":

                if nextline.startswith("#"):
                    #fo.write(line)
                    print ""
                else:
                    #fo.write("\n"+target_line)
                    print "\n"+target_line
            else:
                #fo.write(line)
                print line.rstrip("\n")


if __name__ == "__main__":
    main()
