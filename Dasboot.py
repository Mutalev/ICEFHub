def findGroups(s):
    d = ''
    f = open('Names.txt', 'r')
    a = s.lower().split()
    for line in f:
        g = line.split()
        if a[0] == g[0].lower():
            if a[1] == g[1].lower():
                if len(g) < 5:
                    d = 'Академ_группа: ' + g[2] + ' ' + 'Англ_группа: ' + g[3]
                else:
                    d = 'Академ_группа: ' + g[3] + ' ' + 'Англ_группа: ' + g[4]
                    break
    return d

def findGroup1(s):
    f = open('Names.txt', 'r')
    a = []
    for line in f:
        g = line.split()
        if len(g) < 5:
            if s == int(g[2]):
                a.append(str(g[0] + ' ' + g[1]))
        elif s == int(g[3]):
            a.append(str(g[0] + ' ' + g[1]))

    s1 = ''
    for i in a:
        s1 += i + '\n'
    f.close()
    return s1


def findGroup2(s):
    f = open('Names.txt', 'r')
    a = []
    for line in f:
        g = line.split()
        if len(g) < 5:
            if s == int(g[3]):
                a.append(str(g[0] + ' ' + g[1]))
        elif s == int(g[4]):
            a.append(str(g[0] + ' ' + g[1]))

    s1 = ''
    for i in a:
        s1 += i + '\n'
    f.close()
    return s1



    # if f[0] not in d:
    #     if len(f) < 5:
    #         d[f[0] + ' ' + f[1]] = [f[2], f[3]]
    #     else:
    #         d[f[0] + ' ' + f[1]] = [f[3], f[4]]
        

# for i in d:
#     g = str(i).lower().split()
#     if LastName == g[0]:
#         print(i)
#         print('Академ группа: ' + d[i][0])
#         print('Англ группа: ' + d[i][1])



