    #   -*- coding: utf-8 -*-
    """
    Created on Sun Feb  2 11:24:42 2014
    
    @author: Siddharth Singal
    """
    
    # you may find it useful to import these variables (although you are not required to use them)
    from amino_acids import aa, codons
    from random import shuffle
    
    def collapse(L):
        """ Converts a list of strings to a string by concatenating all elements of the list """
        output = ""
        for s in L:
            output = output + s
        return output
    
    
    def coding_strand_to_AA(dna):
        """ Computes the Protein encoded by a sequence of DNA.  This function
            does not check for start and stop codons (it assumes that the input
            DNA sequence represents an protein coding region).
            
            dna: a DNA sequence represented as a string
            returns: a string containing the sequence of amino acids encoded by the
                     the input DNA fragment
        """
        # Initial return variable
        toReturn = ''
        
        # Iterate through every codon in the dna sequence
        for i in range(0,len(dna)/3):
            strand = dna[i*3:i*3+3]
            
            # Check the codon against each amino acid's corresponding codons
            for j in range(0,len(codons)):
                
                # Concatenate the correct amino acid to the return variable 
                if strand in codons[j]:
                    toReturn = toReturn + aa[j]
        
        # Return results
        return toReturn
        
    def coding_strand_to_AA_unit_tests():
        """ Unit tests for the coding_strand_to_AA function """
        
        print 'Unit tests for the coding_strand_to_AA function'
        
        # Set inputs and expected outputs
        inputs=['ATGCGA','ATGCCCGCTTT','CCCTGTGGAGCCACA','CCTAGTATGAAC','CATAAACAACAG']
        expoutputs=['MR','MPA','PCGAT','PSMN','HKQQ']
        
        # Find actual output and compare to expected output    
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+expoutputs[i]+', actual output: '+coding_strand_to_AA(inputs[i])
    
    def get_reverse_complement(dna):
        """ Computes the reverse complementary sequence of DNA for the specfied DNA
            sequence
        
            dna: a DNA sequence represented as a string
            returns: the reverse complementary DNA sequence represented as a string
        """
        
        # Initialize return variable
        toReturn = ''
        
        # Iterate through every nucleotide in the sequence, starting from the end
        n = len(dna)
        for i in range(0,n):
            code = dna[n-1-i]
            
            # Concatenance complementary nucleotide to return variable
            if code=='A':
                toReturn+='T'
            elif code =='T':
                toReturn+= 'A'
            elif code =='C':
                toReturn+= 'G'
            else:
                toReturn+='C'  
                
        # Return Results
        return toReturn
        
    def get_reverse_complement_unit_tests():
        """ Unit tests for the get_complement function """
            
        print 'Unit tests for the get_complement function'    
        
        #Set inputs and expected outputs    
        inputs=['ATGCGA','ATGCCCGCTTT','CCCTGTGGAGCCACA','CCTAGTATGAAC','CATAAACAACAG']
        expoutputs=['TCGCAT','AAAGCGGGCAT','TGTGGCTCCACAGGG','GTTCATACTAGG','CTGTTGTTTATG']
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+expoutputs[i]+', actual output: '+get_reverse_complement(inputs[i]) 
    
    def rest_of_ORF(dna):
        """ Takes a DNA sequence that is assumed to begin with a start codon and returns
            the sequence up to but not including the first in frame stop codon.  If there
            is no in frame stop codon, returns the whole string.
            
            dna: a DNA sequence
            returns: the open reading frame represented as a string
        """
        
        # Iterate through every codon in the sequence
        for i in range(0,len(dna)/3):
            code = dna[3*i:3*i+3]
            
            # Check to see if stop codon is reached. If so, return open reading frame
            if code=='TAG' or code=='TGA' or code=='TAA':
                return dna[0:3*i]
        
        # If no stop codon was found, return the input dna sequence
        return dna
        
    def rest_of_ORF_unit_tests():
        """ Unit tests for the rest_of_ORF function """
            
        print 'Unit tests for the rest_of_ORF function'
        
        # Set inputs and expected outputs
        inputs=['ATGTGAA','ATGCTGACATAGGCTAGCTAAGGTC','ATGGCAGCGAGCGAGCAGCGAC','ATGCGAGCTACGTCAGCGAACGACTAA']
        expoutputs=['ATG','ATGCTGACA','ATGGCAGCGAGCGAGCAGCGAC','ATGCGAGCTACGTCAGCGAACGAC']
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+expoutputs[i]+', actual output: '+rest_of_ORF(inputs[i]) 
            
    def find_all_ORFs_oneframe(dna):
        """ Finds all non-nested open reading frames in the given DNA sequence and returns
            them as a list.  This function should only find ORFs that are in the default
            frame of the sequence (i.e. they start on indices that are multiples of 3).
            By non-nested we mean that if an ORF occurs entirely within
            another ORF, it should not be included in the returned list of ORFs.
            
            dna: a DNA sequence
            returns: a list of non-nested ORFs
        """
        
        # Initialize codon index and return list
        i=0
        orfs = []
        
        # Keep checking codons until no more codons exist
        while i<len(dna)/3:
            
            # If start codon is found, find the open reading frame and add to return list
            if dna[3*i:3*i+3]=='ATG':
                orfs.append(rest_of_ORF(dna[3*i:]))
                
                # Change codon index to start at codon after last open reading frame
                i=i+(len(orfs[len(orfs)-1]))/3
            i=i+1
        
        # Return the final list
        return orfs
        
    def find_all_ORFs_oneframe_unit_tests():
        """ Unit tests for the find_all_ORFs_oneframe function """
        
        print 'Unit tests for the find_all_ORFs_oneframe function'
            
        # Set inputs and expected ouputs
        inputs=['ATGCATGAATGTAGATAGATGTGCCC','ATGCTAGCTAGCTAGCAT','ACTAGCATCGTACGA']
        expoutputs=[['ATGCATGAATGTAGA', 'ATGTGCCC'],['ATGCTAGCTAGC'],[]]
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+str(expoutputs[i])+', actual output: '+str(find_all_ORFs_oneframe(inputs[i]))
            
    def find_all_ORFs(dna):
        """ Finds all non-nested open reading frames in the given DNA sequence in all 3
            possible frames and returns them as a list.  By non-nested we mean that if an
            ORF occurs entirely within another ORF and they are both in the same frame,
            it should not be incl+uded in the returned list of ORFs.
            
            dna: a DNA sequence
            returns: a list of non-nested ORFs
        """
        # Initialize the return list
        allORFs = []
        
        # Iterate through each of three offset positions of dna sequence
        for i in range(3):
            allORFs.extend(find_all_ORFs_oneframe(dna[i:]))
            
        # Return all ORFs found among all offsets
        return allORFs
    
    def find_all_ORFs_unit_tests():
        """ Unit tests for the find_all_ORFs function """
        
        print 'Unit tests for the find_all_ORFs function'
        
        # Set inputs and expected outputs
        inputs=['ATGCATGAATGTAG','GATCGATATGCAGTATGCGTAGTAATGACGTATAGATTGATAA','TAGCATSCGATGCGTACGATCGATAATGCAGTACGAATTCGATCGTAAAATGATGCGATG']
        expoutputs=[['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG'],['ATGACGTATAGATTGATAA', 'ATGCAGTATGCG', 'ATGCGTAGTAATGACGTA'],['ATGCGTACGATCGATAATGCAGTACGAATTCGATCG', 'ATG', 'ATGCAGTACGAATTCGATCGTAAAATGATGCGATG']]
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+str(expoutputs[i])+', actual output: '+str(find_all_ORFs(inputs[i]))
            
    def find_all_ORFs_both_strands(dna):
        """ Finds all non-nested open reading frames in the given DNA sequence on both
            strands.
            
            dna: a DNA sequence
            returns: a list of non-nested ORFs
        """
        
        # Initialize return list
        allORFs = []
        
        # Add all ORFs from dna sequence and its reverse complement to return list
        allORFs.extend(find_all_ORFs(dna))
        allORFs.extend(find_all_ORFs(get_reverse_complement(dna)))
        
        # Return all ORFs found
        return allORFs
        
    
    def find_all_ORFs_both_strands_unit_tests():
        """ Unit tests for the find_all_ORFs_both_strands function """
    
        print 'Unit tests for the find_all_ORFs_both_strands function'
        
        # Set inputs and expected outputs
        inputs=['ATGCGAATGTAGCATCAAA','GATCGATATGCAGTATGCGTAGTAATGACGTATAGATTGATAA','TAGCATSCGATGCGTACGATCGATAATGCAGTACGAATTCGATCGTAAAATGATGCGATG']
        expoutputs=[['ATGCGAATG', 'ATGCTACATTCGCAT'],['ATGACGTATAGATTGATAA', 'ATGCAGTATGCG', 'ATGCGTAGTAATGACGTA'],['ATGCGTACGATCGATAATGCAGTACGAATTCGATCG', 'ATG', 'ATGCAGTACGAATTCGATCGTAAAATGATGCGATG', 'ATGCTA']]
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+str(expoutputs[i])+', actual output: '+str(find_all_ORFs_both_strands(inputs[i]))
    
    def longest_ORF(dna):
        """ Finds the longest ORF on both strands of the specified DNA and returns it
            as a string"""
        
        # Find all ORFs in the dna sequence and store it
        allORFs = find_all_ORFs_both_strands(dna)
        
        # Keep track of the largest ORF and its index in the ORF list
        maxSize = -1
        maxInd = -1
        
        # Iterate through each ORF
        for i in range(len(allORFs)):
            
            # If the ORF is biggest than the longest stored ORF, then store the ORF
            if len(allORFs[i])>maxSize:
                maxInd = i
                maxSize = allORFs[i]
        
        # Return the longest ORF
        if maxInd != -1:
            return allORFs[maxInd]
        else:
            return ''
                
    def longest_ORF_unit_tests():
        """ Unit tests for the longest_ORF function """
            
        print 'Unit tests for the longest_ORF function'
        
        # Set inputs and expected outputs
        inputs=['ATGCGAATGTAGCATCAAA','GATCGATATGCAGTATGCGTAGTAATGACGTATAGATTGATAA','TAGCATSCGATGCGTACGATCGATAATGCAGTACGAATTCGATCGTAAAATGATGCGATG']
        expoutputs=['ATGCTACATTCGCAT','ATGACGTATAGATTGATAA','ATGCGTACGATCGATAATGCAGTACGAATTCGATCG']
        
        # Find actual output and compare to expected output
        for i in range(0,len(inputs)):
            print 'input: '+inputs[i]+', expected output: '+expoutputs[i]+', actual output: '+longest_ORF(inputs[i]) 
    
    def longest_ORF_noncoding(dna, num_trials):
        """ Computes the maximum length of the longest ORF over num_trials shuffles
            of the specfied DNA sequence
            
            dna: a DNA sequence
            num_trials: the number of random shuffles
            returns: the maximum length longest ORF """
        
        # Convert dna sequence into a list
        dnaarr = list(dna)
        
        # Initialize the largest number of nucleotides in an ORF found
        maxnum = -1
    
        # Iterate through every trial, shuffling the dna sequence each trial
        for i in range(0,num_trials):
            shuffle(dnaarr)
            
            # If longest ORF is larger than largest stored ORF, then store longer ORF
            trialnum = len(longest_ORF(''.join(dnaarr)))
            if trialnum>maxnum:
                maxnum=trialnum
                
        # Return number of codons of longest ORF
        return maxnum/3
    
    def gene_finder_func(dna, threshold):
        """ Returns the amino acid sequences coded by all genes that have an ORF
            larger than the specified threshold.
            
            dna: a DNA sequence
            threshold: the minimum length of the ORF for it to be considered a valid
                       gene.
            returns: a list of all amino acid sequences whose ORFs meet the minimum
                     length specified.
        """
        
        #Store all ORFs found in dna
        all_ORFs = find_all_ORFs_both_strands(dna)
        
        #Initialize return list
        threshold_ORFs = []
        
        #Iterate through each ORF's amino acid representation
        for ORF in all_ORFs:
            amin = coding_strand_to_AA(ORF)
            
            #Only add amino acid sequence to return list if it is smaller than threshold
            if len(amin) <= threshold:
                threshold_ORFs.append(amin)
        
        return threshold_ORFs
        
    # Run these unit tests if this module is executed
    if __name__ == "__main__":
        coding_strand_to_AA_unit_tests()
        get_reverse_complement_unit_tests()
        rest_of_ORF_unit_tests()
        find_all_ORFs_oneframe_unit_tests()
        find_all_ORFs_unit_tests()
        find_all_ORFs_both_strands_unit_tests()
        longest_ORF_unit_tests()
