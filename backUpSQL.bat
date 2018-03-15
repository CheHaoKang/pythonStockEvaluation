cd /d "D:\Program Files\MariaDB 10.2\bin"
if not exist "C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp" mkdir C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp

forfiles /p "C:\Users\blueplanet\PycharmProjects\SQLBackUp" /s /m *.* /D -7 /C "cmd /c del @file"
rem delete files 7 days ago

mysqldump -u root -p89787198 stockevaluation stockdata > C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp\\stockdata-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stockproxies > C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp\\stockproxies-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stocktable > C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp\\stocktable-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stockinstitutionalinvestor > C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp\\stockinstitutionalinvestor-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql
mysqldump -u root -p89787198 stockevaluation stocknewscomments > C:\\Users\\blueplanet\\PycharmProjects\\SQLBackUp\\stocknewscomments-%date:~0,4%-%date:~5,2%-%date:~8,2%.sql

cd "C:\Users\blueplanet\PycharmProjects\pythonStockEvaluation"
C:\\Users\\blueplanet\\Anaconda3\\python.exe stockClassInstance.py retrieveLowestIndexCurrentIndex "%date:~0,4%%date:~5,2%%date:~8,2%"