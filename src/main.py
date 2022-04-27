from habanero import Crossref
import bibtexparser as bib
import numpy as np
import Levenshtein as Ls
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import argparse
def main_bib():
    cr = Crossref()
    nsearch=5
    
    parser = argparse.ArgumentParser(description= "Utility for adding DOI to bibtex items in .bib file uning CrossRef")
    parser.add_argument("input",help="Input .bib file")
    parser.add_argument("-v","--verbose",help="Use verbose output",action="store_true",default=False)
    parser.add_argument("-o","--output",help="The output .bib",default="bibtex.bib")
    parser.add_argument("-n","--nsearch",help="Set the search depth for matches on CrossRef",default=5,type=int)
    args = parser.parse_args()
    inp=args.input
    verbose=args.verbose
    output=args.output
    nsearch=args.nsearch
    
    fails=[]
    
    def yes_or_no(question):
        reply = str(input(question+' (y/n): ')).lower().strip()
        if len(reply)==0:
            return yes_or_no("Uhhhh... please enter ")
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return yes_or_no("Uhhhh... please enter ")
        
        
    with open(inp) as bibtex_file:
        bib_database = bib.load(bibtex_file)
        bibitems=bib_database.entries
        
        
    for i in range(len(bibitems)):
        # do the query
        title=bibitems[i]['title']
        author=bibitems[i]['author'].split("and")[0]
        
    
        if 'doi' in bibitems[i]:
            continue
        q=cr.works(query_bibliographic = title)

        # Empty ratiolist 
        ratios=np.zeros(nsearch)

        for j in range(nsearch):
        
            ratios[j]=Ls.ratio(q['message']['items'][j]['title'][0].lower(),title.lower())

        if np.max(ratios)<0.80: 
            if verbose:
                print("\033[1m"+title+":\033[91m No Match! \033[0m")
            match=False
        
        elif np.max(ratios)<0.99:
            ids=np.where(ratios==np.max(ratios))[0][0]
            first_author=q['message']['items'][ids]['author'][0]['family']+", "+q['message']['items'][ids]['author'][0]['given']
            
            print("Possible match found:")
            print("\033[92mSearched:\033[1m "+title+", "+author+"...\033[0m")
            print("\033[96mFound   :\033[1m "+q['message']['items'][ids]['title'][0]+", "+first_author+"...\033[0m")
            match=yes_or_no("Is it a match?")
        else:
            ids=np.where(ratios==np.max(ratios))[0][0]
            match = True
            if verbose:
                print("\033[1m"+title+':\033[92m Match!\033[0m')

        if match:
            DOI=q['message']['items'][ids]['DOI']
            bibitems[i]['doi']=DOI
            
        if not match:
            fails.append(title)

    db = BibDatabase()
    db.entries = bibitems

    writer = BibTexWriter()
    with open(output, 'w') as bibfile:
        bibfile.write(writer.write(db))
    if len(fails)>0:
        print('')
        print("Unable to match the following:")
        for i in range(len(fails)):
            print(fails[i])


if __name__=='__main__':
    main_bib()
        
