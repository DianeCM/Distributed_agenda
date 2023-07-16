from app import *
import random

ports = ["5123","5050","5030","5132"]
addr = [("127.0.0.1",int(port)) for port in ports]

p = Client(("127.0.0.1",5557),())
p.create_account("Dano","Danilo","Perez","anymore",addr[0])
p.create_account("Jordipynb","Jordan","Pla","lols",addr[0])
p.create_account("La_Nanis","Dania","Mengana","1009",addr[0])
p.create_account("Davi Zamoras","Luis David","Cruz","bruder",addr[0])
p.create_account("Por favor en otro rango","yeyo","lamoru","bruder",addr[0])
p.create_account("DianeCM","Dianelys","Cruz","bruder",addr[0])
p.create_account("Q'bola","luna","lamoru","bruder",addr[0])
p.create_account("Asere","yeyo","lamoru","bruder",addr[0])


p.create_account("por fiiiinnn","Blau","lamoru","bruder",addr[1])
p.create_account("Ultimo_intento","yeyo","lamoru","bruder",addr[1])
p.create_account("Duke","Alma","lopez","bruder",addr[1])
p.create_account("pssss","Ana","Paula","bruder",addr[1])


p.create_account("balablabaka","Le putain","lamoru","bruder",addr[2])
p.create_account("die Farben","Lola","lamoru","bruder",addr[2])
p.create_account("die Krankenhouse","Yo","lopez","bruder",addr[2])
p.create_account("Endlichkeit","Paul","Paula","bruder",addr[2])

p.create_account("99 Luftballons","Nena","lamoru","bruder",addr[3])
p.create_account("Ist da jemand","Ich weiss es nicht","lamoru","bruder",addr[3])
p.create_account("Das ist dein Leben","Ein Man","lopez","bruder",addr[3])
p.create_account("Einsam ohne dich","Lea Marie","Paula","bruder",addr[3])

query = p.get_account(1387790852358793275064937372262159359299396267678,"anymore",addr[random.randint(0,3)])
print(query)
assert query == ("Danilo","Perez")

assert p.get_account(398917283311399037724887355090153082590801165916,"lols",addr[random.randint(0,3)]) == ("Jordan","Pla")
assert p.get_account(5990815086051863829077339305113454546344034054,"1009",addr[random.randint(0,3)]) == ("Dania","Mengana")
assert p.get_account(644374246224340676680599316145848478654176260878,"bruder",addr[random.randint(0,3)])== ("Luis David","Cruz")
assert p.get_account(385479827535489418545693341408436029099082342623,"bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
assert p.get_account(1013894169738043364285930992506374634007071297417,"bruder",addr[random.randint(0,3)]) == ("Dianelys","Cruz")
assert p.get_account(589168393044806810882304187972391309945178053824,"bruder",addr[random.randint(0,3)]) == ("luna","lamoru")
assert p.get_account(868692041044819075563252611536236411404611644521,"bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
assert p.get_account(1173427172178387455921560055220392582823190772710,"bruder",addr[random.randint(0,3)]) == ("Blau","lamoru")
assert p.get_account(931700187466442864342628056246896981574761432074,"bruder",addr[random.randint(0,3)]) == ("yeyo","lamoru")
assert p.get_account(46172992780723561320921680056030571120989981024,"bruder",addr[random.randint(0,3)]) == ("Alma","lopez")
assert p.get_account(312739833230340290289372410573930889658287017218,"bruder",addr[random.randint(0,3)]) == ("Ana","Paula")
assert p.get_account(432597546867143777823621346628504951811606450263,"bruder",addr[random.randint(0,3)]) == ("Le putain","lamoru")
assert p.get_account(1232671626752400433958435308290156597452904976323,"bruder",addr[random.randint(0,3)]) == ("Lola","lamoru")
assert p.get_account(1130028074014823973443257698516755608762041422850,"bruder",addr[random.randint(0,3)]) == ("Yo","lopez")
assert p.get_account(51781571364731217802896712217675907414952684167,"bruder",addr[random.randint(0,3)]) == ("Paul","Paula")
assert p.get_account(1407732756987671920939148703746431562120080898707,"bruder",addr[random.randint(0,3)]) == ("Nena","lamoru")
assert p.get_account(7813470691029383468274408971967838198693486436,"bruder",addr[random.randint(0,3)]) == ("Ich weiss es nicht","lamoru")
assert p.get_account(531114789999197592597297236183954734558301224076,"bruder",addr[random.randint(0,3)]) == ("Lea Marie","Paula")
