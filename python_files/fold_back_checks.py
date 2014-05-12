import sys

# fold_back_checks.py
#
# This function takes two files, one of the reads in the VCF file that were
# not found in dbSNP and the other of the reads that were found in both COSMIC
# and dbSNP and then combines them into a single, ordered file.

__author__="John O'Leary <jco2119@columbia.edu>"
__date__ ="$Apr 4, 2014"

def usage():
    print """
        python fold_back_checks.py [./cosmic_queries/cosmic_query_names.txt] [./nondbsnp_vcfs/nondbsnp_vcf_names.txt]
        """

#this function handles the actual merging of the two data files
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
            
            #this is basically a switch hierarchy that covers all possible cases, written in reverse order
            #the last possible reads in either file will fall on the X and Y chromosomes, which cannot easily be compared with numeric values
            #as such, all possible combinations of X and Y chromosome reads have to be hardcoded in
            if a_parts[0] == b_parts[0]:
                if int(a_parts[1]) < int(b_parts[1]):
                    write_file.write(a)
                    a = cosmic_file.readline()
                else:
                    write_file.write(b)
                    b = nondbsnp_file.readline()
            elif a_parts[0][3:] == 'Y':
                write_file.write(b)
                b = nondbsnp_file.readline()
            elif b_parts[0][3:] == 'Y':
                write_file.write(a)
                a = cosmic_file.readline()
            elif a_parts[0][3:] == 'X':
                write_file.write(b)
                b = nondbsnp_file.readline()
            elif b_parts[0][3:] == 'X':
                write_file.write(a)
                a = nondbsnp_file.readline()
            #once we've handled all the X and Y combinations, it's simple to compare chromosome value
            elif int(a_parts[0][3:]) < int(b_parts[0][3:]):
                write_file.write(a)
                a = cosmic_file.readline()
            else:
                write_file.write(b)
                b = nondbsnp_file.readline()
    #if we have printed all the values in one file before the other, we can skip the switch hierarchy and simply print the rest of the values in the remaining file
    if a:
        print_rest(write_file, cosmic_file)
        nondbsnp_file.close()

    else:
        print_rest(write_file, nondbsnp_file)
        cosmic_file.close()
    write_file.close()
    print '%s and %s merged' % (cosmic_name, nondbsnp_name)

#this is a small function that handles printing all the rest of the values in a leftover file after the other has already been completely processed
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
    while cosmic_name:
        merge(cosmic_name, nondbsnp_name, name_file)
        cosmic_name = cosmic_files.readline()[:-1]
        nondbsnp_name = nondbsnp_files.readline()[:-1]
    print 'All files merged.' 

except IOError:
    sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
    sys.exit(1)