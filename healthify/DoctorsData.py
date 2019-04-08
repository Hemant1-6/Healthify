import json;

with open("doc.txt","r") as data:
    raw = data.read()
    data = json.loads(raw)

def jsonData()->list:
 dentist = []
 ent = []
 dermotologist = []
 neurologist = []
 podiatrist = []
 physical = []
 for rw in data:
  if rw['category'] == "dentist":
        dentist.append(rw)
  if rw['category'] == "ENT":
      ent.append(rw)
  if rw['category'] == "Podiatrist":
      podiatrist.append(rw)
  if rw['category'] == "neurologist":
      neurologist.append(rw)
  if rw['category'] == "Physical Therapist":
      physical.append(rw)
  if rw['category'] == "dermatologist":
      dermotologist.append(rw)

  dict = {}
  dict['dentist'] = dentist
  dict['ent'] = ent
  dict['pod'] = podiatrist
  dict['neuro'] = neurologist
  dict['phy'] = physical
  dict['dermo'] = dermotologist

 return dict

