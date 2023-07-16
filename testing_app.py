from app import *
import random

ports = ["5123","5050","5030","5132"]
addr = [("127.0.0.1",int(port)) for port in ports]

p = Client(("127.0.0.1",5557),())
p.create_account("Dano","Danilo","Perez","anymore",addr[0])
p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",addr[0])
p.create_personal_event("Party","2023-07-1","2023-07-09","Privado",addr[0])

p.create_account("Jordipynb","Jordan","Pla","lols",addr[0])
p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",addr[0])
p.create_personal_event("Beach","2023-09-1","2023-09-09","Privado",addr[0])
p.create_personal_event("Kino","2023-10-1","2023-10-03","Privado",addr[0])

p.create_account("La_Nanis","Dania","Mengana","1009",addr[0])
p.create_group("Das Licht","Jerárquico",addr[0])
p.create_personal_event("Pool","2023-07-1","2023-07-09","Privado",addr[0])


p.create_account("Davi Zamoras","Luis David","Cruz","bruder",addr[0])
p.create_group("Das fucking Licht","No Jerárquico",addr[0])
p.create_personal_event("ML_Conference","2023-11-1","2023-11-09","Público",addr[0])
p.create_personal_event("Thesis","2024-01-01","2023-01-01","Privado",addr[0])



p.create_account("Por favor en otro rango","yeyo","lamoru","bruder",addr[0])
p.create_group("la lumiere","Jerárquico",addr[0])
p.create_personal_event("Pazilo","2023-07-29","2023-08-09","Público",addr[0])
p.create_personal_event("Museum","2023-09-1","2023-09-09","Privado",addr[0])
p.create_personal_event("Meeting","2023-10-1","2023-10-03","Privado",addr[0])

p.create_account("DianeCM","Dianelys","Cruz","bruder",addr[0])
p.create_group("La luz","No Jerárquico",addr[0])
p.create_personal_event("Grandma","2023-07-29","2023-08-09","Público",addr[0])
p.create_personal_event("Trinidad","2023-09-1","2023-09-09","Privado",addr[0])

p.create_account("Q'bola","luna","lamoru","bruder",addr[0])
p.create_account("Asere","yeyo","lamoru","bruder",addr[0])



p.create_account("por fiiiinnn","Blau","lamoru","bruder",addr[1])
p.create_group("Wenn Der Himmel ohne Farben ist","Jerárquico",addr[1])
p.create_personal_event("Car","2023-07-29","2023-08-09","Público",addr[1])
p.create_personal_event("Beach","2023-09-1","2023-09-09","Privado",addr[1])
p.create_personal_event("French","2023-10-1","2023-10-03","Privado",addr[1])

p.create_account("Ultimo_intento","yeyo","lamoru","bruder",addr[1])
p.create_group("Und weisst nicht wohin du rennst","No Jerárquico",addr[1])
p.create_personal_event("Musik","2023-07-29","2023-08-09","Público",addr[1])
p.create_personal_event("Concert","2023-09-1","2023-09-09","Privado",addr[1])


p.create_account("Duke","Alma","lopez","bruder",addr[1])
p.create_group("Looooooolllllll","Jerárquico",addr[1])
p.create_personal_event("Book","2023-07-29","2023-08-09","Público",addr[1])


p.create_account("pssss","Ana","Paula","bruder",addr[1])
p.create_group("Fenster","No Jerárquico",addr[1])


p.create_account("balablabaka","Le putain","lamoru","bruder",addr[2])
p.create_group("Die Zunkunft","Jerárquico",addr[2])

p.create_account("die Farben","Lola","lamoru","bruder",addr[2])
p.create_group("Es geht nicht","No Jerárquico",addr[2])
p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",addr[2])
p.create_personal_event("Meeting","2023-09-1","2023-09-09","Privado",addr[2])
p.create_personal_event("Project","2023-10-1","2023-10-03","Privado",addr[2])

p.create_account("die Krankenhouse","Yo","lopez","bruder",addr[2])
p.create_group("Yayaya coco chambo ya ya ie","Jerárquico",addr[2])
p.create_personal_event("English","2023-07-29","2023-08-09","Público",addr[2])
p.create_personal_event("Beach","2023-09-1","2023-09-09","Privado",addr[2])


p.create_account("Endlichkeit","Paul","Paula","bruder",addr[2])
p.create_group("Dein Augen","No Jerárquico",addr[2])
p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",addr[2])



p.create_account("99 Luftballons","Nena","lamoru","bruder",addr[3])
p.create_group("Wie du bist bist du genung","Jerárquico",addr[3])
p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",addr[3])
p.create_personal_event("Meeting","2023-09-1","2023-09-09","Privado",addr[3])
p.create_personal_event("Project","2023-10-1","2023-10-03","Privado",addr[3])


p.create_account("Ist da jemand","Ich weiss es nicht","lamoru","bruder",addr[3])
p.create_group("Wie du bist bist du gut","No Jerárquico",addr[3])

p.create_account("Das ist dein Leben","Ein Man","lopez","bruder",addr[3])
p.create_group("Du musst meich nicht zum lauchen bringen","Jerárquico",addr[3])
p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",addr[3])



p.create_account("Einsam ohne dich","Lea Marie","Paula","bruder",addr[3])
p.create_group("Wenn du mich lusst","No Jerárquico",addr[3])
p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",addr[3])
p.create_personal_event("Meeting","2023-09-1","2023-09-09","Privado",addr[3])
p.create_personal_event("Project","2023-10-1","2023-10-03","Privado",addr[3])


assert p.get_account("Dano","anymore",addr[random.randint(0,3)]) == ("Danilo","Perez")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Jordipynb","lols",addr[random.randint(0,3)]) == ("Jordan","Pla")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))

assert p.get_account("La_Nanis","1009",addr[random.randint(0,3)]) == ("Dania","Mengana")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Davi Zamoras","bruder",addr[random.randint(0,3)])== ("Luis David","Cruz")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Por favor en otro rango","bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("DianeCM","bruder",addr[random.randint(0,3)]) == ("Dianelys","Cruz")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Q'bola","bruder",addr[random.randint(0,3)]) == ("luna","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Asere","bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("por fiiiinnn","bruder",addr[random.randint(0,3)]) == ("Blau","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Ultimo_intento","bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Duke","bruder",addr[random.randint(0,3)]) == ("Alma","lopez")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("pssss","bruder",addr[random.randint(0,3)]) == ("Ana","Paula")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("balablabaka","bruder",addr[random.randint(0,3)]) == ("Le putain","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("die Farben","bruder",addr[random.randint(0,3)]) == ("Lola","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("die Krankenhouse","bruder",addr[random.randint(0,3)]) == ("Yo","lopez")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Endlichkeit","bruder",addr[random.randint(0,3)]) == ("Paul","Paula")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("99 Luftballons","bruder",addr[random.randint(0,3)]) == ("Nena","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Ist da jemand","bruder",addr[random.randint(0,3)]) == ("Ich weiss es nicht","lamoru")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))


assert p.get_account("Einsam ohne dich","bruder",addr[random.randint(0,3)]) == ("Lea Marie","Paula")
print(p.get_groups_belong_to(addr[random.randint(0,3)]))
print(p.get_all_events(addr[random.randint(0,3)]))

