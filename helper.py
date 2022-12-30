# DO NOT EDIT HERE ONWARDS
def function(dn_wknd, dn_fri, dn_wkday, no_wknd, no_fri, no_days_in_month, dont_give_wknd_or_fri):
    
    for name in dont_give_wknd_or_fri:
        #add ASICs to the back of the list of dn_wknd, so that they won't be allocated fridays, if that is possible
        if name in dn_wknd:
            dn_wknd.remove(name)
            dn_wknd.append(name)
        #in case you accidentally put ASICS into dn_wkday or dn_fri (instead of dn_wknd), then this will remove them from dn_wkday/dn_fri and add them to dn_wknd
        elif name in dn_wkday:
            dn_wkday.remove(name)
            dn_wknd.append(name)
        elif name in dn_fri:
            dn_fri.remove(name)
            dn_wknd.append(name)
    
    no_wkday = [i+1 for i in range(no_days_in_month) if i not in no_wknd+no_fri]
    
    do_wknd = []
    do_fri = []
    do_wkday = [] 
    
    # all those who did weekday will do weekend. any leftover do friday. still leftover, do weekday. any less, do weekend
    do_wknd = dn_wkday[:len(no_wknd)]
    do_fri = dn_wkday[len(no_wknd):len(no_wknd)+len(no_fri)]  
    do_wkday = dn_wkday[len(no_wknd)+len(no_fri):len(no_wknd)+len(no_fri)+len(no_wkday)]
    
    """
    print(len(do_wknd))
    print(len(do_fri))
    print(len(do_wkday))
    """
    #all those who did fridays will first fill up weekends. if leftover, fill up friday. if still left, fill up weekday
    old_do_wknd = do_wknd.copy()
    do_wknd.extend(dn_fri[:len(no_wknd) - len(old_do_wknd)])
    
    old_do_fri = do_fri.copy()
    do_fri.extend(dn_fri[len(no_wknd) - len(old_do_wknd):len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri)])
    
    old_do_wkday = do_wkday.copy()
    do_wkday.extend(dn_fri[len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri):len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri) + len(no_wkday) - len(old_do_wkday)])
    
    """
    print(len(do_wknd))
    print(len(do_fri))
    print(len(do_wkday))
    """
    # all those who did weekend will first fill up weekends. if extra, then fill up fridays, then still extra fill weekdays
    old_do_wknd = do_wknd.copy()
    do_wknd.extend(dn_wknd[:len(no_wknd) - len(old_do_wknd)])
   
    old_do_fri = do_fri.copy()
    do_fri.extend(dn_wknd[len(no_wknd) - len(old_do_wknd):len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri)])
   
    old_do_wkday = do_wkday.copy()
    do_wkday.extend(dn_wknd[len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri):len(no_wknd) - len(old_do_wknd) + len(no_fri) - len(old_do_fri) + len(no_wkday) - len(old_do_wkday)])

    """
    print(len(do_wknd))
    print(len(do_fri))
    print(len(do_wkday))
    """
    
    dictionary = dict()
    dictionary["do_wknd"] = do_wknd
    dictionary["do_wkday"] = do_wkday
    dictionary["do_fri"]= do_fri
    
    return dictionary


"""
# input weekdays, weekends, fridays in subsequent month
no_wknd = [7,14,21,28,1,8,5,22,29,2,23]
no_fri = [6,13,20,27]
no_days_in_month = 30

# input people for each case - done weekday, weekend, friday in the previous month
dn_wknd = ["CPL LEONARD (B)","LCP JUN LONG (ME)","PTE HAIKAL (HQ)","PTE RUSYAIDI (HQ)","PTE SRI (C)","CPL ZIYAN (ME)","LCP JOSEN (ME)","LCP AVIER (HQ)","PTE SHAFIQ (HQ)","PTE EDMUND (C)","PTE MIN QUAN (B)"]
dn_fri = ["PTE YANNIAN (HQ)","CPL ZIYAN (ME)","LCP ELIAS (B)","PTE SRI (C)"]
dn_wkday = ["LCP ERNEST (HQ)","PTE JINGZE (A)","CPL ADRIAN (A)","CPL XINBO (A)","LCP JOSEN (ME)", "PTE CHRISTIAN (HQ)", "PTE WINSON (B)","LCP DARYL (ME)","PTE EUGENE (HQ)","LCP CHING KAI (HQ)"]

print(len(do_wknd))
print(len(do_fri))
print(len(do_wkday))
"""
