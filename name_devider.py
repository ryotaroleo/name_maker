def devide(yomi):
    str = yomi
    devided_names = []
    if len(str) == 2:
        devided_names.append([str[0],str[1]])
        devided_names.append([str[0]+str[1]])
    elif len(str) == 3:
        devided_names.append([str[0],str[1],str[2]])
        devided_names.append([str[0]+str[1],str[2]])
        devided_names.append([str[0],str[1]+str[2]])
        devided_names.append([str[0]+str[1]+str[2]])
    elif len(str) == 4:
        devided_names.append([str[0],str[1],str[2],str[3]])
        devided_names.append([str[0]+str[1],str[2],str[3]])
        devided_names.append([str[0],str[1]+str[2],str[3]])
        devided_names.append([str[0]+str[1]+str[2],str[3]])
        devided_names.append([str[0],str[1],str[2]+str[3]])
        devided_names.append([str[0]+str[1],str[2]+str[3]])
        devided_names.append([str[0],str[1]+str[2]+str[3]])
        devided_names.append([str[0]+str[1]+str[2]+str[3]])

    print(devided_names)
    return(devided_names)
