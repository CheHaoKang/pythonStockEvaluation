cd "C:\Program Files\MariaDB 10.2\bin"
mysqldump -u root -p89787198 stockevaluation stockdata > C:\\Users\\blueplanet\\PycharmProjects\\stockdata-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stockproxies > C:\\Users\\blueplanet\\PycharmProjects\\stockproxies-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stocktable > C:\\Users\\blueplanet\\PycharmProjects\\stocktable-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql