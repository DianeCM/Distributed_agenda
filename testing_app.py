from app import *
import random

ports = ["5123","5050","5030","5132"]

addr = [("127.0.0.1",int(port)) for port in ports]

p = Client(("127.0.0.1",5557),())
# p.create_account("Dano","Danilo","Perez","anymore",address = addr[0])
# p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",address = addr[0])
# p.create_personal_event("Party","2023-07-1","2023-07-09","Privado",address = addr[0])

# p.create_account("Jordipynb","Jordan","Pla","lols",address = addr[0])
# p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",address = addr[0])
# p.create_personal_event("Beach","2024-09-1","2024-09-09","Privado",address = addr[0])
# p.create_personal_event("Kino","2023-10-1","2023-10-03","Privado",address = addr[0])

# p.create_account("La_Nanis","Dania","Mengana","1009",address = addr[0])
# p.create_group("Das Licht","Jerárquico",address = addr[0])
# p.create_personal_event("Pool","2023-07-1","2023-07-09","Privado",address = addr[0])


# p.create_account("Davi Zamoras","Luis David","Cruz","bruder",address = addr[0])
# p.create_group("Das fucking Licht","No Jerárquico",address = addr[0])
# p.create_personal_event("ML_Conference","2023-11-1","2023-11-09","Público",address = addr[0])
# p.create_personal_event("Thesis","2024-01-01","2024-01-01","Privado",address = addr[0])

# p.create_account("Por favor en otro rango","yeyo","lamoru","bruder",address = addr[0])
# p.create_group("la lumiere","Jerárquico",address = addr[0])
# p.create_personal_event("Pazilo","2023-07-29","2023-08-09","Público",address = addr[0])
# p.create_personal_event("Museum","2023-09-1","2023-09-09","Privado",address = addr[0])
# p.create_personal_event("Meeting","2023-10-1","2023-10-03","Privado",address = addr[0])

# p.create_account("DianeCM","Dianelys","Cruz","bruder",address = addr[0])
# p.create_group("La luz","No Jerárquico",address = addr[0])
# p.create_personal_event("Grandma","2023-07-29","2023-08-09","Público",address = addr[0])
# p.create_personal_event("Trinidad","2023-09-1","2023-09-09","Privado",address = addr[0])

# p.create_account("Q'bola","luna","lamoru","bruder",address = addr[0])
# p.create_account("Asere","yeyo","lamoru","bruder",address = addr[0])



# p.create_account("por fiiiinnn","Blau","lamoru","bruder",address = addr[1])
# p.create_group("Wenn Der Himmel ohne Farben ist","Jerárquico",address = addr[1])
# p.create_personal_event("Car","2023-07-29","2023-08-09","Público",address = addr[1])
# p.create_personal_event("Beach","2023-07-1","2023-07-09","Privado",address = addr[1])
# p.create_personal_event("French","2023-10-1","2023-10-03","Privado",address = addr[1])

# p.create_account("Ultimo_intento","yeyo","lamoru","bruder",address = addr[1])
# p.create_group("Und weisst nicht wohin du rennst","No Jerárquico",address = addr[1])
# p.create_personal_event("Musik","2023-07-29","2023-08-09","Público",address = addr[1])
# p.create_personal_event("Concert","2023-09-1","2023-09-09","Privado",address = addr[1])


# p.create_account("Duke","Alma","lopez","bruder",address = addr[1])
# p.create_group("Looooooolllllll","Jerárquico",address = addr[1])
# p.create_personal_event("Book","2023-07-29","2023-08-09","Público",address = addr[1])


# p.create_account("pssss","Ana","Paula","bruder",address = addr[1])
# p.create_group("Fenster","No Jerárquico",address = addr[1])


# p.create_account("balablabaka","Le putain","lamoru","bruder",address = addr[2])
# p.create_group("Die Zunkunft","Jerárquico",address = addr[2])

# p.create_account("die Farben","Lola","lamoru","bruder",address = addr[2])
# p.create_group("Es geht nicht","No Jerárquico",address = addr[2])
# p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",address = addr[2])
# p.create_personal_event("Meeting","2023-09-1","2023-09-09","Privado",address = addr[2])
# p.create_personal_event("Project","2023-9-1","2023-05-03","Privado",address = addr[2])

# p.create_account("die Krankenhouse","Yo","lopez","bruder",address = addr[2])
# p.create_group("Yayaya coco chambo ya ya ie","Jerárquico",address = addr[2])
# p.create_personal_event("English","2023-07-29","2023-08-09","Público",address = addr[2])
# p.create_personal_event("Beach","2023-09-1","2023-09-09","Privado",address = addr[2])


# p.create_account("Endlichkeit","Paul","Paula","bruder",address = addr[2])
# p.create_group("Dein Augen","No Jerárquico",address = addr[2])
# p.create_personal_event("Wedding","2023-07-29","2023-08-09","Público",address = addr[2])



# p.create_account("99 Luftballons","Nena","lamoru","bruder",address = addr[3])
# p.create_group("Wie du bist bist du genung","Jerárquico",address = addr[3])
# p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",address = addr[3])
# p.create_personal_event("Meeting","2023-09-1","2023-09-09","Privado",address = addr[3])
# p.create_personal_event("Project","2023-10-1","2023-10-03","Privado",address = addr[3])


# p.create_account("Ist da jemand","Ich weiss es nicht","lamoru","bruder",address = addr[3])
# p.create_group("Wie du bist bist du gut","No Jerárquico",address = addr[3])

# p.create_account("Das ist dein Leben","Ein Man","lopez","bruder",address = addr[3])
# p.create_group("Du musst meich nicht zum lauchen bringen","Jerárquico",address = addr[3])
# p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",address = addr[3])



# p.create_account("Einsam ohne dich","Lea Marie","Paula","bruder",address = addr[3])
# p.create_group("Wenn du mich lusst","No Jerárquico",address = addr[3])
# p.create_personal_event("Birthday","2023-07-29","2023-08-09","Público",address = addr[3])
# p.create_personal_event("Meeting","2023-10-1","2023-10-09","Privado",address = addr[3])
# p.create_personal_event("Project","2023-10-1","2023-10-03","Privado",address = addr[3])


assert p.get_account("Dano","anymore",addr[random.randint(1,2)]) == ("Danilo","Perez")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))

assert p.get_account("Jordipynb","lols",addr[random.randint(1,2)]) == ("Jordan","Pla")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))

assert p.get_account("La_Nanis","1009",addr[random.randint(1,2)]) == ("Dania","Mengana")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))


assert p.get_account("Davi Zamoras","bruder",addr[random.randint(1,2)])== ("Luis David","Cruz")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("Por favor en otro rango","bruder",addr[random.randint(1,2)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("DianeCM","bruder",addr[random.randint(1,2)]) == ("Dianelys","Cruz")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))


assert p.get_account("Q'bola","bruder",addr[random.randint(1,2)]) == ("luna","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("Asere","bruder",addr[random.randint(1,2)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("por fiiiinnn","bruder",addr[random.randint(1,2)]) == ("Blau","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("Ultimo_intento","bruder",addr[random.randint(1,2)]) == ("yeyo","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))


assert p.get_account("Duke","bruder",addr[random.randint(1,2)]) == ("Alma","lopez")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("pssss","bruder",addr[random.randint(1,2)]) == ("Ana","Paula")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("balablabaka","bruder",addr[random.randint(1,2)]) == ("Le putain","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("die Farben","bruder",addr[random.randint(1,2)]) == ("Lola","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("die Krankenhouse","bruder",addr[random.randint(1,2)]) == ("Yo","lopez")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))


assert p.get_account("Endlichkeit","bruder",addr[random.randint(1,2)]) == ("Paul","Paula")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("99 Luftballons","bruder",addr[random.randint(1,2)]) == ("Nena","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("Ist da jemand","bruder",addr[random.randint(1,2)]) == ("Ich weiss es nicht","lamoru")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))


assert p.get_account("Einsam ohne dich","bruder",addr[random.randint(1,2)]) == ("Lea Marie","Paula")
print(p.get_groups_belong_to(addr[random.randint(1,2)]))
print(p.get_all_events(addr[random.randint(1,2)]))
print(p.get_notifications(addr[random.randint(1,2)]))

