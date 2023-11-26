# docker-lamp project for COMP3335 class of Fall 2023 

Docker example with Vue.js, MySql 8.0 and Python flask

To run these containers:

```
docker compose -f docker-compose-vue.yml up
```

Run mysql client:

`docker-compose exec db mysql -u root -p` 

Open flask backend at [http://localhost:15000](http://localhost:15000).

Open web browser to look at the vue frontend at [http://localhost:8080](http://localhost:8080)

sample accounts:
Patients:
'john_doe', 'password123'
'jane_smith', 'pass1234'

Staff (Lab staff):
'dr_x', 'pass4321'
'dr_y', 'pass5678'

Staff (Secretaries):
'dr_z', 'pass9876'
