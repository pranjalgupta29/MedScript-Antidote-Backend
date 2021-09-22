# run in shell
f = open("Users/diseases.txt" , "rt")

diseases = []
specialists = set()
for line in f:
    li = line.split("#")
    li[0] = li[0].strip()
    li[1] = li[1].strip()
    specialists.add(li[1])
    diseases.append(li)

for s in specialists:
    ob = Specialization.objects.create(Name=s)

for d in diseases:
    s = Specialization.objects.get(Name=d[1])
    ob = Disease.objects.create(Name=d[0],Specialization=s)
    ob.save()


# print(diseases)
# print(specialists)