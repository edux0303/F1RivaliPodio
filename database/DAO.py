from database.DB_connect import DBConnect
from model.driver import Driver
class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT distinct year FROM seasons s  "
                 "ORDER BY year")

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getNodi(anno1,anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT DISTINCT d.driverId AS id, d.forename AS nome, d.surname AS cognome, d.nationality AS nazionalita,COUNT(DISTINCT re.raceId) AS podi "
                 "FROM drivers d, races r, results re "
                 "WHERE d.driverId = re.driverId  AND r.raceId = re.raceId "
                 "AND re.position IS NOT NULL AND re.position <=3 AND r.year BETWEEN %s AND %s "                        
                "GROUP BY d.driverId, d.forename, d.surname, d.nationality ")
        cursor.execute(query,(anno1,anno2))

        for row in cursor:
            results.append(Driver(row["id"],row["nome"],row["cognome"],row["nazionalita"],row["podi"]))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getCoppie(anno1,anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT re1.driverId as id1, re2.driverId AS id2, COUNT(DISTINCT re1.raceId) as peso "
                 "FROM results re1, results re2, races r1 "
                 "WHERE re1.raceId = re2.raceId AND r1.raceId = re2.raceId "
                 "AND r1.year BETWEEN %s AND %s "
                 "AND re1.position IS NOT NULL AND re1.position <= 3 "
                 "AND re2.position IS NOT NULL AND re2.position <= 3 "
                 "AND re1.driverId < re2.driverId "
                 "GROUP BY re1.driverId, re2.driverId "
                 "HAVING COUNT(DISTINCT re1.raceId) >= 1 ")

        cursor.execute(query,(anno1,anno2))

        for row in cursor:
            results.append((row["id1"],row["id2"],row["peso"]))

        cursor.close()
        conn.close()
        return results




