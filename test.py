l = [
	'                                                                  ',
	'                                                                  ',
	'                E  E                       C                      ',
	'        X     XXXXXXXXXs                   XX   X                 ',
	' EXXXE     XX         XX                XXXX EE XX                ',
	' XX XX    C                                  XXXXX                ',
	'          XE    E           E  E   X                            G ',
	'     C  XXXXXX  XXXXE    XXXXXXXXXXX  XX      C       EE E     XXX',
	' P   XX  X XX X  X XXXE     X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
	'XXXXXXX  X  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]

for i in range(len(l)):
    for j in range(len(l[i])):
        if l[i][j] == "t" or l[i][j] == 's':
            l[i][j] = "E"

print(l)