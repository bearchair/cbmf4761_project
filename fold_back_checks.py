import sys

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 4, 2014"

def usage():
    print """
        python fold_back_checks.py [cosmic_queries.txt] [init_vcf.txt]
        """

def merge(cosmic_file, vcf_list):
    a = cosmic_file.readline()
    b = vcf_list.readline()
    f = open("final_vcf.txt", "w")
    e = open("1_spots.txt", "w")
    while a and b:
        a_parts = a.split('\t')
        b_parts = b.split('\t')
        if int(a_parts[0]) < int(b_parts[0]):
            f.write(a)
            a = cosmic_file.readline()
            e.write(a)
        elif int(b_parts[0]) < int(a_parts[0]):
            f.write(b)
            b = vcf_list.readline()
            e.write(b)
        else:
            if int(a_parts[1]) < int(b_parts[1]):
                f.write(a)
                a = cosmic_file.readline()
                e.write(a)
            else:
                f.write(b)
                b = vcf_list.readline()
                e.write(b)
    if a:
        print_rest(f, cosmic_file)
    else:
        print_rest(f, vcf_list)
    f.close()

def print_rest(f, remainder):
    l = remainder.readline()
    while l:
        f.write(l)
        l = remainder.readline()

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    cosmic_file = file(sys.argv[1],"r")
    vcf_list = file(sys.argv[2],"r")
    merge(cosmic_file, vcf_list)

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)