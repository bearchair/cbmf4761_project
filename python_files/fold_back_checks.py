import sys

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 4, 2014"

def usage():
    print """
        python fold_back_checks.py [./cosmic_queries/cosmic_query_names.txt] [./nondbsnp_vcfs/nondbsnp_vcf_names.txt]
        """

def merge(cosmic_name, nondbsnp_name, name_file):
    
    #these are the files which have data to extract
    root_one = './cosmic_queries/'
    root_two = './nondbsnp_vcfs/'
    path_one = '%s%s' % (root_one, cosmic_name)
    path_two = '%s%s' % (root_two, nondbsnp_name)
    cosmic_file = file(path_one, "r")
    nondbsnp_file = file(path_two, "r")
    
    #this is the file that will be written to, once again, picking which name we pass in to splice is arbitrary (you can get tumor_name from either name that is passed in)
    name_parts = cosmic_name.split('_')
    tumor_name = '%s_%s' % (name_parts[0], name_parts[1])
    write_file_name = './final_vcfs/%s_final.vcf' % tumor_name
    write_file = open(write_file_name, "w")
    
    #create file name index
    name_file.write('%s_final.vcf\n' % tumor_name)
    
    a = cosmic_file.readline()
    b = nondbsnp_file.readline()
    while a and b:
        #include the headers regardless
        if a[0] == '#':
            write_file.write(a)
            a = cosmic_file.readline()
            b = nondbsnp_file.readline()
        #begin sort
        else:
            a_parts = a.split('\t')
            b_parts = b.split('\t')
            if int(a_parts[0][3:]) < int(b_parts[0][3:]):
                write_file.write(a)
                a = cosmic_file.readline()
            elif int(b_parts[0][3:]) < int(a_parts[0][3:]):
                write_file.write(b)
                b = nondbsnp_file.readline()
            else:
                if int(a_parts[1]) < int(b_parts[1]):
                    write_file.write(a)
                    a = cosmic_file.readline()
                else:
                    write_file.write(b)
                    b = nondbsnp_file.readline()
    if a:
        print_rest(write_file, cosmic_file)
        nondbsnp_file.close()

    else:
        print_rest(write_file, nondbsnp_file)
        cosmic_file.close()
    write_file.close()

def print_rest(f, remainder):
    l = remainder.readline()
    while l:
        f.write(l)
        l = remainder.readline()
    remainder.close()

if len(sys.argv)!= 3:
    usage()
    sys.exit(2)

try:
    cosmic_files = file(sys.argv[1],"r")
    nondbsnp_files = file(sys.argv[2],"r")
    #remove newlines
    cosmic_name = cosmic_files.readline()[:-1]
    nondbsnp_name = nondbsnp_files.readline()[:-1]
    name_file = open("./final_vcfs/final_vcf_names.txt", "w")
    #I assume both lists are same length. I also use a while loop as opposed to a for loop because I'm dealing with two lists.
    while cosmic_name:
        merge(cosmic_name, nondbsnp_name, name_file)
        cosmic_name = cosmic_files.readline()[:-1]
        nondbsnp_name = nondbsnp_files.readline()[:-1]

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)