import push_up as pu

def start_menu():
    print("\n___________________________________________________ \n\_                                               _/")
    print("  \_ Push-up detecting rep counter initialised _/\n    \_                                       _/ \n      \_1 - pushup, m - menu, t - terminate_/") # Old menu 1 - curls, 2 - push-ups, 3 - squats, 4 - pull-ups, m - menu, t - terminate
    print("        \_________________________________/ ")
    menu = input("\n                     Enter: ") # User input
    
    if menu == 1: # if statement when entering 1
        print("\n     Starting push up     ")
        pu.StartPushUp()
    elif menu == 'm': # if statement when entering m
        print("\n                 Returning to menu    ")
        start_menu()
    elif menu == 't': # if statement when entering t
        print("\n                 Terminating program     ")
        exit()
    
# Old Menu
#    if menu == 1:
#        print("     Starting curls     ")
#        pu.StartCurls()
#    if menu == 2:
#        print("     Starting push-ups     ")
#        pu.StartPushUp()
#    if menu == 3:
#        print("     Starting squats     ")
#        pu.StartSquats()
#    if menu == 4:
#        print("     Starting pull-ups     ")
#        pu.StartPullUp()
#    elif menu == 'm':
#        print("     Returning to menu    ")
#        start_menu()
#    elif menu == 't':
#        print("     Terminating program     ")
#        exit()
