@echo off
rem S3にパッケージ化する

sam local invoke --env-vars env.json --event event.json AskAirconFunction
